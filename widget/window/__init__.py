# coding:utf-8
import win32api,win32con,win32gui,sys

from ctypes import cast
from ctypes.wintypes import LPRECT, MSG
from typing import Union

from PySide6.QtCore import Qt,Signal,QSize,QTimer,QPoint
from PySide6.QtGui import  QCursor,QIcon
from PySide6.QtWidgets import QWidget,QFrame,QApplication

from lib import GetThemeImage,Position
from qss import QssPlusClass,Color_,ColorStyle

from .import win32_utils as win_utils
from .win32_utils import Taskbar
from .c_structures import LPNCCALCSIZE_PARAMS
from .window_effect import WindowsWindowEffect
from .titlebar import TitleBar
from ..icon import SvgIcon,Icon
from ..frame import BackgroundFrame
from ..infobar import Info

class UserFrame(QFrame,QssPlusClass):
    def __init__(self, *args, **kwargs):
        super(UserFrame,self).__init__(*args, **kwargs)
        self.QssApply(self,"UserFrame",True,False)

    def Setqss(self):
        self.qss.SetBackgroundColor(Color_(ColorStyle.FullColor,0))

class WindowsFramelessWindow(QWidget):
    BORDER_WIDTH = 5  # 边框宽度,给鼠标拖拉
    sizechanged=Signal()
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("framelesswindow")
        self._isResizeEnabled = True
        self._windowtop=False

        #窗口大小最小值
        self.setMinimumSize(600,550)
        #窗口效果
        self._windowEffect = WindowsWindowEffect(self)
        #背景
        self._backgroundFrame=BackgroundFrame(GetThemeImage())
        #标题
        self._titleBar = TitleBar(self)
        self._titleBar.sizechanged.connect(self.__SizeAdjust)
        self._titleBar.move(0,0)
        self._titleBar.raise_()
        #用户区域
        self.userFrame=UserFrame(self)
        #聚焦查看功能
        self.focustimer = QTimer(self)
        self.focustimer.timeout.connect(self.__CheckFocus)
        #提示
        self._info=Info(Position_=Position.TOP,ShiftPoint=QPoint(10,30),parent=self.userFrame)
   
        #fullsize_margin
        self.fullsize_margin_x=0
        self.fullsize_margin_y=0

        # remove window border
        if not win_utils.isWin7():
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        elif parent:
            self.setWindowFlags(parent.windowFlags() | Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        else:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)

        # add DWM shadow and window animation
        self._windowEffect.addWindowAnimation(self.winId())
        self._windowEffect.setAeroEffect(self.winId())
        self._windowEffect.addShadowEffect(self.winId())
        self._windowEffect.disablesysmenu(self.winId())

        # solve issue #5
        self.windowHandle().screenChanged.connect(self.__onScreenChanged)
    
    def ShowWindow(self):
        if self.isHidden()==True:
            self.show()
        if self.isMinimized():
            self.showNormal()
        if self._windowtop==False:
            self.TopShow()

    def TopEvent(self):
        hWnd = int(self.windowHandle().winId())
        if self._windowtop:
            self._windowtop=False
            self._titleBar.topBtn._icon.Go(0)
            self._titleBar.topBtn.setToolTip("置顶")
            win32gui.SetWindowPos(hWnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)
        else:
            self._windowtop=True
            self._titleBar.topBtn._icon.Go(1)
            self._titleBar.topBtn.setToolTip("取消置顶")
            win32gui.SetWindowPos(hWnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)
    
    def TopShow(self):#置顶显示一次
        if self._windowtop==False:
            hWnd = int(self.windowHandle().winId())
            win32gui.SetWindowPos(hWnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)
            win32gui.SetWindowPos(hWnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)

    def setTitleBar(self, titleBar:QWidget):
        self._titleBar.deleteLater()
        self._titleBar = titleBar
        self._titleBar.setParent(self)
        self._titleBar.move(0,0)
        self._titleBar.raise_()

    def setResizeEnabled(self, isEnabled: bool):
        """ set whether resizing is enabled """
        self._isResizeEnabled = isEnabled

    def resizeEvent(self, e):
        self.__SizeAdjust()
        self.sizechanged.emit()

    def nativeEvent(self, eventType, message):
        """ Handle the Windows message """
        msg = MSG.from_address(message.__int__())
        if not msg.hWnd:
            return False, 0

        if msg.message == win32con.WM_NCHITTEST and self._isResizeEnabled:
            pos = QCursor.pos()
            xPos = pos.x() - self.x()
            yPos = pos.y() - self.y()
            w, h = self.width(), self.height()

            if self.isMaximized():
                _ty = win_utils.getResizeBorderThickness(msg.hWnd, False)
                _tx = win_utils.getResizeBorderThickness(msg.hWnd, True)

                w, h = self.width() + _tx * 2, self.height() + _ty * 2

            bw = 0 if win_utils.isMaximized(msg.hWnd) or win_utils.isFullScreen(msg.hWnd) else self.BORDER_WIDTH
            lx = xPos < bw
            rx = xPos > w - bw
            ty = yPos < bw
            by = yPos > h - bw
            if lx and ty:
                return True, win32con.HTTOPLEFT
            elif rx and by:
                return True, win32con.HTBOTTOMRIGHT
            elif rx and ty:
                return True, win32con.HTTOPRIGHT
            elif lx and by:
                return True, win32con.HTBOTTOMLEFT
            elif ty:
                return True, win32con.HTTOP
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT
        elif msg.message == win32con.WM_NCCALCSIZE:
            if msg.wParam:
                rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
            else:
                rect = cast(msg.lParam, LPRECT).contents

            isMax = win_utils.isMaximized(msg.hWnd)
            isFull = win_utils.isFullScreen(msg.hWnd)

            # adjust the size of client rect
            if isMax and not isFull:
                # thickness = win_utils.getResizeBorderThickness(msg.hWnd)
                # rect.top += thickness
                # rect.left += thickness
                # rect.right -= thickness
                # rect.bottom -= thickness

                ty = win_utils.getResizeBorderThickness(msg.hWnd, False)
                rect.top += ty
                rect.bottom -= ty
                self.fullsize_margin_y=ty
        
                tx = win_utils.getResizeBorderThickness(msg.hWnd, True)
                rect.left += tx
                rect.right -= tx
                self.fullsize_margin_x=tx

            # handle the situation that an auto-hide taskbar is enabled
            if (isMax or isFull) and Taskbar.isAutoHide():
                position = Taskbar.getPosition(msg.hWnd)
                if position == Taskbar.LEFT:
                    rect.top += Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.BOTTOM:
                    rect.bottom -= Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.LEFT:
                    rect.left += Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.RIGHT:
                    rect.right -= Taskbar.AUTO_HIDE_THICKNESS

            result = 0 if not msg.wParam else win32con.WVR_REDRAW
            return True, result

        return super().nativeEvent(eventType, message)

    def __onScreenChanged(self):
        hWnd = int(self.windowHandle().winId())
        win32gui.SetWindowPos(hWnd, None, 0, 0, 0, 0, win32con.SWP_NOMOVE |
                              win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)

    def __SizeAdjust(self):
        r_=self._backgroundFrame._blur
        self._backgroundFrame.move(-r_,-r_)
        self._backgroundFrame.setFixedSize(self.size()+QSize(2*r_,2*r_))

        self._titleBar.move(0,0)
        self.userFrame.move(self._titleBar.x(),self._titleBar.y()+self._titleBar.height())
        
        if self.isMaximized():
            self._titleBar.resize(self.width(), self._titleBar.height())
            self.userFrame.setFixedSize(self._titleBar.width(),self.height()-self._titleBar.height()-self.fullsize_margin_y)
        else:
            self._titleBar.resize(self.width(), self._titleBar.height())
            self.userFrame.setFixedSize(self._titleBar.width(),self.height()-self._titleBar.height())

    def __WindowLevelAdjust(self):#窗口层级调整
        self._backgroundFrame.lower()
        self.userFrame.raise_()
        self._titleBar.raise_()
        #创建时置顶显示
        self.TopShow()

    def showEvent(self, event) -> None:
        self.__WindowLevelAdjust()
        self.sizechanged.emit()
        return super().showEvent(event)

    def setWindowTitle(self, arg__1: str) -> None:
        self._titleBar.title_.setText(arg__1)
        return super().setWindowTitle(arg__1)

    def setWindowIcon(self, Icon:Union[Icon,str]):
        self._titleBar.icon_.SetIcon(Icon)
        icon_=QIcon(SvgIcon(Icon))
        return super().setWindowIcon(icon_)

    # def closeEvent(self, a0) -> None:
    #     self.hide()
    #     a0.ignore()

    def SetCheckFocus(self,check:bool=True):
        if check:
            self.focustimer.start(1000)  # 每100毫秒检查一次焦点
        else:
            self.focustimer.stop()
            
    def __CheckFocus(self):
        current_focus_widget = QApplication.focusWidget()
        if current_focus_widget:
            print(f"Current focus widget: {current_focus_widget}, type: {type(current_focus_widget)}")
