#include <mutex>
#include <nmmintrin.h>

#include "DDImage/Iop.h"
#include "DDImage/Row.h"
#include "DDImage/Knobs.h"
#include "DDImage/Tile.h"
#include "DDImage/LookupCurves.h"

#include "Euclid.06.06.2020/AABB.h"
#include "Euclid.09.12.2021/ParallelWorkManager.h"
#include "Euclid.09.12.2021/Utils.h"
#include "Euclid.09.12.2021/Time.h"

#include "Euclid.21.05.2022/AlignedMemoryBuffer.h"

//////////////////////////////////////////
// 
// ::TODO::
// - curve_aabb needs to make bbox smaller if second spline is omitted
// - hash checks to recompute different elemetns
// - solve the input bbox issue
// - deallocate memory block if needed to, if too slow pr low on memory
// - can avoid clearing the entire buffer and only clearing the last bbox area
// 
//////////////////////////////////////////

#if 0
    #define PRINT_FUNC_HEAD std::cout<<"Start: "<<__FUNCTION__ <<"\n";
    #define PRINT_FUNC_TAIL std::cout<<"End  : "<<__FUNCTION__ <<"\n";
#else
    #define PRINT_FUNC_HEAD
    #define PRINT_FUNC_TAIL
#endif

#if defined(__GNUC__)
    #define CACHE_ALIGNED __attribute__((aligned(64))) // clang and GCC
#elif defined(_MSC_VER)
    #define CACHE_ALIGNED __declspec(align(64))        // MSVC
#endif

static uint32_t testcounter{0};

class CurvedMotionTrail final : public DD::Image::Iop
{
    // typedef void (*curveFunc)   (__m128&, __m128&, __m128&);
    // typedef void (*shutterFunc) (__m128&, __m128&, __m128&, const __m128&, const __m128&);
    
    // Output Buffer
    constexpr static size_t tileChannelsSize{5};
    
    std::vector<Euclid::Aligned64MemoryBuffer> memoryBlocks{4}; // Currently for RGBA

    // DD::Image::Hash hashUpdate{0};

    // Not sure if 3 seperate tiles are better than one
    DD::Image::Tile* tileRGBA{nullptr};
    DD::Image::Tile* tileVelocity{nullptr};
    DD::Image::Tile* tileControl{nullptr};

    // canvas
	DD::Image::Box inputBBox{0,0,1,1};
	DD::Image::Box outputBBox{0,0,1,1};
    Euclid::AABB<int> outputAABB, inputAABB;
    
    // tiles list -> {tile output bbox, tile input bbox, histogram}
    std::vector<std::tuple<Euclid::AABB<int>, Euclid::AABB<int>, int>> renderTiles;
    const int uniformTileWidth{128};
    int tilesCountRows;
    int tilesCountCols;

    DD::Image::ChannelSet rgbaChanSet{DD::Image::Mask_RGBA};
    DD::Image::ChannelSet vecsChanSet{DD::Image::Mask_None};
    DD::Image::Channel vecsChan[4]{DD::Image::Chan_Black};
    DD::Image::Channel cntlChan[1]{DD::Image::Chan_Black};

    // knobs
    float kShutterMultiplier{0.5f};

    int kBBoxMode{0};
    static const char* const kBBoxModeList[];
    enum kBBoxModeEnum{ FORMAT, BBOX, FORMATBBOX };

    int kCurveOrigin{2};
    static const char* const kCurveOriginList[];
    enum kCurveOriginEnum { HEAD, CENTER, TAIL };
    
    int kExpandBBox{0};

    const unsigned int transparencyCurveLUTsize {256};
    const float transparencyCurveLUTsizef {static_cast<float>(transparencyCurveLUTsize-1)};
    std::vector<std::pair<float, float>> transparencyCurveLUT;
    static const DD::Image::CurveDescription kTransparencyCurveDescription[];
	DD::Image::LookupCurves	kTransparencyLookupCurves{kTransparencyCurveDescription};

    // threas Handlers
    Euclid::ParallelWorkManager threadsWorkManager;
    std::mutex m_lock_main_engine_call{};
    std::mutex m_lock_tiles{};
    int firstCallEngine{false};

    int useControl{true};


public:

    CurvedMotionTrail(Node* node) 
    : DD::Image::Iop(node) 
    {
		// std::cout<<"CurvedMotionTrail :\tEyal Shirazi\t"<<__DATE__<<"  "<<__TIME__<<"\n";        
        transparencyCurveLUT.resize(transparencyCurveLUTsize);
    }
    
    ~CurvedMotionTrail()
    {
        for (auto& m : memoryBlocks) m.Deallocate();
        // we cannot call release on pool beucase Nuke calls destructor only on the last remaining instance so we don't know how maybe instances of the pool we have...
    }

    static const char* const kHelp;
    static const char* const kInfo;
    static const DD::Image::Iop::Description d;
    const char* Class() const override { return d.name; }
    const char* node_help() const override { return kHelp; }

	void append(DD::Image::Hash& hash) override	
    {
        PRINT_FUNC_HEAD
        
		hash.append(__DATE__);
		hash.append(__TIME__);

        hash.append(kShutterMultiplier);
        hash.append(kBBoxMode);
        hash.append(kCurveOrigin);
        hash.append(kExpandBBox);
		kTransparencyLookupCurves.append(hash);

		DD::Image::Iop::append(hash); 
	}

    void knobs(DD::Image::Knob_Callback f) override   
    {
        PRINT_FUNC_HEAD

        Input_Channel_knob( f, vecsChan, 4, 0,"vectors", "vector channels");
        Input_Channel_knob( f, cntlChan, 1, 0,"control", "control channels");

		Divider(f,"");
        Enumeration_knob(f, &kCurveOrigin, kCurveOriginList, "origin", "origin");
        Enumeration_knob(f, &kBBoxMode, kBBoxModeList, "cliptype", "clip to");
		Int_knob(f, &kExpandBBox, "bboxexpand", "bbox expand");
		Divider(f,"");

		Float_knob(f, &kShutterMultiplier, "shutter", "shutter");
        Text_knob(f, "");
        SetFlags(f,DD::Image::Knob::STARTLINE);
		VSpacer(f,20);

		LookupCurves_knob(f, &kTransparencyLookupCurves, "transparency");

		Divider(f,"");

        Tab_knob(f, "info");
        Text_knob(f, kInfo);
    }

    void _validate(bool for_real) override
    {
        PRINT_FUNC_HEAD

        copy_info();
        set_out_channels(DD::Image::Mask_None);

        if (kShutterMultiplier<=0) return;

        vecsChanSet.clear();
        for(const auto& c : vecsChan) vecsChanSet += c;

        if (vecsChanSet == DD::Image::Mask_None || vecsChanSet.size()!=4) {return;} // if no vectors channles, do nothing

        if (!dynamic_cast<DD::Image::Iop*>(Op::input(0))) return;

        input0().validate();
        if (!input0().channels().contains(vecsChanSet)) {return;}
        useControl = (cntlChan[0]!=DD::Image::Chan_Black && input0().channels().contains(cntlChan[0])) ? true : false ;
 
        outputBBox.set(0,0, info_.full_size_format().w(), info_.full_size_format().h());
        inputBBox = input0().info().box();	

        // // get bounding box
        // switch (kBBoxMode){
        //     case kBBoxModeEnum::FORMAT:
        //     {													
        //         break;
        //     }
        //     case kBBoxModeEnum::BBOX:
        //     {
        //         get_bbox();
        //         outputBBox.set(outputAABB.DD_BBOX());
        //         inputBBox.set(inputAABB.DD_BBOX());
        //         break;
        //     }
        //     case kBBoxModeEnum::FORMATBBOX:
        //     {
        //         get_bbox();
        //         outputBBox.set(outputAABB.DD_BBOX());
        //         inputBBox.set(inputAABB.DD_BBOX());
        //         outputBBox.intersect(DD::Image::Box(0,0, info_.full_size_format().w(), info_.full_size_format().h()));
        //         break;
        //     }            
        // }
        outputBBox.expand(kExpandBBox);

        // we are good to go!
        info_.set(outputBBox);
        info_.turn_on(rgbaChanSet);
        set_out_channels(rgbaChanSet);
    }    
	
    void _request(int x, int y, int r, int t, DD::Image::ChannelMask channels, int count) override
	{
        PRINT_FUNC_HEAD
        input0().request(inputBBox, channels + rgbaChanSet + vecsChanSet + cntlChan[0], count*2);
        PRINT_FUNC_TAIL
	}

    void _open() override
	{
        PRINT_FUNC_HEAD
        firstCallEngine = true; 
        // TODO:: update only on knob change
        buildTransparencyLUT();
        callCloseAfter(1.0);
    }

    void _close() override
	{
        PRINT_FUNC_HEAD
        for (auto& m : memoryBlocks) m.Deallocate();
    }

    void engine (int y, int x, int r, DD::Image::ChannelMask channels, DD::Image::Row & out) override 
    {
        if ( firstCallEngine ) 
        {
            std::lock_guard<std::mutex> guard(m_lock_main_engine_call);
            if ( firstCallEngine )
            {            
                if (channels.contains(rgbaChanSet))
                {
					PRINT_FUNC_HEAD

                    // Euclid::Timer stopwatch{"On frame "+std::to_string(static_cast<int>(outputContext().frame())) + ", " + this->node_name() + " build time was"};
                    uint32_t bufferPageSize = outputBBox.h() * outputBBox.w();

                    for (auto& m : memoryBlocks) 
                    {
                        m.Allocate(bufferPageSize*sizeof(float));

                        if (m.GetFloatPtr()==nullptr)
                        {
                            std::cout<<"memory allocation error\n";
                            return;
                        }
                        m.Clear();
                    }

                    DD::Image::Tile tileRGBATemp(input0(), inputBBox, rgbaChanSet, true);
                    DD::Image::Tile tileVelocityTemp(input0(), inputBBox, vecsChanSet, true);
                    DD::Image::Tile tileControlTemp(input0(), inputBBox, cntlChan[0], true);
                    
                    if (Op::aborted())	return;

                    tileRGBA = &tileRGBATemp;
                    tileVelocity = &tileVelocityTemp;
                    tileControl = &tileControlTemp;

                    build_tile_list();
                    render_tile_list();

                    PRINT_FUNC_TAIL
                }
                firstCallEngine = false; 
            }        
        }

        // out.get(input0(),y,x,r, channels);

        DD::Image::ChannelSet channelsNoRGBA = channels;
        channelsNoRGBA -= DD::Image::Chan_Red;
        channelsNoRGBA -= DD::Image::Chan_Green;
        channelsNoRGBA -= DD::Image::Chan_Blue;
        channelsNoRGBA -= DD::Image::Chan_Alpha;
        out.get(input0(),y,x,r, channelsNoRGBA);

        float* outChan1 = out.writable(DD::Image::Chan_Red)   + x;
        float* outChan2 = out.writable(DD::Image::Chan_Green) + x;
        float* outChan3 = out.writable(DD::Image::Chan_Blue)  + x;
        float* outChan4 = out.writable(DD::Image::Chan_Alpha) + x;

        const size_t lineOffset = (y - outputBBox.y()) * outputBBox.w() + (x - outputBBox.x());
        const size_t lineSize = (r - x) * sizeof(float);

        memcpy(outChan1, memoryBlocks[0].GetFloatPtr() + lineOffset, lineSize);
        memcpy(outChan2, memoryBlocks[1].GetFloatPtr() + lineOffset, lineSize);
        memcpy(outChan3, memoryBlocks[2].GetFloatPtr() + lineOffset, lineSize);
        memcpy(outChan4, memoryBlocks[3].GetFloatPtr() + lineOffset, lineSize);
    }
    
    void get_bbox()
    {
		PRINT_FUNC_HEAD

        input0().request(inputBBox, vecsChanSet + cntlChan[0], 1);

        DD::Image::Tile tileVelocityTemp(input0(), inputBBox, vecsChanSet, true);
        DD::Image::Tile tileControlTemp(input0(), inputBBox, cntlChan[0], true);
        
        if (Op::aborted())
        {
            outputAABB.x = 0;
            outputAABB.y = 0;
            outputAABB.r = info_.full_size_format().w();
            outputAABB.t = info_.full_size_format().h();

            inputAABB.x = input0().requestedBox().x();
            inputAABB.y = input0().requestedBox().y();
            inputAABB.r = input0().requestedBox().r();
            inputAABB.t = input0().requestedBox().t();
        	return;
        }

        tileVelocity = &tileVelocityTemp;
        tileControl = &tileControlTemp;

        inputAABB.reset();
        outputAABB.reset();        

        int countFail = 0; 

        threadsWorkManager.setWorkloadFair(inputBBox.h());
        DD::Image::Thread::spawn(get_bbox_cb , static_cast<uint32_t>(threadsWorkManager.size()), (void*)this);
        DD::Image::Thread::wait((void*)this);

        if (Op::aborted())
        {
            outputAABB.x = 0;
            outputAABB.y = 0;
            outputAABB.r = info_.full_size_format().w();
            outputAABB.t = info_.full_size_format().h();

            inputAABB.x = input0().requestedBox().x();
            inputAABB.y = input0().requestedBox().y();
            inputAABB.r = input0().requestedBox().r();
            inputAABB.t = input0().requestedBox().t();

        	return;
        }

        outputAABB.r++;
        outputAABB.t++;

        inputAABB.r++;
        inputAABB.t++;

        inputAABB.intersect(input0().requestedBox());

		PRINT_FUNC_TAIL
    }

    static void get_bbox_cb(unsigned id, unsigned numberCPUthreds, void* _data)
    { 
		PRINT_FUNC_HEAD

        switch (((CurvedMotionTrail*)_data)->kCurveOrigin){
            case kCurveOriginEnum::HEAD:
            {
                break;
            }
            case kCurveOriginEnum::CENTER:
            {
                if (((CurvedMotionTrail*)_data)->useControl)
                    ((CurvedMotionTrail*)_data)->get_bbox_control_mt(id, &curve_points_center, &curve_shutter_center);  
                else 
                    ((CurvedMotionTrail*)_data)->get_bbox_mt(id, &curve_points_center, &curve_shutter_center); 
                break;
            }
            case kCurveOriginEnum::TAIL:
            {
                if (((CurvedMotionTrail*)_data)->useControl)
                    ((CurvedMotionTrail*)_data)->get_bbox_control_mt(id, &curve_points_tail, &curve_shutter_tail); 
                else 
                    ((CurvedMotionTrail*)_data)->get_bbox_mt(id, &curve_points_tail, &curve_shutter_tail); 
                break;
            }            
        }

		PRINT_FUNC_TAIL
    }

    template <typename F1, typename F2>
    void get_bbox_mt(const unsigned& id, F1 curve_mid_Temp_Func, F2 curve_shutter_Temp_Func)
    {
        PRINT_FUNC_HEAD

        int start = threadsWorkManager[id].start;
        int end   = threadsWorkManager[id].end;

        float userShutter1 = kShutterMultiplier * 2.0f;
        float userShutter0 = userShutter1 - 1.0f;
        userShutter1 = userShutter1 < 0.0f ? 0.0f : userShutter1 > 1.0f ? 1.0f : userShutter1 ;
        userShutter0 = userShutter0 < 0.0f ? 0.0f : userShutter0 > 1.0f ? 1.0f : userShutter0 ;

        const __m128 v_0d5 = _mm_set1_ps(0.5f);
        const __m128 v_flip_upper = _mm_castsi128_ps(_mm_set_epi32(0xffffffff,0xffffffff,0,0));

        const __m128 v_shutter    = _mm_setr_ps(userShutter1, userShutter1, userShutter0, userShutter0);
        const __m128 v_shutterMid = _mm_mul_ps(v_shutter, v_0d5);

        constexpr float iMax = static_cast<float>(std::numeric_limits<int>::max()/2);
        __m128 v_outputBBox = _mm_set_ps(-iMax, -iMax, iMax, iMax);
        __m128 v_inputBBox  = _mm_set_ps(-iMax, -iMax, iMax, iMax);

        DD::Image::Box modifiedBBox;
        modifiedBBox.x(input0().requestedBox().x());
        modifiedBBox.y(input0().requestedBox().y() + static_cast<int>(start));
        modifiedBBox.r(input0().requestedBox().r());
        modifiedBBox.t(input0().requestedBox().y() + static_cast<int>(end));

        int ytile = modifiedBBox.y();

        float u = static_cast<float>(modifiedBBox.x());
        float v = static_cast<float>(modifiedBBox.y());

        for ( const float uStart = u,
                          uEnd   = static_cast<float>(modifiedBBox.r()),
                          vEnd   = static_cast<float>(modifiedBBox.t())
             ; v<vEnd ; ++v, u = uStart, ++ytile)
        {           
            DD::Image::Tile::RowPtr p_inMo0 = (*tileVelocity)[vecsChan[0]][ytile];
            DD::Image::Tile::RowPtr p_inMo1 = (*tileVelocity)[vecsChan[1]][ytile];
            DD::Image::Tile::RowPtr p_inMo2 = (*tileVelocity)[vecsChan[2]][ytile];
            DD::Image::Tile::RowPtr p_inMo4 = (*tileVelocity)[vecsChan[3]][ytile];

            for (int xtile = modifiedBBox.x() ; u<uEnd ; ++u, ++xtile)
            {
                const float inMVec[4]
                    { p_inMo0[xtile]
                    , p_inMo1[xtile]
                    , p_inMo2[xtile]
                    , p_inMo4[xtile]
                };

                __m128 v_vectors = _mm_load_ps(inMVec);

                // exit: if no motion vector values, move along
                if (is_vector_zero(v_vectors)) continue;

                __m128 v_uvs = _mm_set_ps(v,u,v,u); //staring point of the curve
                v_inputBBox = _mm_blendv_ps(v_inputBBox, v_uvs, _mm_xor_ps(_mm_castsi128_ps(_mm_cmpgt_epi32(_mm_castps_si128(v_inputBBox), _mm_castps_si128(v_uvs))), v_flip_upper));
                // v_inputBBox = _mm_blendv_ps(v_inputBBox, v_uvs, _mm_xor_ps(_mm_cmpgt_ps(v_inputBBox, v_uvs), v_flip_upper));

                __m128 v_mid, v_curve_aabb;
                    
                vector_fix_error_range(v_vectors);
                (*curve_mid_Temp_Func)(v_uvs, v_mid, v_vectors);
                (*curve_shutter_Temp_Func)(v_uvs, v_mid, v_vectors, v_shutter, v_shutterMid);
                    
                curve_aabb(v_curve_aabb, v_uvs, v_mid, v_vectors);
                v_outputBBox = _mm_blendv_ps(v_outputBBox, v_curve_aabb, _mm_xor_ps(_mm_castsi128_ps(_mm_cmpgt_epi32(_mm_castps_si128(v_outputBBox), _mm_castps_si128(v_curve_aabb))), v_flip_upper));
                // v_outputBBox = _mm_blendv_ps(v_outputBBox, v_curve_aabb, _mm_xor_ps(_mm_cmpgt_ps(v_outputBBox, v_curve_aabb), v_flip_upper));
            }
        }

        // Merging aabb back to main data holder
        std::lock_guard<std::mutex> guard(m_lock_tiles);

        CACHE_ALIGNED int localAABB[4];
        _mm_store_si128((__m128i*)localAABB, _mm_cvttps_epi32(v_outputBBox));
        outputAABB += localAABB;

        _mm_store_si128((__m128i*)localAABB, _mm_cvttps_epi32(v_inputBBox));
        inputAABB += localAABB;

        PRINT_FUNC_TAIL
    }

    template <typename F1, typename F2>
    void get_bbox_control_mt(const unsigned& id, F1 curve_mid_Temp_Func, F2 curve_shutter_Temp_Func)
    {
        PRINT_FUNC_HEAD

        int start = threadsWorkManager[id].start;
        int end   = threadsWorkManager[id].end;

        const __m128 v_0d5 = _mm_set1_ps(0.5f);
        const __m128 v_flip_upper = _mm_castsi128_ps(_mm_set_epi32(0xffffffff,0xffffffff,0,0));

        constexpr float iMax = static_cast<float>(std::numeric_limits<int>::max());
        __m128 v_outputBBox = _mm_set_ps(-iMax, -iMax, iMax, iMax);
        __m128 v_inputBBox  = _mm_set_ps(-iMax, -iMax, iMax, iMax);

        DD::Image::Box modifiedBBox;
        modifiedBBox.x(input0().requestedBox().x());
        modifiedBBox.y(input0().requestedBox().y() + static_cast<int>(start));
        modifiedBBox.r(input0().requestedBox().r());
        modifiedBBox.t(input0().requestedBox().y() + static_cast<int>(end));

        int ytile = modifiedBBox.y();

        float u = static_cast<float>(modifiedBBox.x());
        float v = static_cast<float>(modifiedBBox.y());

        for ( const float uStart = u,
                          uEnd   = static_cast<float>(modifiedBBox.r()),
                          vEnd   = static_cast<float>(modifiedBBox.t())
             ; v<vEnd ; ++v, u = uStart, ++ytile)
        {           
            DD::Image::Tile::RowPtr p_inMo0 = (*tileVelocity)[vecsChan[0]][ytile];
            DD::Image::Tile::RowPtr p_inMo1 = (*tileVelocity)[vecsChan[1]][ytile];
            DD::Image::Tile::RowPtr p_inMo2 = (*tileVelocity)[vecsChan[2]][ytile];
            DD::Image::Tile::RowPtr p_inMo4 = (*tileVelocity)[vecsChan[3]][ytile];

            DD::Image::Tile::RowPtr p_inCtrl = (*tileControl)[cntlChan[0]][ytile];

            for (int xtile = modifiedBBox.x() ; u<uEnd ; ++u, ++xtile)
            {
                const float inMVec[4]
                    { p_inMo0[xtile]
                    , p_inMo1[xtile]
                    , p_inMo2[xtile]
                    , p_inMo4[xtile]
                };

                const float inCntl = p_inCtrl[xtile];

                __m128 v_vectors = _mm_load_ps(inMVec);

                // exit: if no motion vector values, move along
                if (is_vector_zero(v_vectors)) continue;
                if ((inCntl)==0.0f) continue;

                float userShutter1 = kShutterMultiplier * (inCntl) * 2.0f;
                float userShutter0 = userShutter1 - 1.0f;
                userShutter1 = userShutter1 < 0.0f ? 0.0f : userShutter1 > 1.0f ? 1.0f : userShutter1 ;
                userShutter0 = userShutter0 < 0.0f ? 0.0f : userShutter0 > 1.0f ? 1.0f : userShutter0 ;
                const __m128 v_shutter    = _mm_setr_ps(userShutter1, userShutter1, userShutter0, userShutter0);
                const __m128 v_shutterMid = _mm_mul_ps(v_shutter, v_0d5);

                __m128 v_uvs = _mm_set_ps(v,u,v,u); //staring point of the curve
                v_inputBBox = _mm_blendv_ps(v_inputBBox, v_uvs, _mm_xor_ps(_mm_castsi128_ps(_mm_cmpgt_epi32(_mm_castps_si128(v_inputBBox), _mm_castps_si128(v_uvs))), v_flip_upper));
                // v_inputBBox = _mm_blendv_ps(v_inputBBox, v_uvs, _mm_xor_ps(_mm_cmpgt_ps(v_inputBBox, v_uvs), v_flip_upper));

                __m128 v_mid, v_curve_aabb;
                    
                vector_fix_error_range(v_vectors);
                (*curve_mid_Temp_Func)(v_uvs, v_mid, v_vectors);
                (*curve_shutter_Temp_Func)(v_uvs, v_mid, v_vectors, v_shutter, v_shutterMid);
                    
                curve_aabb(v_curve_aabb, v_uvs, v_mid, v_vectors);
                v_outputBBox = _mm_blendv_ps(v_outputBBox, v_curve_aabb, _mm_xor_ps(_mm_castsi128_ps(_mm_cmpgt_epi32(_mm_castps_si128(v_outputBBox), _mm_castps_si128(v_curve_aabb))), v_flip_upper));
                // v_outputBBox = _mm_blendv_ps(v_outputBBox, v_curve_aabb, _mm_xor_ps(_mm_cmpgt_ps(v_outputBBox, v_curve_aabb), v_flip_upper));
            }
        }

        // Merging aabb back to main data holder
        std::lock_guard<std::mutex> guard(m_lock_tiles);

        CACHE_ALIGNED int localAABB[4];
        _mm_store_si128((__m128i*)localAABB, _mm_cvttps_epi32(v_outputBBox));
        outputAABB += localAABB;

        _mm_store_si128((__m128i*)localAABB, _mm_cvttps_epi32(v_inputBBox));
        inputAABB += localAABB;

        // float a[4], b[4];
        // _mm_storeu_ps(a, v_inputBBox);
        // _mm_storeu_ps(b, v_outputBBox);
        // Euclid::AtomicWriter()  <<id<<"  "<<modifiedBBox.y()<<"  "<<modifiedBBox.t()<<"\n"
        //                         <<"in : "<<a[0]<<"  "<<a[1]<<"  "<<a[2]<<"  "<<a[3]<<"\n"    
        //                         <<"put: "<<b[0]<<"  "<<b[1]<<"  "<<b[2]<<"  "<<b[3]<<"\n"    
        //                     ;
		PRINT_FUNC_TAIL
    }

    void build_tile_list() 
    {   
		// PRINT_FUNC_HEAD

        //Euclid::Timer stopwatch{"On frame "+std::to_string(static_cast<int>(outputContext().frame())) + ", " + this->node_name() + " build time was"};

        renderTiles.clear();

        uniform_tile_list();

        // PRINT_FUNC_TAIL
    }

    void uniform_tile_list()
    {
		// PRINT_FUNC_HEAD

        tilesCountRows = static_cast<int>(outputBBox.h()/static_cast<float>(uniformTileWidth)) +1;
        tilesCountCols = static_cast<int>(outputBBox.w()/static_cast<float>(uniformTileWidth)) +1;

        renderTiles.resize(tilesCountCols*tilesCountRows);

        if (!(renderTiles.size())) return;

        threadsWorkManager.setWorkloadFair(inputBBox.h());
        DD::Image::Thread::spawn(uniform_tile_list_cb , static_cast<uint32_t>(threadsWorkManager.size()), (void*)this);
        DD::Image::Thread::wait((void*)this);

        int icount = 0;
        for (auto itrTile = renderTiles.begin(); itrTile != renderTiles.end();)
        {
            if (std::get<2>(*itrTile) != 0)
            {
                const int x = (icount%tilesCountCols)*uniformTileWidth;
                const int y = (icount/tilesCountCols)*uniformTileWidth;
                const int r = x + uniformTileWidth;
                const int t = y + uniformTileWidth;

                std::get<0>(*itrTile).x = x;
                std::get<0>(*itrTile).y = y;
                std::get<0>(*itrTile).r = r;
                std::get<0>(*itrTile).t = t;

                // std::cout<<"out: "<<std::get<0>(*itrTile).x<<"  "<<std::get<0>(*itrTile).y<<"  "<<std::get<0>(*itrTile).r<<"  "<<std::get<0>(*itrTile).t<<"\n";
                // std::cout<<" in: "<<std::get<1>(*itrTile).x<<"  "<<std::get<1>(*itrTile).y<<"  "<<std::get<1>(*itrTile).r<<"  "<<std::get<1>(*itrTile).t<<"\n";
                
                ++itrTile;
            }
            else renderTiles.erase(itrTile);

            icount++;
        }
        // PRINT_FUNC_TAIL
    }

    static void uniform_tile_list_cb(unsigned id, unsigned numberCPUthreds, void* _data) 
    { 
		// PRINT_FUNC_HEAD

        switch (((CurvedMotionTrail*)_data)->kCurveOrigin){
            case kCurveOriginEnum::HEAD:
            {
                break;
            }
            case kCurveOriginEnum::CENTER:
            {
                if (((CurvedMotionTrail*)_data)->useControl) 
                    ((CurvedMotionTrail*)_data)->uniform_tile_list_control_mt(id, &curve_points_center, &curve_shutter_center);  
                else 
                    ((CurvedMotionTrail*)_data)->uniform_tile_list_mt(id, &curve_points_center, &curve_shutter_center); 
                break;
            }
            case kCurveOriginEnum::TAIL:
            {
                if (((CurvedMotionTrail*)_data)->useControl) 
                    ((CurvedMotionTrail*)_data)->uniform_tile_list_control_mt(id, &curve_points_tail, &curve_shutter_tail); 
                else 
                    ((CurvedMotionTrail*)_data)->uniform_tile_list_mt(id, &curve_points_tail, &curve_shutter_tail); 
                break;
            }            
        }
        // PRINT_FUNC_TAIL
    }

    template <typename F1, typename F2>
    void uniform_tile_list_mt(const unsigned& id, F1 curve_mid_Temp_Func, F2 curve_shutter_Temp_Func)
    {
		// PRINT_FUNC_HEAD

        int start = threadsWorkManager[id].start;
        int end   = threadsWorkManager[id].end;
        
        std::vector<std::pair<Euclid::AABB<float>, int>> tilesLocal(renderTiles.size());

        float userShutter1 = kShutterMultiplier * 2.0f;
        float userShutter0 = userShutter1 - 1.0f;
        userShutter1 = userShutter1 < 0.0f ? 0.0f : userShutter1 > 1.0f ? 1.0f : userShutter1 ;
        userShutter0 = userShutter0 < 0.0f ? 0.0f : userShutter0 > 1.0f ? 1.0f : userShutter0 ;

        const __m128 v_0d5 = _mm_set1_ps(0.5f);
        const __m128 v_1   = _mm_set1_ps(1.0f);

        const __m128 v_shutter    = _mm_setr_ps(userShutter1, userShutter1, userShutter0, userShutter0);
        const __m128 v_shutterMid = _mm_mul_ps(v_shutter, v_0d5);

        const __m128 v_tileUpperLimit     = _mm_sub_ps(_mm_cvtepi32_ps(_mm_set_epi32(tilesCountRows, tilesCountCols, tilesCountRows, tilesCountCols)), v_1);
        // const __m128i v_tileUpperMult     = _mm_set_epi32(tilesCountCols, 1, tilesCountCols, 1);

        const __m128 v_tilesScaleToFormat = _mm_set1_ps(1.0f / static_cast<float>(uniformTileWidth));
        const __m128 v_upperTrue          = _mm_castsi128_ps(_mm_set_epi32(0xffffffff,0xffffffff,0,0));

        Euclid::AABB<float> uvs;

        int ytile = inputBBox.y() + static_cast<int>(start);

        float u = static_cast<float>(inputBBox.x() - outputBBox.x()) ;
        float v = static_cast<float>(inputBBox.y() - outputBBox.y()) + static_cast<float>(start);

        for ( const float uStart = u,
                          uEnd   = u + static_cast<float>(inputBBox.w()),
                          vEnd   = v + static_cast<float>(end - start)
             ; v<vEnd ; ++v, u = uStart, ++ytile)
        {           
            DD::Image::Tile::RowPtr p_inMo0 = (*tileVelocity)[vecsChan[0]][ytile];
            DD::Image::Tile::RowPtr p_inMo1 = (*tileVelocity)[vecsChan[1]][ytile];
            DD::Image::Tile::RowPtr p_inMo2 = (*tileVelocity)[vecsChan[2]][ytile];
            DD::Image::Tile::RowPtr p_inMo4 = (*tileVelocity)[vecsChan[3]][ytile];

            for (int xtile = inputBBox.x() ; u<uEnd ; ++u, ++xtile)
            {
                const float inMVec[4]
                    { p_inMo0[xtile]
                    , p_inMo1[xtile]
                    , p_inMo2[xtile]
                    , p_inMo4[xtile]
                };

                __m128 v_vectors = _mm_load_ps(inMVec);

                // exit: if no motion vector values, move along
                if (is_vector_zero(v_vectors)) continue;

                __m128 v_uvs = _mm_set_ps(v,u,v,u); //staring point of the curve
                __m128 v_mid, v_curve_aabb;
                
                vector_fix_error_range(v_vectors);
                (*curve_mid_Temp_Func)(v_uvs, v_mid, v_vectors); // mid point for curve
                (*curve_shutter_Temp_Func)(v_uvs, v_mid, v_vectors, v_shutter, v_shutterMid);
                
                curve_aabb(v_curve_aabb, v_uvs, v_mid, v_vectors);

                // // curve aabb in range of tiles indcies
                CACHE_ALIGNED int tilesIndices[4];
                _mm_store_si128((__m128i*)tilesIndices, 
                _mm_cvttps_epi32(_mm_min_ps(v_tileUpperLimit, _mm_max_ps(_mm_setzero_ps(), _mm_mul_ps(v_curve_aabb, v_tilesScaleToFormat)))));

                tilesIndices[1] *= tilesCountCols; 
                tilesIndices[3] *= tilesCountCols;  
                
                uvs.x = u; uvs.y = v;
                uvs.r = u; uvs.t = v;

                for (int j=tilesIndices[1]; j<=tilesIndices[3]; j += tilesCountCols) // rows -> y
                for (int i=tilesIndices[0]; i<=tilesIndices[2]; ++i) // colms -> x
                {
                    tilesLocal[i+j].first += uvs; // input aabb intersection
                    ++tilesLocal[i+j].second;       // tile hits histogram
                }
            }
        }

        {
            // Merging aabb back to main data holder
            std::lock_guard<std::mutex> guard(m_lock_tiles);

            auto itrTilesLocalHistogram = tilesLocal.begin();

            const auto inputTranslate = std::make_pair(outputBBox.x() - inputBBox.x(), outputBBox.y() - inputBBox.y());
            const Euclid::AABB<int> inputClamp{0,0,inputBBox.w(),inputBBox.h()};
            for(auto& tile: renderTiles)
            {                
                Euclid::AABB<int> lTile 
                    { static_cast<int>((*itrTilesLocalHistogram).first.x)
                    , static_cast<int>((*itrTilesLocalHistogram).first.y)
                    , static_cast<int>((*itrTilesLocalHistogram).first.r)
                    , static_cast<int>((*itrTilesLocalHistogram).first.t)
                };

                ++lTile.r;
                ++lTile.t;
                lTile.expend();
                lTile.translate(inputTranslate);
                lTile.intersect(inputClamp);
                lTile.translatei(inputTranslate);

                std::get<1>(tile).merge(lTile);// input AABB
                std::get<2>(tile) +=    (*itrTilesLocalHistogram).second;// Hit Histogram
                ++itrTilesLocalHistogram;
            }           
        }
        // PRINT_FUNC_TAIL
    }

    template <typename F1, typename F2>
    void uniform_tile_list_control_mt(const unsigned& id, F1 curve_mid_Temp_Func, F2 curve_shutter_Temp_Func)
    {
		// PRINT_FUNC_HEAD

        int start = threadsWorkManager[id].start;
        int end   = threadsWorkManager[id].end;
        
        std::vector<std::pair<Euclid::AABB<float>, int>> tilesLocal(renderTiles.size());

        const __m128 v_0d5 = _mm_set1_ps(0.5f);
        const __m128 v_1   = _mm_set1_ps(1.0f);

        const __m128 v_tileUpperLimit     = _mm_sub_ps(_mm_cvtepi32_ps(_mm_set_epi32(tilesCountRows, tilesCountCols, tilesCountRows, tilesCountCols)), v_1);
        // const __m128i v_tileUpperMult     = _mm_set_epi32(tilesCountCols, 1, tilesCountCols, 1);

        const __m128 v_tilesScaleToFormat = _mm_set1_ps(1.0f / static_cast<float>(uniformTileWidth));
        const __m128 v_upperTrue          = _mm_castsi128_ps(_mm_set_epi32(0xffffffff,0xffffffff,0,0));
        
        Euclid::AABB<float> uvs;

        int ytile = inputBBox.y() + static_cast<int>(start);

        float u = static_cast<float>(inputBBox.x() - outputBBox.x()) ;
        float v = static_cast<float>(inputBBox.y() - outputBBox.y()) + static_cast<float>(start);
    
        for ( const float uStart = u,
                          uEnd   = u + static_cast<float>(inputBBox.w()),
                          vEnd   = v + static_cast<float>(end - start)
             ; v<vEnd ; ++v, u = uStart, ++ytile)
        {
            DD::Image::Tile::RowPtr p_inMo0 = (*tileVelocity)[vecsChan[0]][ytile];
            DD::Image::Tile::RowPtr p_inMo1 = (*tileVelocity)[vecsChan[1]][ytile];
            DD::Image::Tile::RowPtr p_inMo2 = (*tileVelocity)[vecsChan[2]][ytile];
            DD::Image::Tile::RowPtr p_inMo4 = (*tileVelocity)[vecsChan[3]][ytile];

            DD::Image::Tile::RowPtr p_inCtrl = (*tileControl)[cntlChan[0]][ytile];

            for (int xtile = inputBBox.x() ; u<uEnd ; ++u, ++xtile)
            {
                const float inMVec[4]
                    { p_inMo0[xtile]
                    , p_inMo1[xtile]
                    , p_inMo2[xtile]
                    , p_inMo4[xtile]
                };

                const float inCntl = p_inCtrl[xtile];

                __m128 v_vectors = _mm_load_ps(inMVec);

                // exit: if no motion vector values, move along
                if (is_vector_zero(v_vectors)) continue;
                if ((inCntl)==0.0f) continue;

                float userShutter1 = kShutterMultiplier * (inCntl) * 2.0f;
                float userShutter0 = userShutter1 - 1.0f;
                userShutter1 = userShutter1 < 0.0f ? 0.0f : userShutter1 > 1.0f ? 1.0f : userShutter1 ;
                userShutter0 = userShutter0 < 0.0f ? 0.0f : userShutter0 > 1.0f ? 1.0f : userShutter0 ;
                const __m128 v_shutter    = _mm_setr_ps(userShutter1, userShutter1, userShutter0, userShutter0);
                const __m128 v_shutterMid = _mm_mul_ps(v_shutter, v_0d5);

                __m128 v_uvs = _mm_set_ps(v,u,v,u); //staring point of the curve
                __m128 v_mid, v_curve_aabb;
                
                vector_fix_error_range(v_vectors);
                (*curve_mid_Temp_Func)(v_uvs, v_mid, v_vectors); // mid point for curve
                (*curve_shutter_Temp_Func)(v_uvs, v_mid, v_vectors, v_shutter, v_shutterMid);
                
                curve_aabb(v_curve_aabb, v_uvs, v_mid, v_vectors);

                // // curve aabb in range of tiles indcies
                CACHE_ALIGNED int tilesIndices[4];
                _mm_store_si128((__m128i*)tilesIndices, 
                _mm_cvttps_epi32(_mm_min_ps(v_tileUpperLimit, _mm_max_ps(_mm_setzero_ps(), _mm_mul_ps(v_curve_aabb, v_tilesScaleToFormat)))));

                tilesIndices[1] *= tilesCountCols; 
                tilesIndices[3] *= tilesCountCols;  
                
                uvs.x = u; uvs.y = v;
                uvs.r = u; uvs.t = v;

                for (int j=tilesIndices[1]; j<=tilesIndices[3]; j += tilesCountCols) // rows -> y
                for (int i=tilesIndices[0]; i<=tilesIndices[2]; ++i) // colms -> x
                {
                    tilesLocal[i+j].first += uvs; // input aabb intersection
                    ++tilesLocal[i+j].second;       // tile hits histogram
                }
            }
        }

        {
            // Merging aabb back to main data holder
            std::lock_guard<std::mutex> guard(m_lock_tiles);

            auto itrTilesLocalHistogram = tilesLocal.begin();

            const auto inputTranslate = std::make_pair(outputBBox.x() - inputBBox.x(), outputBBox.y() - inputBBox.y());
            const Euclid::AABB<int> inputClamp{0,0,inputBBox.w(),inputBBox.h()};
            for(auto& tile: renderTiles)
            {
                Euclid::AABB<int> lTile 
                    { static_cast<int>((*itrTilesLocalHistogram).first.x)
                    , static_cast<int>((*itrTilesLocalHistogram).first.y)
                    , static_cast<int>((*itrTilesLocalHistogram).first.r)
                    , static_cast<int>((*itrTilesLocalHistogram).first.t)
                };

                ++lTile.r;
                ++lTile.t;
                lTile.expend();
                lTile.translate(inputTranslate);
                lTile.intersect(inputClamp);
                lTile.translatei(inputTranslate);

                std::get<1>(tile).merge(lTile);// input AABB
                std::get<2>(tile) +=    (*itrTilesLocalHistogram).second;// Hit Histogram
                ++itrTilesLocalHistogram;
            }        
        }
        // PRINT_FUNC_TAIL
    }

    void render_tile_list() 
    {   
		// PRINT_FUNC_HEAD
        // std::cout<<"\n";
        //Euclid::Timer stopwatch{"On frame "+std::to_string(static_cast<int>(outputContext().frame())) + ", " + this->node_name() + " render time was"};
        DD::Image::Thread::spawn(render_tiles_cb , static_cast<uint32_t>(threadsWorkManager.m_threads), (void*)this);
        DD::Image::Thread::wait((void*)this);
    }

    static void render_tiles_cb(unsigned id, unsigned numberCPUthreds, void* _data) 
    { 
		// PRINT_FUNC_HEAD

        switch (((CurvedMotionTrail*)_data)->kCurveOrigin){
            case kCurveOriginEnum::HEAD:
            {
                break;
            }
            case kCurveOriginEnum::CENTER:
            {
                if (((CurvedMotionTrail*)_data)->useControl) 
                    ((CurvedMotionTrail*)_data)->render_tiles_control_mt(id, &curve_points_center, &curve_shutter_center);
                else 
                    ((CurvedMotionTrail*)_data)->render_tiles_mt(id, &curve_points_center, &curve_shutter_center);
                break;
            }
            case kCurveOriginEnum::TAIL:
            {
                if (((CurvedMotionTrail*)_data)->useControl) 
                    ((CurvedMotionTrail*)_data)->render_tiles_control_mt(id, &curve_points_tail, &curve_shutter_tail);
                else 
                    ((CurvedMotionTrail*)_data)->render_tiles_mt(id, &curve_points_tail, &curve_shutter_tail);
                break;
            }            
        }
        // PRINT_FUNC_TAIL
    }
    
    template <typename F1, typename F2>
    void render_tiles_mt(const unsigned& id, F1 curve_mid_Temp_Func, F2 curve_shutter_Temp_Func)
    {
		// PRINT_FUNC_HEAD
        // Euclid::Timer stopwatch{"On frame "+std::to_string(static_cast<int>(outputContext().frame())) + ", id:" + std::to_string(id) + ",  " + this->node_name() + " build time was"};

        const int bufferPedding  = 2; 

        CACHE_ALIGNED std::vector<float> tileBuffer;

        float userShutter1 = kShutterMultiplier * 2.0f;
        float userShutter0 = userShutter1 - 1.0f;
        userShutter1 = userShutter1 < 0.0f ? 0.0f : userShutter1 > 1.0f ? 1.0f : userShutter1 ;
        userShutter0 = userShutter0 < 0.0f ? 0.0f : userShutter0 > 1.0f ? 1.0f : userShutter0 ;

        const __m128 v_0d5 = _mm_set1_ps(0.5f);
        const __m128 v_shutter    = _mm_setr_ps(userShutter1, userShutter1, userShutter0, userShutter0);
        const __m128 v_shutterMid = _mm_mul_ps(v_shutter, v_0d5);

        for(;;)
        {
            if (Op::aborted())	return;

            Euclid::AABB<int> tileOutputAABB, tileInputAABB;
            int histo;
            {
                // grab a tile from queue
                std::lock_guard<std::mutex> guard(m_lock_tiles);
                
                if (renderTiles.size())
                {
                    tileOutputAABB = std::get<0>(renderTiles.back()); // tile aabb
                    tileInputAABB  = std::get<1>(renderTiles.back()); // input image aabb
                    histo = std::get<2>(renderTiles.back());
                    renderTiles.pop_back();
                }
                else return;
            }
           
            tileOutputAABB.expend(bufferPedding);

            const int allocSize = tileOutputAABB.w()*tileOutputAABB.h()*tileChannelsSize + tileOutputAABB.w()*tileChannelsSize + tileChannelsSize;
            if (allocSize!=tileBuffer.size())
                tileBuffer.resize(allocSize);
            else
                memset(tileBuffer.data(), 0, sizeof(float)*tileBuffer.size());

            // tile input start location of x and y
            int u = tileInputAABB.x-tileOutputAABB.x;
            int v = tileInputAABB.y-tileOutputAABB.y;

            const int uStart = u;
            const int uEnd   = u + tileInputAABB.w() ;
            const int vEnd   = v + tileInputAABB.h() ;

            const __m128 v_bbox = _mm_setr_ps(0, 0, static_cast<float>(tileOutputAABB.w()+1), static_cast<float>(tileOutputAABB.h()+1));
            float* const v_outBilinear[4] = { tileBuffer.data() 
                                            , tileBuffer.data() + tileChannelsSize
                                            , tileBuffer.data() + tileOutputAABB.w()*tileChannelsSize
                                            , tileBuffer.data() + tileOutputAABB.w()*tileChannelsSize + tileChannelsSize};

            for ( int ytile = tileInputAABB.y + outputBBox.y() ; v<vEnd ; ++v, u = uStart, ++ytile )
            {
                DD::Image::Tile::RowPtr p_inRed = (*tileRGBA)[DD::Image::Chan_Red]  [ytile];
                DD::Image::Tile::RowPtr p_inGrn = (*tileRGBA)[DD::Image::Chan_Green][ytile];
                DD::Image::Tile::RowPtr p_inBlu = (*tileRGBA)[DD::Image::Chan_Blue] [ytile];
                DD::Image::Tile::RowPtr p_inAlp = (*tileRGBA)[DD::Image::Chan_Alpha][ytile];

                DD::Image::Tile::RowPtr p_inMo0 = (*tileVelocity)[vecsChan[0]][ytile];
                DD::Image::Tile::RowPtr p_inMo1 = (*tileVelocity)[vecsChan[1]][ytile];
                DD::Image::Tile::RowPtr p_inMo2 = (*tileVelocity)[vecsChan[2]][ytile];
                DD::Image::Tile::RowPtr p_inMo4 = (*tileVelocity)[vecsChan[3]][ytile];

                for ( int xtile = tileInputAABB.x + outputBBox.x() ; u<uEnd ; ++u, ++xtile)
                {   
                    const float inMVec[4]
                        { p_inMo0[xtile]
                        , p_inMo1[xtile]
                        , p_inMo2[xtile]
                        , p_inMo4[xtile]
                    };

                    const float inRGBA[4]
                        { p_inRed[xtile]
                        , p_inGrn[xtile]
                        , p_inBlu[xtile]
                        , p_inAlp[xtile]
                    };

                    __m128 v_vectors = _mm_load_ps(inMVec);

                    // exit: if no motion vector values, move along
                    if (is_vector_zero(v_vectors)) continue;

                    // if ((u < 0) || (v < 0) || (u >= tileOutputAABB.w()) || (v >= tileOutputAABB.h())) continue;
                    // const int plotOffset = (u + v*tileOutputAABB.w())*tileChannelsSize;
                    // float* m_output = tileBuffer.data()+plotOffset;
                    // m_output[0] = inMVec[0];
                    // m_output[1] = inMVec[1];
                    // m_output[2] = inMVec[2];
                    // m_output[3] = inMVec[3];
                    // m_output[4] = 1.0f;
                    // continue;

                    vector_fix_error_range(v_vectors);
                    
                    __m128 v_uvs = _mm_cvtepi32_ps(_mm_set_epi32(v,u,v,u)); //staring point of the curve
                    __m128 v_mid;
                    (*curve_mid_Temp_Func)(v_uvs, v_mid, v_vectors); // mid point for curve
                    (*curve_shutter_Temp_Func)(v_uvs, v_mid, v_vectors, v_shutter, v_shutterMid);

                    CACHE_ALIGNED float quad[16];
                    curve_coefficients(quad, v_uvs, v_mid, v_vectors); // two quadratic bezier splines coefficients

                    float roots_inter[16]; // intersection with tile output
                    curve_roots_intersection(roots_inter,   quad,   v_bbox); // only the top 6 are releveant
                    curve_roots_intersection(roots_inter+6, quad+8, v_bbox); // shifting 8 forward

                    float arcLength[2];
                    curve_arc_length(arcLength, quad);

                    const __m128 v_rgba =_mm_load_ps(inRGBA); //color of spline
                    render_spline_to_buffer(v_outBilinear, v_rgba, 2, tileOutputAABB.w(), tileOutputAABB.h(), roots_inter, quad, arcLength );
                }
            }

            copy_tile_to_buffer(tileBuffer.data(), tileOutputAABB, tileChannelsSize, bufferPedding);
        }
        // PRINT_FUNC_TAIL
    }

    template <typename F1, typename F2>
    void render_tiles_control_mt(const unsigned& id, F1 curve_mid_Temp_Func, F2 curve_shutter_Temp_Func)
    {
        // PRINT_FUNC_HEAD

        // copying render_tiles_mt function and adding control effect on the splines
        // I know... it is dumb, but it is for speed...
        const int bufferPedding  = 2; 

        CACHE_ALIGNED std::vector<float> tileBuffer;

        const __m128 v_0d5 = _mm_set1_ps(0.5f);

        for(;;)
        {
            if (Op::aborted())	return;

            Euclid::AABB<int> tileOutputAABB, tileInputAABB;
            int histo;
            {
                // grab a tile from queue
                std::lock_guard<std::mutex> guard(m_lock_tiles);
                
                if (renderTiles.size())
                {
                    tileOutputAABB = std::get<0>(renderTiles.back()); // tile aabb
                    tileInputAABB  = std::get<1>(renderTiles.back()); // input image aabb
                    histo = std::get<2>(renderTiles.back());
                    renderTiles.pop_back();
                }
                else return;
            }
           
            tileOutputAABB.expend(bufferPedding);

            const int allocSize = tileOutputAABB.w()*tileOutputAABB.h()*tileChannelsSize + tileOutputAABB.w()*tileChannelsSize + tileChannelsSize;
            if (allocSize!=tileBuffer.size())
                tileBuffer.resize(allocSize);
            else
                memset(tileBuffer.data(), 0, sizeof(float)*tileBuffer.size());

            // tile input start location of x and y
            int u = tileInputAABB.x-tileOutputAABB.x;
            int v = tileInputAABB.y-tileOutputAABB.y;

            const int uStart = u;
            const int uEnd   = u + tileInputAABB.w();
            const int vEnd   = v + tileInputAABB.h();

            const __m128 v_bbox = _mm_setr_ps(0, 0, static_cast<float>(tileOutputAABB.w()+1), static_cast<float>(tileOutputAABB.h()+1));
            float* const v_outBilinear[4] = { tileBuffer.data() 
                                            , tileBuffer.data() + tileChannelsSize
                                            , tileBuffer.data() + tileOutputAABB.w()*tileChannelsSize
                                            , tileBuffer.data() + tileOutputAABB.w()*tileChannelsSize + tileChannelsSize};

            for ( int ytile = tileInputAABB.y + outputBBox.y() ; v<vEnd ; ++v, u = uStart, ++ytile )
            {
                DD::Image::Tile::RowPtr p_inRed = (*tileRGBA)[DD::Image::Chan_Red]  [ytile];
                DD::Image::Tile::RowPtr p_inGrn = (*tileRGBA)[DD::Image::Chan_Green][ytile];
                DD::Image::Tile::RowPtr p_inBlu = (*tileRGBA)[DD::Image::Chan_Blue] [ytile];
                DD::Image::Tile::RowPtr p_inAlp = (*tileRGBA)[DD::Image::Chan_Alpha][ytile];
                
                DD::Image::Tile::RowPtr p_inMo0 = (*tileVelocity)[vecsChan[0]][ytile];
                DD::Image::Tile::RowPtr p_inMo1 = (*tileVelocity)[vecsChan[1]][ytile];
                DD::Image::Tile::RowPtr p_inMo2 = (*tileVelocity)[vecsChan[2]][ytile];
                DD::Image::Tile::RowPtr p_inMo4 = (*tileVelocity)[vecsChan[3]][ytile];

                DD::Image::Tile::RowPtr p_inCtrl = (*tileControl)[cntlChan[0]][ytile];

                for ( int xtile = tileInputAABB.x + outputBBox.x() ; u<uEnd ; ++u, ++xtile)
                {   
                    const float inMVec[4]
                        { p_inMo0[xtile]
                        , p_inMo1[xtile]
                        , p_inMo2[xtile]
                        , p_inMo4[xtile]
                    };

                    const float inRGBA[4]
                        { p_inRed[xtile]
                        , p_inGrn[xtile]
                        , p_inBlu[xtile]
                        , p_inAlp[xtile]
                    };

                    const float inCntl = p_inCtrl[xtile];

                    __m128 v_vectors = _mm_load_ps(inMVec);

                    // exit: if no motion vector values, move along
                    if (is_vector_zero(v_vectors)) continue;
                    if ((inCntl)==0.0f) continue;
        
                    float userShutter1 = kShutterMultiplier * (inCntl) * 2.0f;
                    float userShutter0 = userShutter1 - 1.0f;
                    userShutter1 = userShutter1 < 0.0f ? 0.0f : userShutter1 > 1.0f ? 1.0f : userShutter1 ;
                    userShutter0 = userShutter0 < 0.0f ? 0.0f : userShutter0 > 1.0f ? 1.0f : userShutter0 ;
                    const __m128 v_shutter    = _mm_setr_ps(userShutter1, userShutter1, userShutter0, userShutter0);
                    const __m128 v_shutterMid = _mm_mul_ps(v_shutter, v_0d5);

                    vector_fix_error_range(v_vectors);
                    
                    __m128 v_uvs = _mm_cvtepi32_ps(_mm_set_epi32(v,u,v,u)); //staring point of the curve
                    __m128 v_mid;
                    (*curve_mid_Temp_Func)(v_uvs, v_mid, v_vectors); // mid point for curve
                    (*curve_shutter_Temp_Func)(v_uvs, v_mid, v_vectors, v_shutter, v_shutterMid);

                    CACHE_ALIGNED float quad[16];
                    curve_coefficients(quad, v_uvs, v_mid, v_vectors); // two quadratic bezier splines coefficients

                    float roots_inter[16]; // intersection with tile output
                    curve_roots_intersection(roots_inter,   quad,   v_bbox); // only the top 6 are releveant
                    curve_roots_intersection(roots_inter+6, quad+8, v_bbox); // shifting 8 forward

                    float arcLength[2];
                    curve_arc_length(arcLength, quad);

                    // raster splines
                    const __m128 v_rgba = _mm_load_ps(inRGBA); //color of spline
                    const unsigned int splinesCout = (inCntl)<0.5f ? 0 : 2 ;
                    render_spline_to_buffer(v_outBilinear, v_rgba, splinesCout, tileOutputAABB.w(), tileOutputAABB.h(), roots_inter, quad, arcLength );
                }
            }            

            copy_tile_to_buffer(tileBuffer.data(), tileOutputAABB, tileChannelsSize, bufferPedding);
        }
        // PRINT_FUNC_TAIL
    }

    void render_spline_to_buffer( float* const buffer[], const __m128& v_color
                                , const unsigned int& splinesCout, const int& bufferWidth, const int& bufferHeight
                                , const float* const intersections, const float* const coefficients, float* const length )
    {

        const __m128 v_signbit     = _mm_set1_ps(-0.0f);

        const float fullLength = length[0] + length[1];
        const float ratioLength[2]  { fullLength < 1e-5 ? 0.0f : length[0]/fullLength
                                    , fullLength < 1e-5 ? 0.0f : length[1]/fullLength};
        length[0] = length[0] < 1e-5 ? 1.0f : 1.0f/length[0];
        length[1] = length[1] < 1e-5 ? 1.0f : 1.0f/length[1];

        for (unsigned int spline = 0; spline<splinesCout; ++spline)
        {

            const float* p_quad =  &coefficients[spline<<3]; // shifting the pointer 8 float, next spline
            const float step = length[spline];
            const float shiftLut = spline == 1 ? ratioLength[0] : 0;

            const __m128 v_coeffx = _mm_load_ps(p_quad);
            const __m128 v_coeffy = _mm_load_ps(p_quad+4);

            const __m128 v_ta = _mm_shuffle_ps(v_coeffx, v_coeffy, _MM_SHUFFLE( 0,0,0,0));   // a
            const __m128 v_tb = _mm_shuffle_ps(v_coeffx, v_coeffy, _MM_SHUFFLE( 1,1,1,1));   // b
            const __m128 v_tc = _mm_shuffle_ps(v_coeffx, v_coeffy, _MM_SHUFFLE( 2,2,2,2));   // c

            const __m128 v_a     = _mm_shuffle_ps(v_ta, v_ta, _MM_SHUFFLE( 0,2,2,0));   // xyyx
            const __m128 v_b     = _mm_shuffle_ps(v_tb, v_tb, _MM_SHUFFLE( 0,2,2,0));   // xyyx
            const __m128 v_c     = _mm_shuffle_ps(v_tc, v_tc, _MM_SHUFFLE( 0,2,2,0));   // xyyx
            const __m128 v_1half = _mm_set_ps(0.0f, 0.0f, 1.0f, 1.0f);

            for (unsigned int segment = 0; segment<3; ++segment)
            {
                const int rootIndex = (spline==0?0:6) + (segment<<1);
                float       t    = intersections[rootIndex];
                const float tend = intersections[rootIndex+1];

                const __m128 v_step = _mm_set1_ps(step);
                __m128 v_t = _mm_set1_ps(t);

                for (; t<tend; t += step)
                {

                    const __m128  v_uvst = _mm_add_ps(_mm_mul_ps(_mm_add_ps(_mm_mul_ps(v_a ,v_t), v_b), v_t), v_c);
                    const __m128i v_uvsi = _mm_cvttps_epi32(v_uvst);
                    v_t = _mm_add_ps(v_t,v_step);

                    CACHE_ALIGNED int iuvs[4];
                    _mm_store_si128((__m128i*)iuvs, v_uvsi);

                    const int plotOffset = (iuvs[0] + iuvs[1]*bufferWidth)*tileChannelsSize; 

                    if ((iuvs[0] < 0) | (iuvs[1] < 0) | (iuvs[0] >= bufferWidth) | (iuvs[1] >= bufferHeight)) continue;

                    const __m128 v_bilinear = _mm_andnot_ps(v_signbit, _mm_sub_ps(_mm_sub_ps(v_uvst, v_1half), _mm_cvtepi32_ps(v_uvsi)));
                    const __m128 v_filter   = _mm_mul_ps(_mm_mul_ps(_mm_set1_ps(1.0f), v_bilinear), _mm_shuffle_ps(v_bilinear, v_bilinear, _MM_SHUFFLE( 2,0,3,1)));
                    
                    CACHE_ALIGNED float filter[4];
                    _mm_store_ps(filter, v_filter);

                    float* const m_output[4] =  { buffer[0] + plotOffset
                                                , buffer[1] + plotOffset
                                                , buffer[2] + plotOffset
                                                , buffer[3] + plotOffset};

                    *(m_output[0]+4) += filter[0];
                    *(m_output[1]+4) += filter[1];
                    *(m_output[2]+4) += filter[2];
                    *(m_output[3]+4) += filter[3];

                    const float lutSample = getTransparecnyLUT(shiftLut + t*ratioLength[spline]);
                    const __m128 v_rgbaFaded = _mm_mul_ps(v_color, _mm_set1_ps(lutSample));

                    _mm_storeu_ps(m_output[0],_mm_add_ps(_mm_loadu_ps(m_output[0]),_mm_mul_ps(v_rgbaFaded, _mm_shuffle_ps(v_filter, v_filter, _MM_SHUFFLE(0,0,0,0)))));
                    _mm_storeu_ps(m_output[1],_mm_add_ps(_mm_loadu_ps(m_output[1]),_mm_mul_ps(v_rgbaFaded, _mm_shuffle_ps(v_filter, v_filter, _MM_SHUFFLE(1,1,1,1)))));
                    _mm_storeu_ps(m_output[2],_mm_add_ps(_mm_loadu_ps(m_output[2]),_mm_mul_ps(v_rgbaFaded, _mm_shuffle_ps(v_filter, v_filter, _MM_SHUFFLE(2,2,2,2)))));
                    _mm_storeu_ps(m_output[3],_mm_add_ps(_mm_loadu_ps(m_output[3]),_mm_mul_ps(v_rgbaFaded, _mm_shuffle_ps(v_filter, v_filter, _MM_SHUFFLE(3,3,3,3)))));
                }
            }
        }
    }
    template<class T>
    void copy_tile_to_buffer(const float* const p_tile, const Euclid::AABB<T>& tileAABB, const int& tileChannelsSize, const int& pedding)
    {
        // PRINT_DEBUG
        const auto outputTranslate = std::make_pair(outputBBox.x(), outputBBox.y());
    
        Euclid::AABB<T> m_AABB = tileAABB;
        m_AABB.shrink(pedding);
        m_AABB.translate(outputTranslate);
        m_AABB.intersect(outputBBox);
        m_AABB.translatei(outputTranslate);

        float* outRed   = memoryBlocks[0].GetFloatPtr() + (m_AABB.x + m_AABB.y * outputBBox.w());
        float* outGreen = memoryBlocks[1].GetFloatPtr() + (m_AABB.x + m_AABB.y * outputBBox.w());
        float* outBlue  = memoryBlocks[2].GetFloatPtr() + (m_AABB.x + m_AABB.y * outputBBox.w());
        float* outAlpha = memoryBlocks[3].GetFloatPtr() + (m_AABB.x + m_AABB.y * outputBBox.w());

        const float* p_input = p_tile + (pedding * tileChannelsSize * (tileAABB.w() + 1)) + (tileChannelsSize-1) ;

        const int intputLineOffset = (tileAABB.w() - m_AABB.w())* tileChannelsSize; 
        const int outputLineOffset = outputBBox.w() - m_AABB.w(); 
        const int yEnd = m_AABB.h();
        for ( int y = 0 ; y<yEnd  ; ++y
            , outRed   += outputLineOffset, outGreen += outputLineOffset, outBlue  += outputLineOffset, outAlpha += outputLineOffset
            , p_input += intputLineOffset)
        for ( const float* const outEnd = outRed + m_AABB.w()
            ; outRed<outEnd 
            ; ++outRed, ++outGreen, ++outBlue, ++outAlpha, p_input += tileChannelsSize)
        {

            if (*p_input == 0.0f) continue;
            const float recpAccum = *p_input < 5.0f ? 1.0f / ((5.0f + (*p_input)) * 0.5f) : 1.0f / (*p_input);
            // const float recpAccum = 1.0f / (*p_input) ;
            // const float recpAccum = (*p_input) < 1.0f ? 1.0f : 1.0f / (*p_input) ;
            *outAlpha = *(p_input-1) * recpAccum;
            *outBlue  = *(p_input-2) * recpAccum;
            *outGreen = *(p_input-3) * recpAccum;
            *outRed   = *(p_input-4) * recpAccum;
        }
    }

    void buildTransparencyLUT()
    {
        float counter = 0.0f;
        for (auto& lut : transparencyCurveLUT)
        {
            lut.first = static_cast<float>(kTransparencyLookupCurves.getValue(0, counter / transparencyCurveLUTsizef));
            ++counter;

            lut.second = static_cast<float>(kTransparencyLookupCurves.getValue(0, counter / transparencyCurveLUTsizef));
            lut.second -= lut.first;
        }
        
        // for (auto l:transparencyCurveLUT) std::cout<<l.x<<"  "<<l.y<<"\n";
    }

    float getTransparecnyLUT(const float& index)
    {
        float indexInterval = index * transparencyCurveLUTsizef;
        int indexA  = indexInterval >= transparencyCurveLUTsizef ? transparencyCurveLUTsize-1 : static_cast<int>(indexInterval);
        indexInterval -= static_cast<float>(indexA);
        
        return transparencyCurveLUT[indexA].first + transparencyCurveLUT[indexA].second * indexInterval;
    }

    ////////////////////////////////////////// 
    //      SIMD helpers functions          //
    ////////////////////////////////////////// 
    
    EUCLID_INLINE static bool is_vector_zero(const __m128& v) 
    {
        const __m128 v_signbit     = _mm_set1_ps(-0.0f);
        // checking if all values are zero
        return !_mm_movemask_epi8(_mm_cmpgt_epi32(_mm_castps_si128(_mm_andnot_ps(v_signbit, v)), _mm_setzero_si128()));
    }

    EUCLID_INLINE static void vector_fix_error_range(__m128& v_vectors) 
    {
        const __m128 v_nonfinite   = _mm_set1_ps(0x7f800000);
        const __m128 v_maxfloat   = _mm_set1_ps(65504.0f);
        const __m128 v_signbit     = _mm_set1_ps(-0.0f);

        // fixing vectors in case isfinite is false, replacing it with 65504.0f and copysign
        v_vectors = _mm_blendv_ps(v_vectors,
                    _mm_or_ps(_mm_and_ps(v_signbit, v_vectors), _mm_andnot_ps(v_signbit, v_maxfloat)), //max value with copysign
                    _mm_castsi128_ps(_mm_cmpeq_epi32(_mm_castps_si128(_mm_and_ps(v_nonfinite,v_vectors)),_mm_castps_si128(v_nonfinite)))); // mask for each nonfinite                
    }

    EUCLID_INLINE static void curve_points_center(__m128& v_uvs, __m128& v_mid, __m128& v_vectors)
    {
        // solving mid points for quadratic curve
        // fitting quadratic curve in the cubic curve.
        // find spline maximum location and use the location to build the mid point. 
        // to find this point we need the a and c coefficient of the spline. 
        // then rotating it to align with the x-axis and find the maximum.
        // TODO:: This is a good approximation, for accuracy we can split the curve into 2 quad curves

        // The magic constant, t = 3.213117962394331f, is to fix so the splines would be continious and won't break.
        // somehow, solving this -> t^-1.5-3t^-0.5+1.5, gives us the constant
        // canceling terms gives us -> t^-0.5 - t^-1.5 = 0.384250603337
        const __m128 v_signbit     = _mm_set1_ps(-0.0f);
        
        const __m128 v_sqrd_vect = _mm_mul_ps(v_vectors, v_vectors);
        const __m128 v_sqrt_dist = _mm_sqrt_ps(_mm_add_ps(_mm_movehdup_ps(v_sqrd_vect),_mm_moveldup_ps(v_sqrd_vect)));

        // "h" is the % of each spline, together they will sum to 1
        const __m128 v_h_pre = _mm_div_ss(v_sqrt_dist, _mm_add_ss(v_sqrt_dist, _mm_movehl_ps(v_sqrt_dist,v_sqrt_dist)));
        const __m128 v_h     = _mm_shuffle_ps(v_h_pre, _mm_sub_ps(_mm_set1_ps(1.0f), _mm_shuffle_ps(v_h_pre,v_h_pre,_MM_SHUFFLE(0, 0, 0, 0))),_MM_SHUFFLE(0, 0, 0, 0));
        const __m128 v_hrcp  = _mm_rcp_ps(v_h);

        const __m128 v_nr = _mm_mul_ps(v_h, _mm_mul_ps(v_hrcp, v_hrcp));
        const __m128 v_hrcp_nr = _mm_sub_ps(_mm_add_ps(v_hrcp, v_hrcp), v_nr);

        // for the cubic coefficients we solve the second derivitive.
        const __m128 v_dervpre  = _mm_mul_ps(v_vectors, v_hrcp_nr);           
        const __m128 v_2nd_derv = _mm_mul_ps(_mm_mul_ps(v_h, v_h), _mm_add_ps(_mm_movelh_ps(v_dervpre, v_dervpre), _mm_movehl_ps(v_dervpre, v_dervpre)));

        // linear interpolate vectors in case of collinear => (absolute[x0 * y2 - x2 * y0 ]) <  0.0001
        const __m128 v_dot      = _mm_mul_ps(v_vectors,_mm_shuffle_ps(v_vectors,v_vectors,_MM_SHUFFLE(0, 0, 2, 3)));
        const __m128 v_isCollinear = _mm_cmplt_ss(_mm_andnot_ps(v_signbit, _mm_sub_ss(v_dot,_mm_shuffle_ps(v_dot,v_dot,_MM_SHUFFLE(0, 0, 0, 1)))),  _mm_set_ss(0.0001f));
        const __m128 v_collinear = _mm_shuffle_ps(v_isCollinear,v_isCollinear,_MM_SHUFFLE(0, 0, 0, 0));

        const __m128 v_magic_const = _mm_set1_ps(0.384250603337f);
        v_mid = _mm_mul_ps(v_magic_const, _mm_sub_ps(v_vectors, _mm_andnot_ps(v_collinear, v_2nd_derv)));
    }

    EUCLID_INLINE static void curve_points_tail(__m128& v_uvs, __m128& v_mid, __m128& v_vectors)
    {
        // solving mid points for quadratic curve
        // fitting quadratic curve in the cubic curve.
        // find spline maximum location and use the location to build the mid point. 
        // to find this point we need the a and c coefficient of the spline. 
        // then rotating it to align with the x-axis and find the maximum.
        // TODO:: This is a good approximation, for accuracy we can split the curve into 2 quad curves

        // The magic constant, t = 3.213117962394331f, is to fix so the splines would be continious and won't break.
        // somehow, solving this -> t^-1.5-3t^-0.5+1.5, gives us the constant
        // canceling terms gives us -> t^-0.5 - t^-1.5 = 0.384250603337

        // placing first vector as the center of the splines
        const __m128 v_signbit     = _mm_set1_ps(-0.0f);

        const __m128 v_tempuv = v_uvs;
        v_vectors = _mm_add_ps(v_uvs, v_vectors);
        v_uvs = _mm_shuffle_ps(v_vectors, v_vectors,_MM_SHUFFLE(1, 0, 1, 0));

        v_vectors = _mm_sub_ps(_mm_shuffle_ps(v_tempuv, v_vectors,_MM_SHUFFLE(3, 2, 1, 0)), v_uvs);

        const __m128 v_sqrd_vect = _mm_mul_ps(v_vectors, v_vectors);
        const __m128 v_sqrt_dist = _mm_sqrt_ps(_mm_add_ps(_mm_movehdup_ps(v_sqrd_vect),_mm_moveldup_ps(v_sqrd_vect)));

        // "h" is the % of each spline, together they will sum to 1
        const __m128 v_h_pre = _mm_div_ss(v_sqrt_dist, _mm_add_ss(v_sqrt_dist, _mm_movehl_ps(v_sqrt_dist,v_sqrt_dist)));
        const __m128 v_h     = _mm_shuffle_ps(v_h_pre, _mm_sub_ps(_mm_set1_ps(1.0f), _mm_shuffle_ps(v_h_pre,v_h_pre,_MM_SHUFFLE(0, 0, 0, 0))),_MM_SHUFFLE(0, 0, 0, 0));
        const __m128 v_hrcp  = _mm_rcp_ps(v_h);

        const __m128 v_nr = _mm_mul_ps(v_h, _mm_mul_ps(v_hrcp, v_hrcp));
        const __m128 v_hrcp_nr = _mm_sub_ps(_mm_add_ps(v_hrcp, v_hrcp), v_nr);

        // for the cubic coefficients we solve the second derivitive.
        const __m128 v_dervpre  = _mm_mul_ps(v_vectors, v_hrcp_nr);           
        const __m128 v_2nd_derv = _mm_mul_ps(_mm_mul_ps(v_h, v_h), _mm_add_ps(_mm_movelh_ps(v_dervpre, v_dervpre), _mm_movehl_ps(v_dervpre, v_dervpre)));

        // linear interpolate vectors in case of collinear => (absolute[x0 * y2 - x2 * y0 ]) <  0.0001
        const __m128 v_dot      = _mm_mul_ps(v_vectors,_mm_shuffle_ps(v_vectors,v_vectors,_MM_SHUFFLE(0, 0, 2, 3)));
        const __m128 v_isCollinear = _mm_cmplt_ss(_mm_andnot_ps(v_signbit, _mm_sub_ss(v_dot,_mm_shuffle_ps(v_dot,v_dot,_MM_SHUFFLE(0, 0, 0, 1)))),  _mm_set_ss(0.0001f));
        const __m128 v_collinear = _mm_shuffle_ps(v_isCollinear,v_isCollinear,_MM_SHUFFLE(0, 0, 0, 0));

        const __m128 v_magic_const = _mm_set1_ps(0.384250603337f);
        v_mid = _mm_mul_ps(v_magic_const, _mm_sub_ps(v_vectors, _mm_andnot_ps(v_collinear, v_2nd_derv)));
    }

    EUCLID_INLINE static void curve_aabb(__m128& v_aabb, const __m128& v_uvs, const __m128& v_mid, const __m128& v_end)
    {    
        // axis align bounding box
        // Computing Axis-Align Bounding Box for the two quadratic splines
        // https://www.iquilezles.org/www/articles/bezierbbox/bezierbbox.htm
        // t = (uvs-mid) / (uvs-2*mid+end)
        // Curves needs to be in zero space i.e. starting point in zero
        // at the end we shift the bouding box to the natual starting point
        const __m128 v_signbit     = _mm_set1_ps(-0.0f);

        const __m128 v_1   = _mm_set1_ps(1.0f);
        const __m128 v_2   = _mm_set1_ps(2.0f);

        const __m128 v_b = _mm_mul_ps(v_2, v_mid);
        const __m128 v_a = _mm_sub_ps(v_end, v_b);
        const __m128 v_denom_rcp = _mm_rcp_ps(v_a);

        // t needs to be in 0..1 range
        const __m128 v_t = _mm_mul_ps(_mm_xor_ps(v_signbit, v_mid),v_denom_rcp);
        const __m128 v_clamp_t = _mm_castsi128_ps( _mm_or_si128(
                                 _mm_cmpgt_epi32(_mm_castps_si128(v_t),  _mm_castps_si128(v_1)), // greater than 1
                                 _mm_cmplt_epi32(_mm_castps_si128(v_t),  _mm_setzero_si128()))); // less    than 0

        const __m128 v_new = _mm_andnot_ps(v_clamp_t, _mm_mul_ps(_mm_add_ps(_mm_mul_ps(v_a, v_t), v_b), v_t));

        const __m128 v_wend = _mm_add_ps(v_uvs, v_end);
        const __m128 v_wnew = _mm_add_ps(v_uvs, v_new);

        __m128 v_min = _mm_min_ps(_mm_min_ps(v_wend, v_wnew), v_uvs);
        __m128 v_max = _mm_max_ps(_mm_max_ps(v_wend, v_wnew), v_uvs);
        
        v_min = _mm_min_ps(v_min, _mm_shuffle_ps(v_min, v_min, _MM_SHUFFLE(1, 0, 3, 2)));
        v_max = _mm_max_ps(v_max, _mm_shuffle_ps(v_max, v_max, _MM_SHUFFLE(1, 0, 3, 2)));

        v_aabb = _mm_blend_ps(v_min, v_max, 0xc);
        v_aabb = _mm_add_ps(v_aabb, _mm_set_ps(2.0f , 2.0f, -1.0f, -1.0f));

        // float a[4], b[4], c[4];
        // _mm_storeu_ps(a, v_min);
        // _mm_storeu_ps(b, v_max);
        // _mm_storeu_ps(c, v_aabb);
        // Euclid::AtomicWriter()  <<"before\n"
        //                         <<"a : "<<a[0]<<"  "<<a[1]<<"  "<<a[2]<<"  "<<a[3]<<"\n"    
        //                         <<"b : "<<b[0]<<"  "<<b[1]<<"  "<<b[2]<<"  "<<b[3]<<"\n"    
        //                         <<"c : "<<c[0]<<"  "<<c[1]<<"  "<<c[2]<<"  "<<c[3]<<"\n"    
        //                         ;
    }

    EUCLID_INLINE static void curve_coefficients(float* coeff, const __m128& v_start, const __m128& v_mid, const __m128& v_end)
    {    
        const __m128 v_2   = _mm_set1_ps(2.0f);

        // 1st and 2nd quadratic bezier coefficion
        const __m128 v_b = _mm_mul_ps(v_2, v_mid);
        const __m128 v_a = _mm_sub_ps(v_end, v_b);
        const __m128 v_der = _mm_mul_ps(v_2, v_a);

        // traspose, we can also do it with unpack
        const __m128 tmp0 = _mm_shuffle_ps((v_a), (v_b), 0x44);
        const __m128 tmp2 = _mm_shuffle_ps((v_a), (v_b), 0xEE);
        const __m128 tmp1 = _mm_shuffle_ps((v_start), (v_der), 0x44);
        const __m128 tmp3 = _mm_shuffle_ps((v_start), (v_der), 0xEE);

        _mm_store_ps(coeff   , _mm_shuffle_ps(tmp0, tmp1, 0x88));
        _mm_store_ps(coeff+4 , _mm_shuffle_ps(tmp0, tmp1, 0xDD));
        _mm_store_ps(coeff+8 , _mm_shuffle_ps(tmp2, tmp3, 0x88));
        _mm_store_ps(coeff+12, _mm_shuffle_ps(tmp2, tmp3, 0xDD));
    }

    EUCLID_INLINE static void curve_shutter_center(__m128& v_start, __m128& v_mid, __m128& v_end, const __m128& v_scale, const __m128& v_scaleHalf)
    {}

    EUCLID_INLINE static void curve_shutter_tail(__m128& v_start, __m128& v_mid, __m128& v_end, const __m128& v_scale, const __m128& v_scaleHalf)
    {   
        const __m128 v_0d5 = _mm_set1_ps(0.5f);
        const __m128 v_2   = _mm_set1_ps(2.0f);

        const __m128 v_temp = v_start;
        v_start = _mm_shuffle_ps(_mm_add_ps(v_start, v_end) , v_start, _MM_SHUFFLE(3, 2, 1, 0));
        v_end   = _mm_shuffle_ps(_mm_sub_ps(v_temp, v_start), v_end  , _MM_SHUFFLE(3, 2, 1, 0));
        v_mid   = _mm_shuffle_ps(_mm_add_ps(v_mid, v_end)   , v_mid  , _MM_SHUFFLE(3, 2, 1, 0));

        // 1st and 2nd quadratic bezier coefficion
        const __m128 v_b = _mm_mul_ps(v_2, v_mid);
        const __m128 v_a = _mm_sub_ps(v_end, v_b);
        
        v_end = _mm_mul_ps(_mm_add_ps(_mm_mul_ps(v_a, v_scale), v_b), v_scale);
        
        v_mid = _mm_mul_ps(_mm_add_ps(_mm_mul_ps(v_a, v_scaleHalf), v_b), v_scaleHalf);
        v_mid = _mm_sub_ps(_mm_mul_ps(v_2, v_mid), _mm_mul_ps(v_0d5, v_end));
    }

    EUCLID_INLINE static void curve_roots_intersection(float* roots, const float* coeff, const __m128& v_bbox)//, const bool print = false) // const __m128& v_start
    {                
        const __m128 v_signbit = _mm_set1_ps(-0.0f);

        // getting all possible roots from two parametric quadratic equations
        const __m128 v_coeffx = _mm_load_ps(coeff);
        const __m128 v_coeffy = _mm_load_ps(coeff+4);

        const __m128 v_a = _mm_shuffle_ps(v_coeffx, v_coeffy, _MM_SHUFFLE( 0,0,0,0));   // a
        const __m128 v_b = _mm_shuffle_ps(v_coeffx, v_coeffy, _MM_SHUFFLE( 1,1,1,1));   // b
        const __m128 v_c = _mm_sub_ps(_mm_shuffle_ps(v_coeffx, v_coeffy, _MM_SHUFFLE( 2,2,2,2)), _mm_shuffle_ps(v_bbox, v_bbox, _MM_SHUFFLE( 3,1,2,0))); // c - 0 w 0 h  

        const __m128 v_Disciminant     = _mm_sub_ps(_mm_mul_ps(v_b, v_b), _mm_mul_ps(_mm_set1_ps(4.0f), _mm_mul_ps(v_a, v_c)));    // discriminant -> b*b - 4*a*c
        const __m128 v_Nominator       = _mm_sub_ps(_mm_or_ps(_mm_andnot_ps(v_b, v_signbit), _mm_sqrt_ps(v_Disciminant)), v_b); // sign(-b)+sqrt(discriminant) - b
        
        const __m128 v_is_a_Zero               = _mm_castsi128_ps(_mm_cmpeq_epi32(_mm_castps_si128(v_a),         _mm_setzero_si128())); // if a is zero                -> one intersection -> -c/b
        const __m128 v_isNominatorAboveZero    = _mm_castsi128_ps(_mm_cmpeq_epi32(_mm_castps_si128(v_Nominator), _mm_setzero_si128())); // if nominator is zero        -> one intersection

        const __m128 v_ConstantMultiplier = _mm_blendv_ps(_mm_set1_ps(2.0f), _mm_set1_ps(-1.0f), v_isNominatorAboveZero); // discriminant == 0 ? -1 : 2
        const __m128 v_NominatorBlend     = _mm_blendv_ps(v_Nominator, v_b,                      v_isNominatorAboveZero); // discriminant == 0 ? b : discriminant

        const __m128 v_isNoIntersecion = _mm_castsi128_ps(_mm_cmplt_epi32(_mm_castps_si128(_mm_set1_ps(1.e-4f)), _mm_castps_si128(v_Disciminant))); // if discriminant is negitive -> no intersection
        __m128 v_root1 =  _mm_and_ps(v_isNoIntersecion, _mm_div_ps(_mm_mul_ps(v_ConstantMultiplier, v_c) ,v_NominatorBlend));    // (2*c / b-disc) or (-c/b) in case a is zero
        __m128 v_root2 =  _mm_and_ps(v_isNoIntersecion, _mm_div_ps(v_NominatorBlend, _mm_mul_ps(v_ConstantMultiplier, v_a)));    // (b-disc / 2*a) or (b/-a) in case c is zero

        v_root1 = _mm_shuffle_ps(v_root1, v_root1, _MM_SHUFFLE( 1,0,3,2)); // flipping order for bounding checks: x x y y -> y y x x 
        v_root2 = _mm_shuffle_ps(v_root2, v_root2, _MM_SHUFFLE( 1,0,3,2)); // flipping order for bounding checks: x x y y -> y y x x 
        
        // __m128 v_root1cp =  v_root1;
        // __m128 v_root2cp =  v_root2;
        
        const __m128 v_dupc    = _mm_moveldup_ps(v_c);
        const __m128 v_proj1   = _mm_add_ps(_mm_mul_ps(_mm_add_ps(_mm_mul_ps(v_a ,v_root1), v_b), v_root1), v_dupc); // coeff y y x x 
        const __m128 v_proj2   = _mm_add_ps(_mm_mul_ps(_mm_add_ps(_mm_mul_ps(v_a ,v_root2), v_b), v_root2), v_dupc); // coeff y y x x    
        const __m128 v_aabb_wh = _mm_shuffle_ps(v_bbox, v_bbox, _MM_SHUFFLE( 3,3,2,2)); // wwhh 

        // roots in range 0..1 and projections inside of aabb
        const __m128 v_range_check1 = 
        _mm_castsi128_ps(_mm_or_si128(  _mm_cmpeq_epi32(_mm_castps_si128(v_root1), _mm_setzero_si128()),               // roots on 0
                         _mm_or_si128(  _mm_cmplt_epi32(_mm_castps_si128(v_root1), _mm_setzero_si128()),               // roots below 0 
                         _mm_or_si128(  _mm_cmpgt_epi32(_mm_castps_si128(v_root1), _mm_set1_epi32(0x3f800000)),        // roots above 1
                         _mm_or_si128(  _mm_cmplt_epi32(_mm_castps_si128(v_proj1), _mm_setzero_si128()),              // point below aabb -> x y 
                                        _mm_cmpgt_epi32(_mm_castps_si128(v_proj1), _mm_castps_si128(v_aabb_wh))))))); // point above aabb -> r t  

        const __m128 v_range_check2 = 
        _mm_castsi128_ps(_mm_or_si128(  _mm_cmpeq_epi32(_mm_castps_si128(v_root2), _mm_setzero_si128()),               // roots on 0
                         _mm_or_si128(  _mm_cmplt_epi32(_mm_castps_si128(v_root2), _mm_setzero_si128()),               // roots below 0
                         _mm_or_si128(  _mm_cmpgt_epi32(_mm_castps_si128(v_root2), _mm_set1_epi32(0x3f800000)),        // roots above 1
                         _mm_or_si128(  _mm_cmplt_epi32(_mm_castps_si128(v_proj2), _mm_setzero_si128()),              // point below aabb -> x y 
                                        _mm_cmpgt_epi32(_mm_castps_si128(v_proj2), _mm_castps_si128(v_aabb_wh))))))); // point above aabb -> r t

        v_root1 = _mm_blendv_ps(v_root1, _mm_set1_ps(1.0f), v_range_check1);
        v_root2 = _mm_blendv_ps(v_root2, _mm_set1_ps(1.0f), v_range_check2);

        // Sorting all roots, not sure if it's necessery.
        sorting_network_8(v_root1, v_root2);

        // taking mid point of first intersection
        const __m128 v_first_t = _mm_mul_ps(_mm_set1_ps(0.5f) , _mm_shuffle_ps(v_root1, v_root1, _MM_SHUFFLE(0,0,0,0))); // mid point of first intersection point
        const __m128 v_mid_intersection = _mm_add_ps(_mm_mul_ps(_mm_add_ps(_mm_mul_ps(v_a ,v_first_t), v_b), v_first_t), v_dupc);

        // cheking if it is inside the aabb? if so we add zero at the beginning
        const int isIntersectionInside = 15 == 
                _mm_movemask_ps( // all 4 sign bits needs to be on -> 1111 -> 15
                    _mm_castsi128_ps(_mm_cmpgt_epi32(
                    _mm_castps_si128(_mm_shuffle_ps(v_mid_intersection, v_aabb_wh       , _MM_SHUFFLE(2,0,2,0))),    // x y w h > 
                    _mm_castps_si128(_mm_shuffle_ps(_mm_setzero_ps(), v_mid_intersection, _MM_SHUFFLE(2,0,0,0)))))); // 0 0 x y 
        
        roots[0] = 0;
        _mm_storeu_ps(roots+isIntersectionInside, v_root1);	
        _mm_storeu_ps(roots+isIntersectionInside+4, v_root2);
    }

    EUCLID_INLINE static void sorting_network_8(__m128& v_1, __m128& v_2)
    {
        // Batcher's Merge Exchange (parallel sorting network) of 8 elements
        // lv.1  0123 4567 (0,4)(1,5)(2,6)(3,7)
        __m128 v_tmp1 = _mm_min_ps(v_1, v_2);
        __m128 v_tmp2 = _mm_max_ps(v_1, v_2);

        // lv.2 0246 1357 (0,2)(4,6)(1,3)(5,7)
        v_1 = _mm_shuffle_ps(v_tmp1, v_tmp2, _MM_SHUFFLE(2, 0, 2, 0));
        v_2 = _mm_shuffle_ps(v_tmp1, v_tmp2, _MM_SHUFFLE(3, 1, 3, 1));
        
        v_tmp1 = _mm_min_ps(v_1, v_2);
        v_tmp2 = _mm_max_ps(v_2, v_1);
        
        // lv.3 0415 2637 (0,2)(4,6)(1,3)(5,7)
        v_1 = _mm_shuffle_ps(v_tmp1, v_tmp2, _MM_SHUFFLE(2, 0, 2, 0));
        v_2 = _mm_shuffle_ps(v_tmp1, v_tmp2, _MM_SHUFFLE(3, 1, 3, 1));
        
        v_tmp1 = _mm_min_ps(v_1, v_2);
        v_tmp2 = _mm_max_ps(v_2, v_1);

        // lv.4 1504 2637 (1,2)(5,6)
        v_1 = _mm_shuffle_ps(v_tmp1, v_tmp1, _MM_SHUFFLE(1, 0, 3, 2));
        v_2 = v_tmp2;

        v_tmp1 = _mm_min_ps(v_1, v_2); 
        v_tmp2 = _mm_max_ps(v_2, v_1);
        v_tmp1 = _mm_shuffle_ps(v_tmp1, v_1, _MM_SHUFFLE(3, 2, 1, 0)); //original highter half register
        v_tmp2 = _mm_shuffle_ps(v_tmp2, v_2, _MM_SHUFFLE(3, 2, 1, 0)); //original highter half register
        
        // lv.5 2301 4567 (2,4)(3,5)
        v_1 = _mm_shuffle_ps(v_tmp2, v_tmp1, _MM_SHUFFLE(0, 2, 2, 0));
        v_2 = _mm_shuffle_ps(v_tmp1, v_tmp2, _MM_SHUFFLE(3, 1, 1, 3));

        v_tmp1 = _mm_min_ps(v_1, v_2); 
        v_tmp2 = _mm_max_ps(v_2, v_1);
        v_tmp1 = _mm_shuffle_ps(v_tmp1, v_1, _MM_SHUFFLE(3, 2, 1, 0)); //original highter half register
        v_tmp2 = _mm_shuffle_ps(v_tmp2, v_2, _MM_SHUFFLE(3, 2, 1, 0)); //original highter half register
        
        // lv.6 0246 7135 (1,2)(3,4)(5,6)
        v_1 = _mm_shuffle_ps(v_tmp1, v_tmp2, _MM_SHUFFLE(2, 0, 0, 2));
        v_2 = _mm_shuffle_ps(v_tmp1, v_tmp2, _MM_SHUFFLE(3, 1, 1, 3));
        v_2 = _mm_shuffle_ps(v_2, v_2, _MM_SHUFFLE(2, 1, 0, 3));

        v_tmp1 = _mm_max_ps(v_1, v_2); 
        v_tmp2 = _mm_min_ps(v_2, v_1);
        v_tmp1 = _mm_blend_ps(v_tmp1, v_1, 0x1); 
        v_tmp2 = _mm_blend_ps(v_tmp2, v_2, 0x1);

        // shuffle back in order
        v_tmp2 = _mm_shuffle_ps(v_tmp2, v_tmp2, _MM_SHUFFLE(0, 3, 2, 1));
        v_1 = _mm_unpacklo_ps(v_tmp1, v_tmp2);
        v_2 = _mm_unpackhi_ps(v_tmp1, v_tmp2);
    }

    EUCLID_INLINE static void curve_arc_length(float* result, const float* coeff) 
    {   
        __m128d v_a    = _mm_setr_pd(coeff[0], coeff[8]);// ax 
        __m128d v_c    = _mm_setr_pd(coeff[1], coeff[9]);// bx

        __m128d v_derv = _mm_setr_pd(coeff[4], coeff[12]);//ay 
        __m128d v_s4ac = _mm_setr_pd(coeff[5], coeff[13]);//by

        const __m128d v_b = _mm_mul_pd(_mm_add_pd(_mm_mul_pd(v_a,v_c),_mm_mul_pd(v_derv,v_s4ac)),_mm_set1_pd(4.0));
                      v_c = _mm_add_pd(_mm_mul_pd(v_c,v_c),_mm_mul_pd(v_s4ac,v_s4ac));
                      v_a = _mm_mul_pd(_mm_add_pd(_mm_mul_pd(v_a,v_a),_mm_mul_pd(v_derv,v_derv)),_mm_set1_pd(4.0));


                        v_derv = _mm_add_pd( v_b, _mm_mul_pd(_mm_set1_pd(2.0),v_a));
                        v_s4ac = _mm_mul_pd(_mm_set1_pd(4.0),_mm_mul_pd(v_a, v_c));
              __m128d v_s4aabc = _mm_mul_pd(_mm_set1_pd(4.0),_mm_mul_pd(v_a, _mm_add_pd(_mm_add_pd(v_a,v_b), v_c)));
        const __m128d v_root   = _mm_sub_pd(_mm_mul_pd(v_b,v_b), v_s4ac);

        v_s4ac   = _mm_sqrt_pd(v_s4ac);
        v_s4aabc = _mm_sqrt_pd(v_s4aabc);

        __m128d v_denom  = _mm_add_pd(v_s4ac, v_b);
        __m128d v_isZero = _mm_cmpneq_pd(v_denom, _mm_setzero_pd());
        __m128d v_nomin  = _mm_and_pd( v_isZero , _mm_div_pd(_mm_add_pd(v_s4aabc, v_derv),v_denom));
        
        // replace this with a simd natrual log version
        CACHE_ALIGNED double denom[2], nomin[2];
        _mm_store_pd(denom,v_denom);
        _mm_store_pd(nomin,v_nomin);
        nomin[0] = denom[0] < 1e-5 ? 0 : log(nomin[0]);
        nomin[1] = denom[1] < 1e-5 ? 0 : log(nomin[1]);
        v_nomin = _mm_load_pd(nomin);

        v_denom  = _mm_mul_pd(_mm_mul_pd(_mm_set1_pd(8.0), v_a), _mm_sqrt_pd(v_a));
        v_isZero = _mm_cmpneq_pd(v_denom, _mm_setzero_pd());
        v_nomin  = _mm_and_pd( v_isZero ,_mm_div_pd(_mm_sub_pd(_mm_sub_pd(_mm_mul_pd(v_s4aabc, v_derv),_mm_mul_pd(v_s4ac, v_b)),_mm_mul_pd(v_root, v_nomin)), v_denom));

        CACHE_ALIGNED float tmp[4];
        _mm_store_ps(tmp,_mm_cvtpd_ps(v_nomin));
        result[0] = tmp[0];
        result[1] = tmp[1];
    }

    // mFnDDImageMultiTileIop_DeclareFunctions_engine(int y, int x, int r, DD::Image::ChannelMask m, DD::Image::Row& row);
};

const char* const CurvedMotionTrail::kHelp = "";
const char* const CurvedMotionTrail::kInfo = "author :\tEyal Shirazi\n"
                                            "version:\t2.24\n"
                                            "update :\t"
                                            __DATE__
                                            "\n";

const char* const CurvedMotionTrail::kBBoxModeList[] = {
"to format",
"to bbox",
"to bbox+format",
0
};

const char* const CurvedMotionTrail::kCurveOriginList[] = {
"head",
"center",
"tail",
0
};

const DD::Image::CurveDescription CurvedMotionTrail::kTransparencyCurveDescription[] = { 
    { "transparency", "y C 1 0" },
    {0}
};

static DD::Image::Iop* build(Node* node) { return new CurvedMotionTrail(node); }
const DD::Image::Iop::Description CurvedMotionTrail::d("CurvedMotionTrail", 0, build);

#undef PRINT_FUNC_HEAD
#undef PRINT_FUNC_TAIL

// using namespace DD::Image;
// mFnDDImageMultiTileIop_DefineFunctions_engine(CurvedMotionTrail)

// float a[4], b[4], c[4];
// _mm_storeu_ps(a, v_uvs);
// _mm_storeu_ps(b, v_mid);
// _mm_storeu_ps(c, v_vectors);
// Euclid::AtomicWriter()  <<"before\n"
//                         <<"a : "<<a[0]<<"  "<<a[1]<<"  "<<a[2]<<"  "<<a[3]<<"\n"    
//                         <<"b : "<<b[0]<<"  "<<b[1]<<"  "<<b[2]<<"  "<<b[3]<<"\n"    
//                         <<"c : "<<c[0]<<"  "<<c[1]<<"  "<<c[2]<<"  "<<c[3]<<"\n"    
//                         ;

// void swapVelocity()
// {
//     // not sure why but channelSet is getting reversed oreder sometimes(when too many channels)...???
    
//     const char* a = DD::Image::getName(vecsChan[0]);
//     const char* b = DD::Image::getName(vecsChanSet.first());

//     int notEqual = 0;
//     for(int i = 0; (a[i] != '\0') | (b[i] != '\0') ; ++i)
//         if(a[i] != b[i]) 
//         {
//             notEqual = 1;
//             break;
//         }

//     if (notEqual)
//     {
//         DD::Image::Channel temp = vecsChan[3];
//         vecsChan[3] = vecsChan[0];
//         vecsChan[0] = temp;

//         temp = vecsChan[1];
//         vecsChan[1] = vecsChan[2];
//         vecsChan[2] = temp;
//     }
// }

// for(const auto& c : vecsChan) std::cout<<getName(c)<<"\n";
// for(const auto& c : vecsChanSet) std::cout<<getName(c)<<"\n";
