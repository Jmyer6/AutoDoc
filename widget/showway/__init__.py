
from PySide6.QtCore import QEasingCurve,Qt,QPoint,QRect,Signal,QEventLoop,QObject
from PySide6.QtGui import  QFocusEvent, QGuiApplication,QCursor,QRegion
from PySide6.QtWidgets import QFrame,QWidget,QVBoxLayout

from qss import Color_,ColorStyle,QssPlusClass
from ..frame import MoveFrame,MaskFrame

from lib import Position,Animation,IntExcess,BlurEffect,ConvenientSet,ShadowEffect

class PopupFrame(QFrame,QssPlusClass):
    def __init__(self, *args, **kwargs):
        super(PopupFrame, self).__init__(*args, **kwargs)
        self.QssApply(self,"PopupFrame",False,False)
        self.__SetDefaultLayout()

    def Setqss(self):
        self.qss.SetBackgroundColor(Color_(ColorStyle.FullColor,0))
        self.qss.SetBorderRadius(Radius=5)
        return super().Setqss()
    
    def __SetDefaultLayout(self):
        self.layouts=QVBoxLayout()
        self.layouts.setSpacing(0)
        self.layouts.setContentsMargins(0,0,0,0)
        self.setLayout(self.layouts)

    def set_shadow(self,color_:Color_=Color_(ColorStyle.FullColor,30),blurRadius:int=15,offset: QPoint=QPoint(0,2)):
        self._shadow=ShadowEffect(color_,blurRadius,offset)
        self.setGraphicsEffect(self._shadow)
    
class PopupBase(QFrame,ConvenientSet):
    '''
    弹出窗口基类

    构建基本属性及基本控件框架
    '''
    showed =Signal()
    closed =Signal()
    def __init__(self, *args, **kwargs):
        super(PopupBase, self).__init__(*args, **kwargs)
        #窗口类型
        self._windowtype=None
        #mask
        self.Mask=None
        self._maskwindow=None
        self._maskeffect=None
        #message
        self._msgstop=None
        #窗口属性
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        #布局
        self.__layout()

    def SetWindowNormal(self):
        self._windowtype="normal"

    def SetWindowPopup(self):
        self._windowtype="popup"
     
    def SetWindowTool(self):
        self._windowtype="tool"
 
    def SetWindowMessage(self):
        self._windowtype="message"
 
    def SetMask(self,Object:QWidget,Blure:int=0):
        '''
        object_:遮罩显示控件
        blure:遮罩显示控件模糊半径
        '''
        self.Mask=MaskFrame(parent=Object)

        if Blure==0:
            self._maskwindow=None
        else:
            self._maskwindow=Object
            self._maskeffect=BlurEffect(Blure)
            Object.setGraphicsEffect(self._maskeffect)

    def __layout(self):
        '''
        结构如下,阴影不会报错

        Qframe
          |-_moveframe
               |-shadow_frame
        '''
        self._moveframe=MoveFrame(parent=self)
        self._moveframe.layouts.setContentsMargins(5,5,5,5)#间隔给show_frame阴影
        self._showframe=PopupFrame()
        self._moveframe.layouts.addWidget(self._showframe)

    def WindowModeUpdate(self,Mouse:bool=False):
        '''
        Mouse:开启鼠标穿透
        '''
        if self._windowtype=="popup":
            self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
        elif self._windowtype=="tool":
            self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
        elif self._windowtype=="message":
            self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
            self.setWindowModality(Qt.ApplicationModal)

        self.SetMousePenetration(Mouse)
      
    def Close(self,ClosePosition:Position=Position.CENTER,
               EasingCurve:QEasingCurve=QEasingCurve.OutQuad,
               Duration:int=500,
               Opacity:bool=True,
               MoveMultiple:float=0.8,
               HideEvent_=None):#关闭
        '''
        ClosePosition:动画隐藏方向
        EasingCurve:动画类型
        Duration:动画时间
        Opacity:透明效果
        MoveMultiple:位置偏移系数
        HideEvent_:隐藏事件,参数是函数def
        '''
        #重新设置动画参数  
        self._moveframe.SetAnimationType(EasingCurve,Duration)

        #暂停运行
        if self._moveframe._animation.IsRun():
            self._moveframe._animation.Stop()
        else:
            self._moveframe._animation.SetValue(100)

        #事件连接
        self._moveframe._hideisclose=True
        if HideEvent_!=None:
            self._moveframe.hideed.connect(HideEvent_)
        
        #透明
        self._moveframe.MovePosition(ClosePosition,True,not Opacity,MoveMultiple,False)

    def showEvent(self, event) -> None:
        self.showed.emit()
        return super().showEvent(event)

    def closeEvent(self, event) -> None:
        self.closed.emit()
        if self.Mask!=None:
            self.Mask.deleteLater()
            if self._maskwindow!=None:
                self._maskwindow.setGraphicsEffect(None)
        if self._msgstop!=None:
            self._msgstop.exit()
            self._msgstop=None
        return super().closeEvent(event)

class Popup_(PopupBase):
    '''
    弹出窗口

    使用前需要定义窗口类型 setwindows_Popup()/setwindows_Tool()/setwindows_Message()

    show_frame内置Qvboxlayout,使用时需要设置窗口内容 self._showframe.layouts.addWidget(self.content_)

    show_frame可以添加阴影ShadowEffect类,阴影显示范围只有5px,注意控制模糊半径及偏移

    '''
    def __init__(self, *args, **kwargs):
        super(Popup_, self).__init__(*args, **kwargs)
        # self.setStyleSheet("QFrame{background-color:rgba(255,255,0,255)}")

    def __ExecFollow(self,Mouse:bool=False):

        if self._showframe.layouts.count()==0:#没有内容不弹出
            self.close()
        if self._windowtype==None:#窗口没有定义类型不弹出
            self.close()

        #根据窗口类型同步窗口模式
        self.WindowModeUpdate(Mouse)
        
        #跟随内容设置大小
        _margin=self._moveframe.layouts.contentsMargins()
        #自动调整大小
        self._showframe.adjustSize()
        #moveframe大小跟随
        self._moveframe.setFixedSize(self._showframe.width()+_margin.left()+_margin.right(),self._showframe.height()+_margin.top()+_margin.bottom())
        #主窗口大小跟随
        self.setFixedSize(self._moveframe.size()) 

        return _margin

    def __ShowEvent(self,
                 ShowType:Position=Position.TOP,
                 EasingCurve:QEasingCurve=QEasingCurve.OutQuad,
                 Duration:int = 500,
                 Opacity:bool=False,
                 MoveMultiple:float=1):
        """
        每种方式都需要用到弹出,所以封装

        ShowType:动画弹出方向,注意有自动调节情况,使用调节后参数
        EasingCurve:动画类型
        Duration:动画时间
        Opacity:透明加载
        MoveMultiple:位置偏移系数
        """
        
        #显示遮罩
        if self.Mask!=None:
            self.Mask.SetAnimationType(EasingCurve,Duration)
            self.Mask.Show()
        #显示showway
        self.show()
        self._showframe.show()
        self.raise_()
        #重新设置动画参数
        self._moveframe.SetAnimationType(EasingCurve,Duration)
        self._moveframe.MovePosition(ShowType,not Opacity,True,MoveMultiple,True)
  
    def ExecPos(self,
                 ShowPoint:QPoint,
                 MovePosition=Position.BOTTOM_RIGHT,
                 ShowType:Position=Position.TOP,
                 EasingCurve:QEasingCurve=QEasingCurve.OutQuad,
                 Duration:int = 500,
                 Opacity:bool=False,
                 MoveMultiple:float=1,
                 PositionAdjuest:bool=True,
                 Mouse:bool=False):
        '''
        按坐标弹出,当存在父窗口时,坐标是相对父窗口的坐标

        ShowPoint:弹出位置坐标
        MovePosition:控件与坐标的相对位置,默认右下
        ShowType:动画弹出方向
        EasingCurve:动画类型
        Duration:动画时间
        Opacity:透明加载
        MoveMultiple:位置偏移系数
        PositionAdjuest:位置自动调节,弹出位置不足会自动调整show_type位置
        Mouse:鼠标穿透
        '''
        l=self.__ExecFollow(Mouse)
        #判断是否有父窗口
        if self.parent()==None:
            #取坐标所在屏幕
            for window in QGuiApplication.screens():
                rect=window.geometry()
                if ShowPoint.x()>=rect.x() and ShowPoint.x()<=rect.x()+rect.width():
                    break
        else:
            #获取父窗口大小坐标
            ParentRect=self.parent().geometry()
            rect=QRect(0,0,ParentRect.width(),ParentRect.height())
            ShowPoint=QPoint(ShowPoint.x()-ParentRect.x(),ShowPoint.y()-ParentRect.y())
        #更改位置变量
        _positionchange=False
        #根据位置重新计算显示位置
        if MovePosition==Position.LEFT:
            x_=ShowPoint.x()-self.width()+l.right()
            y_=ShowPoint.y()-int(self.height()/2)

            if x_<rect.x():
                _positionchange=True
                x_=ShowPoint.x()-l.left()
            
            if y_<rect.y():
                y_=rect.y()-l.top()
            elif y_+self.height()>rect.y()+rect.height():
                y_=rect.y()+rect.height()-self.height()+l.bottom()
        elif MovePosition==Position.TOP:
            x_=ShowPoint.x()-int(self.width()/2)
            y_=ShowPoint.y()-self.height()+l.bottom()
        
            if x_<rect.x():
                x_=rect.x()-l.left()
            elif x_+self.width()>rect.x()+rect.width():
                x_=rect.x()+rect.width()-self.width()+l.right()

            if y_<rect.y():
                _positionchange=True
                y_=ShowPoint.y()-l.top()
        elif MovePosition==Position.RIGHT:
            x_=ShowPoint.x()-l.left()
            y_=ShowPoint.y()-int(self.height()/2)

            if x_+self.width()>rect.x()+rect.width():
                _positionchange=True
                x_=ShowPoint.x()-self.width()+l.right()
            
            if y_<rect.y():
                y_=rect.y()-l.top()
            elif y_+self.height()>rect.y()+rect.height():
                y_=rect.y()+rect.height()-self.height()+l.bottom()
        elif MovePosition==Position.BOTTOM:
            x_=ShowPoint.x()-int(self.width()/2)
            y_=ShowPoint.y()-l.top()   
        
            if x_<rect.x():
                x_=rect.x()-l.left()
            elif x_+self.width()>rect.x()+rect.width():
                x_=rect.x()+rect.width()-self.width()+l.right()
            
            if y_+self.height()>rect.y()+rect.height():
                _positionchange=True
                y_=ShowPoint.y()-self.height()+l.bottom()      
        elif MovePosition==Position.TOP_LEFT or MovePosition==Position.LEFT_TOP:
            x_=ShowPoint.x()-self.width()+l.right() 
            y_=ShowPoint.y()-self.height()+l.bottom()   
        
            if x_<rect.x():
                x_=rect.y()-l.left()
            if y_<rect.y():
                _positionchange=True
                y_=ShowPoint.y()-l.top()
        elif MovePosition==Position.TOP_RIGHT or MovePosition==Position.RIGHT_TOP:
            x_=ShowPoint.x()-l.left()
            y_=ShowPoint.y()-self.height()+l.bottom()   
        
            if x_+self.width()>rect.x()+rect.width():
                x_=rect.x()+rect.width()-self.width()+l.right()
            if y_<rect.y():
                _positionchange=True
                y_=ShowPoint.y()-l.top()
        elif MovePosition==Position.BOTTOM_LEFT or MovePosition==Position.LEFT_BOTTOM:
            x_=ShowPoint.x()-self.width()+l.right() 
            y_=ShowPoint.y()-l.top()
        
            if x_<rect.x():
                x_=rect.y()-l.left()
            if y_+self.height()>rect.y()+rect.height():
                _positionchange=True
                y_=ShowPoint.y()-self.height()+l.bottom()  
        elif MovePosition==Position.BOTTOM_RIGHT or MovePosition==Position.RIGHT_BOTTOM:
            x_=ShowPoint.x()-l.left()
            y_=ShowPoint.y()-l.top()   
        
            if x_+self.width()>rect.x()+rect.width():
                x_=rect.x()+rect.width()-self.width()+l.right()
            if y_+self.height()>rect.y()+rect.height():
                _positionchange=True
                y_=ShowPoint.y()-self.height()+l.bottom()  
        elif MovePosition==Position.CENTER:
            x_=ShowPoint.x()-int(self.width()/2)
            y_=ShowPoint.y()-int(self.height()/2)

            if x_<rect.x():
                x_=rect.x()-l.left()
            elif x_+self.width()>rect.x()+rect.width():
                x_=rect.x()+rect.width()-self.width()+l.right()
            
            if y_<rect.y():
                y_=rect.y()-l.top()
            if y_+self.height()>rect.y()+rect.height():
                y_=rect.y()+rect.height()-self.height()+l.bottom()
        #刷新位置
        self.move(QPoint(x_,y_))
        #根据位置是否被更改,修改动画
        _showtype=ShowType
        if PositionAdjuest and _positionchange:
            if MovePosition==Position.LEFT:
                if ShowType==Position.RIGHT:
                    _showtype=Position.LEFT
                elif ShowType==Position.TOP_RIGHT:
                    _showtype=Position.TOP_LEFT
                elif ShowType==Position.BOTTOM_RIGHT:
                    _showtype=Position.TOP_RIGHT
            elif MovePosition==Position.TOP or MovePosition==Position.TOP_LEFT or MovePosition==Position.TOP_RIGHT:
                if ShowType==Position.BOTTOM:
                    _showtype=Position.TOP
                elif ShowType==Position.BOTTOM_LEFT:
                    _showtype=Position.TOP_LEFT
                elif ShowType==Position.BOTTOM_RIGHT:
                    _showtype=Position.TOP_RIGHT
            elif MovePosition==Position.RIGHT:
                if ShowType==Position.LEFT:
                    _showtype=Position.RIGHT
                elif ShowType==Position.TOP_LEFT:
                    _showtype=Position.TOP_RIGHT
                elif ShowType==Position.BOTTOM_LEFT:
                    _showtype=Position.BOTTOM_RIGHT
            elif MovePosition==Position.BOTTOM or MovePosition==Position.BOTTOM_LEFT or MovePosition==Position.BOTTOM_RIGHT:
                if ShowType==Position.TOP:
                    _showtype=Position.BOTTOM
                elif ShowType==Position.TOP_LEFT:
                    _showtype=Position.BOTTOM_LEFT
                elif ShowType==Position.TOP_RIGHT:
                    _showtype=Position.BOTTOM_RIGHT
        
        self.__ShowEvent(_showtype,EasingCurve,Duration,Opacity,MoveMultiple)
     
    def ExecWindowIn(self,
                     PositionShift:QPoint=QPoint(0,0),
                     MovePosition=Position.BOTTOM_RIGHT,
                     ShowType:Position=Position.TOP,\
                     EasingCurve:QEasingCurve=QEasingCurve.OutQuad,
                     Duration:int=500,
                     Opacity:bool=False,
                     MoveMultiple:float=1,
                     Mouse:bool=False):
        '''
        窗口内部弹出,设置父窗口则在窗口内,没有父窗口就是桌面

        PositionShift:MovePosition位置偏移量
        MovePosition:控件与坐标的相对位置
        ShowType:动画弹出方向
        EasingCurve:动画类型
        Duration:弹出时间
        Opacity:透明加载
        MoveMultiple:位置弹出系数
        Mouse:鼠标穿透
        '''
        #大小跟随
        self.__ExecFollow(Mouse)

        #判断是否有父窗口
        if self.parent()==None:
            #取坐标所在屏幕
            pos_=QCursor.pos()
            for window in QGuiApplication.screens():
                rect=window.availableGeometry()
                if pos_.x()>=rect.x() and pos_.x()<=rect.x()+rect.width():
                    break
        else:    
            parenr_rect=self.parent().geometry()
            rect=QRect(0,0,parenr_rect.width(),parenr_rect.height())

        if MovePosition==Position.LEFT:
            x_=rect.x()+PositionShift.x()
            y_=rect.y()+int((rect.height()-self.height())/2)+PositionShift.y()
        elif MovePosition==Position.TOP:
            x_=rect.x()+int((rect.width()-self.width())/2)+PositionShift.x()
            y_=rect.y()+PositionShift.y()
        elif MovePosition==Position.RIGHT:
            x_=rect.x()+rect.width()-self.width()-PositionShift.x()
            y_=rect.y()+int((rect.height()-self.height())/2)+PositionShift.y()
        elif MovePosition==Position.BOTTOM:
            x_=rect.x()+int((rect.width()-self.width())/2)+PositionShift.x()
            y_=rect.x()+rect.height()-self.height()-PositionShift.y()
        elif MovePosition==Position.TOP_LEFT or MovePosition==Position.LEFT_TOP:
            x_=rect.x()+PositionShift.x()
            y_=rect.y()+PositionShift.y()
        elif MovePosition==Position.TOP_RIGHT or MovePosition==Position.RIGHT_TOP:
            x_=rect.x()+rect.width()-self.width()-PositionShift.x()
            y_=rect.y()+PositionShift.y()
        elif MovePosition==Position.BOTTOM_LEFT or MovePosition==Position.LEFT_BOTTOM:
            x_=rect.x()+PositionShift.x()
            y_=rect.x()+rect.height()-self.height()-PositionShift.y()
        elif MovePosition==Position.BOTTOM_RIGHT or MovePosition==Position.RIGHT_BOTTOM:
            x_=rect.x()+rect.width()-self.width()-PositionShift.x()
            y_=rect.x()+rect.height()-self.height()-PositionShift.y()
        elif MovePosition==Position.CENTER or MovePosition==Position.NONE:
            x_=rect.x()+int((rect.width()-self.width())/2)+PositionShift.x()
            y_=rect.y()+int((rect.height()-self.height())/2)+PositionShift.y()
        #刷新位置
        self.move(QPoint(x_,y_))

        self.__ShowEvent(ShowType,EasingCurve,Duration,Opacity,MoveMultiple)
     
    def ExecWindowOut(self,
                      Widget:QWidget=None,
                      PointShift:QPoint=QPoint(0,0),
                      MovePosition=Position.BOTTOM_RIGHT,
                      ShowType:Position=Position.TOP,
                      EasingCurve:QEasingCurve=QEasingCurve.OutQuad,
                      Duration:int=500,
                      Opacity:bool=False,
                      MoveMultiple:float=1,
                      PositionAdjuest:bool=True,
                      Mouse:bool=False):
        '''
        窗口及控件外弹出,不支持父窗口,如存在父窗口会取消父窗口
        MovePosition=Position.NONE:#桌面居中
        
        Widget:窗口或控件
        PointShift:MovePosition位置偏移量
        MovePosition:控件与坐标的相对位置
        ShowType:动画弹出方向
        EasingCurve:动画类型
        Duration:弹出时间
        Opacity:透明加载
        MoveMultiple:位置弹出系数
        PositionAdjuest:自动调整ShowType位置,只有相对应情况才会变更
        Mouse:鼠标穿透
        '''
        #大小跟随
        l=self.__ExecFollow(Mouse)
        #取控件所在屏幕
        if Widget==None:#桌面定位
            pos_=QCursor.pos()
            MovePosition=Position.NONE #强制修改弹出类型
        else:#控件定位
            pos_=Widget.mapToGlobal(QPoint(0, 0))
            #如控件超出了父控件的显示范围
            _w=Widget.width()
            _h=Widget.height()
            if Widget.parent()!=None:#控件存在父控件
                #计算控件显示范围
                visible_region = QRegion(Widget.geometry()).intersected(Widget.parent().geometry())
                visible_rect = visible_region.boundingRect()
                _w=visible_rect.width()
                _h=visible_rect.height()

        for window in QGuiApplication.screens():
            rect=window.geometry()
            if pos_.x()>=rect.x() and pos_.x()<=rect.x()+rect.width():
                break

        #更改位置变量
        _positionchange=False

        #根据位置重新计算显示位置
        if MovePosition==Position.LEFT:
            x_=pos_.x()-self.width()+l.right()-PointShift.x()
            y_=pos_.y()+int((_h-self.height())/2)+PointShift.y()

            if x_<rect.x():
                _positionchange=True
                x_=pos_.x()+_w-l.left()+PointShift.x()
            
            if y_<rect.y():
                y_=rect.y()-l.top()
            elif y_+self.height()>rect.y()+rect.height():
                y_=rect.y()+rect.height()-self.height()+l.bottom()
        elif MovePosition==Position.TOP:
            x_=pos_.x()+int((_w-self.width())/2)+PointShift.x()
            y_=pos_.y()-self.height()+l.bottom()-PointShift.y()

            if x_<rect.x():
                x_=rect.x()-l.left()
            elif x_+self.width()>rect.x()+rect.width():
                x_=rect.x()+rect.width()-self.width()+l.right()

            if y_<rect.y():
                _positionchange=True
                y_=pos_.y()+_h-l.top()+PointShift.y()
        elif MovePosition==Position.RIGHT:
            x_=pos_.x()+_w-l.left()+PointShift.x()
            y_=pos_.y()+int((_h-self.height())/2)+PointShift.y()

            if x_+self.width()>rect.x()+rect.width():
                _positionchange=True
                x_=pos_.x()-self.width()+l.right()-PointShift.x()
            
            if y_<rect.y():
                y_=rect.y()-l.top()
            elif y_+self.height()>rect.y()+rect.height():
                y_=rect.y()+rect.height()-self.height()+l.bottom()
        elif MovePosition==Position.BOTTOM:
            x_=pos_.x()+int((_w-self.width())/2)+PointShift.x()
            y_=pos_.y()+_h-l.top()+PointShift.y()

            if x_<rect.x():
                x_=rect.x()-l.left()
            elif x_+self.width()>rect.x()+rect.width():
                x_=rect.x()+rect.width()-self.width()+l.right()

            if y_+self.height()>rect.y()+rect.height():
                _positionchange=True
                y_=pos_.y()-self.height()+l.bottom()-PointShift.y()
        elif MovePosition==Position.TOP_LEFT:
            x_=pos_.x()-l.left()+PointShift.x()
            y_=pos_.y()-self.height()+l.bottom()-PointShift.y() 
        
            if x_<rect.x():
                x_=rect.x()-l.left()
            elif x_+self.width()>rect.x()+rect.width():
                x_=rect.x()+rect.width()-self.width()+l.right()

            if y_<rect.y():
                _positionchange=True
                y_=pos_.y()+_h-l.top()+PointShift.y()
        elif MovePosition==Position.TOP_RIGHT:
            x_=pos_.x()+_w-self.width()+l.right()+PointShift.x()
            y_=pos_.y()-self.height()+l.bottom()-PointShift.y() 

            if x_<rect.x():
                x_=rect.x()-l.left()
            elif x_+self.width()>rect.x()+rect.width():
                x_=rect.x()+rect.width()-self.width()+l.right()

            if y_<rect.y():
                _positionchange=True
                y_=pos_.y()+_h-l.top()+PointShift.y()
        elif MovePosition==Position.RIGHT_TOP:
            x_=pos_.x()+_w-l.left()+PointShift.x()
            y_=pos_.y()-l.top()+PointShift.y() 
        
            if x_+self.width()>rect.x()+rect.width():
                _positionchange=True
                x_=pos_.x()-self.width()+l.right()-PointShift.x()
            
            if y_<rect.y():
                y_=rect.y()-l.top()
            elif y_+self.height()>rect.y()+rect.height():
                y_=rect.y()+rect.height()-self.height()+l.bottom()
        elif MovePosition==Position.RIGHT_BOTTOM:
            x_=pos_.x()+_w-l.left()+PointShift.x()
            y_=pos_.y()+_h-self.height()+l.bottom()+PointShift.y() 
        
            if x_+self.width()>rect.x()+rect.width():
                _positionchange=True
                x_=pos_.x()-self.width()+l.right()-PointShift.x()
            
            if y_<rect.y():
                y_=rect.y()-l.top()
            elif y_+self.height()>rect.y()+rect.height():
                y_=rect.y()+rect.height()-self.height()+l.bottom()
        elif MovePosition==Position.BOTTOM_LEFT:
            x_=pos_.x()-l.left()+PointShift.x()
            y_=pos_.y()+_h-l.top()+PointShift.y()
        
            if x_<rect.x():
                x_=rect.x()-l.left()
            elif x_+self.width()>rect.x()+rect.width():
                x_=rect.x()+rect.width()-self.width()+l.right()

            if y_+self.height()>rect.y()+rect.height():
                _positionchange=True
                y_=pos_.y()-self.height()+l.bottom()-PointShift.y()
        elif MovePosition==Position.BOTTOM_RIGHT:
            x_=pos_.x()+_w-self.width()+l.right()+PointShift.x()
            y_=pos_.y()+_h-l.top()+PointShift.y()

            if x_<rect.x():
                x_=rect.x()-l.left()
            elif x_+self.width()>rect.x()+rect.width():
                x_=rect.x()+rect.width()-self.width()+l.right()

            if y_+self.height()>rect.y()+rect.height():
                _positionchange=True
                y_=pos_.y()-self.height()+l.bottom()-PointShift.y() 
        elif MovePosition==Position.LEFT_TOP:
            x_=pos_.x()-self.width()+l.right()-PointShift.x()
            y_=pos_.y()-l.top()+PointShift.y() 
        
            if x_<rect.x():
                _positionchange=True
                x_=pos_.x()+_w-l.left()+PointShift.x()
            
            if y_<rect.y():
                y_=rect.y()-l.top()
            elif y_+self.height()>rect.y()+rect.height():
                y_=rect.y()+rect.height()-self.height()+l.bottom()
        elif MovePosition==Position.LEFT_BOTTOM:
            x_=pos_.x()-self.width()+l.right()-PointShift.x()
            y_=pos_.y()+_h-self.height()+l.bottom()+PointShift.y() 
        
            if x_<rect.x():
                _positionchange=True
                x_=pos_.x()+_w-l.left()+PointShift.x()
            
            if y_<rect.y():
                y_=rect.y()-l.top()
            elif y_+self.height()>rect.y()+rect.height():
                y_=rect.y()+rect.height()-self.height()+l.bottom()
        elif MovePosition==Position.CENTER:
            x_=pos_.x()+int((_w-self.width())/2)+PointShift.x()
            y_=pos_.y()+int((_h-self.height())/2)+PointShift.y()

            if x_<rect.x():
                x_=rect.x()-l.left()
            elif x_+self.width()>rect.x()+rect.width():
                x_=rect.x()+rect.width()-self.width()+l.right()
            
            if y_<rect.y():
                y_=rect.y()-l.top()
            if y_+self.height()>rect.y()+rect.height():
                y_=rect.y()+rect.height()-self.height()+l.bottom()
        elif MovePosition==Position.NONE:#桌面居中
            x_=rect.x()+int((rect.width()-self.width())/2)+PointShift.x()
            y_=rect.y()+int((rect.height()-self.height())/2)+PointShift.y()

        #刷新位置
        self.move(QPoint(x_,y_))
        #根据位置是否被更改,修改动画
        _showtype=ShowType
        if PositionAdjuest and _positionchange:
            if MovePosition==Position.LEFT or MovePosition==Position.LEFT_TOP or MovePosition==Position.LEFT_BOTTOM:
                if ShowType==Position.RIGHT:
                    _showtype=Position.LEFT
                elif ShowType==Position.TOP_RIGHT:
                    _showtype=Position.TOP_LEFT
                elif ShowType==Position.BOTTOM_RIGHT:
                    _showtype=Position.BOTTOM_LEFT
            elif MovePosition==Position.TOP or MovePosition==Position.TOP_LEFT or MovePosition==Position.TOP_RIGHT:
                if ShowType==Position.BOTTOM:
                    _showtype=Position.TOP
                elif ShowType==Position.BOTTOM_LEFT:
                    _showtype=Position.TOP_LEFT
                elif ShowType==Position.BOTTOM_RIGHT:
                    _showtype=Position.TOP_RIGHT
            elif MovePosition==Position.RIGHT or MovePosition==Position.RIGHT_TOP or MovePosition==Position.RIGHT_BOTTOM:
                if ShowType==Position.LEFT:
                    _showtype=Position.RIGHT
                elif ShowType==Position.TOP_LEFT:
                    _showtype=Position.TOP_RIGHT
                elif ShowType==Position.BOTTOM_LEFT:
                    _showtype=Position.BOTTOM_RIGHT
            elif MovePosition==Position.BOTTOM or MovePosition==Position.BOTTOM_LEFT or MovePosition==Position.BOTTOM_RIGHT:
                if ShowType==Position.TOP:
                    _showtype=Position.BOTTOM
                elif ShowType==Position.TOP_LEFT:
                    _showtype=Position.BOTTOM_LEFT
                elif ShowType==Position.TOP_RIGHT:
                    _showtype=Position.BOTTOM_RIGHT
        
        self.__ShowEvent(_showtype,EasingCurve,Duration,Opacity,MoveMultiple)
     
    def Move(self,
             PointNew:QPoint,
             EasingCurve:QEasingCurve=QEasingCurve.OutQuad,
             Duration:int=500,
             FinishedEvent=None):
        '''
        窗口弹出后移动事件

        PointNew:移动到的坐标
        EasingCurve:动画类型
        Duration:动画时间
        FinishedEvent:动画结束事件,参数是函数def
        '''
        self._startpoint=self.pos()
        self._endpoint=PointNew
        self._moveanimation = Animation(0,EasingCurve,Duration)
        self._moveanimation._animation.finished.connect(FinishedEvent)
        self._moveanimation.Animationed.connect(self.__MoveEvent)
        self._moveanimation.GoValue(100)

    def __MoveEvent(self,Value:int):
        """
        坐标移动事件
        """
        self.move(IntExcess(self._startpoint.x(),self._endpoint.x(),Value),\
                  IntExcess(self._startpoint.y(),self._endpoint.y(),Value))

class PopupMessage(Popup_):
    '''
    message类型弹出
    '''
    def __init__(self, *args, **kwargs):
        super(PopupMessage, self).__init__(*args, **kwargs)
        #message阻塞

    def Exec(self,
              Widget:QWidget=None,
              ShowType:Position=Position.TOP,
              EasingCurve:QEasingCurve=QEasingCurve.OutQuad,
              Duration:int=500,
              Opacity:bool=False,
              MoveMultiple:float=0.3,
              Mask:QObject=None):
        '''
        message弹出

        widget:定位窗口或控件,None为桌面
        ShowType:动画弹出方向
        EasingCurve:动画类型
        Duration:弹出时间
        Opacity:透明加载
        MoveMultiple:位置弹出系数
        Mask:遮罩窗口
        '''
        #设置窗口属性
        self.SetWindowMessage()
        #遮罩
        if Mask!=None:
            self.SetMask(Mask)
        #弹出
        self.ExecWindowOut(Widget=Widget,MovePosition=Position.CENTER,ShowType=ShowType,EasingCurve=EasingCurve,Duration=Duration,Opacity=Opacity,MoveMultiple=MoveMultiple)
        #锁死进程，等待按键
        self._msgstop=QEventLoop()
        self._msgstop.exec()

class PopupInfo(Popup_):
    '''
    infobar 类型弹出
    '''
    def __init__(self, *args, **kwargs):
        super(PopupInfo, self).__init__(*args, **kwargs)

    def Exec(self,
              y_:int,
              MovePosition:Position=Position.TOP,
              easingCurves_:QEasingCurve=QEasingCurve.OutQuad,
              Duration:int=500,
              Opacity:bool=False,
              MoveMultiple:float=1,
              ShiftPoint:QPoint=QPoint(0,0),
              Mouse:bool=False):
        '''
        y_:纵向坐标点
        MovePosition:弹出位置
        show_time_:弹出时间
        easingCurves_:动画类型
        Opacity:透明加载
        MoveMultiple:位置弹出系数
        shift_:位置偏移
        Mouse:鼠标穿透
        '''
        #类型弹出调整
        if MovePosition== Position.TOP or MovePosition== Position.TOP_LEFT or \
                MovePosition== Position.TOP_RIGHT or MovePosition== Position.LEFT_TOP or \
                MovePosition== Position.RIGHT_TOP: 
                ShowType=Position.TOP
        elif MovePosition== Position.BOTTOM or MovePosition== Position.BOTTOM_LEFT or \
                MovePosition== Position.BOTTOM_RIGHT or MovePosition== Position.LEFT_BOTTOM or \
                MovePosition== Position.RIGHT_BOTTOM: 
                ShowType=Position.BOTTOM
        else:
            ShowType=MovePosition

        #弹出
        self.ExecWindowIn(QPoint(ShiftPoint.x(),ShiftPoint.y()+y_),MovePosition,ShowType,easingCurves_,Duration,Opacity,MoveMultiple,Mouse)
