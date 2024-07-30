from PySide6.QtCore import QEasingCurve,Signal,QRect,QTimer,QEvent
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QVBoxLayout,QFrame,QWidget

from lib import AnimationOpacityEffect,Animation,Position,IntExcess,Color_,QcolorToStr,OpacityEffect,IsColorStr,BlurEffect

from typing import Union

class MoveFrame(QFrame):
    '''
    frame 动态移动基类

    LoadShow:初次加载是否显示
    EasingCurve:动画曲线,参考函数QEasingCurve
    Duration:动画时间
    '''
    showed=Signal()
    hideed=Signal()
    closed=Signal()
    def __init__(self,
                 LoadShow:bool=True,\
                 EasingCurve:QEasingCurve=QEasingCurve.OutQuad,\
                 Duration:int = 300,\
                 parent=None):
        '''
        LoadShow:窗口加载时是否显示
        EasingCurve:动画曲线
        Duration:动画时间
        '''
        super(MoveFrame,self).__init__(parent=parent) 
        #隐藏关闭功能
        self._hideisclose=False
        #透明状态
        self._opacitystate=LoadShow
        #缓存时间
        self._duration=0

        self.__SetMoveAnimation()
        self.__SetOpacityAnimation(LoadShow)
        self.SetAnimationType(EasingCurve,Duration)
        self.__SetDefaultLayout()
        self.destroyed.connect(self.__SetDestroyedEvent)

    def __SetDestroyedEvent(self):
        if self._opacity._animation.IsRun():
            self._opacity._animation.Stop()
        if self._animation.IsRun():
            self._animation.Stop()

    def __SetDefaultLayout(self):
        self.layouts=QVBoxLayout()
        self.layouts.setSpacing(0)
        self.layouts.setContentsMargins(0,0,0,0)
        self.setLayout(self.layouts)

    def __SetMoveAnimation(self):
        self._movedirection=True
        self._animation=Animation(0)
        self._animation.Animationed.connect(self.__AnimationEvent)
        self._animation._animation.finished.connect(self.__MoveFinished)

    def __SetOpacityAnimation(self,ShowType:bool):
        self._opacity=AnimationOpacityEffect(Show_=ShowType)
        self._opacity._animation._animation.finished.connect(self.__OpacityFinishedEvent)
        self.setGraphicsEffect(self._opacity)

    def SetAnimationType(self,EasingCurve:QEasingCurve=QEasingCurve.OutQuad,Duration:int = 300):
        self._animation._animation.setDuration(Duration)
        self._animation._animation.setEasingCurve(EasingCurve)
        self._opacity._animation._animation.setDuration(Duration)
        self._opacity._animation._animation.setEasingCurve(EasingCurve)
        self._duration=Duration

    def SetHideisClose(self,HideisClose:bool):
        '''
        设置是否隐藏关闭功能
        '''
        self._hideisclose=HideisClose
 
    def Show(self):
        '''
        frame 显示事件
        '''
        #修改显示状态
        self._opacitystate=True
        
        #设置窗口状态
        self.show()
        self.raise_()

        self._opacity.Show()
        
    def Hide(self):
        '''
        frame 隐藏事件
        '''
        #修改显示状态
        self._opacitystate=False

        self._opacity.Hide()

    def Move(self,RectStart:QRect,RectEnd:QRect,OpacityStart:bool,OpacityEnd:bool,MoveMultiple:float=1,MoveDirection:bool=True):
        '''
        frame 移动事件

        RectStart:开始位置
        RectEnd:结束位置
        OpacityStart:开始透明状态
        OpacityEnd:结束透明状态
        Movemultiple:移动偏移,范围1-0.0,如果为0.5,则移动动画从一半的位置开始
        MoveDirection:移动方向,True为正向移动,False为反向移动
        '''
        #计算位置
        self._startrect=self.__RectMultiple(RectStart,RectEnd,MoveMultiple)
        self._endrect=RectEnd
        self._movedirection=MoveMultiple

        if MoveDirection:#正向移动
            self._animation.GoValue(100)
        else:#反向移动
            # self._animation.SetValue(100)
            self._animation.GoValue(0)

        #透明值
        if OpacityStart!=OpacityEnd:
            if OpacityStart:
                self._opacity._animation.SetValue(99)#透明动画值重置
                self._opacity.SetOpacity(0.99)
                self.Hide()
            else:
                self._opacity._animation.SetValue(1)#透明动画值重置
                self._opacity.SetOpacity(0.01)
                self.Show()

    def MovePosition(self,Position_:Position,OpacityStart:bool,OpacityEnd:bool,MoveMultiple:float=1,MoveDirection:bool=True):
        '''
        frame 移动便捷事件
        适用move_frame覆盖整个父窗口进行移动,参考组件轮播图

        Position_:移动位置,参考函数move_position
        OpacityStart:开始透明状态
        OpacityEnd:结束透明状态
        MoveMultiple:移动偏移,范围1-0.0,如果为0.5,则移动动画从一半的位置开始
        MoveDirection:移动方向,True为正向移动,False为反向移动
        '''
        if self.parent() is None:#不存在父窗口不运行
            return
        
        self.setFixedSize(self.parent().size())#同步父窗口大小

        #设置动画时间
        self._animation.SetDuration(self._duration)
        self._opacity._animation.SetDuration(self._duration)

        #计算位置
        if Position_==Position.LEFT:
            x_=-self.width()
            y_=0
        elif Position_==Position.RIGHT:
            x_=self.width()
            y_=0
        elif Position_==Position.TOP:
            x_=0
            y_=-self.height()
        elif Position_==Position.BOTTOM:
            x_=0
            y_=self.height()
        elif Position_==Position.TOP_LEFT or Position_==Position.LEFT_TOP:
            x_=-self.width()
            y_=-self.height()
        elif Position_==Position.TOP_RIGHT or Position_==Position.RIGHT_TOP:
            x_=self.width()
            y_=-self.height()
        elif Position_==Position.BOTTOM_LEFT or Position_==Position.LEFT_BOTTOM:
            x_=-self.width()
            y_=self.height()
        elif Position_==Position.BOTTOM_RIGHT or Position_==Position.RIGHT_BOTTOM:
            x_=self.width()
            y_=self.height()
        elif Position_==Position.CENTER:
            x_=0
            y_=0  
        elif Position_==Position.NONE:
            x_=0
            y_=0

            #设置时间为10ms
            self._animation.SetDuration(10)
            self._opacity._animation.SetDuration(10)
        elif Position_==Position.NOW:
            x_=self.x()
            y_=self.y()

        self.Move(QRect(x_,y_,self.width(),self.height()),QRect(0,0,self.width(),self.height()),OpacityStart,OpacityEnd,MoveMultiple,MoveDirection)

    def __MoveFinished(self):
        '''
        移动动画完成事件
        '''
        self._animation.SetValue(0) if self._movedirection else self._animation.SetValue(100)

    def __RectMultiple(self,RectStart:QRect,RectEnd:QRect,MoveMultiple:float):
        '''
        计算rect类型的偏移位置
        '''
        _m=1-MoveMultiple#倒置
        _temprect=QRect()
        _temprect.setX(RectStart.x()+int((RectEnd.x()-RectStart.x())*_m))
        _temprect.setY(RectStart.y()+int((RectEnd.y()-RectStart.y())*_m))
        _temprect.setWidth(RectStart.width()+int((RectEnd.width()-RectStart.width())*_m))
        _temprect.setHeight(RectStart.height()+int((RectEnd.height()-RectStart.height())*_m))
        return _temprect
      
    def __AnimationEvent(self,value_:int):
        self.move(IntExcess(self._startrect.x(),self._endrect.x(),value_),IntExcess(self._startrect.y(),self._endrect.y(),value_))
        self.setFixedSize(IntExcess(self._startrect.width(),self._endrect.width(),value_),IntExcess(self._startrect.height(),self._endrect.height(),value_))

    def __OpacityFinishedEvent(self):
        '''
        显示隐藏完成事件
        '''
        if self._opacitystate:#显示
            self.showed.emit()
        else:#隐藏
            self.hideed.emit()
            #判断是否关闭窗口
            if self._hideisclose:
                self.closed.emit()
                self.close()
            else:
                self.hide()

class MaskFrame(QFrame):
    '''
    遮罩窗口

    alpha:透明度
    parent:父窗口
    '''
    mousepressed=Signal()
    sizechangeed=Signal()
    def __init__(self,Alpha:int=180,parent=None):
        super(MaskFrame, self).__init__(parent=parent)  

        if self.parent()==None:
            return
             
        #设置窗口属性
        self.setObjectName("windows_mask")
        self.setStyleSheet("QFrame#windows_mask{background:rgba(0,0,0,"+str(Alpha)+")}")

        #平铺父窗口
        self.setGeometry(-100,-100,self.parent().width()+200,self.parent().height()+200) 
        #设置透明特效
        self._opacity = AnimationOpacityEffect(Show_=False)
        self.setGraphicsEffect(self._opacity) 
        #事件
        self._resizeevent=self.parent().resizeEvent
        self.parent().resizeEvent=self.ResizeEvent
        #隐藏窗口
        self.hide()

    def deleteLater(self) -> None:
        self.parent().resizeEvent=self._resizeevent
        return super().deleteLater()

    def SetAnimationType(self,EasingCurve:QEasingCurve=QEasingCurve.OutQuad,Duration:int = 300):
        self._opacity._animation.SetDuration(Duration)
        self._opacity._animation.SetEasingCurve(EasingCurve)

    def Show(self):
        #显示并置顶
        self.show()
        self.raise_()
        #显示
        self._opacity.Show()

    def mousePressEvent(self, event) -> None:
        self.mousepressed.emit()
        return super().mousePressEvent(event)

    def ResizeEvent(self,event):#父窗口大小改变事件
        self.setGeometry(-100,-100,self.parent().width()+200,self.parent().height()+200) 
        self.sizechangeed.emit()
        #事件重新连接
        self._resizeevent(event) 

class CarouselFrame(QFrame):
    '''
    轮播控件

    MovePosition:移动方向,参考函数Position
    Opacity:透明渐变功能,开启会忽略MovePosition参数
    EasingCurve:动画曲线,参考函数QEasingCurve
    Duration:动画时间
    Time:自动轮播时间,0为不自动轮播
    parent:父窗口
    '''
    indexchanged=Signal(int)
    def __init__(self,
                 MovePosition:Position=Position.NONE,
                 Opacity:bool=False,
                 EasingCurve:QEasingCurve=QEasingCurve.InSine,
                 Duration:int=600,
                 Time:int=0,
                 parent=None):
        super(CarouselFrame, self).__init__(parent=parent) 
        self._list=[]#缓存列表
        self._index=0#当前索引
        self._moveposition=MovePosition#移动位置
        self._opacity=Opacity#透明功能

        #加载定时器,自动轮播
        self.auto_=QTimer()
        self.auto_.timeout.connect(self.Next)
        self.SetTime(Time)

        self._moveframe1=MoveFrame(True,EasingCurve,Duration,self)
        self._moveframe2=MoveFrame(True,EasingCurve,Duration,self)
        self._moveframe2._animation._animation.finished.connect(self.__RefreshIndex)

        self._moveframe1.move(0,0)
        self.__MoveFrameSizeFollow()
        self._moveframe2.hide()

    def SetTime(self,Time:int):
        '''
        设置自动轮播时间

        Time:自动轮播时间,0为不自动轮播
        '''
        if Time==0:#不自动轮播
            self._autotime=0
            self.auto_.stop()
        else:#自动轮播
            self._autotime=Time
            self.auto_.start(self._autotime)

    def SetAnimationType(self,EasingCurve:QEasingCurve=QEasingCurve.OutQuad,Duration:int = 600):
        self._moveframe1.SetAnimationType(EasingCurve,Duration)
        self._moveframe2.SetAnimationType(EasingCurve,Duration)

    def AddItem(self,Item:QWidget):
        '''
        添加控件

        Item:任意控件
        '''
        if len(self._list)==0:#第一帧
            Item.setFixedSize(self.size())
            self._moveframe1.layouts.addWidget(Item)
        
        self._list.append(Item)
        
    def Next(self):
        if self._moveframe1._animation.IsRun():
            return 
        
        #刷新轮播
        self.SetTime(self._autotime)
        
        #递增
        index=self._index+1
        if index>len(self._list)-1:#超出范围返回第一个
            index=0
        
        self.__LoadMoveFrame2(index)
        self.__move(True)

        self._index=index
        self.indexchanged.emit(index)

    def Before(self):
        if self._moveframe1._animation.IsRun():
            return
        
        #刷新轮播
        self.SetTime(self._autotime)
        
        #递增
        index=self._index-1
        if index<0:#超出范围返回最后一个
            index=len(self._list)-1
        
        self.__LoadMoveFrame2(index)
        self.__move(False)

        self._index=index
        self.indexchanged.emit(index)

    def Go(self,Index:int,Position:bool=None):
        '''
        Index:控件位置
        Position:移动位置,None为默认,True强制正向移动,False强制反向移动
        '''
        if self._moveframe1._animation.IsRun():
            return
        
        if self._index==Index:#重复不运行
            return
        
        if not self.IsindexRange(Index):#超出范围不运行
            return
        
        #刷新轮播
        self.SetTime(self._autotime)
        
        self.__LoadMoveFrame2(Index)

        if Position!=None:
            self.__move(Position)
        elif Position is None and Index>self._index:
            self.__move(True)
        elif Position is None and Index<self._index:
            self.__move(False)
        

        self._index=Index
        self.indexchanged.emit(Index)

    def IsindexRange(self,Index:int):
        '''
        判断索引是否在范围内
        '''
        if Index<0 or Index>=len(self._list):#超出范围不运行
            return False
        return True

    def __move(self,Direction:bool):
        '''
        移动动画

        Direction:移动方向,True为正向移动,False为反向移动
        '''
        w_=self.width()
        h_=self.height()
        
        move_frame1_start_rect=QRect(0,0,w_,h_)
        move_frame1_end_rect=QRect(0,0,w_,h_)
        move_frame2_start_rect=QRect(0,0,w_,h_)
        move_frame2_end_rect=QRect(0,0,w_,h_)

        def left():
            move_frame1_end_rect.setRect(-w_,0,w_,h_)
            move_frame2_start_rect.setRect(w_,0,w_,h_)
        def right():
            move_frame1_end_rect.setRect(w_,0,w_,h_)
            move_frame2_start_rect.setRect(-w_,0,w_,h_)
        def top():
            move_frame1_end_rect.setRect(0,-h_,w_,h_)
            move_frame2_start_rect.setRect(0,h_,w_,h_)
        def bottom():
            move_frame1_end_rect.setRect(0,h_,w_,h_)
            move_frame2_start_rect.setRect(0,-h_,w_,h_)

        #计算位置
        if self._opacity==False:   
            if self._moveposition==Position.LEFT:
                left() if Direction else right()
            elif self._moveposition==Position.RIGHT:
                right() if Direction else left()
            elif self._moveposition==Position.TOP:
                top() if Direction else bottom()
            elif self._moveposition==Position.BOTTOM:
                bottom() if Direction else top()
            elif self._moveposition==Position.TOP_LEFT or self._moveposition==Position.LEFT_TOP:
                top() if Direction else bottom()
                left() if Direction else top()
            elif self._moveposition==Position.TOP_RIGHT or self._moveposition==Position.RIGHT_TOP:
                top() if Direction else bottom()
                right() if Direction else left()
            elif self._moveposition==Position.BOTTOM_LEFT or self._moveposition==Position.LEFT_BOTTOM:
                bottom() if Direction else top()
                left() if Direction else top()
            elif self._moveposition==Position.BOTTOM_RIGHT or self._moveposition==Position.RIGHT_BOTTOM:
                bottom() if Direction else top()
                right() if Direction else left()
            
            if  self._moveposition==Position.NONE:
                self._moveframe1._animation.SetDuration(10)
                self._moveframe1._opacity._animation.SetDuration(10)
                self._moveframe2._animation.SetDuration(10)
                self._moveframe2._opacity._animation.SetDuration(10)
            else:
                self._moveframe1._animation.SetDuration(self._moveframe1._duration)
                self._moveframe1._opacity._animation.SetDuration(self._moveframe1._duration)
                self._moveframe2._animation.SetDuration(self._moveframe2._duration)
                self._moveframe2._opacity._animation.SetDuration(self._moveframe2._duration)

        self._moveframe1.setGeometry(move_frame1_start_rect)
        self._moveframe2.setGeometry(move_frame2_start_rect)

        self._moveframe1.show()
        self._moveframe2.show()
        self._moveframe2.raise_()#置顶

        self._moveframe1.Move(move_frame1_start_rect,move_frame1_end_rect,True,not self._opacity)
        self._moveframe2.Move(move_frame2_start_rect,move_frame2_end_rect,False,self._opacity)

    def __LoadMoveFrame2(self,Index:int):
        '''
        加载moveframe2
        '''
        if not self.IsindexRange(Index): #超出范围不运行
            return
        
        self._moveframe2.hide()
        
        #移除move_frame2上控件
        for i in range(0,self._moveframe2.layout().count()):
            self._moveframe2.layout().itemAt(i).widget().setParent(None)
        
        widget_=self._list[Index]
        widget_.setFixedSize(self.size())
        self._moveframe2.layouts.addWidget(widget_)
        
    def __RefreshIndex(self):
        '''
        刷新index显示
        '''
        if not self.IsindexRange(self._index):#超出范围不运行
            return
        
        #隐藏move_frame1
        self._moveframe1.hide()

        #移除move_frame1上控件
        for i in range(0,self._moveframe1.layout().count()):
            self._moveframe1.layout().itemAt(i).widget().setParent(None)
        
        #加载控件
        widget_=self._list[self._index]
        widget_.setFixedSize(self.size())
        self._moveframe1.layouts.addWidget(widget_)
        
        #move_frame1参数修改
        self._moveframe1.move(0,0)
        self._moveframe1._opacity.SetOpacity(0.99)
        self._moveframe1.show()

        self._moveframe2.hide()

    def __MoveFrameSizeFollow(self):
        '''
        跟随父窗口大小变化
        '''
        self._moveframe1.setFixedSize(self.width(),self.height())
        self._moveframe2.setFixedSize(self.width(),self.height())

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__MoveFrameSizeFollow()
        return super().resizeEvent(event)
    
class ColorFrame(QFrame):
    '''
    颜色窗口

    color:颜色
    parent:父窗口
    '''
    def __init__(self,Color:Color_,parent=None):
        super(ColorFrame, self).__init__(parent=parent)
        self.SetColor(Color)

    def SetColor(self,Color:Color_):
        '''
        设置颜色
        '''
        self.setStyleSheet(f"background-color: rgba("+QcolorToStr(Color.GetColor())+");")

class BackgroundFrame(QFrame):
    '''
    背景窗口

    ImageLink:背景,可以是图片路径,也可以是颜色,也可以文本颜色
    Alpha:透明度
    parent:父窗口
    '''
    
    def __init__(self,ImageLink:Union[Color_,str],Blur:int=0,Alpha:int=255,parent=None):
        super(BackgroundFrame, self).__init__(parent=parent)
        self._frame=None
        self._blur=Blur
        self.SetImage(ImageLink)
        self._alphaEffect=OpacityEffect(self.__CalAlpha(Alpha))
        self.setGraphicsEffect(self._alphaEffect)
        self.SetBlur(Blur)
        
    def __CalAlpha(self,Alpha:int=255):
        return 0.01+0.98/255*Alpha

    def SetAlpha(self,Alpha:int=255):
        self._alphaEffect.setOpacity(self.__CalAlpha(Alpha))

    def SetImage(self,ImageLink:Union[Color_,str]):
        from icon import GetLink
        from ..image import ImageView
        import os
        #清除缓存
        if self._frame!=None:
            self._frame.deleteLater()

        _image=""

        if isinstance(ImageLink,Color_):
            _image="color"
        elif isinstance(ImageLink,str):
            if IsColorStr(ImageLink):
                _image="color"
            elif os.path.exists(ImageLink):
                _image="picture"
            elif os.path.exists(GetLink()+"\\picture\\"+ImageLink):
                _image="picture"
            else:
                return
       
        if _image=="color":
            self._frame=ColorFrame(ImageLink,parent=self)
        elif _image=="picture":
            self._frame=ImageView(ImageLink,True,parent=self)
        else:
            return

        #平铺
        self.__ImageMove()

    def SetBlur(self,Blur:int=5):
        '''
        设置模糊
        '''
        if self._frame==None:
            return
        self._blur=Blur
        self._blur=BlurEffect(Blur)
        self._frame.setGraphicsEffect(self._blur)

    def __ImageMove(self):
        if self._frame!=None:
            self._frame.move(0,0)
            self._frame.setFixedSize(self.size())

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__ImageMove()
        return super().resizeEvent(event)
    
