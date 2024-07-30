
from PySide6.QtCore import QEasingCurve,Qt,QPoint,QRect,Signal,QTimer,QEvent
from PySide6.QtGui import  QCursor, QMouseEvent,QRegion,QPainterPath,QResizeEvent,QPainter,QPixmap,QFocusEvent
from PySide6.QtWidgets import QFrame,QWidget,QVBoxLayout,QScrollArea,QApplication,QLabel

from qss import Color_,ColorStyle,QssPlusClass,themes
from lib import ShadowEffect,QcolorToStr

from ..frame import MoveFrame
from ..scrollbar import ScrollDelegate
from ..showway import Popup_
from ..image import GetRadiusPath



class ItemFrame(QFrame,QssPlusClass):
    def __init__(self, *args, **kwargs):
        super(ItemFrame, self).__init__(*args, **kwargs)
        self.QssApply(self,"ItemFrame",True,False)
        self.__SetDefaultLayout()

    def Setqss(self):
        self.qss.SetBackgroundColor(Color_(ColorStyle.FullColor,0,FixAlpha=0))
        self.qss.SetBorderRadius(Radius=5)
        return super().Setqss()
    
    def __SetDefaultLayout(self):
        self.layouts=QVBoxLayout()
        self.layouts.setSpacing(0)
        self.layouts.setContentsMargins(0,0,0,0)
        self.setLayout(self.layouts)

    def SetShadow(self,color_:Color_=Color_(ColorStyle.FullColor,30),blurRadius:int=15,offset: QPoint=QPoint(0,2)):
        self._shadow=ShadowEffect(color_,blurRadius,offset)
        self.setGraphicsEffect(self._shadow)

class DragItem(MoveFrame):
    pressed=Signal(QWidget)
    deleted=Signal(QWidget)
    draged=Signal(bool)
    
    def __init__(self,
                 EasingCurve:QEasingCurve=QEasingCurve.OutQuad,\
                 Duration:int = 300,\
                 parent=None):
        super(DragItem, self).__init__(LoadShow=True,EasingCurve=EasingCurve,Duration=Duration,parent=parent)
        self._press=False
        self.__SetLayout()

    def __SetLayout(self):
        self._moveframe=MoveFrame(True,parent=self)
        self._moveframe.layouts.setContentsMargins(4,4,4,4)#间隔给show_frame阴影
        self._showframe=ItemFrame()
        self._showframe.SetShadow(blurRadius=10)
        self._moveframe.layouts.addWidget(self._showframe)

    def AddWidget(self,Widget:QWidget):
        Widget.setFocusPolicy(Qt.NoFocus)
        self._showframe.layouts.addWidget(Widget)

        self._widgetresizeEvent=Widget.resizeEvent
        Widget.resizeEvent=self.__ReSizeEvent

        self._widgetmousePressEvent=Widget.mousePressEvent
        Widget.mousePressEvent=self.__mousePressEvent

        self._widgetmouseReleaseEvent=Widget.mouseReleaseEvent
        Widget.mouseReleaseEvent=self.__mouseReleaseEvent

        Widget.show()
        self.__ReSize()

    def __ReSize(self):
        self._showframe.adjustSize()
        #跟随内容设置大小
        _margin=self._moveframe.layouts.contentsMargins()
        #moveframe大小跟随
        self._moveframe.setFixedSize(self._showframe.width()+_margin.left()+_margin.right(),self._showframe.height()+_margin.top()+_margin.bottom())
        #主窗口大小跟随
        self.setFixedSize(self._moveframe.size()) 

    def __ReSizeEvent(self,event):
        self.__ReSize()
        self._widgetresizeEvent(event)
    
    def __mousePressEvent(self, event):
        self._press=True
        self.pressed.emit(self)
        self._widgetmousePressEvent(event)
        
    def __mouseReleaseEvent(self, event):
        if self._press:
            self.draged.emit(False)

        self._press=False
        self._widgetmouseReleaseEvent(event)
   
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._press:
            self.draged.emit(True)
        return super().mouseMoveEvent(event)
    
    def Delete(self):
        self.deleted.emit(self)

class DragList(QScrollArea):
    draged=Signal()
    def __init__(self,*args, **kwargs):
        super(DragList, self).__init__(*args, **kwargs)
        self._isShow=False  #是否已显示

        self._drag=False   #是否拖动
        self._dragWidget=None  #拖动时按下的item
        self._dragPutWidget=None #拖动时欲将放下的item
        self._dragPosition=None  #欲将放下item的位置,左右判断缓存
        self._dragPopup=None   #拖动弹窗
        self._xSpacing=2  #横向间隔
        self._ySpacing=2  #纵向间隔

        self._rightWidget=None

        self._listMode=False #True:强制横向 False:纵向自动

        self._list=[]  #item缓存列表
        self._listCache=[]  #item缓存备份列表
        self._moveTime=QTimer()
        self._moveTime.timeout.connect(self.__DragMoveEvent)

        self._frame=QWidget()  #显示框架
        self._frame.setObjectName("DragListFrame")

        self._scroll=ScrollDelegate(self)
        self.setWidget(self._frame)

        self._dragSeparate=QFrame(self._frame)
        self._dragSeparate.setFixedWidth(3)
        self._dragSeparate.hide()
        self._dragSeparate.setWindowFlag(Qt.WindowTransparentForInput,True)
        self._dragSeparate.setAttribute(Qt.WA_TransparentForMouseEvents,True)

        self.__SetBackgroundColor()
        themes.colorchanged.connect(self.__SetBackgroundColor)
    
    def Clear(self):
        for item in self._list:
            item.close()
        self._list=[]
        self.__AdjustPos()

    def AddItem(self,Item:DragItem,AdjustPos:bool=True):
        '''
        Item:拖拽项
        AdjustPos:是否调整位置
        '''
        self._list.append(Item)
        Item.setParent(self._frame)
        Item.draged.connect(self.__DragEvent)
        Item.pressed.connect(self.__PressEvent)
        Item.deleted.connect(self.__DeleteItem)

        Item.show()
        if AdjustPos:
            self.__AdjustPos()

    def AddItems(self,Items:list[DragItem],AdjustPos:bool=True):
        '''
        Items:拖拽项列表
        AdjustPos:是否调整位置
        '''
        for item in Items:
            self.AddItem(item,False)
        if AdjustPos:
            self.__AdjustPos()
        
    def InSertIitem(self,Item:DragItem,Index:int):
        self._list.insert(Index,Item)
        self.__AdjustPos()

    def SetSpacing(self,xspacing:int=None,yspacing:int=None):
        if xspacing is None and yspacing is None:
            return
      
        if xspacing is not None:
            self._xSpacing=xspacing

        if yspacing is not None:
            self._ySpacing=yspacing

        self.__AdjustPos()

    def SetListMode(self,ListMode:bool):
        '''
        True:强制横向 False:纵向自动
        '''
        self._listMode=ListMode
        self.__ReSize()
        self.__AdjustPos()

    def SetRightWidget(self,Widget:QWidget=None):
        if self._rightWidget is not None:
            self._rightWidget.deleteLater()

        self._rightWidget=Widget

        if Widget is not None:
            self._rightWidget.setParent(self)
            self._rightWidget.show()
            self._rightWidget.raise_()

        self.__SetBackgroundColor()
        self.__ReSize()
        self.__AdjustPos()

    def resizeEvent(self, arg__1: QResizeEvent) -> None:
        self.__ReSize()
        self.__AdjustPos()
        return super().resizeEvent(arg__1)
    
    def showEvent(self, event) -> None:
        self._isShow=True
        self.__AdjustPos()
        return super().showEvent(event)

    def __AdjustPos(self):
        if self._isShow==False:
            return
        
        #清空备份缓存
        self._listCache=[]
        #宽高度归0
        _width=0
        _height=0
        _y=0
        #临时数组,格式[当前列顶部y坐标,列最大高度,item1，item2....itemx]
        _list=[]
        for item in self._list:
            if _width+item.width()>self._frame.width() and _list!=[] and self._listMode==False:  #超出范围,换行
                #加入缓存
                self._listCache.append([_y,_height,_list])
                #递增参数
                _y+=_height+self._ySpacing
                #还原参数
                _width=0
                _height=0
                _list=[]
        
            #宽度递增
            _width+=item.width()+self._xSpacing

            #高度比较,取出最高高度
            if _height<item.height():
                _height=item.height()

            _list.append(item)

        #最后item加入缓存
        self._listCache.append([_y,_height,_list])

        #移动算法
        for itemlist in self._listCache:
            _y=itemlist[0]
            _x=0
            _height=itemlist[1]
            for item in itemlist[2]:
                _oldRect=QRect(item.x(),item.y(),item.width(),item.height())
                _newRect=QRect(_x,_y+int((_height-item.height())/2),item.width(),item.height())
                item._animation.SetValue(0)
                item.Move(_oldRect,_newRect,True,True,0.2,True)
                _x+=item.width()+self._xSpacing

        
        if self._listMode:
            _width=_x-self._xSpacing
            if _width>=0:
                self._frame.setFixedWidth(_width)
        else:
            self._frame.setFixedHeight(_y+_height)

    def __ReSize(self):
        _rightpadding=0

        if self._rightWidget!=None:
            self._rightWidget.move(self.width()-self._rightWidget.width()-5,int((self.height()-self._rightWidget.height())/2))
            _rightpadding=self._rightWidget.width()+10

        if self._listMode:
            self._frame.setFixedHeight(self.height()-4)
        else:
            self._frame.setFixedWidth(self.width()-2-_rightpadding)

    def __DragEvent(self,Drag:bool):
        if self._drag==Drag:
            return 
    
        self._drag=Drag

        if self._drag:
            self._moveTime.start(30)
            self.DragPopup()
        else:
            self._moveTime.stop()
            self._dragSeparate.hide()
            self._dragPopup=None

            if self._dragPutWidget!=None and self._dragWidget!=None and self._dragPutWidget!=self._dragWidget:
                self._list.remove(self._dragWidget)
                _index=self._list.index(self._dragPutWidget)
                if self._dragPosition:
                    self._list.insert(_index,self._dragWidget)
                elif self._dragPosition==False:
                    self._list.insert(_index+1,self._dragWidget)

            self.draged.emit()
            
            self.__AdjustPos()
                
    def __DragMoveEvent(self):
        _pos=self.mapFromGlobal(QCursor.pos())

        #移动
        if _pos.x()<0:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value()+int(_pos.x()/10))
            self._scroll.hScrollBar.ScrollHandleMove(self.horizontalScrollBar().value())

        if _pos.x()>self.width():
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value()+int((_pos.x()-self.width())/10))
            self._scroll.hScrollBar.ScrollHandleMove(self.horizontalScrollBar().value())

        if _pos.y()<0:
            self.verticalScrollBar().setValue(self.verticalScrollBar().value()+int(_pos.y()/10))
            self._scroll.vScrollBar.ScrollHandleMove(self.verticalScrollBar().value())

        if _pos.y()>self.height():
            self.verticalScrollBar().setValue(self.verticalScrollBar().value()+int((_pos.y()-self.height())/10))
            self._scroll.vScrollBar.ScrollHandleMove(self.verticalScrollBar().value())

        #显示移动位置

        if _pos.x()>0 and _pos.x()<self.width() and _pos.y()>0 and _pos.y()<self.height():
            _posWidget = QApplication.widgetAt(QCursor.pos())

            _widget=None

            try:
                if isinstance(_posWidget,DragItem):
                    _widget=_posWidget
                elif isinstance(_posWidget.parent(),DragItem):
                    _widget=_posWidget.parent()
                elif isinstance(_posWidget.parent().parent(),DragItem):
                    _widget=_posWidget.parent().parent()
                elif isinstance(_posWidget.parent().parent().parent(),DragItem):
                    _widget=_posWidget.parent().parent().parent()
            except:
                pass

            #位置

            if _widget!=None:
                _widgetPos=_widget.mapFromGlobal(QCursor.pos())
                if _widgetPos.x()>_widget.width()/2:
                    self._dragPosition=False
                    self._dragSeparate.move(_widget.x()+_widget.width()-self._dragSeparate.width(),_widget.y())
                else:
                    self._dragPosition=True
                    self._dragSeparate.move(_widget.x()+self._dragSeparate.width()-1,_widget.y())
                
                self._dragSeparate.setFixedHeight(_widget.height())
                self._dragSeparate.raise_()

            #缓存控件
            if _widget!=None and self._dragWidget!=_widget:
                self._dragPutWidget=_widget
            else:
                self._dragPutWidget=None

            #显示
            if _widget!=None and self._dragPutWidget!=None:
                self._dragSeparate.show()
            else:
                self._dragSeparate.hide()
  
        else:
            self._dragPutWidget=None
            self._dragPosition=None
            self._dragSeparate.hide()
      
        #popup

        if self._dragPopup!=None:
            self._dragPopup.Move(QCursor.pos()+QPoint(-10,10),Duration=100)

    def __PressEvent(self,Widget:DragItem):
        self._dragWidget=Widget

    def DragPopup(self):
        pass
        # self._dragPopup=Popup_()
        # self._dragPopup.SetWindowTool()
        # self._dragPopup.SetMousePenetration(True)
        # self._dragPopup._showframe.layouts.addWidget(self._dragWidget._showframe)

        # self._dragPopup.ExecPos(QCursor.pos()+QPoint(-10,10),Duration=100)

    def __DeleteItem(self,Widget:DragItem):
        self._list.remove(Widget)
        Widget.close()
        self.__AdjustPos()

    def __SetBackgroundColor(self): 
        _rightpadding=0

        if self._rightWidget is not None:
            _rightpadding=self._rightWidget.width()+8

        self._dragSeparate.setStyleSheet("QFrame{background:rgba("+QcolorToStr(Color_(ColorStyle.FullColor,80).GetColor())+")}")
        self.setStyleSheet("QWidget#DragListFrame{background:transparent;}"
                           "QScrollArea{background:transparent;"
                           "border:1px solid rgba("+QcolorToStr(Color_(ColorStyle.FullColor,10).GetColor())+");"
                           "border-bottom:1px solid rgba("+QcolorToStr(Color_(ColorStyle.FullColor,20).GetColor())+");"
                           "border-radius:4px;padding-left:2px;padding-top:2px;padding-right:"+str(_rightpadding)+"px;}"
                           "QWidget#scrollAreaWidgetContents{background:transparent;}")
        

