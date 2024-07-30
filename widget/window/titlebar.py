# coding:utf-8
import sys

from PySide6.QtCore import QEvent, Qt,QSize,Signal
from PySide6.QtGui import QColor, QShowEvent
from PySide6.QtWidgets import QHBoxLayout,QFrame

from ..label import LabelNormal
from ..button import ButtonBase
from ..icon import IconView,Icon

from .win32_utils import WindowsMoveResize as MoveResize

from qss import themes,QssPlusClass,ColorStyle,Color_,BorderStyle
from lib import GetThemeMode,ThemeMode,Position

def startSystemMove(window, globalPos):
    MoveResize.startSystemMove(window, globalPos)

def starSystemResize(window, globalPos, edges):
    MoveResize.starSystemResize(window, globalPos, edges)

class TitleButton(ButtonBase):
    '''
    普通按钮
    '''
    def __init__(self,parent=None):
        super(TitleButton, self).__init__(Text="",objectName="TitleButton",parent=parent)
        self.SetFocusType(0)
        self.setFixedSize(46,32)

    def SetTempLightqss(self):
        self._TempLightqss.SetBorderWidth(Width=0)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.Set_("outline","none")

    def SetTempDarkqss(self):
        self._TempDarkqss.SetBorderWidth(Width=0)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.Set_("outline","none")

    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()

        self._NormalLightqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._NormalLightqss.SetBackgroundColor(Color_(ColorStyle.NullColor,10,Rshift=-10,Bshift=3))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()

        self._HoverLightqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._HoverLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,8,Rshift=-10,Bshift=3))

    def SetPressLightqss(self):
        self._PressLightqss=self._TempLightqss.Copy()

        self._PressLightqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._PressLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,10,Rshift=-10,Bshift=3))

    def SetCheckNormalLightqss(self):
        self._CheckNormalLightqss=self._TempLightqss.Copy()

        self._CheckNormalLightqss.SetColor(Color_(ColorStyle.Light))
        self._CheckNormalLightqss.SetBackgroundColor(Color_(ColorStyle.ThemeColor,100))

    def SetCheckHoverLightqss(self):
        self._CheckHoverLightqss=self._TempLightqss.Copy()

        self._CheckHoverLightqss.SetColor(Color_(ColorStyle.Light))
        self._CheckHoverLightqss.SetBackgroundColor(Color_(ColorStyle.ThemeColor,90))

    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempDarkqss.Copy()

        self._NormalDarkqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._NormalDarkqss.SetBackgroundColor(Color_(ColorStyle.NullColor,10))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempDarkqss.Copy()

        self._HoverDarkqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._HoverDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,10))

    def SetPressDarkqss(self):
        self._PressDarkqss=self._TempDarkqss.Copy()

        self._PressDarkqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._PressDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,10))

    def SetCheckNormalDarkqss(self):
        self._CheckNormalDarkqss=self._TempDarkqss.Copy()

        self._CheckNormalDarkqss.SetColor(Color_(ColorStyle.Dark))
        self._CheckNormalDarkqss.SetBackgroundColor(Color_(ColorStyle.ThemeColor,100))

    def SetCheckHoverDarkqss(self):
        self._CheckHoverDarkqss=self._TempDarkqss.Copy()

        self._CheckHoverDarkqss.SetColor(Color_(ColorStyle.Dark))
        self._CheckHoverDarkqss.SetBackgroundColor(Color_(ColorStyle.ThemeColor,90))

class TitleButtonClose(ButtonBase):
    '''
    普通按钮
    '''
    def __init__(self,parent=None):
        super(TitleButtonClose, self).__init__(Text="",objectName="TitleButtonClose",parent=parent)
        self.SetFocusType(0)
        self.setFixedSize(46,32)

    def SetTempLightqss(self):
        self._TempLightqss.SetBorderWidth(Width=0)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.Set_("outline","none")

    def SetTempDarkqss(self):
        self._TempDarkqss.SetBorderWidth(Width=0)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.Set_("outline","none")

    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()

        self._NormalLightqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._NormalLightqss.SetBackgroundColor(Color_(Color_(ColorStyle.FullColor,0).GetColor(),QColor(255,0,0,255),200,Alpha=0))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()

        self._HoverLightqss.SetColor(Color_(ColorStyle.Light))
        self._HoverLightqss.SetBackgroundColor(Color_(Color_(ColorStyle.FullColor,0).GetColor(),QColor(255,0,0,255),200))

    def SetPressLightqss(self):
        self._PressLightqss=self._TempLightqss.Copy()

        self._PressLightqss.SetColor(Color_(ColorStyle.Light))
        self._PressLightqss.SetBackgroundColor(Color_(Color_(ColorStyle.FullColor,0).GetColor(),QColor(255,0,0,255),200,Alpha=200))

    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempLightqss.Copy()

        self._NormalDarkqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._NormalDarkqss.SetBackgroundColor(Color_(Color_(ColorStyle.FullColor,0).GetColor(),QColor(255,0,0,255),200,Alpha=0))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempLightqss.Copy()

        self._HoverDarkqss.SetColor(Color_(ColorStyle.Light))
        self._HoverDarkqss.SetBackgroundColor(Color_(Color_(ColorStyle.FullColor,0).GetColor(),QColor(255,0,0,255),200))

    def SetPressDarkqss(self):
        self._PressDarkqss=self._TempLightqss.Copy()

        self._PressDarkqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._PressDarkqss.SetBackgroundColor(Color_(Color_(ColorStyle.FullColor,0).GetColor(),QColor(255,0,0,255),200,Alpha=200))
   
class TitleBar(QFrame,QssPlusClass):
    sizechanged=Signal()
    def __init__(self, *args, **kwargs):
        super(TitleBar,self).__init__(*args, **kwargs)
        self.QssApply(self,"TitleBar")
        #设置双击功能
        self._isDoubleClickEnabled = True
        #设置title高度
        self.SetHeight()
        #布局设置
        self.__SetLayout()
        #绑定事件
        self.__EventConnect()
        #事件筛选
        self.window().installEventFilter(self)

    def SetNormalLightqss(self):
        self._NormalLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,0,Rshift=-10,Bshift=3))

    def SetHoverLightqss(self):
        self._HoverLightqss.SetBackgroundColor(Color_(ColorStyle.Color,0,Rshift=-10,Bshift=3))

    def SetPressLightqss(self):
        self._PressLightqss.SetBackgroundColor(Color_(ColorStyle.Color,7,Rshift=-10,Bshift=3))

    def SetNormalDarkqss(self):
        self._NormalDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,0))

    def SetHoverDarkqss(self):
        self._HoverDarkqss.SetBackgroundColor(Color_(ColorStyle.Color,0))

    def SetPressDarkqss(self):
        self._PressDarkqss.SetBackgroundColor(Color_(ColorStyle.Color,5))

    def SetHeight(self,Height_:int=None):
        '''
        设置标题高度,None为32
        '''
        self.setFixedHeight(32) if Height_==None else self.setFixedHeight(Height_)
        self.sizechanged.emit()

    def __SetLayout(self):
        self.icon_=IconView(Icon.icon,IconSize=QSize(20,20))
        self.icon_.setFixedSize(QSize(self.height(),self.height()))
        self.icon_.SetMousePenetration(True)

        self.title_=LabelNormal()

        self.minBtn = TitleButton()
        self.closeBtn = TitleButtonClose()
        self.maxBtn =TitleButton()
        self.themeBtn =TitleButton()
        self.topBtn =TitleButton()
        # self.userBtn=TitleButton()

        self.minBtn.SetIcon_(Icon.minsize,QSize(12,12))
        self.closeBtn.SetIcon_(Icon.close,QSize(16,16))

        self.maxBtn.SetIcons_()
        self.maxBtn.IconsAdd(Icon.maxsize1,QSize(12,12))
        self.maxBtn.IconsAdd(Icon.maxsize2,QSize(12,12))

        self.themeBtn.SetIcons_(MovePosition=Position.TOP)
        self.themeBtn.SetIconClickMove(False)

        self.topBtn.SetIcons_()
        self.topBtn.IconsAdd(Icon.fix1,QSize(14,14))
        self.topBtn.IconsAdd(Icon.fix2,QSize(14,14))
        
        #根据目前主题切换icon
        if GetThemeMode()==ThemeMode.LIGHT:
            self.themeBtn.IconsAdd(Icon.light,QSize(14,14))
            self.themeBtn.IconsAdd(Icon.dark,QSize(14,14))
            self.themeBtn.setToolTip("浅色")
        elif GetThemeMode()==ThemeMode.DARK:
            self.themeBtn.IconsAdd(Icon.dark,QSize(14,14))
            self.themeBtn.IconsAdd(Icon.light,QSize(14,14))
            self.themeBtn.setToolTip("深色")
        else:
            self.themeBtn.hide()
        
        self.closeBtn.setToolTip("关闭")
        self.minBtn.setToolTip("最小化")
        self.maxBtn.setToolTip("最大化")
        self.topBtn.setToolTip("置顶")

        self.layouts=QHBoxLayout()
        self.layouts.setSpacing(0)
        self.layouts.setContentsMargins(3,0,0,0)

        self.layouts.addWidget(self.icon_)
        self.layouts.addWidget(self.title_)
        self.layouts.addStretch(1)
        # self.layouts.addWidget(self.userBtn,alignment=Qt.AlignTop)
        self.layouts.addWidget(self.themeBtn,alignment=Qt.AlignTop)
        self.layouts.addWidget(self.topBtn,alignment=Qt.AlignTop)
        self.layouts.addWidget(self.minBtn,alignment=Qt.AlignTop)
        self.layouts.addWidget(self.maxBtn,alignment=Qt.AlignTop)
        self.layouts.addWidget(self.closeBtn,alignment=Qt.AlignTop)

        self.setLayout(self.layouts)
    
    def __EventConnect(self):
        self.themeBtn.clicked.connect(self.__ThemeChangeEvent)
        self.topBtn.clicked.connect(self.parent().TopEvent)
        self.minBtn.clicked.connect(self.window().showMinimized)
        self.maxBtn.clicked.connect(self.__toggleMaxState)
        self.closeBtn.clicked.connect(self.parent().close)

    def __ThemeChangeEvent(self):
        if self.themeBtn._icon._moveframe1._animation.IsRun():
            return

        if GetThemeMode()==ThemeMode.DARK:
            themes.SetThemeMode(ThemeMode.LIGHT)
            self.themeBtn.setToolTip("深色")
        else:
            themes.SetThemeMode(ThemeMode.DARK)
            self.themeBtn.setToolTip("浅色")
        self.themeBtn._icon.Next()

    def eventFilter(self, obj, e):
        if obj is self.window():
            if e.type() == QEvent.WindowStateChange:
                if self.window().isMaximized():
                    self.maxBtn._icon.Go(1)
                    self.maxBtn.setToolTip("还原")
                else:
                    self.maxBtn._icon.Go(0)
                    self.maxBtn.setToolTip("最大化")
                return False
        return super().eventFilter(obj, e)

    def mouseDoubleClickEvent(self, event):
        if event.button() != Qt.LeftButton or not self._isDoubleClickEnabled:
            return
        self.__toggleMaxState()

    def mouseMoveEvent(self, e):
        if sys.platform != "win32" or not self.canDrag(e.pos()):
            return
        startSystemMove(self.window(), e.globalPos())

    def mousePressEvent(self, e):
        if sys.platform == "win32" or not self.canDrag(e.pos()):
            return
        startSystemMove(self.window(), e.globalPos())

    def __toggleMaxState(self):
        self.window().isMinimized()
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def _isDragRegion(self, pos):
        width = 0
        for button in self.findChildren(ButtonBase):
            if button.isVisible():
                width += button.width()

        return 0 < pos.x() < self.width() - width

    def _hasButtonPressed(self):
        return any(btn.isDown() for btn in self.findChildren(ButtonBase))

    def canDrag(self, pos):
        return self._isDragRegion(pos) and not self._hasButtonPressed()

    def setDoubleClickEnabled(self, isEnabled):
        self._isDoubleClickEnabled = isEnabled

    




