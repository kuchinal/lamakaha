from Qt import __binding__
#print __binding__
import nuke
import sys
import os
from os import listdir
from os.path import isfile, join
import module.scan_metadata as smd

from tx_nuke import nuketools

#import tx_comp_app as comp_app
#import module.trixterartists as artists
#import module.trixtertypes as types
#import module.trixterdepartments as dep

#from tx.path import Path
#from functools import partial

#from ED_shot_folder import ED_shot_folder

from Qt import QtWidgets, QtGui, QtCore

import collections


class ED_AssetLoader(QtWidgets.QWidget):

    def __init__(self):
        super(ED_AssetLoader, self).__init__()
        
        self.version = 'Beta' #DISPLAYED VERSION OF THE ASSETLOADER
        self.already_loaded_assets = []
        self.already_loaded_asset_versions_dict = {}

        self.retrieveShotData()
        self.setUpAssetconfig()
        self.initUI()

    def initUI(self):

        ## auto layout count
        self.layout_count_y = 0
        self.layout_count_x = 0
        self.column_row_rel = {}

        # Widgets caches
        self.label_cache = []
        self.dropdown_cache = []
        self.checkbox_cache = []


        ## DEFINE LAYOUT GRIDS
        main_layout = QtWidgets.QGridLayout()
        main_layout.setSpacing(5)

        self.sub_grid_top = QtWidgets.QGridLayout()
        self.sub_grid_low = QtWidgets.QGridLayout()
        self.sub_grid_low.setAlignment(QtCore.Qt.AlignTop)
        self.sub_grid_low_assets = QtWidgets.QGridLayout()
        self.sub_grid_low_assets.setAlignment(QtCore.Qt.AlignTop)
        
        #self.verticalSpacer = QtWidgets.QSpacerItem(10, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)


        ## FILL UP TOP GRID 
        grid_posx = 0
        grid_posy = 1

        shot_info_label = QtWidgets.QLabel(self.shot_title, self)
        self.sub_grid_top.addWidget(shot_info_label , 0 , 0 )

        for element in self.shot_info:
            label = QtWidgets.QLabel(element, self)
            self.sub_grid_top.addWidget(label, grid_posy, grid_posx )
            grid_posy += 1


        ## FILL UP BOTTOM GRID 
        button_gather_assets = QtWidgets.QPushButton('Gather Assets')
        button_gather_assets.clicked.connect(self.gatherAllAssets)
        button_gather_assets.setToolTip('Refresh Available Assets')
        button_load_assets = QtWidgets.QPushButton('Load Selected Assets')
        button_load_assets.setToolTip('Load assets that are checked')
        button_load_assets.clicked.connect(self.selectedAsset)

        self.sub_grid_low.addWidget(button_gather_assets, 0  , 0 )
        self.sub_grid_low.addLayout(self.sub_grid_low_assets, 1  , 0 )
        self.sub_grid_low.addWidget(self.HLine(), 2 , 0 )  
        self.sub_grid_low.addWidget(button_load_assets, 3  , 0 )


        ## MAIN GRID GETS FILLED
        main_layout.addLayout(self.sub_grid_top, 0  , 0 )
        main_layout.addWidget(self.HLine(), 1, 0)
        main_layout.addLayout(self.sub_grid_low, 2  , 0 )


        ## UI SETUP
        self.setLayout(main_layout) 
        self.setWindowTitle('AssetLoader' + ' ' + self.version)
        self.setWindowIcon(QtGui.QIcon('/corky/projects/RnD_00001/exchange/underUserErnest/icons/menuicon.jpg'))        
        
        self.center() #The code that will center the window is placed in the custom center() method. 
        #self.show()

        # tabs = QtGui.QTabWidget(self)
        # self.addWidget(tabs)

    def center(self): #The center method
        
        panelgeo = self.frameGeometry() #We get a rectangle specifying the geometry of the main window. This includes any window frame. 
        monitorcenter = QtWidgets.QDesktopWidget().availableGeometry().center() #We figure out the screen resolution of our monitor. And from this resolution, we get the center point. 
        panelgeo.moveCenter(monitorcenter) #Our rectangle has already its width and height. Now we set the center of the rectangle to the center of the screen. The rectangle's size is unchanged. 
        self.move(panelgeo.topLeft()) #We move the top-left point of the application window to the top-left point of the qr rectangle, thus centering the window on our screen.     

    def HLine(self): # The horizontal line method
        toto = QtWidgets.QFrame()
        toto.setFrameShape(QtWidgets.QFrame.HLine)
        toto.setFrameShadow(QtWidgets.QFrame.Sunken)
        return toto

    def VLine(self): # The vertical line method
        vovo = QtWidgets.QFrame()
        vovo.setFrameShape(QtWidgets.QFrame.VLine)
        vovo.setFrameShadow(QtWidgets.QFrame.Sunken)
        return vovo

    def gatherAllAssets(self):

        self.message_list = []

        #self.setUpAssetconfig() ## that is not nice TODO try to don't run this every time

        for assettype in self.ED_assetconfig:

            #we gather the asset type custom config
            assetconfig = self.ED_assetconfig[assettype]
            assettypecolumn = assetconfig['column']
            assetpath = assetconfig['path']
            assetquality= assetconfig['quality']
            assetfilter = assetconfig['filter']
            assetfiletype = assetconfig['file_types']
            assetfalse = assetconfig['false_message']

            asset_dict = self.ED_loaded_asset_Dict[assettype]
            asset_sub_list = asset_dict['subasset_list']
            asset_list = asset_dict['asset_list']
            asset_path_list = asset_dict['asset_path_list']
            asset_versions_dict = asset_dict['asset_versions_dict']
            
            if assettypecolumn in self.column_row_rel.keys():
                  self.layout_count_y =  self.column_row_rel.get(assettypecolumn)
                  #print 'true'
            else:
                self.layout_count_y = 0 
                self.sub_grid_low_assets_assettype = QtWidgets.QGridLayout()
                self.sub_grid_low_assets_assettype.setSpacing(10)
                self.sub_grid_low_assets_assettype.setAlignment(QtCore.Qt.AlignTop)
                self.sub_grid_low_assets.addLayout(self.sub_grid_low_assets_assettype, 0  , assettypecolumn )

            self.listAssets(assettype,assetpath,assetfilter,assetfiletype)
            self.dict_compare(self.already_loaded_asset_versions_dict, asset_versions_dict)

            for asset in self.added:            
                self.controllersAsset(assettype,assettypecolumn,assetpath,assetquality,assetfilter,assetfiletype,assetfalse,asset_sub_list,asset_list,asset_path_list,asset_versions_dict,asset)

            self.sub_grid_low_assets.addWidget(self.VLine(), 0, 0)
            self.sub_grid_low_assets.addWidget(self.VLine(), 0, assettypecolumn+1)
        
        # if self.message_list != []:
        #     message = QtWidgets.QMessageBox.information(self, 'info', str(self.message_list) + ' new assets to gather')

    def controllersAsset(self, assettype = 'Plate', assettypecolumn = 1, assetpath = '', assetquality = [] , assetfilter = '', assetfiletype = [], assetfalse='', asset_sub_list=[] , asset_list=[], asset_path_list=[], asset_versions_dict={} ,asset = ''):

        self.layout_count_x = 2
        self.versions_path = assetpath + '/' + asset + '/' + 'versions' #we get the versions folder

        if assettype == 'Edit_ref':

            self.versions_path = assetpath
            #print self.versions_path

        version_list = asset_versions_dict.get(asset)


        if os.path.exists(self.versions_path): #we check if the version folder exists if not we assume the asset is rubbish

            ## we create a text per asset
            btn = QtWidgets.QLabel(str(asset))
            btn.setToolTip('Name of the ' + assettype)
            self.sub_grid_low_assets_assettype.addWidget(btn, self.layout_count_y , 0)
            self.label_cache.append(btn)
            ##
   
            ## we deal with versions and versions dropdown cache here
            versiondropdown = QtWidgets.QComboBox() # the dropdown widget
            versiondropdown.setToolTip('Choose the asset version you want to import')                 
                                           
            self.dropdown_cache.append(versiondropdown)
            ##

            ## we create the dropdown
            for k in version_list:
                newk = 'v' + k.rpartition(assetfilter)[2]
                if '.abc' in newk:
                    newk = newk.rpartition('.abc')[0]
                versiondropdown.addItem(newk)
            
            self.sub_grid_low_assets_assettype.addWidget(versiondropdown, self.layout_count_y , 1)
            #####

            ### we create the checkboxes
            if assetquality is not None: # create the checkbox if an asset has subtypes
                self.checkbox_cache.append([])
                for quality in assetquality:
                    
                    self.check = QtWidgets.QCheckBox(quality)# create checkboxes
                    self.checkboxTooltip(self.check,quality)
                    self.sub_grid_low_assets_assettype.addWidget(self.check, self.layout_count_y , self.layout_count_x) # add them to the layout
                    self.checkbox_cache[len(self.checkbox_cache)-1].append(self.check) ## this is freaking important checkbox cache is a list that contains lists of checkboxes to keep track of the index print it to see it
                    self.layout_count_x += 1
                    connect_list = []
                    connect_list.append(self.check)

            ###

            
            self.layout_count_y += 1

            # self.sub_grid_low_assets_assettype.addWidget(self.VLine(), 0, self.layout_count_x)
            # self.layout_count_x += 1

        else:
            pass

        self.column_row_rel[assettypecolumn] = self.layout_count_y
        #print self.column_row_rel
        self.already_loaded_asset_versions_dict.update(asset_versions_dict) # we refresh the already loaded assets
        #print self.already_loaded_assets
                  
        versiondropdown.currentIndexChanged.connect(lambda: self.restore_color(btn)) 
        #else: #we display the no asset message

            #message = QtWidgets.QMessageBox.information(self, 'info', assetfalse)

    def restore_color( self, btn ):
   
        assetname = btn.text()

        for assetlbl in self.label_cache:

            if assetlbl == btn:
           
                target_index = self.label_cache.index(assetlbl)
                print target_index
                try:
                    for checkers in self.checkbox_cache[target_index]:
                        checkers.setStyleSheet("color: rgb(210 , 210, 210);")
                except:
                    pass


    def checkboxTooltip(self, check, quality):
        if quality == 'F':
            check.setToolTip('Full quality plate')
        elif quality == 'P':
            check.setToolTip('Proxy quality plate')
        elif quality == 'S':
            check.setToolTip('Scanned plate before any treatment')
        elif quality == 'R':
            check.setToolTip('Edit reference')
        elif quality == 'cam':
            check.setToolTip('Camera')
        elif quality == 'H':
            check.setToolTip('High Poly Mesh')
        elif quality == 'L':
            check.setToolTip('Low Poly Mesh')
        elif quality == 'A':
            check.setToolTip('Axis')

    def dict_compare(self, old, new):
        #old_ordered =  collections.OrderedDict(sorted(old.items()))
        #new_ordered =  collections.OrderedDict(sorted(new.items()))
        old_keys = set(old.keys())
        #print old_keys
        new_keys = set(new.keys())
        #print new_keys
        intersect_keys = old_keys.intersection(new_keys)
        self.added = new_keys - old_keys
        #removed = new_keys - old_keys
        self.modified = {o : (old[o], new[o]) for o in intersect_keys if old[o] != new[o]}
        #same = set(o for o in intersect_keys if old_ordered[o] == new_ordered[o])
        #return self.added
        #print self.added

    # Gets the shot data
    def retrieveShotData(self):
        ## WE SET DEFAULTS
        self.shot_title = 'Shot Data:'
        prj = 'Please get the Shot Data first'
        seq = 'Please get the Shot Data first'
        shot = '' 
        fullshot = seq + '_' + shot       
        shot_folder = 'Please get the Shot Data first'
        self.folder = ''

        plates_type = []
        plates = []

        
        cam_versions = []

        
        geo_subassets = []
        geo_versions = []
        
        
        axis_subassets = []
        axis_versions = []

        edit_ref_path = ''
        edit_ref_versions = []

        render_input_path = ''
        render_input_versions = []
        render_input_elements = []


        ## WE TRY TO RETRIEVE THE METADATA IF THERE IS A TRIXTER SHOT DATA NODE
        tsdnode = nuke.toNode('TrixterShotData')

        if tsdnode is not None:

            self.folder = tsdnode['projectpath'].value() + '/' + 'seq'
            self.folder = self.folder +  '/' + tsdnode['sequence'].value()
            self.folder = self.folder +  '/' + tsdnode['shot'].value()

            prj = 'Project: ' + tsdnode['projectname'].value()
            #sss = tsd.SSS()
            #seq = sss[0]
            #shot = sss[1]
            seq = tsdnode['sequence'].value()
            shot = tsdnode['shot'].value()
            fullshot = 'Shot: ' + seq + '_' + shot   
            shot_folder= 'Folder: ' + self.folder

        self.shot_info = [prj, fullshot, shot_folder]

    # DEFINES CLASS, PATHS AND DEFAULTS FOR OUR ASSETS]
    def setUpAssetconfig(self):
        self.ED_assetconfig = { 'Camera' : 
                    { 'class' : 'Camera2',
                      'read_from_file' : False,
                      'quality': ['cam'],
                      'false_message': 'no camera found',
                      'filter' : 'cache_v',
                      'file_types': ['abc'],
                      'column': 3,
                      'path' : self.folder + '/' + 'data' + '/' + 'animation' + '/' + 'cameras' },
                    # 'Axis' :
                    # { 'class' : 'Axis2',
                    #   'read_from_file' : True,
                    #   'quality': None,
                    #   'filter' : 'utility_',
                    #   'false_message': 'no axis found',
                    #   'path' : self.folder + '/' + 'data' + '/' + 'animation' },
                    'Geometry' :
                    { 'class' : ['ReadGeo2', 'Axis2'],
                      'read_from_file' : True,
                      'quality': ['H', 'L', 'A'],
                      'filter' : 'cache_v',
                      'file_types': ['abc'],
                      'false_message': 'no geometry found',
                      'column': 5,
                      'path' : self.folder + '/' + 'data' + '/' + 'animation' },
                    'Plate' :
                    { 'class' : 'Read',
                      'read_from_file' : None,
                      'false_message': 'no plate found',
                      'quality': ['F','P', 'S'],
                      'filter' : 'linear_v',
                      'file_types': [],
                      'column': 1,
                      'path' : self.folder + '/' + 'data' + '/' + 'plates'  },
                    'Edit_ref' :
                    { 'class' : 'Read',
                      'read_from_file' : None,
                      'quality': ['R'],
                      'filter' : 'edit_reference_v',
                      'file_types': [],
                      'false_message': 'no edit_ref found',
                      'column': 1,
                      'path' : self.folder + '/' + 'data' + '/' + 'edit_reference' },
                  }

        self.ED_loaded_asset_Dict = {
        'Plate':
            {
            'subasset_list' : [] ,
            'asset_list' : [] ,
            'asset_path_list' : [],
            'asset_versions_dict':{},
            },

        'Camera':
            {
            'subasset_list' : [] ,
            'asset_list' : [] ,
            'asset_path_list' : [],
            'asset_versions_dict':{},
            },
        'Geometry':
            {
            'subasset_list' : [] ,
            'asset_list' : [] ,
            'asset_path_list' : [],
            'asset_versions_dict':{},
            },
        'Edit_ref':
            {
            'subasset_list' : [] ,
            'asset_list' : [] ,
            'asset_path_list' : [],
            'asset_versions_dict':{},
            }
        }
   
    def listAssets(self,assettype='Plate',assetpath='',assetfilter='',assetfiletype=[]):

        asset_dict = self.ED_loaded_asset_Dict[assettype]
        asset_sub_list = asset_dict['subasset_list']
        asset_list = asset_dict['asset_list']
        asset_path_list = asset_dict['asset_path_list']
        asset_versions_dict = asset_dict['asset_versions_dict']
          


        ## SUPER IMPORTANT: WE RETRIEVE THE ASSETS AND STORE THEM IN THE DICT
        if os.path.exists(assetpath) == True: # we check if the asset folder exists

            if assettype == 'Geometry':
                
                temp_list = os.listdir(assetpath) #first create a list of subasset
                temp_list.remove('cameras') #we remove the camera
                asset_sub_list.extend(temp_list) #we added to the sub asset list

                for subasset in asset_sub_list: #iterate through that list

                    subasset_path = assetpath + '/' + subasset #the new asset+subasset path

                    subsubasset_list = os.listdir(subasset_path) #we added to a list

                    for subsubasset in subsubasset_list:

                        new_name_a = subasset + '/' + subsubasset

                        if new_name_a not in asset_list:

                            self.message_list.append(new_name_a)
                            asset_list.append(new_name_a)

            elif assettype == 'Edit_ref':

                if 'Edit_ref' not in asset_list:

                    self.message_list.append('Edit_ref')
                    asset_list.append('Edit_ref')


            else:

                new_asset_list = os.listdir(assetpath) #create a list of assets

                for i in new_asset_list:

                    if i not in asset_list:

                        asset_list.append(i)
                        self.message_list.append(i)

            #print asset_list

        else: #we display the no asset message

            message = QtWidgets.QMessageBox.information(self, 'info', self.assetconfig['false_message'])


        #print asset_list

        ## SUPER IMPORTANT: WE RETRIEVE THE VERSIONS FOR EACH ASSET AND STORE THEM IN THE DICT
        for asset in asset_list:

            versions_path = assetpath + '/' + asset + '/' + 'versions'
            if assettype == 'Edit_ref':
                versions_path = assetpath

            asset_path_list.append(versions_path)


            if os.path.exists(versions_path): ## we check if the path exists
                #print asset

                ###### we create the versions list with only the supported file types     
                versionselements = os.listdir(versions_path)
                versions_useful = [k for k in versionselements if assetfilter in k]

                versions_trash = []
                for version in versions_useful:
                    for typefilter in assetfiletype:
                        if typefilter not in version:
                            versions_trash.append(version)

                versions_filtered  = list(set(versions_useful).difference(versions_trash))
                versions_filtered.sort(reverse=True)
                ###

                ##we compare the dictionary we had with the new values
                old_versions = asset_versions_dict.get(asset)
                
                if old_versions == None:

                    total_versions = versions_filtered
                    asset_versions_dict[asset] = total_versions
                    
                else:
                                       
                    new_versions = list(set(versions_filtered).difference(old_versions)) #we compare to the old assets
                    
                    if new_versions != []:

                        total_versions = list(old_versions.extend(new_versions))
                        #message = QtWidgets.QMessageBox.information(self, 'info', 'There are new versions of'+ asset + 'to gather')

                    else:
                        total_versions = list(old_versions)

                    asset_versions_dict[asset] = total_versions

            else: ## we skip if the path does not exist
                pass
            
    def selectedAsset(self):
        for assetlbl in self.label_cache: ## we itarate through the asset labels.
            selindexget = self.label_cache.index(assetlbl) ## we get the index in the list
            sel_assetname = assetlbl.text() ## we get the asset name
            sel_version = self.dropdown_cache[selindexget].currentText() ## we get the version of the asset

            for checkers in self.checkbox_cache[selindexget]: ## we iterate in the list in the list of checkers 

                if checkers.isChecked(): ## we get the ones that are checked, the rest suck
                    sel_checker = checkers.text() ## we get the checkerbox name

                    if sel_checker == 'F' or sel_checker ==  'P' or sel_checker ==  'S': ## plate checker
                        self.loadPlates(sel_assetname,sel_version,sel_checker)
                        
                    elif sel_checker == 'cam': ## cam checker
                        self.loadCameras(sel_assetname,sel_version,sel_checker)

                    elif sel_checker == 'H' or sel_checker == 'L' or sel_checker == 'A': ## geo checker
                        self.loadGeo(sel_assetname,sel_version,sel_checker)

                    elif sel_checker == 'R' : ## edit_ref checker
                        self.loadEditRef(sel_assetname,sel_version,sel_checker)

                    checkers.setChecked(False)
                    checkers.setStyleSheet("color: rgb(30, 30, 30);")
                    # elif sel_checker == 'S' : ## scan checker
                    #     self.loadScan(sel_assetname,sel_version,sel_checker)

    def loadEditRef(self,sel_assetname,sel_version,sel_checker,assettype='Edit_ref'):
        self.assetconfig = self.ED_assetconfig[assettype]
        self.assetpath = self.assetconfig['path']
        self.nodeclass = self.assetconfig['class']

        sel_checker = 'edit_reference'
        loadfolder = sel_checker + '_' + sel_version
        loadpath = self.assetpath + '/' + loadfolder + '/'
        #print loadpath

        for seq in nuke.getFileNameList(loadpath ):

            readNode = nuke.createNode(self.nodeclass)
            readNode.knob('file').fromUserText(loadpath + seq)    

    def loadPlates(self,sel_assetname,sel_version,sel_checker,assettype='Plate'):
        self.assetconfig = self.ED_assetconfig[assettype]
        self.assetpath = self.assetconfig['path']
        self.nodeclass = self.assetconfig['class']

        if sel_checker == 'F'or sel_checker == 'P':
            if sel_checker == 'F':
                sel_checker = 'linear'
            elif sel_checker == 'P':
                sel_checker = 'proxy'

            loadfolder = sel_checker + '_' + sel_version
            loadpath = self.assetpath + '/' + sel_assetname + '/' + 'versions' + '/' + loadfolder + '/' + 'full' + '/'

        elif sel_checker == 'S':
            self.assetpath = self.folder + '/' + 'data' + '/' + 'scans'
            sel_checker = sel_assetname
            loadfolder = sel_checker + '_' + sel_version
            loadpath = self.assetpath + '/' + 'versions' + '/' + loadfolder + '/' 

        for seq in nuke.getFileNameList(loadpath ):
            if seq != 'metadata':
                readNode = nuke.createNode(self.nodeclass)
                readNode.knob('file').fromUserText(loadpath + seq)
            else:
                pass

        self.loadLensDist(sel_assetname, sel_version, loadfolder)

    def loadLensDist(self, sel_assetname, sel_version, loadfolder , assettype='Plate' ):
        
        loadfolder = sel_assetname + '_' + sel_version
        
        lenspath = self.folder + '/' + 'data' + '/' + 'scans' + '/' + 'versions' + '/' + loadfolder + '/' + 'metadata' + '/' + 'lens_data.yaml'

        if os.path.exists(lenspath):
            lensdata = smd.load_lens_from_yaml(lenspath, False)

            imgnode = nuke.selectedNode()

            nuketools.makeDAGNeighbours(imgnode, lensdata)

    def loadCameras(self,sel_assetname,sel_version,sel_checker,assettype='Camera'):
        self.assetconfig = self.ED_assetconfig[assettype]
        self.assetpath = self.assetconfig['path']
        self.nodeclass = self.assetconfig['class']
        fullname = 'cache' + '_' + sel_version + '.abc'
        loadpath = self.assetpath + '/' + sel_assetname + '/' + 'versions' + '/' 
        camNode = nuke.createNode(self.nodeclass)
        camNode.knob('file').fromUserText(loadpath + fullname)
        ## todo remove the warning message

    def loadGeo(self,sel_assetname,sel_version,sel_checker,assettype='Geometry'):
        self.assetconfig = self.ED_assetconfig[assettype]
        self.assetpath = self.assetconfig['path']
        self.nodeclass = self.assetconfig['class']
        if sel_checker == 'H':
            self.nodeclass = self.nodeclass[0]
            sel_checker = 'cache'
        elif sel_checker == 'L':
            self.nodeclass = self.nodeclass[0]
            sel_checker = 'cache_low'
        elif sel_checker == 'A':
            self.nodeclass = self.nodeclass[1]
            sel_checker = 'utility'
        #print self.nodeclass
        fullname = sel_checker + '_' + sel_version + '.abc'
        loadpath = self.assetpath + '/' + sel_assetname + '/' + 'versions' + '/' 
        if os.path.exists(loadpath+fullname):
            geoNode = nuke.createNode(self.nodeclass)
            geoNode.knob('file').fromUserText(loadpath + fullname)
        else:
            message = QtWidgets.QMessageBox.information(self, 'info', sel_assetname.rpartition('/')[2] + ' ' + fullname + ' does not exist')

    def helloworld(self):
        print 'hey'






ED_AssetLoader = ED_AssetLoader()


def loadED_AssetLoader():
    ED_AssetLoader.show()
    ED_AssetLoader.setFixedSize(ED_AssetLoader.size())