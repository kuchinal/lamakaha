//
// Copyright (c) 2009, Jim Hourihan
// All rights reserved.
//
// SPDX-License-Identifier: Apache-2.0 
// 
#ifndef __MuQt5__QWidgetActionType__h__
#define __MuQt5__QWidgetActionType__h__
#include <iostream>
#include <Mu/Class.h>
#include <Mu/MuProcess.h>
#include <QtCore/QtCore>
#include <QtGui/QtGui>
#include <QtWidgets/QtWidgets>
#include <QtNetwork/QtNetwork>
#include <QtWebEngine/QtWebEngine>
#include <QtWebEngineWidgets/QtWebEngineWidgets>
#include <QtQml/QtQml>
#include <QtQuick/QtQuick>
#include <QtQuickWidgets/QtQuickWidgets>
#include <QtSvg/QtSvg>
#include <MuQt5/Bridge.h>

namespace Mu {
class MuQt_QWidgetAction;

//
//  NOTE: file generated by qt2mu.py
//

class QWidgetActionType : public Class
{
  public:

    typedef MuQt_QWidgetAction MuQtType;
    typedef QWidgetAction QtType;

    //
    //  Constructors
    //

    QWidgetActionType(Context* context, 
           const char* name,
           Class* superClass = 0,
           Class* superClass2 = 0);

    virtual ~QWidgetActionType();

    static bool isInheritable() { return true; }
    static inline ClassInstance* cachedInstance(const MuQtType*);

    //
    //  Class API
    //

    virtual void load();

    MemberFunction* _func[4];
};

// Inheritable object

class MuQt_QWidgetAction : public QWidgetAction
{
  public:
    virtual ~MuQt_QWidgetAction();
    MuQt_QWidgetAction(Pointer muobj, const CallEnvironment*, QObject * parent) ;
  protected:
    virtual QWidget * createWidget(QWidget * parent) ;
    virtual void deleteWidget(QWidget * widget) ;
    virtual bool event(QEvent * event_) ;
    virtual bool eventFilter(QObject * obj, QEvent * event) ;
  public:
    QWidget * createWidget_pub(QWidget * parent)  { return createWidget(parent); }
    QWidget * createWidget_pub_parent(QWidget * parent)  { return QWidgetAction::createWidget(parent); }
    void deleteWidget_pub(QWidget * widget)  { deleteWidget(widget); }
    void deleteWidget_pub_parent(QWidget * widget)  { QWidgetAction::deleteWidget(widget); }
    bool event_pub(QEvent * event_)  { return event(event_); }
    bool event_pub_parent(QEvent * event_)  { return QWidgetAction::event(event_); }
    bool eventFilter_pub(QObject * obj, QEvent * event)  { return eventFilter(obj, event); }
    bool eventFilter_pub_parent(QObject * obj, QEvent * event)  { return QWidgetAction::eventFilter(obj, event); }
  public:
    const QWidgetActionType* _baseType;
    ClassInstance* _obj;
    const CallEnvironment* _env;
};

inline ClassInstance* QWidgetActionType::cachedInstance(const QWidgetActionType::MuQtType* obj) { return obj->_obj; }

} // Mu

#endif // __MuQt__QWidgetActionType__h__
