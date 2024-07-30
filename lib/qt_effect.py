from PySide6.QtWidgets import QGraphicsDropShadowEffect,QGraphicsOpacityEffect,QGraphicsBlurEffect
from PySide6.QtCore import QPoint,QEasingCurve
from PySide6.QtGui import QColor

from .qt_color import Color_,QcolorExcess
from .qt_animation import Animation
from .qt_excess import IntExcess,QPointExcess
from qss import themes


class ShadowEffect(QGraphicsDropShadowEffect):#阴影
    '''
    阴影类

    Color:颜色值
    BlurRadius:模糊半径
    offset:偏移
    '''
    def __init__(self,Color:Color_,BlurRadius:int=15,Offset:QPoint=QPoint(0,5)):
        super().__init__()

        self.setBlurRadius(BlurRadius)
        self.setOffset(Offset)
        self._color=Color
        self.__ColorApply()

        #主题变化，颜色刷新显示
        themes.colorchanged.connect(self.__ColorApply)
 
    def __ColorApply(self):
        self.setColor(self._color.GetColor())

class AnimationShadowEffect(QGraphicsDropShadowEffect):#颜色循环变动
    '''
    阴影颜色循环变动,运行add_item加入的阴影item,start开始动画,stop终止动画
    '''
    def __init__(self,EasingCurve:QEasingCurve=QEasingCurve.Linear,Duration:int = 500):
        super().__init__()
        self._shadowlist=[]
        self._curruntitem=0
        self._backupvalue=0

        self._animation=Animation(0,EasingCurve=EasingCurve,Duration=Duration)
        self._animation.Animationed.connect(self.__AnimationEvent)

        #主题变化，颜色刷新显示
        themes.colorchanged.connect(self.__ColorApply)
 
    def __ColorApply(self):
        if self._curruntitem >= len(self._shadowlist):#当前位置大于或等于数据列表不运行
            return
        
        if self._animation.IsRun():#动画正在停止时运行
            self.__SetEffect(self._shadowlist[self._curruntitem][0].GetColor(),self._shadowlist[self._curruntitem][1],self._shadowlist[self._curruntitem][2])

    def __SetEffect(self,Color:QColor,BlurRadius:int,Offset:QPoint):
        '''
        设置阴影效果
        '''
        self.setColor(Color)
        self.setBlurRadius(BlurRadius)
        self.setOffset(Offset)

    def AddItem(self,Color:Color_=None,BlurRadius:int=None,Offset:QPoint=None):
        """
        添加item
        """
        self._shadowlist.append([Color,BlurRadius,Offset])
        self.__ColorApply()

    def Clean(self):
        """
        清空所有item
        """
        self._shadowlist.clear()

    def __AnimationEvent(self,Value:int):
        #获取下一个item的序号
        if Value<self._backupvalue:
            self._curruntitem+=1
            if self._curruntitem>=len(self._shadowlist):#判断是否超出范围
                self._curruntitem=0
                if self._onerun:#只运行一次
                    self.stop()

        self._backupvalue=Value
        
        _nextnumber=self._curruntitem+1
        if _nextnumber>=len(self._shadowlist):#判断是否超出范围
            _nextnumber=0

        #获取当前item的颜色值
        color1=self._shadowlist[self._curruntitem][0].GetColor()
        #获取下一个item的颜色值
        color2=self._shadowlist[_nextnumber][0].GetColor()
        
        self.__SetEffect(QcolorExcess(color1,color2,str(Value)+"%"),\
                         IntExcess(self._shadowlist[self._curruntitem][1],self._shadowlist[_nextnumber][1],Value),\
                         QPointExcess(self._shadowlist[self._curruntitem][2],self._shadowlist[_nextnumber][2],Value))
        
    def Start(self,OneRun:bool=False):
        '''
        开始动画
        OneRun:只运行一次
        '''
        if len(self._shadowlist)<=1:#颜色组小于2个不运行
            return
        
        self._onerun=OneRun
        
        self._animation.SetLoop(-1)

    def Stop(self,Number:int=None):
        '''
        强制终止动画
        Number:终止到第几个item,超出范围不执行,None默认自动完成动画,即item0在过渡到item1效果时被终止会直接完成过渡,即立刻跳转到item1效果。
        '''
        if len(self._shadowlist)<=1:#颜色组小于2个不运行
            return
        
        self._animation.Stop()

        if Number is None:
            #获取下一个item的序号
            _nextnumber=self._curruntitem+1
            if _nextnumber>=len(self._shadowlist):#判断是否超出范围
                _nextnumber=0

            self.__SetEffect(self._shadowlist[_nextnumber][0].GetColor(),self._shadowlist[_nextnumber][1],self._shadowlist[_nextnumber][2])
        else:
            if Number>=len(self._shadowlist):#判断是否超出范围
                return
            
            self.__SetEffect(self._shadowlist[Number][0].GetColor(),self._shadowlist[Number][1],self._shadowlist[Number][2])

class OpacityEffect(QGraphicsOpacityEffect):#透明值
    '''
    透明效果
    qt_bug:不能将透明值设置为完全透明或者完全不透明,所以透明值范围在0.01-0.99之间
    '''
    def __init__(self,Opacity:float=0.99):
        super().__init__()
        self.setOpacity(Opacity)

class BlurEffect(QGraphicsBlurEffect):#模糊
    '''
    模糊效果
    '''
    def __init__(self,BlurRadius:int=5):
        super().__init__()
        self.setBlurRadius(BlurRadius)

class AnimationOpacityEffect(QGraphicsOpacityEffect):#透明值变动
    '''
    透明值变动
    Show_:是否显示,后续根据状态运行show_()或hide_()进行显示或隐藏
    
    qt_bug:不能将透明值设置为完全透明或者完全不透明,所以透明值范围在0.01-0.99之间
    '''
    def __init__(self,EasingCurve:QEasingCurve=QEasingCurve.OutQuad,Duration:int = 500,Show_=True):
        super().__init__()
        if Show_:
            self.setOpacity(0.99)
            self._animation=Animation(99,EasingCurve=EasingCurve,Duration=Duration)
        else:
            self.setOpacity(0.01)
            self._animation=Animation(1,EasingCurve=EasingCurve,Duration=Duration)

        self._animation.Animationed.connect(self.__AnimationEvent)

    def __AnimationEvent(self,Value:int):
        self.setOpacity(float(Value/100))

    def Show(self):
        self._animation.GoValue(99)

    def Hide(self):
        self._animation.GoValue(1)

    def SetOpacity(self,Value:float):
        self._animation.Stop()
        self.setOpacity(Value)


    
     
