//
// Copyright (c) 2009, Jim Hourihan
// All rights reserved.
//
// SPDX-License-Identifier: Apache-2.0 
// 
#include <MuQt5/qtUtils.h>
#include <MuQt5/QTableWidgetItemType.h>
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
#include <MuQt5/QSizeType.h>
#include <MuQt5/QIconType.h>
#include <MuQt5/QBrushType.h>
#include <MuQt5/QTableWidgetType.h>
#include <MuQt5/QVariantType.h>
#include <MuQt5/QFontType.h>

//
//  NOTE: this file was automatically generated by qt2mu.py
//

namespace Mu {
using namespace std;

QTableWidgetItemType::QTableWidgetItemType(Context* c, const char* name, Class* super)
    : Class(c, name, super)
{
}

QTableWidgetItemType::~QTableWidgetItemType()
{
}

//----------------------------------------------------------------------
//  PRE-COMPILED FUNCTIONS

Pointer qt_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_int(Mu::Thread& NODE_THREAD, Pointer param_this, int param_type)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    int arg1 = (int)(param_type);
    setqpointer<QTableWidgetItemType>(param_this,new QTableWidgetItem(arg1));
    return param_this;
}

Pointer qt_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_string_int(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_text, int param_type)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    const QString  arg1 = qstring(param_text);
    int arg2 = (int)(param_type);
    setqpointer<QTableWidgetItemType>(param_this,new QTableWidgetItem(arg1, arg2));
    return param_this;
}

Pointer qt_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_QIcon_string_int(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_icon, Pointer param_text, int param_type)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    const QIcon  arg1 = getqtype<QIconType>(param_icon);
    const QString  arg2 = qstring(param_text);
    int arg3 = (int)(param_type);
    setqpointer<QTableWidgetItemType>(param_this,new QTableWidgetItem(arg1, arg2, arg3));
    return param_this;
}

Pointer qt_QTableWidgetItem_background_QBrush_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return makeqtype<QBrushType>(c,arg0->background(),"qt.QBrush");
}

int qt_QTableWidgetItem_checkState_int_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return int(arg0->checkState());
}

Pointer qt_QTableWidgetItem_clone_QTableWidgetItem_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return makeqpointer<QTableWidgetItemType>(c,arg0->clone(),"qt.QTableWidgetItem");
}

int qt_QTableWidgetItem_column_int_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return arg0->column();
}

Pointer qt_QTableWidgetItem_data_QVariant_QTableWidgetItem_int(Mu::Thread& NODE_THREAD, Pointer param_this, int param_role)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    int arg1 = (int)(param_role);
    return makeqtype<QVariantType>(c,arg0->data(arg1),"qt.QVariant");
}

int qt_QTableWidgetItem_flags_int_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return int(arg0->flags());
}

Pointer qt_QTableWidgetItem_font_QFont_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return makeqtype<QFontType>(c,arg0->font(),"qt.QFont");
}

Pointer qt_QTableWidgetItem_foreground_QBrush_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return makeqtype<QBrushType>(c,arg0->foreground(),"qt.QBrush");
}

Pointer qt_QTableWidgetItem_icon_QIcon_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return makeqtype<QIconType>(c,arg0->icon(),"qt.QIcon");
}

bool qt_QTableWidgetItem_isSelected_bool_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return arg0->isSelected();
}

int qt_QTableWidgetItem_row_int_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return arg0->row();
}

void qt_QTableWidgetItem_setBackground_void_QTableWidgetItem_QBrush(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_brush)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    const QBrush  arg1 = getqtype<QBrushType>(param_brush);
    arg0->setBackground(arg1);
    setqpointer<QTableWidgetItemType>(param_this,arg0);
}

void qt_QTableWidgetItem_setCheckState_void_QTableWidgetItem_int(Mu::Thread& NODE_THREAD, Pointer param_this, int param_state)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    Qt::CheckState arg1 = (Qt::CheckState)(param_state);
    arg0->setCheckState(arg1);
    setqpointer<QTableWidgetItemType>(param_this,arg0);
}

void qt_QTableWidgetItem_setData_void_QTableWidgetItem_int_QVariant(Mu::Thread& NODE_THREAD, Pointer param_this, int param_role, Pointer param_value)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    int arg1 = (int)(param_role);
    const QVariant  arg2 = getqtype<QVariantType>(param_value);
    arg0->setData(arg1, arg2);
    setqpointer<QTableWidgetItemType>(param_this,arg0);
}

void qt_QTableWidgetItem_setFlags_void_QTableWidgetItem_int(Mu::Thread& NODE_THREAD, Pointer param_this, int param_flags)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    Qt::ItemFlags arg1 = (Qt::ItemFlags)(param_flags);
    arg0->setFlags(arg1);
    setqpointer<QTableWidgetItemType>(param_this,arg0);
}

void qt_QTableWidgetItem_setFont_void_QTableWidgetItem_QFont(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_font)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    const QFont  arg1 = getqtype<QFontType>(param_font);
    arg0->setFont(arg1);
    setqpointer<QTableWidgetItemType>(param_this,arg0);
}

void qt_QTableWidgetItem_setForeground_void_QTableWidgetItem_QBrush(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_brush)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    const QBrush  arg1 = getqtype<QBrushType>(param_brush);
    arg0->setForeground(arg1);
    setqpointer<QTableWidgetItemType>(param_this,arg0);
}

void qt_QTableWidgetItem_setIcon_void_QTableWidgetItem_QIcon(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_icon)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    const QIcon  arg1 = getqtype<QIconType>(param_icon);
    arg0->setIcon(arg1);
    setqpointer<QTableWidgetItemType>(param_this,arg0);
}

void qt_QTableWidgetItem_setSelected_void_QTableWidgetItem_bool(Mu::Thread& NODE_THREAD, Pointer param_this, bool param_select)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    bool arg1 = (bool)(param_select);
    arg0->setSelected(arg1);
    setqpointer<QTableWidgetItemType>(param_this,arg0);
}

void qt_QTableWidgetItem_setSizeHint_void_QTableWidgetItem_QSize(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_size)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    const QSize  arg1 = getqtype<QSizeType>(param_size);
    arg0->setSizeHint(arg1);
    setqpointer<QTableWidgetItemType>(param_this,arg0);
}

void qt_QTableWidgetItem_setStatusTip_void_QTableWidgetItem_string(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_statusTip)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    const QString  arg1 = qstring(param_statusTip);
    arg0->setStatusTip(arg1);
    setqpointer<QTableWidgetItemType>(param_this,arg0);
}

void qt_QTableWidgetItem_setText_void_QTableWidgetItem_string(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_text)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    const QString  arg1 = qstring(param_text);
    arg0->setText(arg1);
    setqpointer<QTableWidgetItemType>(param_this,arg0);
}

void qt_QTableWidgetItem_setTextAlignment_void_QTableWidgetItem_int(Mu::Thread& NODE_THREAD, Pointer param_this, int param_alignment)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    int arg1 = (int)(param_alignment);
    arg0->setTextAlignment(arg1);
    setqpointer<QTableWidgetItemType>(param_this,arg0);
}

void qt_QTableWidgetItem_setToolTip_void_QTableWidgetItem_string(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_toolTip)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    const QString  arg1 = qstring(param_toolTip);
    arg0->setToolTip(arg1);
    setqpointer<QTableWidgetItemType>(param_this,arg0);
}

void qt_QTableWidgetItem_setWhatsThis_void_QTableWidgetItem_string(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_whatsThis)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    const QString  arg1 = qstring(param_whatsThis);
    arg0->setWhatsThis(arg1);
    setqpointer<QTableWidgetItemType>(param_this,arg0);
}

Pointer qt_QTableWidgetItem_sizeHint_QSize_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return makeqtype<QSizeType>(c,arg0->sizeHint(),"qt.QSize");
}

Pointer qt_QTableWidgetItem_statusTip_string_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return makestring(c,arg0->statusTip());
}

Pointer qt_QTableWidgetItem_tableWidget_QTableWidget_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return makeinstance<QTableWidgetType>(c,arg0->tableWidget(),"qt.QTableWidget");
}

Pointer qt_QTableWidgetItem_text_string_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return makestring(c,arg0->text());
}

int qt_QTableWidgetItem_textAlignment_int_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return arg0->textAlignment();
}

Pointer qt_QTableWidgetItem_toolTip_string_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return makestring(c,arg0->toolTip());
}

int qt_QTableWidgetItem_type_int_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return arg0->type();
}

Pointer qt_QTableWidgetItem_whatsThis_string_QTableWidgetItem(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QTableWidgetItem * arg0 = getqpointer<QTableWidgetItemType>(param_this);
    return makestring(c,arg0->whatsThis());
}


static NODE_IMPLEMENTATION(_n_QTableWidgetItem0, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_int(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, int)));
}

static NODE_IMPLEMENTATION(_n_QTableWidgetItem1, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_string_int(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer), NODE_ARG(2, int)));
}

static NODE_IMPLEMENTATION(_n_QTableWidgetItem2, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_QIcon_string_int(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer), NODE_ARG(2, Pointer), NODE_ARG(3, int)));
}

static NODE_IMPLEMENTATION(_n_background0, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_background_QBrush_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_checkState0, int)
{
    NODE_RETURN(qt_QTableWidgetItem_checkState_int_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_clone0, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_clone_QTableWidgetItem_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_column0, int)
{
    NODE_RETURN(qt_QTableWidgetItem_column_int_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_data0, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_data_QVariant_QTableWidgetItem_int(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, int)));
}

static NODE_IMPLEMENTATION(_n_flags0, int)
{
    NODE_RETURN(qt_QTableWidgetItem_flags_int_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_font0, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_font_QFont_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_foreground0, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_foreground_QBrush_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_icon0, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_icon_QIcon_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_isSelected0, bool)
{
    NODE_RETURN(qt_QTableWidgetItem_isSelected_bool_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_row0, int)
{
    NODE_RETURN(qt_QTableWidgetItem_row_int_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_setBackground0, void)
{
    qt_QTableWidgetItem_setBackground_void_QTableWidgetItem_QBrush(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer));
}

static NODE_IMPLEMENTATION(_n_setCheckState0, void)
{
    qt_QTableWidgetItem_setCheckState_void_QTableWidgetItem_int(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, int));
}

static NODE_IMPLEMENTATION(_n_setData0, void)
{
    qt_QTableWidgetItem_setData_void_QTableWidgetItem_int_QVariant(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, int), NODE_ARG(2, Pointer));
}

static NODE_IMPLEMENTATION(_n_setFlags0, void)
{
    qt_QTableWidgetItem_setFlags_void_QTableWidgetItem_int(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, int));
}

static NODE_IMPLEMENTATION(_n_setFont0, void)
{
    qt_QTableWidgetItem_setFont_void_QTableWidgetItem_QFont(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer));
}

static NODE_IMPLEMENTATION(_n_setForeground0, void)
{
    qt_QTableWidgetItem_setForeground_void_QTableWidgetItem_QBrush(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer));
}

static NODE_IMPLEMENTATION(_n_setIcon0, void)
{
    qt_QTableWidgetItem_setIcon_void_QTableWidgetItem_QIcon(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer));
}

static NODE_IMPLEMENTATION(_n_setSelected0, void)
{
    qt_QTableWidgetItem_setSelected_void_QTableWidgetItem_bool(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, bool));
}

static NODE_IMPLEMENTATION(_n_setSizeHint0, void)
{
    qt_QTableWidgetItem_setSizeHint_void_QTableWidgetItem_QSize(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer));
}

static NODE_IMPLEMENTATION(_n_setStatusTip0, void)
{
    qt_QTableWidgetItem_setStatusTip_void_QTableWidgetItem_string(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer));
}

static NODE_IMPLEMENTATION(_n_setText0, void)
{
    qt_QTableWidgetItem_setText_void_QTableWidgetItem_string(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer));
}

static NODE_IMPLEMENTATION(_n_setTextAlignment0, void)
{
    qt_QTableWidgetItem_setTextAlignment_void_QTableWidgetItem_int(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, int));
}

static NODE_IMPLEMENTATION(_n_setToolTip0, void)
{
    qt_QTableWidgetItem_setToolTip_void_QTableWidgetItem_string(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer));
}

static NODE_IMPLEMENTATION(_n_setWhatsThis0, void)
{
    qt_QTableWidgetItem_setWhatsThis_void_QTableWidgetItem_string(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer));
}

static NODE_IMPLEMENTATION(_n_sizeHint0, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_sizeHint_QSize_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_statusTip0, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_statusTip_string_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_tableWidget0, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_tableWidget_QTableWidget_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_text0, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_text_string_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_textAlignment0, int)
{
    NODE_RETURN(qt_QTableWidgetItem_textAlignment_int_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_toolTip0, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_toolTip_string_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_type0, int)
{
    NODE_RETURN(qt_QTableWidgetItem_type_int_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_whatsThis0, Pointer)
{
    NODE_RETURN(qt_QTableWidgetItem_whatsThis_string_QTableWidgetItem(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}



void
QTableWidgetItemType::load()
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
    new Alias(c, "ItemType", "int"),
      new SymbolicConstant(c, "Type", "int", Value(int(QTableWidgetItem::Type))),
      new SymbolicConstant(c, "UserType", "int", Value(int(QTableWidgetItem::UserType))),
    EndArguments);

addSymbols(
    // enums
    // member functions
    new Function(c, "QTableWidgetItem", _n_QTableWidgetItem0, None, Compiled, qt_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_int, Return, "qt.QTableWidgetItem", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "type", "int", Value((int)QTableWidgetItem::Type)), End),
    new Function(c, "QTableWidgetItem", _n_QTableWidgetItem1, None, Compiled, qt_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_string_int, Return, "qt.QTableWidgetItem", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "text", "string"), new Param(c, "type", "int", Value((int)QTableWidgetItem::Type)), End),
    new Function(c, "QTableWidgetItem", _n_QTableWidgetItem2, None, Compiled, qt_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_QTableWidgetItem_QIcon_string_int, Return, "qt.QTableWidgetItem", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "icon", "qt.QIcon"), new Param(c, "text", "string"), new Param(c, "type", "int", Value((int)QTableWidgetItem::Type)), End),
    // MISSING: QTableWidgetItem (QTableWidgetItem; QTableWidgetItem this, QTableWidgetItem other)
    new Function(c, "background", _n_background0, None, Compiled, qt_QTableWidgetItem_background_QBrush_QTableWidgetItem, Return, "qt.QBrush", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new Function(c, "checkState", _n_checkState0, None, Compiled, qt_QTableWidgetItem_checkState_int_QTableWidgetItem, Return, "int", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new MemberFunction(c, "clone", _n_clone0, None, Compiled, qt_QTableWidgetItem_clone_QTableWidgetItem_QTableWidgetItem, Return, "qt.QTableWidgetItem", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new Function(c, "column", _n_column0, None, Compiled, qt_QTableWidgetItem_column_int_QTableWidgetItem, Return, "int", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new MemberFunction(c, "data", _n_data0, None, Compiled, qt_QTableWidgetItem_data_QVariant_QTableWidgetItem_int, Return, "qt.QVariant", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "role", "int"), End),
    new Function(c, "flags", _n_flags0, None, Compiled, qt_QTableWidgetItem_flags_int_QTableWidgetItem, Return, "int", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new Function(c, "font", _n_font0, None, Compiled, qt_QTableWidgetItem_font_QFont_QTableWidgetItem, Return, "qt.QFont", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new Function(c, "foreground", _n_foreground0, None, Compiled, qt_QTableWidgetItem_foreground_QBrush_QTableWidgetItem, Return, "qt.QBrush", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new Function(c, "icon", _n_icon0, None, Compiled, qt_QTableWidgetItem_icon_QIcon_QTableWidgetItem, Return, "qt.QIcon", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new Function(c, "isSelected", _n_isSelected0, None, Compiled, qt_QTableWidgetItem_isSelected_bool_QTableWidgetItem, Return, "bool", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    // MISSING: read (void; QTableWidgetItem this, "QDataStream &" in)
    new Function(c, "row", _n_row0, None, Compiled, qt_QTableWidgetItem_row_int_QTableWidgetItem, Return, "int", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new Function(c, "setBackground", _n_setBackground0, None, Compiled, qt_QTableWidgetItem_setBackground_void_QTableWidgetItem_QBrush, Return, "void", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "brush", "qt.QBrush"), End),
    new Function(c, "setCheckState", _n_setCheckState0, None, Compiled, qt_QTableWidgetItem_setCheckState_void_QTableWidgetItem_int, Return, "void", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "state", "int"), End),
    new MemberFunction(c, "setData", _n_setData0, None, Compiled, qt_QTableWidgetItem_setData_void_QTableWidgetItem_int_QVariant, Return, "void", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "role", "int"), new Param(c, "value", "qt.QVariant"), End),
    new Function(c, "setFlags", _n_setFlags0, None, Compiled, qt_QTableWidgetItem_setFlags_void_QTableWidgetItem_int, Return, "void", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "flags", "int"), End),
    new Function(c, "setFont", _n_setFont0, None, Compiled, qt_QTableWidgetItem_setFont_void_QTableWidgetItem_QFont, Return, "void", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "font", "qt.QFont"), End),
    new Function(c, "setForeground", _n_setForeground0, None, Compiled, qt_QTableWidgetItem_setForeground_void_QTableWidgetItem_QBrush, Return, "void", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "brush", "qt.QBrush"), End),
    new Function(c, "setIcon", _n_setIcon0, None, Compiled, qt_QTableWidgetItem_setIcon_void_QTableWidgetItem_QIcon, Return, "void", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "icon", "qt.QIcon"), End),
    new Function(c, "setSelected", _n_setSelected0, None, Compiled, qt_QTableWidgetItem_setSelected_void_QTableWidgetItem_bool, Return, "void", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "select", "bool"), End),
    new Function(c, "setSizeHint", _n_setSizeHint0, None, Compiled, qt_QTableWidgetItem_setSizeHint_void_QTableWidgetItem_QSize, Return, "void", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "size", "qt.QSize"), End),
    new Function(c, "setStatusTip", _n_setStatusTip0, None, Compiled, qt_QTableWidgetItem_setStatusTip_void_QTableWidgetItem_string, Return, "void", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "statusTip", "string"), End),
    new Function(c, "setText", _n_setText0, None, Compiled, qt_QTableWidgetItem_setText_void_QTableWidgetItem_string, Return, "void", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "text", "string"), End),
    new Function(c, "setTextAlignment", _n_setTextAlignment0, None, Compiled, qt_QTableWidgetItem_setTextAlignment_void_QTableWidgetItem_int, Return, "void", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "alignment", "int"), End),
    new Function(c, "setToolTip", _n_setToolTip0, None, Compiled, qt_QTableWidgetItem_setToolTip_void_QTableWidgetItem_string, Return, "void", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "toolTip", "string"), End),
    new Function(c, "setWhatsThis", _n_setWhatsThis0, None, Compiled, qt_QTableWidgetItem_setWhatsThis_void_QTableWidgetItem_string, Return, "void", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), new Param(c, "whatsThis", "string"), End),
    new Function(c, "sizeHint", _n_sizeHint0, None, Compiled, qt_QTableWidgetItem_sizeHint_QSize_QTableWidgetItem, Return, "qt.QSize", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new Function(c, "statusTip", _n_statusTip0, None, Compiled, qt_QTableWidgetItem_statusTip_string_QTableWidgetItem, Return, "string", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new Function(c, "tableWidget", _n_tableWidget0, None, Compiled, qt_QTableWidgetItem_tableWidget_QTableWidget_QTableWidgetItem, Return, "qt.QTableWidget", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new Function(c, "text", _n_text0, None, Compiled, qt_QTableWidgetItem_text_string_QTableWidgetItem, Return, "string", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new Function(c, "textAlignment", _n_textAlignment0, None, Compiled, qt_QTableWidgetItem_textAlignment_int_QTableWidgetItem, Return, "int", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new Function(c, "toolTip", _n_toolTip0, None, Compiled, qt_QTableWidgetItem_toolTip_string_QTableWidgetItem, Return, "string", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new Function(c, "type", _n_type0, None, Compiled, qt_QTableWidgetItem_type_int_QTableWidgetItem, Return, "int", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    new Function(c, "whatsThis", _n_whatsThis0, None, Compiled, qt_QTableWidgetItem_whatsThis_string_QTableWidgetItem, Return, "string", Parameters, new Param(c, "this", "qt.QTableWidgetItem"), End),
    // MISSING: write (void; QTableWidgetItem this, "QDataStream &" out)
    // static functions
    EndArguments);
globalScope()->addSymbols(
    // MISSING: = (QTableWidgetItem; QTableWidgetItem this, QTableWidgetItem other)
    EndArguments);
scope()->addSymbols(
    EndArguments);


c->arrayType(this, 1, 0);

                        
}

} // Mu
