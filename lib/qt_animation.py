from PySide6.QtCore import QObject,QPropertyAnimation,QEasingCurve,Property,Signal,QPoint,QPointF,QRect,QRectF,QSize,QSizeF
from enum import Enum

DefaultEasingCurve=QEasingCurve.OutQuad
DefaultDuration=500

def SetDefaultEasingCurve(EasingCurve:QEasingCurve=QEasingCurve.OutQuad):
    '''
    设置动画类型,详情参考QEasingCurve
    '''
    global DefaultEasingCurve
    DefaultEasingCurve=EasingCurve

def SetDefaultDuration(Duration:int=500):
    '''
    设置动画运行时间,单位毫秒
    '''
    global DefaultDuration
    DefaultDuration=Duration

class Position(Enum):
    '''
    动画类的移动方向
    '''
    LEFT="left"
    TOP="top"
    RIGHT="right"
    BOTTOM="bottom"
    TOP_LEFT="top_left"
    TOP_RIGHT="top_right"
    RIGHT_TOP="right_top"
    RIGHT_BOTTOM="right_bottom"
    BOTTOM_LEFT="bottom_left"
    BOTTOM_RIGHT="bottom_right"
    LEFT_TOP="left_top"
    LEFT_BOTTOM="left_bottom"
    CENTER="center"
    NONE = "none"
    NOW = "now"

class Animation(QObject):#动画类
    '''
    动画类

    Value:初始值
    EasingCurve:动画类型,详情参考QEasingCurve
    Duration:动画运行时间,单位毫秒
    '''
    Animationed=Signal(int)
    def __init__(self,Value:int=None,EasingCurve:QEasingCurve=DefaultEasingCurve,Duration:int=DefaultDuration):
        super().__init__()
        self._value=Value
        #定义赋值变量
        self._animationvalue=None
        self._animation=QPropertyAnimation(self,b'AnimationValueEvent',easingCurve=EasingCurve,duration=Duration)
        self._animation.valueChanged.connect(self.SetValue)
        self.Animationed.emit(self._animationvalue)

    def SetEasingCurve(self,EasingCurve:QEasingCurve=QEasingCurve.OutQuad):
        '''
        设置动画类型,详情参考QEasingCurve
        '''
        self._animation.setEasingCurve(EasingCurve)

    def SetDuration(self,Duration:int=500):
        '''
        设置动画运行时间,单位毫秒
        '''
        self._animation.setDuration(Duration)

    def SetValue(self,Value:int):
        """
        设置值
        """
        self._value=int(Value)

    def GoValue(self,Value:int):
        """
        移动到目标值,开启动画
        """
        if self._value==None:
            return
        if  isinstance(self._value,int):
            self._animation.stop()
            self._animation.setStartValue(self._value)
            self._animation.setEndValue(Value)
            self._animation.start()
        else:
            return

    def SetLoop(self,count:int=1,MxaValue:int=100):
        '''
        循环目标值,目标值在0-100循环,可使用Stop函数强制停止

        count:次数,-1无限循环
        MxaValue:最大值

        '''
        self._animation.setStartValue(0)
        self._animation.setEndValue(MxaValue)
        self._animation.setLoopCount(count) 
        self._animation.start()

    def Stop(self):
        '''
        强制停止动画
        '''
        self._animation.stop()

    def IsRun(self):
        '''
        返回动画是否正在运行
        '''
        return self._animation.state()==QPropertyAnimation.Running

    def IsStop(self):
        '''
        返回动画是否已经停止
        '''
        return self._animation.state()==QPropertyAnimation.Stopped

    @Property(int)
    def AnimationValueEvent(self):
        return self._animationvalue

    @AnimationValueEvent.setter
    def AnimationValueEvent(self,AnimationValue):
        self._animationvalue =AnimationValue
        self.Animationed.emit(self._animationvalue)

