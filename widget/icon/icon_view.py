
from PySide6.QtGui import Qt,QPainter
from PySide6.QtCore import QSize,QEasingCurve
from PySide6.QtWidgets import QLabel,QFrame

from lib import Position,Animation,Range360,ConvenientSet
from qss import Color_
from typing import Union

from ..frame import CarouselFrame
from .svg import SvgIcon,Icon

import os

class IconBase(QLabel):
    '''
    Icon: Icon:内置svg图标,str:svg,icon,png文件路径
    Color:svg颜色
    Size:svg大小
    Angle:svg旋转角度
    parent:父控件
    '''
    def __init__(self,Icon:Union[Icon,str],Color:Color_=None,Size:QSize=QSize(16,16),Angle:int=None,parent=None):
        super(IconBase, self).__init__(parent=parent)
        #缓存变量
        self._color=Color
        self._angle=Angle
        self._iconname=Icon
        self._size=Size

        self._disablecolorfollow=False#disable状态颜色跟随
        self._sizefollow=False#size跟随
        self._pixmap=True

        self.setAlignment(Qt.AlignCenter)

        self.__ReloadIcon()

    def __ReloadIcon(self): 
        self.setPixmap(SvgIcon(self._iconname,self._color,self._angle).getpixmap(self._size))
       
    def GetIconName(self):
        if isinstance(self._iconname,Icon):
            return self._iconname.name
        elif isinstance(self._iconname,str):
            if not os.path.exists(self._iconname):
                return ""
            
            (filepath_, filename_) = os.path.split(self._iconname)
            (name_, suffix_) = os.path.splitext(filename_)

            return name_
        return ""

    def SetIconColorFollow(self,Open:bool=True):
        '''
        图标被disable时颜色是否跟随,开启跟随icon颜色,关闭不跟随
        '''
        self._disablecolorfollow=Open

    def SetSizeFollow(self,Open:bool=True):
        '''
        设置图标是否跟随控件大小,开启跟随控件大小,关闭不跟随
        '''
        self._sizefollow=Open
        self.SetSize(self.size())
  
    def setPixmap(self, arg__1) -> None:
        self._pixmap=arg__1
        return super().setPixmap(arg__1)

    def paintEvent(self, arg__1) -> None:
        if self.isEnabled()==False and self._disablecolorfollow:
            label=self
            label.style().drawItemPixmap(QPainter(label),label.rect(),label.alignment(),self._pixmap)   
            return True
        return super().paintEvent(arg__1)

    def SetIcon(self,Icon:Union[Icon,str]):
        '''
        Icon: Icon:内置svg图标,str:svg,icon,png文件路径
        '''
        self._iconname=Icon
        self.__ReloadIcon()

    def SetColor(self,Color:Color_=None):
        '''
        设置图标颜色
        '''
        self._color=Color
        self.__ReloadIcon()

    def SetAngle(self,Angle:int=None):
        '''
        设置图标旋转角度
        '''
        self._angle=Angle
        self.__ReloadIcon()

    def SetSize(self,Size:QSize=None):
        '''
        设置图标大小
        '''
        self._size=Size
        self.__ReloadIcon()

    def resizeEvent(self, event) -> None:
        if self._sizefollow:
            self.SetSize(self.size())
        return super().resizeEvent(event)

class IconView(QFrame,ConvenientSet):
    '''
    svg浏览

    Icon:2种情况,Icon:内置svg图标,str:svg,icon,png文件路径
    IconColor:svg颜色
    IconSize:svg大小
    IconAngle:svg旋转角度
    parent:父控件
    '''
    def __init__(self,Icon:Union[Icon,str],IconColor:Color_=None,IconSize:QSize=QSize(16,16),IconAngle:int=None,parent=None):
        super(IconView,self).__init__(parent=parent)
        self.Icon=IconBase(Icon,IconColor,IconSize,IconAngle,parent=self)
        self.Icon.setGeometry(0,0,self.width(),self.height())

    def SetIconColorFollow(self,Open:bool=True):
        '''
        图标被disable时颜色是否跟随,开启跟随icon颜色,关闭不跟随
        '''
        self.Icon.SetIconColorFollow(Open)
 
    def SetIcon(self,Icon:Union[Icon,str]):
        '''
        Icon: Icon:内置svg图标,str:svg,icon,png文件路径
        '''
        self.Icon.SetIcon(Icon)

    def SetIconColor(self,IconColor:Color_=None):
        '''
        设置图标颜色,none是原icon颜色
        '''
        self.Icon.SetColor(IconColor)

    def SetIconSize(self,IconSize:QSize):
        '''
        设置图标大小
        '''
        self.Icon.SetSize(IconSize)
        
    def SetIconAngle(self,IconAngle:int):
        '''
        设置图标旋转角度
        '''
        self.Icon.SetAngle(IconAngle)
      
    def resizeEvent(self, event) -> None:
        self.Icon.setGeometry(0,0,self.width(),self.height())
        return super().resizeEvent(event)

    def RotateIcon(self,
                          StartAngel:int=None,
                          EndAngel:int=360,
                          Direction:bool=True,\
                          EasingCurve:QEasingCurve=QEasingCurve.OutQuad,
                          Duration:int=500):
        '''
        图标旋转动画

        StartAngel:开始角度,None为当前角度
        EndAngel:结束角度
        Direction:旋转方向,True顺时针,False逆时针
        EasingCurve:动画曲线
        Duration:动画持续时间
        '''
        self.animation=Animation(0,EasingCurve,Duration)
        self.animation.Animationed.connect(self.SetIconAngle)

        if StartAngel==None:
            _startangle=Range360(self.Icon._angle)
        else:
            _startangle=Range360(StartAngel)

        _endangle=Range360(EndAngel)

        if Direction:
            #判断大小
            if _startangle<_endangle:
                self.animation.SetValue(_startangle)
            else:
                self.animation.SetValue(_startangle-360)
        else:
            if _startangle>_endangle:
                self.animation.SetValue(_startangle)
            else:
                self.animation.SetValue(_startangle+360)
 
        self.animation.GoValue(_endangle)

class IconViews(CarouselFrame,ConvenientSet):
    '''
    svg浏览 轮播
    
    MovePosition:移动方向,参考函数move_position
    Opacity:渐变功能,开启会忽略moveposition参数
    EasingCurve:动画曲线,参考函数QEasingCurve
    Duration:动画时间
    parent:父窗口
    '''
    def __init__(self, 
                 MovePosition:Position=Position.NONE,
                 Opacity:bool=False,
                 EasingCurve:QEasingCurve=QEasingCurve.InSine,
                 Duration:int = 600,
                 parent=None):
        super(IconViews, self).__init__(MovePosition=MovePosition,Opacity=Opacity,EasingCurve=EasingCurve,Duration=Duration,parent=parent) 

    def AddIcon(self,Icon:Union[Icon,str],Color:Color_=None,Size:QSize=QSize(16,16),Angle:int=None):
        '''
        Icon: Icon:内置svg图标,str:svg,icon,png文件路径
        Color:图标颜色
        Size:图标大小
        Angle:图标旋转角度
        '''
        Icon=IconBase(Icon,Color,Size,Angle)
        self.AddItem(Icon)

    def SetIcon(self,Icon:Union[Icon,str],Index:int=None):
        '''
        设置图标名称

        Icon: Icon:内置svg图标,str:svg,icon,png文件路径
        Index:图标索引,必须索引
        '''
        if self.IsindexRange(Index):
            self._list[Index].SetIcon(Icon)

    def SetIconColor(self,IconColor:Color_=None,Index:int=None):
        '''
        设置图标颜色,none是原icon颜色

        IconColor:图标颜色
        Index:图标索引,None是所有图标
        '''
        if Index==None:
            for i in range(len(self._list)):
                self._list[i].SetColor(IconColor)
        else:
            if self.IsindexRange(Index):
                self._list[Index].SetColor(IconColor)

    def SetIconSize(self,IconSize:QSize,Index:int=None):
        '''
        设置图标大小

        IconSize:图标大小
        Index:图标索引,None是所有图标
        '''
        if Index==None:
            for i in range(len(self._list)):
                self._list[i].SetSize(IconSize)
        else:   
            if self.IsindexRange(Index):
                self._list[Index].SetSize(IconSize)
            
    def SetIconAngle(self,IconAngle:int,Index:int=None):
        '''
        设置图标旋转角度

        IconAngle:图标旋转角度
        Index:图标索引,None是所有图标
        '''
        if Index==None:
            for i in range(len(self._list)):
                self._list[i].SetAngle(IconAngle)
        else:
            if self.IsindexRange(Index):
                self._list[Index].SetAngle(IconAngle)

    def SetIconColorFollow(self,IconColorFollow:bool=True,Index:int=None):
        '''
        设置图标被disable时颜色是否跟随

        IconColorFollow:开启跟随icon颜色,关闭不跟随
        Index:图标索引,None是所有图标

        '''
        if Index==None:
            for i in range(len(self._list)):
                self._list[i].SetIconColorFollow(IconColorFollow)
        else:
            if self.IsindexRange(Index):
                self._list[Index].SetIconColorFollow(IconColorFollow)

