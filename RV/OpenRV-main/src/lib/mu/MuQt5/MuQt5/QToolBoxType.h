//
// Copyright (c) 2009, Jim Hourihan
// All rights reserved.
//
// SPDX-License-Identifier: Apache-2.0 
// 
#ifndef __MuQt5__QToolBoxType__h__
#define __MuQt5__QToolBoxType__h__
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
class MuQt_QToolBox;

//
//  NOTE: file generated by qt2mu.py
//

class QToolBoxType : public Class
{
  public:

    typedef MuQt_QToolBox MuQtType;
    typedef QToolBox QtType;

    //
    //  Constructors
    //

    QToolBoxType(Context* context, 
           const char* name,
           Class* superClass = 0,
           Class* superClass2 = 0);

    virtual ~QToolBoxType();

    static bool isInheritable() { return true; }
    static inline ClassInstance* cachedInstance(const MuQtType*);

    //
    //  Class API
    //

    virtual void load();

    MemberFunction* _func[7];
};

// Inheritable object

class MuQt_QToolBox : public QToolBox
{
  public:
    virtual ~MuQt_QToolBox();
    MuQt_QToolBox(Pointer muobj, const CallEnvironment*, QWidget * parent, Qt::WindowFlags f) ;
  protected:
    virtual void itemInserted(int index) ;
    virtual void itemRemoved(int index) ;
    virtual void changeEvent(QEvent * ev) ;
    virtual bool event(QEvent * e) ;
    virtual void showEvent(QShowEvent * e) ;
  public:
    virtual QSize sizeHint() const;
  protected:
    virtual void paintEvent(QPaintEvent * _p14) ;
  public:
    void itemInserted_pub(int index)  { itemInserted(index); }
    void itemInserted_pub_parent(int index)  { QToolBox::itemInserted(index); }
    void itemRemoved_pub(int index)  { itemRemoved(index); }
    void itemRemoved_pub_parent(int index)  { QToolBox::itemRemoved(index); }
    void changeEvent_pub(QEvent * ev)  { changeEvent(ev); }
    void changeEvent_pub_parent(QEvent * ev)  { QToolBox::changeEvent(ev); }
    bool event_pub(QEvent * e)  { return event(e); }
    bool event_pub_parent(QEvent * e)  { return QToolBox::event(e); }
    void showEvent_pub(QShowEvent * e)  { showEvent(e); }
    void showEvent_pub_parent(QShowEvent * e)  { QToolBox::showEvent(e); }
    void paintEvent_pub(QPaintEvent * _p14)  { paintEvent(_p14); }
    void paintEvent_pub_parent(QPaintEvent * _p14)  { QToolBox::paintEvent(_p14); }
  public:
    const QToolBoxType* _baseType;
    ClassInstance* _obj;
    const CallEnvironment* _env;
};

inline ClassInstance* QToolBoxType::cachedInstance(const QToolBoxType::MuQtType* obj) { return obj->_obj; }

} // Mu

#endif // __MuQt__QToolBoxType__h__
