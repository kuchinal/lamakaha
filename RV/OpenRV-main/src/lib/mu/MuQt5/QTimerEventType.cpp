//
// Copyright (c) 2009, Jim Hourihan
// All rights reserved.
//
// SPDX-License-Identifier: Apache-2.0 
// 
#include <MuQt5/qtUtils.h>
#include <MuQt5/QTimerEventType.h>
#include <QtGui/QtGui>
#include <QtWidgets/QtWidgets>
#include <QtSvg/QtSvg>
#include <QtNetwork/QtNetwork>
#include <MuQt5/QWidgetType.h>
#include <MuQt5/QActionType.h>
#include <MuQt5/QIconType.h>
#include <Mu/BaseFunctions.h>
#include <Mu/Alias.h>
#include <Mu/SymbolicConstant.h>
#include <Mu/Thread.h>
#include <Mu/ClassInstance.h>
#include <Mu/Function.h>
#include <Mu/MemberFunction.h>
#include <Mu/MemberVariable.h>
#include <Mu/Node.h>
#include <Mu/Exception.h>
#include <Mu/ParameterVariable.h>
#include <Mu/ReferenceType.h>
#include <Mu/Value.h>
#include <MuLang/MuLangContext.h>
#include <MuLang/StringType.h>

//
//  NOTE: this file was automatically generated by qt2mu.py
//

namespace Mu {
using namespace std;

QTimerEventType::QTimerEventType(Context* c, const char* name, Class* super)
    : Class(c, name, super)
{
}

QTimerEventType::~QTimerEventType()
{
}

//----------------------------------------------------------------------
//  PRE-COMPILED FUNCTIONS

Pointer qt_QTimerEvent_QTimerEvent_QTimerEvent_QTimerEvent_int(Mu::Thread& NODE_THREAD, Pointer param_this, int param_timerId)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    int arg1 = (int)(param_timerId);
    setqpointer<QTimerEventType>(param_this,new QTimerEvent(arg1));
    return param_this;
}

int qt_QTimerEvent_timerId_int_QTimerEvent(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTimerEvent * arg0 = getqpointer<QTimerEventType>(param_this);
    return arg0->timerId();
}


static NODE_IMPLEMENTATION(_n_QTimerEvent0, Pointer)
{
    NODE_RETURN(qt_QTimerEvent_QTimerEvent_QTimerEvent_QTimerEvent_int(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, int)));
}

static NODE_IMPLEMENTATION(_n_timerId0, int)
{
    NODE_RETURN(qt_QTimerEvent_timerId_int_QTimerEvent(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}



void
QTimerEventType::load()
{
    USING_MU_FUNCTION_SYMBOLS;
    MuLangContext* c = static_cast<MuLangContext*>(context());
    Module* global = globalModule();
    
    const string typeName        = name();
    const string refTypeName     = typeName + "&";
    const string fullTypeName    = fullyQualifiedName();
    const string fullRefTypeName = fullTypeName + "&";
    const char*  tn              = typeName.c_str();
    const char*  ftn             = fullTypeName.c_str();
    const char*  rtn             = refTypeName.c_str();
    const char*  frtn            = fullRefTypeName.c_str();

    scope()->addSymbols(new ReferenceType(c, rtn, this),

                        new Function(c, tn, BaseFunctions::dereference, Cast,
                                     Return, ftn,
                                     Args, frtn, End),

                        EndArguments);
    
    addSymbols(new Function(c, "__allocate", BaseFunctions::classAllocate, None,
                            Return, ftn,
                            End),

               new MemberVariable(c, "native", "qt.NativeObject"),

               EndArguments );


addSymbols(
    EndArguments);

addSymbols(
    // enums
    // member functions
    new Function(c, "QTimerEvent", _n_QTimerEvent0, None, Compiled, qt_QTimerEvent_QTimerEvent_QTimerEvent_QTimerEvent_int, Return, "qt.QTimerEvent", Parameters, new Param(c, "this", "qt.QTimerEvent"), new Param(c, "timerId", "int"), End),
    new Function(c, "timerId", _n_timerId0, None, Compiled, qt_QTimerEvent_timerId_int_QTimerEvent, Return, "int", Parameters, new Param(c, "this", "qt.QTimerEvent"), End),
    // static functions
    EndArguments);
globalScope()->addSymbols(
    EndArguments);
scope()->addSymbols(
    EndArguments);

}

} // Mu
