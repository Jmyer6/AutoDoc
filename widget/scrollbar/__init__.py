from PySide6.QtCore import Signal,Qt,QSize,QPoint,QTimer,QEvent,QObject,QEasingCurve
from PySide6.QtWidgets import QFrame,QAbstractScrollArea,QAbstractItemView,QListView

from qss import QssPlusClass,BorderStyle,Color_,ColorStyle
from lib import AnimationOpacityEffect,Position,Animation,IntExcess

from ..button import ButtonBase
from ..icon import Icon

class ScrollButton(ButtonBase):
    def __init__(self,parent=None):
        super(ScrollButton, self).__init__(Text="",objectName="ScrollButton",parent=parent)
        self.SetFocusType(0)

    def SetTempLightqss(self):
        self._TempLightqss.SetBorderWidth(Width=0)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBackgroundColor(Color_(ColorStyle.NullColor,100))
        self._TempLightqss.Set_("outline","none")

    def SetTempDarkqss(self):
        self._TempDarkqss.SetBorderWidth(Width=0)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBackgroundColor(Color_(ColorStyle.NullColor,100))
        self._TempDarkqss.Set_("outline","none")

    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()
        self._NormalLightqss.SetColor(Color_(ColorStyle.FullColor,50))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()
        self._HoverLightqss.SetColor(Color_(ColorStyle.FullColor,80))

    def SetPressLightqss(self):
        self._PressLightqss=self._TempLightqss.Copy()
        self._PressLightqss.SetColor(Color_(ColorStyle.FullColor,100))
    
    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempLightqss.Copy()
        self._NormalDarkqss.SetColor(Color_(ColorStyle.FullColor,50))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempLightqss.Copy()
        self._HoverDarkqss.SetColor(Color_(ColorStyle.FullColor,80))

    def SetPressDarkqss(self):
        self._PressDarkqss=self._TempLightqss.Copy()
        self._PressDarkqss.SetColor(Color_(ColorStyle.FullColor,100))

class ScrollHandle(QFrame,QssPlusClass):
    def __init__(self,Orient: Qt.Orientation,parent=None):
        super(ScrollHandle, self).__init__(parent=parent)
        self._orient=Orient
        self.SetInOut(False)
        self.QssApply(self,"ScrollHandle")  

    def SetInOut(self,InOut:bool,EventConnect:bool=False):
        if self._orient==Qt.Vertical and InOut:
            self._radius=3
            self._leftmargin=3
            self._topmargin=1
            self._rightmargin=3
            self._bottommargin=1
        elif self._orient==Qt.Vertical and InOut==False:
            self._radius=1
            self._leftmargin=7
            self._topmargin=1
            self._rightmargin=3
            self._bottommargin=1
        elif self._orient==Qt.Horizontal and InOut:
            self._radius=3
            self._leftmargin=1
            self._topmargin=3
            self._rightmargin=1
            self._bottommargin=3
        elif self._orient==Qt.Horizontal and InOut==False:
            self._radius=1
            self._leftmargin=1
            self._topmargin=7
            self._rightmargin=1
            self._bottommargin=3

        if EventConnect:
            self.SetTempDarkqss()
            self.SetTempLightqss()

            if InOut:
                self._Colorin()
            else:
                self._Colorout()
 
    def SetTempLightqss(self):
        self._TempLightqss.SetBorderWidth(Width=0)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBorderRadius(Radius=self._radius)
        self._TempLightqss.Set_("outline","none")
        self._TempLightqss.SetMargin(MarginLeft=self._leftmargin,\
                                     MarginTop=self._topmargin,\
                                     MarginRight=self._rightmargin,\
                                     MarginBottom=self._bottommargin)

    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()
        self._NormalLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,30,Rshift=-10,Bshift=3))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()
        self._HoverLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,40,Rshift=-10,Bshift=3))

    def SetPressLightqss(self):
        self._PressLightqss=self._TempLightqss.Copy()
        self._PressLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,50,Rshift=-10,Bshift=3))

    def SetTempDarkqss(self):
        self._TempDarkqss.SetBorderWidth(Width=0)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.SetBorderRadius(Radius=3)
        self._TempDarkqss.Set_("outline","none")
        self._TempDarkqss.SetMargin(MarginLeft=self._leftmargin,\
                                     MarginTop=self._topmargin,\
                                     MarginRight=self._rightmargin,\
                                     MarginBottom=self._bottommargin)

    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempDarkqss.Copy()
        self._NormalDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,30))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempDarkqss.Copy()
        self._HoverDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,40))

    def SetPressDarkqss(self):
        self._PressDarkqss=self._TempDarkqss.Copy()
        self._PressDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,50))

class Scroll(QFrame,QssPlusClass):
    '''
    Orient:方向  Qt.Vertical|Qt.Horizontal
    '''

    valuechanged=Signal(int)
    showed=Signal()
    def __init__(self,Orient: Qt.Orientation,parent=None):
        super(Scroll, self).__init__(parent=parent)

        self._orient=Orient #Scroll方向
        self._value=None    #Scroll的值

        self._valuechange=False  #开启后才能触发valuechanged信号
        self._renewvalue=False   #开启后才能触发根据handle计算value值

        self._handleTopPos=None
        self._handlePressPos=None

        self._buttonBefore=None   #前按钮
        self._buttonAfter=None    #后按钮
        self._buttonPressType=None#按钮按下类型
        self._buttonWidth=0       #按钮宽高度
        self._buttonClicktime=100 #按钮按下时间

        self._wheelstep=0   #鼠标滚轮步长

        self._buttonClickThread=QTimer()
        self._buttonClickThread.timeout.connect(self.__ButtonClickThreadEvent)

        self._scrollAnimation=Animation(0,QEasingCurve.OutSine,250)#创建动画
        self._scrollAnimationPos=None
        self._scrollAnimation.Animationed.connect(self.__ScrollAnimationEvent)
        self._scrollAnimation._animation.finished.connect(self.__ScrollAnimationFinishEvent)

        #透明效果
        self._scrollOpacity=AnimationOpacityEffect(Show_=False)
        self.setGraphicsEffect(self._scrollOpacity)

        self.__SetScrollHandle()#设置滑块
        self.__SetScrollBotton()#设置按钮大小及参数
        self.ScrollSizeAdjust()#调整整个滑块大小

        self.parent().installEventFilter(self)#事件注册

        self.QssApply(self,"Scroll",True)  
        self.SetClickFunciton(False)
        self.LoadDelay(100,1000)

        #置顶
        self.raise_()

    def SetTempLightqss(self):
        self._TempLightqss.SetBorderWidth(Width=0)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBorderRadius(Radius=6)

    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()
        self._NormalLightqss.SetBackgroundColor(Color_(ColorStyle.NullColor,10,Rshift=-10,Bshift=3))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()
        self._HoverLightqss.SetBackgroundColor(Color_(ColorStyle.Color,10,Rshift=-10,Bshift=3))

    def SetTempDarkqss(self):
        self._TempDarkqss.SetBorderWidth(Width=0)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.SetBorderRadius(Radius=6)
        self._TempDarkqss.Set_("outline","none")

    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempDarkqss.Copy()
        self._NormalDarkqss.SetBackgroundColor(Color_(ColorStyle.NullColor,10,Rshift=-10,Bshift=3))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempDarkqss.Copy()
        self._HoverDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,10,Rshift=-10,Bshift=3))
    
    #各种计算集合
    def __Cal(self,type_:int):
        """位置计算中心,详情看备注"""
        if self._orient==Qt.Vertical:
            if type_==1:#滑块大小值范围
                return int(self._scrollMaxValue-self._scrollMinValue)
            elif type_==2:#滑块在frame内区间大小
                return int(self.height()-self._buttonWidth*2)
            elif type_==3:#滑块在frame内可移动范围（去除btn和handle）
                return int(self.__Cal(2)-self._scrollHandle.height())
            elif type_==4:#滑块置底位置
                return int(self.__Cal(3)+self._buttonWidth)
            elif type_==5:#根据value计算滑块位置
                if self.__Cal(1)==0:
                    return self._buttonWidth
                return int(self.__Cal(3)/self.__Cal(1)*self._value+self._buttonWidth)
            elif type_==6:#根据滑块位置计算value
                return self._scrollMinValue+int((self._scrollHandle.y()-self._buttonWidth)/self.__Cal(3)*self.__Cal(1))
        else:
            if type_==1:#滑块大小值范围
                return int(self._scrollMaxValue-self._scrollMinValue)
            elif type_==2:#滑块在frame内区间大小
                return int(self.width()-self._buttonWidth*2)
            elif type_==3:#滑块在frame内可移动范围（去除btn和handle）
                return int(self.__Cal(2)-self._scrollHandle.width())
            elif type_==4:#滑块置底位置
                return int(self.__Cal(3)+self._buttonWidth)
            elif type_==5:#根据value计算滑块位置
                if self.__Cal(1)==0:
                    return self._buttonWidth
                return int(self.__Cal(3)/self.__Cal(1)*self._value+self._buttonWidth)
            elif type_==6:#根据滑块位置计算value
                return self._scrollMinValue+int((self._scrollHandle.x()-self._buttonWidth)/self.__Cal(3)*self.__Cal(1))

    #滑块
    def __SetScrollHandle(self,Min_:int=0,Max_:int=100):#设置滑块最大小值
        '''
        Min_:滑块value最小值
        Max_:滑块value最大值
        '''
        self._scrollHandle=ScrollHandle(self._orient,self)

        self.SetScrollValueRange(Min_,Max_)

    def SetScrollValueRange(self,Min_:int=0,Max_:int=100):#设置value最大最小值
        '''
        Min_:滑块value最小值
        Max_:滑块value最大值
        '''
        self._scrollMinValue=Min_
        self._scrollMaxValue=Max_

        #隐藏控件
        if Min_==Max_:
            self.hide()
            return
        
        #限制范围
        if self._value==None or self._value< Min_:
            self._value=Min_
        elif self._value>Max_:
            self._value=Max_
        
        self.__ScrollHandleSizeAdjust()
        self.show()

    def __ScrollHandleSizeAdjust(self):#handle调节size
        s_=self.__Cal(1)
        h_=self.__Cal(2)-s_
        h_=h_ if h_>0 else 0  #限制范围
        if self._orient==Qt.Vertical:
            if s_>0 and h_<50:
                self._scrollHandle.setFixedHeight(50)
            else:
                self._scrollHandle.setFixedHeight(h_)
        else:
            if s_>0 and h_<50:
                self._scrollHandle.setFixedWidth(50)
            else:
                self._scrollHandle.setFixedWidth(h_)

        self.ScrollHandleMove()

    def ScrollHandleMove(self,Value:int=None,Animation:bool=False):#根据value调节滑块位置
        '''
        Value:指定value值,None则根据当前value值
        Animation:是否使用动画

        返回value是否超出范围
        '''
        if self.isHidden():
           return None
        
        if self._valuechange==False:
            self._renewvalue=True
        
        #判断范围是否超出
        _overRange=False
        
        #Value取值
        _value=self._value if Value is None else Value  

        #大小范围判断
        if _value<=self._scrollMinValue:
            if Value is None:
                self._value=self._scrollMinValue
            else:
                _value=self._scrollMinValue
            _overRange=True
        elif _value>=self._scrollMaxValue:
            if Value is None:
                self._value=self._scrollMaxValue
            else:
                _value=self._scrollMaxValue
            _overRange=True

        #计算滑块新位置
        _newpos=self._scrollHandle.pos()
        if self.__Cal(1)==0:
            _pos=self._buttonWidth
        else:
            _pos= int(self.__Cal(3)/self.__Cal(1)*_value+self._buttonWidth)
        _newpos.setY(_pos) if self._orient==Qt.Vertical else  _newpos.setX(_pos)

        #根据是否动画刷新位置
        if Animation:
            self._scrollAnimationPos=_newpos
            self._handleTopPos=self._scrollHandle.pos()
            self._scrollAnimation.SetValue(0)
            self._scrollAnimation.GoValue(100) 
        else:
            self.__HandleMoveRange(_newpos.x(),_newpos.y())
            
            #还原
            if self._valuechange:
                self._valuechange=False

        return _overRange
    
    def __ScrollAnimationEvent(self,value_:int):
        if self._orient==Qt.Vertical and self._scrollAnimationPos==None:
            x_=self._handleTopPos.x()
            y_=IntExcess(self._handleTopPos.y(),self.__Cal(5),value_)
        elif self._orient==Qt.Vertical and self._scrollAnimationPos!=None:
            x_=self._handleTopPos.x()
            y_=IntExcess(self._handleTopPos.y(),self._scrollAnimationPos.y(),value_)
        elif self._orient!=Qt.Vertical and self._scrollAnimationPos==None:
            x_=IntExcess(self._handleTopPos.x(),self.__Cal(5),value_)
            y_=self._handleTopPos.y()
        elif self._orient!=Qt.Vertical and self._scrollAnimationPos!=None:
            x_=IntExcess(self._handleTopPos.x(),self._scrollAnimationPos.x(),value_)
            y_=self._handleTopPos.y()
        self.__HandleMoveRange(x_,y_)

    def __ScrollAnimationFinishEvent(self):
        if self._valuechange:
                self._valuechange=False

    def __HandleMoveRange(self,x_:int,y_:int):#范围控制
        '''
        x_:x坐标
        y_:y坐标
        '''
        if self._orient==Qt.Vertical:
            y_=y_ if y_>self._buttonWidth else self._buttonWidth
            y_=y_ if y_<self.__Cal(4) else self.__Cal(4)
        else:
            x_=x_ if x_>self._buttonWidth else self._buttonWidth
            x_=x_ if x_<self.__Cal(4) else self.__Cal(4)
        self._scrollHandle.move(x_,y_)

        if self._valuechange:
            self.valuechanged.emit(self.__Cal(6))
  
    def __RenewValueFromHandle(self,):#根据handle位置刷新value
        if self.isHidden():
           return
        
        self._value=self.__Cal(6)
        self.valuechanged.emit(self._value)

    def SetValue(self,Value:int,Animation:bool=True):#设置value
        '''
        Animation:移动动画
        '''
        if self.isHidden():
           return False
    
        self._valuechange=True
        self._value=Value

        return self.ScrollHandleMove(None,Animation)

    #按钮
    def __SetScrollBotton(self,Width:int=12):#按钮显示
        '''
        控制显示按钮显示及大小,小于12隐藏

        Width:按钮大小v:高度 h:宽度
        '''
        if Width<12:#
            self._buttonWidth=0

            if self._buttonAfter is not None:
                self._buttonAfter.deleteLater()
                self._buttonAfter=None
            
            if self._buttonBefore is not None:
                self._buttonBefore.deleteLater()
                self._buttonBefore=None
 
            return

        self._buttonWidth=Width

        #创建按钮
        if self._orient==Qt.Vertical:
            self._buttonBefore=ScrollButton(self)
            self._buttonBefore.SetIcon_(Icon.arrow1,QSize(10,10))
            self._buttonBefore.SetIconClickPositon(Position.TOP)

            self._buttonAfter=ScrollButton(self)
            self._buttonAfter.SetIcon_(Icon.arrow1,QSize(10,10),IconAngle=180)
            self._buttonAfter.SetIconClickPositon(Position.BOTTOM)
        else:
            self._buttonBefore=ScrollButton(self)
            self._buttonBefore.SetIcon_(Icon.arrow1,QSize(10,10),IconAngle=270)
            self._buttonBefore.SetIconClickPositon(Position.LEFT)

            self._buttonAfter=ScrollButton(self)
            self._buttonAfter.SetIcon_(Icon.arrow1,QSize(10,10),IconAngle=90)
            self._buttonAfter.SetIconClickPositon(Position.RIGHT)

        #透明效果
        self.scrollBeforeeffect=AnimationOpacityEffect(Show_=False)
        self._buttonBefore.setGraphicsEffect(self.scrollBeforeeffect)
        self.scrollAftereffect=AnimationOpacityEffect(Show_=False)
        self._buttonAfter.setGraphicsEffect(self.scrollAftereffect)

        self._buttonBefore.mousepressed.connect(lambda: self.__ButtonClickEvent(True))
        self._buttonAfter.mousepressed.connect(lambda: self.__ButtonClickEvent(False))
        self._buttonBefore.mousereleaseed.connect(self._buttonClickThread.stop)
        self._buttonAfter.mousereleaseed.connect(self._buttonClickThread.stop)
 
        self.__BottonSizeAdjust()#调整按钮位置
        self.ScrollHandleMove()#重新加载滑块位置

    def __ButtonClickEvent(self,BeforeAfter:bool):#按钮点击事件
        if BeforeAfter:
            self._buttonPressType="up"
        else:   
            self._buttonPressType="down"

        if self._renewvalue:
            self.__RenewValueFromHandle()#根据handle位置刷新value
            self._renewvalue=False

        self._buttonClickThread.start(self._buttonClicktime)

    def __ButtonClickThreadEvent(self):
        _stop=False  #停止标识
        _minstep=17  #最小步长

        if self._buttonPressType=="up":
            _newValue=self._value-self._wheelstep
            if _newValue+_minstep>self._value:
                _newValue=self._value-_minstep
        elif  self._buttonPressType=="down":
            _newValue=self._value+self._wheelstep
            if _newValue-_minstep<self._value:
                _newValue=self._value+_minstep

        _stop=self.SetValue(_newValue)
        if _stop:
            self._buttonClickThread.stop()
 
    def __BottonSizeAdjust(self):
        if self._orient==Qt.Vertical:
            self._buttonBefore.move(0,0)
            self._buttonBefore.setFixedSize(self.width(),self._buttonWidth)
            self._buttonAfter.move(0,self.height()-self._buttonWidth)
            self._buttonAfter.setFixedSize(self.width(),self._buttonWidth)
        else:
            self._buttonBefore.move(0,0)
            self._buttonBefore.setFixedSize(self.height(),self._buttonWidth)
            self._buttonAfter.move(self.width()-self._buttonWidth,0)
            self._buttonAfter.setFixedSize(self.height(),self._buttonWidth)

    def ScrollSizeAdjust(self):#总调节大小
        if self._orient == Qt.Vertical:
            self.resize(12, self.parent().height() - 2)
            self.move(self.parent().width() - 12, 1)
            self._scrollHandle.setFixedWidth(self.width())
        else:
            self.resize(self.parent().width() - 2, 12)
            self.move(1, self.parent().height() - 12)
            self._scrollHandle.setFixedHeight(self.height())

        #计算滑块移动因子
        if self.__Cal(1)==0 or self.height()==0:
            self._wheelstep=0
        elif self.__Cal(1)>self.height():
            self._wheelstep=self.__Cal(1)/self.height()
        else:
            self._wheelstep=self.height()/self.__Cal(1)

        self.__BottonSizeAdjust()
        self.__ScrollHandleSizeAdjust()

    #事件
    def mousePressEvent(self, event):
        if self.isHidden():
           return
        
        self.__HandleMoveFromPos(event.pos())
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if self.isHidden():
           return
        
        self._handlePressPos=None
        return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.isHidden():
           return
        
        if self._handlePressPos!=None:
            self._scrollAnimation.Stop()
            self.__HandleMoveFromPos(event.pos(),False)      
        return super().mouseMoveEvent(event)

    def __HandleMoveStart(self):
        self._scrollAnimation.SetValue(0)
        self._handleTopPos=self._scrollHandle.pos()
        self._scrollAnimation._animation.finished.connect(self.__HandleMoveFinishEvent)

    def __HandleMoveFinishEvent(self):
        self._scrollAnimationPos=None
        self._value=self.__Cal(6)
        self._scrollAnimation._animation.finished.disconnect(self.__HandleMoveFinishEvent)

    def __HandleMoveFromPos(self,Pos:QPoint,Animation_:bool=True):
        self._valuechange=True
        if Animation_:
            if self._orient==Qt.Vertical:
                #分3个区域，按钮上到handle区域、handle区域、handle到按钮下区域
                if Pos.y()>self._buttonWidth and Pos.y()<self._scrollHandle.y():#按钮上到handle区域
                    self.__HandleMoveStart()
                    self._scrollAnimationPos=QPoint(0,Pos.y()-int(self._scrollHandle.height()/2))
                    self._handlePressPos=QPoint(0,int(self._scrollHandle.height()/2))
                    self._scrollAnimation.GoValue(100) 
                elif Pos.y()>self._scrollHandle.y() and Pos.y()<self._scrollHandle.y()+self._scrollHandle.height():#handle区域
                    self._handleTopPos=self._scrollHandle.pos()
                    self._handlePressPos=QPoint(0,Pos.y()-self._scrollHandle.y())
                elif Pos.y()>self._scrollHandle.y()+self._scrollHandle.height() and Pos.y()<self.height()-self._buttonWidth:#handle到按钮下区域
                    self.__HandleMoveStart()
                    self._scrollAnimationPos=QPoint(0,Pos.y()-int(self._scrollHandle.height()/2))
                    self._handlePressPos=QPoint(0,int(self._scrollHandle.height()/2))
                    self._scrollAnimation.GoValue(100) 
            else:
                #分3个区域，按钮上到handle区域、handle区域、handle到按钮下区域
                if Pos.x()>self._buttonWidth and Pos.x()<self._scrollHandle.x():#按钮上到handle区域
                    self.__HandleMoveStart()
                    self._scrollAnimationPos=QPoint(Pos.x()-int(self._scrollHandle.width()/2),0)
                    self._handlePressPos=QPoint(int(self._scrollHandle.width()/2),0)
                    self._scrollAnimation.GoValue(100) 
                elif Pos.x()>self._scrollHandle.x() and Pos.x()<self._scrollHandle.x()+self._scrollHandle.width():#handle区域
                    self._handleTopPos=self._scrollHandle.pos()
                    self._handlePressPos=QPoint(Pos.x()-self._scrollHandle.x(),0)
                elif Pos.x()>self._scrollHandle.x()+self._scrollHandle.width() and Pos.x()<self.width()-self._buttonWidth:#handle到按钮下区域
                    self.__HandleMoveStart()
                    self._scrollAnimationPos=QPoint(Pos.x()-int(self._scrollHandle.width()/2),0)
                    self._handlePressPos=QPoint(int(self._scrollHandle.width()/2),0)
                    self._scrollAnimation.GoValue(100) 
        else:
            if self._orient==Qt.Vertical:
                self._handleTopPos.setY(Pos.y()-self._handlePressPos.y())
            else:
                self._handleTopPos.setX(Pos.x()-self._handlePressPos.x())
            self.__HandleMoveRange(self._handleTopPos.x(),self._handleTopPos.y())
            self.__RenewValueFromHandle()
            
    def wheelEvent(self, event) -> None:
        if self.isHidden():
           return
    
        if self._renewvalue:
            self.__RenewValueFromHandle()#根据handle位置刷新value
            self._renewvalue=False

        if event.angleDelta().y() != 0:
            if event.angleDelta().y()>0:
                self.SetValue(self._value-self._wheelstep*2)
            else:
                self.SetValue(self._value+self._wheelstep*2)
        event.setAccepted(True)
        return super().wheelEvent(event)

    def eventFilter(self, obj, e: QEvent):
        if obj == self.parent() and e.type() == QEvent.Resize:
            self.ScrollSizeAdjust()
        elif obj == self.parent() and e.type() == QEvent.Enter:
            if self._handlePressPos!=None:
                return False
            self._scrollOpacity.Show()
            self.raise_()
        elif obj == self.parent() and e.type() == QEvent.Leave:
            if self._handlePressPos!=None:
                return False
            self._scrollOpacity.Hide()
        e.setAccepted(True)
        return super().eventFilter(obj, e)  

    def _Colorin(self, animation_: bool = True):
        self._scrollHandle.SetInOut(True,True)

        self.scrollBeforeeffect.Show()
        self.scrollAftereffect.Show()
        self.raise_()
        return super()._Colorin(animation_)
    
    def _Colorout(self, animation_: bool = True):
        self._scrollHandle.SetInOut(False,True)

        self.scrollBeforeeffect.Hide()
        self.scrollAftereffect.Hide()
        return super()._Colorout(animation_)

    def showEvent(self, event) -> None:
        if self.isHidden():
           return
        
        self.ScrollHandleMove()#移动handle

        self.showed.emit()
        self.raise_()
        return super().showEvent(event)

class ScrollDelegate(QObject):
    def __init__(self,ScrollArea: QAbstractScrollArea,parent=None):
        super().__init__()
        self._mouseclick=False
        self.ScrollArea=ScrollArea

        if parent==None:
            parent=ScrollArea
        self.vScrollBar = Scroll(Qt.Vertical,parent)
        self.hScrollBar = Scroll(Qt.Horizontal,parent)

        self.vScrollBar.showed.connect(lambda: self.__SetVscrollValueRange(ScrollArea.verticalScrollBar().minimum(),ScrollArea.verticalScrollBar().maximum()))
        self.hScrollBar.showed.connect(lambda: self.__SetHscrollValueRange(ScrollArea.horizontalScrollBar().minimum(),ScrollArea.horizontalScrollBar().maximum()))

        self.vScrollBar.valuechanged.connect(ScrollArea.verticalScrollBar().setValue)
        self.hScrollBar.valuechanged.connect(ScrollArea.horizontalScrollBar().setValue)
        self.ScrollArea.verticalScrollBar().rangeChanged.connect(self.__SetVscrollValueRange)
        self.ScrollArea.horizontalScrollBar().rangeChanged.connect(self.__SetHscrollValueRange)

        if isinstance(ScrollArea, QAbstractItemView):
            ScrollArea.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
            ScrollArea.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        if isinstance(ScrollArea, QListView):
            ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            ScrollArea.horizontalScrollBar().setStyleSheet("QScrollBar:horizontal{height: 0px}")
        else:
            ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        ScrollArea.viewport().installEventFilter(self)

    def eventFilter(self, obj, e: QEvent):
        if e.type() == QEvent.Wheel:
            if e.angleDelta().y() != 0:
                self.vScrollBar.wheelEvent(e)
            e.setAccepted(True)
            return True
        
        #父控件事件
        if e.type() == QEvent.MouseButtonPress:
            self._mouseclick=True
        if e.type() == QEvent.MouseButtonRelease:
            self._mouseclick=False
            
        if e.type() == QEvent.MouseMove:
            if self._mouseclick:
                self.hScrollBar.ScrollHandleMove(self.ScrollArea.horizontalScrollBar().value())
                self.vScrollBar.ScrollHandleMove(self.ScrollArea.verticalScrollBar().value())

        return super().eventFilter(obj, e)

    def __SetVscrollValueRange(self,Min_:int=0,Max_:int=100):
        _value=self.ScrollArea.verticalScrollBar().value()
        self.vScrollBar.SetScrollValueRange(Min_,Max_)
        self.vScrollBar.ScrollHandleMove(_value)

    def __SetHscrollValueRange(self,Min_:int=0,Max_:int=100):
        _value=self.ScrollArea.horizontalScrollBar().value()
        self.hScrollBar.SetScrollValueRange(Min_,Max_)
        self.hScrollBar.ScrollHandleMove(_value)

class VScrollDelegate(QObject):
    def __init__(self,ScrollArea: QAbstractScrollArea,parent=None):
        super().__init__(parent=parent)
        self._mouseclick=False
        self.ScrollArea=ScrollArea

        if parent==None:
            parent=ScrollArea
        self.vScrollBar = Scroll(Qt.Vertical,parent)
    
        self.vScrollBar.showed.connect(lambda: self.__SetVscrollValueRange(ScrollArea.verticalScrollBar().minimum(),ScrollArea.verticalScrollBar().maximum()))
        self.vScrollBar.valuechanged.connect(ScrollArea.verticalScrollBar().setValue)
        self.ScrollArea.verticalScrollBar().rangeChanged.connect(self.__SetVscrollValueRange)

        if isinstance(ScrollArea, QAbstractItemView):
            self.ScrollArea.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
            self.ScrollArea.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
       
        self.ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ScrollArea.horizontalScrollBar().setStyleSheet("QScrollBar:horizontal{height: 0px}")
        
        self.ScrollArea.viewport().installEventFilter(self)

    def eventFilter(self, obj, e: QEvent):
        if e.type() == QEvent.Wheel:
            if e.angleDelta().y() != 0:
                self.vScrollBar.wheelEvent(e)
            e.setAccepted(True)
            return True
        
        #父控件事件
        if e.type() == QEvent.MouseButtonPress:
            self._mouseclick=True
        if e.type() == QEvent.MouseButtonRelease:
            self._mouseclick=False
            
        if e.type() == QEvent.MouseMove:
            if self._mouseclick:
                self.vScrollBar.ScrollHandleMove(self.ScrollArea.verticalScrollBar().value())

        return super().eventFilter(obj, e)

    def __SetVscrollValueRange(self,Min_:int=0,Max_:int=100):
        _value=self.ScrollArea.verticalScrollBar().value()
        self.vScrollBar.SetScrollValueRange(Min_,Max_)
        self.vScrollBar.ScrollHandleMove(_value)
    