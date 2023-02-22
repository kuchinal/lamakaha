//
// Copyright (c) 2009, Jim Hourihan
// All rights reserved.
//
// SPDX-License-Identifier: Apache-2.0 
// 
#ifndef __MuQt5__QResizeEventType__h__
#define __MuQt5__QResizeEventType__h__
#include <iostream>
#include <Mu/Class.h>

namespace Mu {

//
//  NOTE: file generated by qt2mu.py
//

class QResizeEventType : public Class
{
  public:
    //
    //  Types
    //

    typedef QResizeEvent ValueType;

    struct Struct
    {
        QResizeEvent* object;
    };

    //
    //  Constructors
    //

    QResizeEventType(Context* context, const char* name, Class* superClass = 0);
    virtual ~QResizeEventType();

    //
    //  Class API
    //

    virtual void load();
};

} // Mu

#endif // __MuQt5__QResizeEventType__h__
