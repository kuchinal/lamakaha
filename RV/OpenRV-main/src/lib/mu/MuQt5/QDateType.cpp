//
// Copyright (c) 2009, Jim Hourihan
// All rights reserved.
//
// SPDX-License-Identifier: Apache-2.0 
// 
#include <MuQt5/qtUtils.h>
#include <MuQt5/QDateType.h>
#include <MuQt5/QActionType.h>
#include <MuQt5/QWidgetType.h>
#include <Mu/Alias.h>
#include <Mu/BaseFunctions.h>
#include <Mu/ClassInstance.h>
#include <Mu/Exception.h>
#include <Mu/Function.h>
#include <Mu/MemberFunction.h>
#include <Mu/MemberVariable.h>
#include <Mu/Node.h>
#include <Mu/ParameterVariable.h>
#include <Mu/ReferenceType.h>
#include <Mu/SymbolicConstant.h>
#include <Mu/Thread.h>
#include <Mu/Value.h>
#include <MuLang/MuLangContext.h>
#include <MuLang/StringType.h>
#include <QtGui/QtGui>
#include <QtWidgets/QtWidgets>
#include <QtSvg/QtSvg>
#include <QtNetwork/QtNetwork>

//
//  NOTE: this file was automatically generated by qt2mu.py
//

namespace Mu {
using namespace std;

QDateType::Instance::Instance(const Class* c) : ClassInstance(c)
{
}

QDateType::QDateType(Context* c, const char* name, Class* super)
    : Class(c, name, super)
{
}

QDateType::~QDateType()
{
}

static NODE_IMPLEMENTATION(__allocate, Pointer)
{
    QDateType::Instance* i = new QDateType::Instance((Class*)NODE_THIS.type());
    QDateType::registerFinalizer(i);
    NODE_RETURN(i);
}

void 
QDateType::registerFinalizer (void* o)
{
    GC_register_finalizer(o, QDateType::finalizer, 0, 0, 0);
}

void 
QDateType::finalizer (void* obj, void* data)
{
    QDateType::Instance* i = reinterpret_cast<QDateType::Instance*>(obj);
    delete i;
}

//----------------------------------------------------------------------
//  PRE-COMPILED FUNCTIONS

Pointer qt_QDate_QDate_QDate_QDate(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    setqtype<QDateType>(param_this,QDate());
    return param_this;
}

Pointer qt_QDate_QDate_QDate_QDate_int_int_int(Mu::Thread& NODE_THREAD, Pointer param_this, int param_y, int param_m, int param_d)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    int arg1 = (int)(param_y);
    int arg2 = (int)(param_m);
    int arg3 = (int)(param_d);
    setqtype<QDateType>(param_this,QDate(arg1, arg2, arg3));
    return param_this;
}

Pointer qt_QDate_addDays_QDate_QDate_int64(Mu::Thread& NODE_THREAD, Pointer param_this, int64 param_ndays)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    qint64 arg1 = (int64)(param_ndays);
    return makeqtype<QDateType>(c,arg0.addDays(arg1),"qt.QDate");
}

Pointer qt_QDate_addMonths_QDate_QDate_int(Mu::Thread& NODE_THREAD, Pointer param_this, int param_nmonths)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    int arg1 = (int)(param_nmonths);
    return makeqtype<QDateType>(c,arg0.addMonths(arg1),"qt.QDate");
}

Pointer qt_QDate_addYears_QDate_QDate_int(Mu::Thread& NODE_THREAD, Pointer param_this, int param_nyears)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    int arg1 = (int)(param_nyears);
    return makeqtype<QDateType>(c,arg0.addYears(arg1),"qt.QDate");
}

int qt_QDate_day_int_QDate(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    return arg0.day();
}

int qt_QDate_dayOfWeek_int_QDate(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    return arg0.dayOfWeek();
}

int qt_QDate_dayOfYear_int_QDate(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    return arg0.dayOfYear();
}

int qt_QDate_daysInMonth_int_QDate(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    return arg0.daysInMonth();
}

int qt_QDate_daysInYear_int_QDate(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    return arg0.daysInYear();
}

int64 qt_QDate_daysTo_int64_QDate_QDate(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_d)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    const QDate  arg1 = getqtype<QDateType>(param_d);
    return arg0.daysTo(arg1);
}

bool qt_QDate_isNull_bool_QDate(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    return arg0.isNull();
}

bool qt_QDate_isValid_bool_QDate(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    return arg0.isValid();
}

int qt_QDate_month_int_QDate(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    return arg0.month();
}

bool qt_QDate_setDate_bool_QDate_int_int_int(Mu::Thread& NODE_THREAD, Pointer param_this, int param_year, int param_month, int param_day)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    int arg1 = (int)(param_year);
    int arg2 = (int)(param_month);
    int arg3 = (int)(param_day);
    return arg0.setDate(arg1, arg2, arg3);
}

int64 qt_QDate_toJulianDay_int64_QDate(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    return arg0.toJulianDay();
}

Pointer qt_QDate_toString_string_QDate_string(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_format)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    const QString  arg1 = qstring(param_format);
    return makestring(c,arg0.toString(arg1));
}

Pointer qt_QDate_toString_string_QDate_int(Mu::Thread& NODE_THREAD, Pointer param_this, int param_format)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    Qt::DateFormat arg1 = (Qt::DateFormat)(param_format);
    return makestring(c,arg0.toString(arg1));
}

int qt_QDate_year_int_QDate(Mu::Thread& NODE_THREAD, Pointer param_this)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    return arg0.year();
}

bool qt_QDate_operatorBang_EQ__bool_QDate_QDate(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_d)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    const QDate  arg1 = getqtype<QDateType>(param_d);
    return arg0.operator!=(arg1);
}

bool qt_QDate_operatorLT__bool_QDate_QDate(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_d)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    const QDate  arg1 = getqtype<QDateType>(param_d);
    return arg0.operator<(arg1);
}

bool qt_QDate_operatorLT_EQ__bool_QDate_QDate(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_d)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    const QDate  arg1 = getqtype<QDateType>(param_d);
    return arg0.operator<=(arg1);
}

bool qt_QDate_operatorEQ_EQ__bool_QDate_QDate(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_d)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    const QDate  arg1 = getqtype<QDateType>(param_d);
    return arg0.operator==(arg1);
}

bool qt_QDate_operatorGT__bool_QDate_QDate(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_d)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    const QDate  arg1 = getqtype<QDateType>(param_d);
    return arg0.operator>(arg1);
}

bool qt_QDate_operatorGT_EQ__bool_QDate_QDate(Mu::Thread& NODE_THREAD, Pointer param_this, Pointer param_d)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    QDate arg0 = getqtype<QDateType>(param_this);
    const QDate  arg1 = getqtype<QDateType>(param_d);
    return arg0.operator>=(arg1);
}

Pointer qt_QDate_currentDate_QDate(Mu::Thread& NODE_THREAD)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    return makeqtype<QDateType>(c,QDate::currentDate(),"qt.QDate");
}

Pointer qt_QDate_fromJulianDay_QDate_int64(Mu::Thread& NODE_THREAD, int64 param_jd)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    qint64 arg0 = (int64)(param_jd);
    return makeqtype<QDateType>(c,QDate::fromJulianDay(arg0),"qt.QDate");
}

Pointer qt_QDate_fromString_QDate_string_int(Mu::Thread& NODE_THREAD, Pointer param_string, int param_format)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    const QString  arg0 = qstring(param_string);
    Qt::DateFormat arg1 = (Qt::DateFormat)(param_format);
    return makeqtype<QDateType>(c,QDate::fromString(arg0, arg1),"qt.QDate");
}

Pointer qt_QDate_fromString_QDate_string_string(Mu::Thread& NODE_THREAD, Pointer param_string, Pointer param_format)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    const QString  arg0 = qstring(param_string);
    const QString  arg1 = qstring(param_format);
    return makeqtype<QDateType>(c,QDate::fromString(arg0, arg1),"qt.QDate");
}

bool qt_QDate_isLeapYear_bool_int(Mu::Thread& NODE_THREAD, int param_year)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    int arg0 = (int)(param_year);
    return QDate::isLeapYear(arg0);
}

bool qt_QDate_isValid_bool_int_int_int(Mu::Thread& NODE_THREAD, int param_year, int param_month, int param_day)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    int arg0 = (int)(param_year);
    int arg1 = (int)(param_month);
    int arg2 = (int)(param_day);
    return QDate::isValid(arg0, arg1, arg2);
}

Pointer qt_QDate_longDayName_string_int_int(Mu::Thread& NODE_THREAD, int param_weekday, int param_type)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    int arg0 = (int)(param_weekday);
    QDate::MonthNameType arg1 = (QDate::MonthNameType)(param_type);
    return makestring(c,QDate::longDayName(arg0, arg1));
}

Pointer qt_QDate_longMonthName_string_int_int(Mu::Thread& NODE_THREAD, int param_month, int param_type)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    int arg0 = (int)(param_month);
    QDate::MonthNameType arg1 = (QDate::MonthNameType)(param_type);
    return makestring(c,QDate::longMonthName(arg0, arg1));
}

Pointer qt_QDate_shortDayName_string_int_int(Mu::Thread& NODE_THREAD, int param_weekday, int param_type)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    int arg0 = (int)(param_weekday);
    QDate::MonthNameType arg1 = (QDate::MonthNameType)(param_type);
    return makestring(c,QDate::shortDayName(arg0, arg1));
}

Pointer qt_QDate_shortMonthName_string_int_int(Mu::Thread& NODE_THREAD, int param_month, int param_type)
{
    MuLangContext* c = static_cast<MuLangContext*>(NODE_THREAD.context());
    int arg0 = (int)(param_month);
    QDate::MonthNameType arg1 = (QDate::MonthNameType)(param_type);
    return makestring(c,QDate::shortMonthName(arg0, arg1));
}


static NODE_IMPLEMENTATION(_n_QDate0, Pointer)
{
    NODE_RETURN(qt_QDate_QDate_QDate_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_QDate1, Pointer)
{
    NODE_RETURN(qt_QDate_QDate_QDate_QDate_int_int_int(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, int), NODE_ARG(2, int), NODE_ARG(3, int)));
}

static NODE_IMPLEMENTATION(_n_addDays0, Pointer)
{
    NODE_RETURN(qt_QDate_addDays_QDate_QDate_int64(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, int64)));
}

static NODE_IMPLEMENTATION(_n_addMonths0, Pointer)
{
    NODE_RETURN(qt_QDate_addMonths_QDate_QDate_int(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, int)));
}

static NODE_IMPLEMENTATION(_n_addYears0, Pointer)
{
    NODE_RETURN(qt_QDate_addYears_QDate_QDate_int(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, int)));
}

static NODE_IMPLEMENTATION(_n_day0, int)
{
    NODE_RETURN(qt_QDate_day_int_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_dayOfWeek0, int)
{
    NODE_RETURN(qt_QDate_dayOfWeek_int_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_dayOfYear0, int)
{
    NODE_RETURN(qt_QDate_dayOfYear_int_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_daysInMonth0, int)
{
    NODE_RETURN(qt_QDate_daysInMonth_int_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_daysInYear0, int)
{
    NODE_RETURN(qt_QDate_daysInYear_int_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_daysTo0, int64)
{
    NODE_RETURN(qt_QDate_daysTo_int64_QDate_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer)));
}

static NODE_IMPLEMENTATION(_n_isNull0, bool)
{
    NODE_RETURN(qt_QDate_isNull_bool_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_isValid0, bool)
{
    NODE_RETURN(qt_QDate_isValid_bool_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_month0, int)
{
    NODE_RETURN(qt_QDate_month_int_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_setDate0, bool)
{
    NODE_RETURN(qt_QDate_setDate_bool_QDate_int_int_int(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, int), NODE_ARG(2, int), NODE_ARG(3, int)));
}

static NODE_IMPLEMENTATION(_n_toJulianDay0, int64)
{
    NODE_RETURN(qt_QDate_toJulianDay_int64_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_toString0, Pointer)
{
    NODE_RETURN(qt_QDate_toString_string_QDate_string(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer)));
}

static NODE_IMPLEMENTATION(_n_toString1, Pointer)
{
    NODE_RETURN(qt_QDate_toString_string_QDate_int(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, int)));
}

static NODE_IMPLEMENTATION(_n_year0, int)
{
    NODE_RETURN(qt_QDate_year_int_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer)));
}

static NODE_IMPLEMENTATION(_n_operatorBang_EQ_0, bool)
{
    NODE_RETURN(qt_QDate_operatorBang_EQ__bool_QDate_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer)));
}

static NODE_IMPLEMENTATION(_n_operatorLT_0, bool)
{
    NODE_RETURN(qt_QDate_operatorLT__bool_QDate_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer)));
}

static NODE_IMPLEMENTATION(_n_operatorLT_EQ_0, bool)
{
    NODE_RETURN(qt_QDate_operatorLT_EQ__bool_QDate_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer)));
}

static NODE_IMPLEMENTATION(_n_operatorEQ_EQ_0, bool)
{
    NODE_RETURN(qt_QDate_operatorEQ_EQ__bool_QDate_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer)));
}

static NODE_IMPLEMENTATION(_n_operatorGT_0, bool)
{
    NODE_RETURN(qt_QDate_operatorGT__bool_QDate_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer)));
}

static NODE_IMPLEMENTATION(_n_operatorGT_EQ_0, bool)
{
    NODE_RETURN(qt_QDate_operatorGT_EQ__bool_QDate_QDate(NODE_THREAD, NONNIL_NODE_ARG(0, Pointer), NODE_ARG(1, Pointer)));
}

static NODE_IMPLEMENTATION(_n_currentDate0, Pointer)
{
    NODE_RETURN(qt_QDate_currentDate_QDate(NODE_THREAD));
}

static NODE_IMPLEMENTATION(_n_fromJulianDay0, Pointer)
{
    NODE_RETURN(qt_QDate_fromJulianDay_QDate_int64(NODE_THREAD, NODE_ARG(0, int64)));
}

static NODE_IMPLEMENTATION(_n_fromString0, Pointer)
{
    NODE_RETURN(qt_QDate_fromString_QDate_string_int(NODE_THREAD, NODE_ARG(0, Pointer), NODE_ARG(1, int)));
}

static NODE_IMPLEMENTATION(_n_fromString1, Pointer)
{
    NODE_RETURN(qt_QDate_fromString_QDate_string_string(NODE_THREAD, NODE_ARG(0, Pointer), NODE_ARG(1, Pointer)));
}

static NODE_IMPLEMENTATION(_n_isLeapYear0, bool)
{
    NODE_RETURN(qt_QDate_isLeapYear_bool_int(NODE_THREAD, NODE_ARG(0, int)));
}

static NODE_IMPLEMENTATION(_n_isValid1, bool)
{
    NODE_RETURN(qt_QDate_isValid_bool_int_int_int(NODE_THREAD, NODE_ARG(0, int), NODE_ARG(1, int), NODE_ARG(2, int)));
}

static NODE_IMPLEMENTATION(_n_longDayName0, Pointer)
{
    NODE_RETURN(qt_QDate_longDayName_string_int_int(NODE_THREAD, NODE_ARG(0, int), NODE_ARG(1, int)));
}

static NODE_IMPLEMENTATION(_n_longMonthName0, Pointer)
{
    NODE_RETURN(qt_QDate_longMonthName_string_int_int(NODE_THREAD, NODE_ARG(0, int), NODE_ARG(1, int)));
}

static NODE_IMPLEMENTATION(_n_shortDayName0, Pointer)
{
    NODE_RETURN(qt_QDate_shortDayName_string_int_int(NODE_THREAD, NODE_ARG(0, int), NODE_ARG(1, int)));
}

static NODE_IMPLEMENTATION(_n_shortMonthName0, Pointer)
{
    NODE_RETURN(qt_QDate_shortMonthName_string_int_int(NODE_THREAD, NODE_ARG(0, int), NODE_ARG(1, int)));
}



void
QDateType::load()
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
    
    addSymbols(new Function(c, "__allocate", __allocate, None,
                            Return, ftn,
                            End),

               EndArguments );

addSymbols(
    new Alias(c, "MonthNameType", "int"),
      new SymbolicConstant(c, "DateFormat", "int", Value(int(QDate::DateFormat))),
      new SymbolicConstant(c, "StandaloneFormat", "int", Value(int(QDate::StandaloneFormat))),
    EndArguments);

addSymbols(
    // enums
    // member functions
    new Function(c, "QDate", _n_QDate0, None, Compiled, qt_QDate_QDate_QDate_QDate, Return, "qt.QDate", Parameters, new Param(c, "this", "qt.QDate"), End),
    new Function(c, "QDate", _n_QDate1, None, Compiled, qt_QDate_QDate_QDate_QDate_int_int_int, Return, "qt.QDate", Parameters, new Param(c, "this", "qt.QDate"), new Param(c, "y", "int"), new Param(c, "m", "int"), new Param(c, "d", "int"), End),
    new Function(c, "addDays", _n_addDays0, None, Compiled, qt_QDate_addDays_QDate_QDate_int64, Return, "qt.QDate", Parameters, new Param(c, "this", "qt.QDate"), new Param(c, "ndays", "int64"), End),
    new Function(c, "addMonths", _n_addMonths0, None, Compiled, qt_QDate_addMonths_QDate_QDate_int, Return, "qt.QDate", Parameters, new Param(c, "this", "qt.QDate"), new Param(c, "nmonths", "int"), End),
    new Function(c, "addYears", _n_addYears0, None, Compiled, qt_QDate_addYears_QDate_QDate_int, Return, "qt.QDate", Parameters, new Param(c, "this", "qt.QDate"), new Param(c, "nyears", "int"), End),
    new Function(c, "day", _n_day0, None, Compiled, qt_QDate_day_int_QDate, Return, "int", Parameters, new Param(c, "this", "qt.QDate"), End),
    new Function(c, "dayOfWeek", _n_dayOfWeek0, None, Compiled, qt_QDate_dayOfWeek_int_QDate, Return, "int", Parameters, new Param(c, "this", "qt.QDate"), End),
    new Function(c, "dayOfYear", _n_dayOfYear0, None, Compiled, qt_QDate_dayOfYear_int_QDate, Return, "int", Parameters, new Param(c, "this", "qt.QDate"), End),
    new Function(c, "daysInMonth", _n_daysInMonth0, None, Compiled, qt_QDate_daysInMonth_int_QDate, Return, "int", Parameters, new Param(c, "this", "qt.QDate"), End),
    new Function(c, "daysInYear", _n_daysInYear0, None, Compiled, qt_QDate_daysInYear_int_QDate, Return, "int", Parameters, new Param(c, "this", "qt.QDate"), End),
    new Function(c, "daysTo", _n_daysTo0, None, Compiled, qt_QDate_daysTo_int64_QDate_QDate, Return, "int64", Parameters, new Param(c, "this", "qt.QDate"), new Param(c, "d", "qt.QDate"), End),
    // MISSING: getDate (void; QDate this, "int *" year, "int *" month, "int *" day)
    new Function(c, "isNull", _n_isNull0, None, Compiled, qt_QDate_isNull_bool_QDate, Return, "bool", Parameters, new Param(c, "this", "qt.QDate"), End),
    new Function(c, "isValid", _n_isValid0, None, Compiled, qt_QDate_isValid_bool_QDate, Return, "bool", Parameters, new Param(c, "this", "qt.QDate"), End),
    new Function(c, "month", _n_month0, None, Compiled, qt_QDate_month_int_QDate, Return, "int", Parameters, new Param(c, "this", "qt.QDate"), End),
    new Function(c, "setDate", _n_setDate0, None, Compiled, qt_QDate_setDate_bool_QDate_int_int_int, Return, "bool", Parameters, new Param(c, "this", "qt.QDate"), new Param(c, "year", "int"), new Param(c, "month", "int"), new Param(c, "day", "int"), End),
    new Function(c, "toJulianDay", _n_toJulianDay0, None, Compiled, qt_QDate_toJulianDay_int64_QDate, Return, "int64", Parameters, new Param(c, "this", "qt.QDate"), End),
    new Function(c, "toString", _n_toString0, None, Compiled, qt_QDate_toString_string_QDate_string, Return, "string", Parameters, new Param(c, "this", "qt.QDate"), new Param(c, "format", "string"), End),
    new Function(c, "toString", _n_toString1, None, Compiled, qt_QDate_toString_string_QDate_int, Return, "string", Parameters, new Param(c, "this", "qt.QDate"), new Param(c, "format", "int", Value((int)Qt::TextDate)), End),
    // MISSING: weekNumber (int; QDate this, "int *" yearNumber)
    new Function(c, "year", _n_year0, None, Compiled, qt_QDate_year_int_QDate, Return, "int", Parameters, new Param(c, "this", "qt.QDate"), End),
    // static functions
    new Function(c, "currentDate", _n_currentDate0, None, Compiled, qt_QDate_currentDate_QDate, Return, "qt.QDate", End),
    new Function(c, "fromJulianDay", _n_fromJulianDay0, None, Compiled, qt_QDate_fromJulianDay_QDate_int64, Return, "qt.QDate", Parameters, new Param(c, "jd", "int64"), End),
    new Function(c, "fromString", _n_fromString0, None, Compiled, qt_QDate_fromString_QDate_string_int, Return, "qt.QDate", Parameters, new Param(c, "string", "string"), new Param(c, "format", "int", Value((int)Qt::TextDate)), End),
    new Function(c, "fromString", _n_fromString1, None, Compiled, qt_QDate_fromString_QDate_string_string, Return, "qt.QDate", Parameters, new Param(c, "string", "string"), new Param(c, "format", "string"), End),
    new Function(c, "isLeapYear", _n_isLeapYear0, None, Compiled, qt_QDate_isLeapYear_bool_int, Return, "bool", Parameters, new Param(c, "year", "int"), End),
    new Function(c, "isValid", _n_isValid1, None, Compiled, qt_QDate_isValid_bool_int_int_int, Return, "bool", Parameters, new Param(c, "year", "int"), new Param(c, "month", "int"), new Param(c, "day", "int"), End),
    new Function(c, "longDayName", _n_longDayName0, None, Compiled, qt_QDate_longDayName_string_int_int, Return, "string", Parameters, new Param(c, "weekday", "int"), new Param(c, "type", "int", Value((int)QDate::DateFormat)), End),
    new Function(c, "longMonthName", _n_longMonthName0, None, Compiled, qt_QDate_longMonthName_string_int_int, Return, "string", Parameters, new Param(c, "month", "int"), new Param(c, "type", "int", Value((int)QDate::DateFormat)), End),
    new Function(c, "shortDayName", _n_shortDayName0, None, Compiled, qt_QDate_shortDayName_string_int_int, Return, "string", Parameters, new Param(c, "weekday", "int"), new Param(c, "type", "int", Value((int)QDate::DateFormat)), End),
    new Function(c, "shortMonthName", _n_shortMonthName0, None, Compiled, qt_QDate_shortMonthName_string_int_int, Return, "string", Parameters, new Param(c, "month", "int"), new Param(c, "type", "int", Value((int)QDate::DateFormat)), End),
    EndArguments);
globalScope()->addSymbols(
    new Function(c, "!=", _n_operatorBang_EQ_0, Op, Compiled, qt_QDate_operatorBang_EQ__bool_QDate_QDate, Return, "bool", Parameters, new Param(c, "this", "qt.QDate"), new Param(c, "d", "qt.QDate"), End),
    new Function(c, "<", _n_operatorLT_0, Op, Compiled, qt_QDate_operatorLT__bool_QDate_QDate, Return, "bool", Parameters, new Param(c, "this", "qt.QDate"), new Param(c, "d", "qt.QDate"), End),
    new Function(c, "<=", _n_operatorLT_EQ_0, Op, Compiled, qt_QDate_operatorLT_EQ__bool_QDate_QDate, Return, "bool", Parameters, new Param(c, "this", "qt.QDate"), new Param(c, "d", "qt.QDate"), End),
    new Function(c, "==", _n_operatorEQ_EQ_0, Op, Compiled, qt_QDate_operatorEQ_EQ__bool_QDate_QDate, Return, "bool", Parameters, new Param(c, "this", "qt.QDate"), new Param(c, "d", "qt.QDate"), End),
    new Function(c, ">", _n_operatorGT_0, Op, Compiled, qt_QDate_operatorGT__bool_QDate_QDate, Return, "bool", Parameters, new Param(c, "this", "qt.QDate"), new Param(c, "d", "qt.QDate"), End),
    new Function(c, ">=", _n_operatorGT_EQ_0, Op, Compiled, qt_QDate_operatorGT_EQ__bool_QDate_QDate, Return, "bool", Parameters, new Param(c, "this", "qt.QDate"), new Param(c, "d", "qt.QDate"), End),
    EndArguments);
scope()->addSymbols(
    EndArguments);

}

} // Mu
