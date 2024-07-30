from PySide6.QtWidgets import QWidget,QAbstractButton
from PySide6.QtGui import Qt,QKeySequence,QShortcut
from PySide6.QtCore import QTimer,Signal

class MouseEvent:
    '''
    使用前需要加载mouse_event_load,如需延迟事件需要加载load_delay
    提供qss动画在鼠标进出事件、选中、聚焦、点击事件判断情况
    '''
    mousepressed=Signal()
    mousereleaseed=Signal()
    keypressed=Signal()
    keyreleaseed=Signal()
    mouseined=Signal()
    mouseouted=Signal()
    focusin=Signal()
    focusout=Signal()

    def MouseEventLoad(self,Object:QWidget):
        '''
        Object:控件
        '''
        self._mouse=False #鼠标状态，True为鼠标进入，False为鼠标离开
        self._fouce=False #聚焦状态，True为聚焦，False为未聚焦
        self._check=False #选中状态，True为选中，False为未选中
        self._checkfunction=False #选中功能，True为开启，False为关闭
        self._click=False #点击状态，True为点击，False为未点击
        self._clickfunction=True #点击功能，True为开启，False为关闭
        self._menu=False #菜单状态，True为打开菜单，False为关闭菜单
        self._foucefunction=True #聚焦功能，True为开启，False为关闭
        self._widget=Object #缓存控件
        #延迟事件
        self._mouseindelay=None
        self._mouseoutdelay=None
        self._mousecheckindelay=None
        self._mousecheckoutdelay=None
        self.LoadDelay()
        self.__EeventLoad()

    def __EeventLoad(self):
        self._widgetenterEvent=self._widget.enterEvent
        self._widgetleaveEvent=self._widget.leaveEvent
        self._widgetfocusInEvent=self._widget.focusInEvent
        self._widgetfocusOutEvent=self._widget.focusOutEvent
        self._widgetmousePressEvent=self._widget.mousePressEvent
        self._widgetmouseReleaseEvent=self._widget.mouseReleaseEvent
        self._widgetsetEnabled=self._widget.setEnabled
        self._widgetsetDisabled=self._widget.setDisabled
        self._widgetsetFouce=self._widget.setFocusPolicy
        self._widgetkeyPressEvent=self._widget.keyPressEvent
        self._widgetkeyReleaseEvent=self._widget.keyReleaseEvent

        self._widget.enterEvent=self.__MouseinEvent
        self._widget.leaveEvent=self.__MouseoutEvent
        self._widget.focusInEvent=self.__FocusinEvent
        self._widget.focusOutEvent=self.__FocusoutEvent
        self._widget.mousePressEvent=self.__MousepressEvent
        self._widget.mouseReleaseEvent=self.__MousereleaseEvent
        self._widget.setEnabled=self.__SetEnable
        self._widget.setDisabled=self.__SetDisable
        self._widget.setFocusPolicy=self.__SetFocusPolicy
        self._widget.keyPressEvent=self.__KeypressEvent
        self._widget.keyReleaseEvent=self.__KeyreleaseEvent

        #判断是否按钮类
        if isinstance(self._widget,QAbstractButton):  
            self._widget.toggled.connect(self.__SetCheck)

    def __MouseinEvent(self,event):
        if self._widget.isEnabled()==False:#如果控件不可用，则不触发鼠标进入事件
            return
        self._mouse=True #鼠标进入，True为鼠标进入，False为鼠标离开

        if self._click==False and self._fouce==False:#判断按下
            self.__MouseinEventing()
            
        self._widgetenterEvent(event)
        
    def __MouseoutEvent(self,event):
        if self._widget.isEnabled()==False:#如果控件不可用，则不触发鼠标进入事件
            return
        self._mouse=False #鼠标进入，True为鼠标进入，False为鼠标离开

        if self._click==False and self._fouce==False:#判断按下
            self.__MouseoutEventing()
        
        self._widgetleaveEvent(event)
        
    def __FocusinEvent(self,event):
        if self._widget.isEnabled()==False:#如果控件不可用，则不触发聚焦事件
            return
        
        if self._menu:#如果菜单打开，则不触发聚焦事件
            self._menu=False
            return
        
        if self._foucefunction: #聚焦功能未打开，不触发聚焦事件
            self._fouce=True #聚焦状态，True为聚焦，False为失焦

        if self._click==False and self._mouse==False and self._foucefunction:#判断按下
            self.__MouseinEventing()
        
        self.focusin.emit()
        self._widgetfocusInEvent(event)
        
    def __FocusoutEvent(self,event):
        if self._widget.isEnabled()==False:#如果控件不可用，则不触发失焦事件
            return
        
        if self._menu:#如果菜单打开，则不触发失焦事件
            return

        if self._foucefunction: #聚焦功能未打开，不触发失焦事件
            self._fouce=False #聚焦状态，True为聚焦，False为失焦
        
        if self._click==False and self._mouse==False and self._foucefunction:#判断按下
            self.__MouseoutEventing()
        
        self.focusout.emit()
        self._widgetfocusOutEvent(event)

    def __MouseinEventing(self):
        if self._mouseindelay==None and self._check==True:#没有延迟事件,选中
            self._ColorCheckin()
        elif  self._mouseindelay==None and self._check==False:#没有延迟事件,未选中
            self._Colorin()
        elif  self._mouseindelay!=None and self._check==True:#有延迟事件,选中
            if self._mousecheckoutdelay==None:#不存在鼠标离开延迟事件
                self._mousecheckindelay.start(self._mousecheckindelaytime)
            else:#存在鼠标离开延迟事件，判断鼠标离开延迟事件是否在运行,否的话则启动鼠标进入延迟事件,否则终止离开事件
                self._mousecheckoutdelay.stop() if self._mousecheckoutdelay.isActive() else self._mousecheckindelay.start(self._mousecheckindelaytime)
        elif  self._mouseindelay!=None and self._check==False:#有延迟事件,未选中
            if self._mouseoutdelay==None:#不存在鼠标离开延迟事件
                self._mouseindelay.start(self._mouseindelaytime)
            else:#存在鼠标离开延迟事件，判断鼠标离开延迟事件是否在运行,否的话则启动鼠标进入延迟事件,否则终止离开事件

                self._mouseoutdelay.stop() if self._mouseoutdelay.isActive() else self._mouseindelay.start(self._mouseindelaytime)

    def __MouseoutEventing(self):
        if self._mouseoutdelay==None and self._check==True:#没有延迟事件,选中
            self._ColorCheckout()
        elif  self._mouseoutdelay==None and self._check==False:#没有延迟事件,未选中
            self._Colorout()
        elif  self._mouseoutdelay!=None and self._check==True:#有延迟事件,选中
            if self._mousecheckindelay==None:#不存在鼠标离开延迟事件
                self._mousecheckoutdelay.start(self._mousecheckoutdelaytime)
            else:#存在鼠标离开延迟事件，判断鼠标离开延迟事件是否在运行,否的话则启动鼠标进入延迟事件,否则终止离开事件
                self._mousecheckindelay.stop() if self._mousecheckindelay.isActive() else self._mousecheckoutdelay.start(self._mousecheckoutdelaytime)
        elif  self._mouseoutdelay!=None and self._check==False:#有延迟事件,未选中
            if self._mouseindelay==None:#不存在鼠标离开延迟事件
                self._mouseoutdelay.start(self._mouseoutdelaytime)
            else:#存在鼠标离开延迟事件，判断鼠标离开延迟事件是否在运行,否的话则启动鼠标进入延迟事件,否则终止离开事件
                self._mouseindelay.stop() if self._mouseindelay.isActive() else self._mouseoutdelay.start(self._mouseoutdelaytime)

    def __MousepressEvent(self,event):
        if self._widget.isEnabled()==False:#如果控件不可用，则不触发鼠标按下事件
            return

        if isinstance(self._widget,QAbstractButton):#选中打开,不触发按下
            _run=False if self._widget.isCheckable() else True
        else:
            _run=False if self._checkfunction else True

        if _run and self._clickfunction:
            self._click=True #鼠标按下，True为鼠标按下，False为鼠标未按下
            self.mousepressed.emit()
            self._Colorpress(False)

        self._widgetmousePressEvent(event)

    def __MousereleaseEvent(self,event):
        if self._widget.isEnabled()==False:#如果控件不可用，则不触发鼠标弹起事件
            return
        
        if isinstance(self._widget,QAbstractButton):#选中打开,不触发按下
            _run=False if self._widget.isCheckable() else True
        else:
            _run=False if self._checkfunction else True

        if _run and self._clickfunction:
            self._click=False #鼠标按下，True为鼠标按下，False为鼠标未按下
            self.mousereleaseed.emit()
            self._Colorin(False)

        self._widgetmouseReleaseEvent(event)

    def __KeypressEvent(self,event):
        if self._widget.isEnabled()==False:#如果控件不可用，则不触发Space按下事件
            return
        
        if isinstance(self._widget,QAbstractButton):#选中打开,不触发按下
            _run=False if self._widget.isCheckable() else True
        else:
            _run=False if self._checkfunction else True

        if event.key()==Qt.Key_Space and _run and self._clickfunction:
            self._click=True 
            self.keypressed.emit()
            self._Colorpress(False)

        self._widgetkeyPressEvent(event)

    def __KeyreleaseEvent(self,event):
        if self._widget.isEnabled()==False:#如果控件不可用，则不触发Space弹起事件
            return 

        if isinstance(self._widget,QAbstractButton):#选中打开,不触发按下
            _run=False if self._widget.isCheckable() else True
        else:
            _run=False if self._checkfunction else True

        if event.key()==Qt.Key_Space and _run and self._clickfunction:
            self._click=False
            self.keyreleaseed.emit()
            self._Colorin(False)
    
        self._widgetkeyReleaseEvent(event)

    #功能性函数
    def __SetCheck(self,Check:bool):
        '''
        选中操作
        '''
        self._check=Check
        self.__MouseinEventing()

    def SetCheckFunction(self,Check:bool):
        '''
        选中操作
        '''
        self._checkfunction=Check
            
    def __SetFocusPolicy(self,Policy):
        if Policy==Qt.NoFocus:
            self._foucefunction=False
        else:
            self._foucefunction=True
        self._widgetsetFouce(Policy)

    def __SetEnable(self,Value:bool):
        if Value:
            #判断是否选中
            self._ColorCheckout() if self._check else self._Colorout()
        else:
            self._ColorDisabled()
 
        self._widgetsetEnabled(Value)

    def __SetDisable(self,Value:bool):
        if Value:
            self._ColorDisabled()
        else:
            #判断是否选中
            self._ColorCheckout() if self._check else self._Colorout()
 
        self._widgetsetDisabled(Value)

    def SetClickFunciton(self,Open:bool=True):
        """
        设置控件的按下功能
        """
        self._clickfunction=Open

    def SetMenu(self):
        '''
        有菜单功能,打开菜单前运行
        '''
        self._menu=True

    def LoadDelay(self,MouseinDelayTime:int=None,MouseoutDelayTime:int=None,\
                        MouseCheckinDelayTime:int=None,MouseCheckoutDelayTime:int=None):
        '''
        延迟事件,单位毫秒，用于鼠标进入或离开等,颜色效果需要延迟显示的情况
        '''
        if MouseinDelayTime==None:
            if self._mouseindelay!=None:
                self._mouseindelay=None
        else:
            self._mouseindelay=QTimer()
            self._mouseindelaytime=MouseinDelayTime
            self._mouseindelay.timeout.connect(self.__MouseinDelayTimeoutEvent)
      
        if MouseoutDelayTime==None:
            if self._mouseoutdelay!=None:
                self._mouseoutdelay=None
        else:
            self._mouseoutdelay=QTimer()
            self._mouseoutdelaytime=MouseoutDelayTime
            self._mouseoutdelay.timeout.connect(self.__MouseoutDelayTimeoutEvent)

        if MouseCheckinDelayTime==None:
            if self._mousecheckindelay!=None:
                self._mousecheckindelay=None
        else:
            self._mousecheckindelay=QTimer()
            self._mousecheckindelaytime=MouseCheckinDelayTime
            self._mousecheckindelay.timeout.connect(self.__MouseCheckinDelayTimeoutEvent)

        if MouseCheckoutDelayTime==None:
            if self._mousecheckoutdelay!=None:
                self._mousecheckoutdelay=None
        else:
            self._mousecheckoutdelay=QTimer()
            self._mousecheckoutdelaytime=MouseCheckoutDelayTime
            self._mousecheckoutdelay.timeout.connect(self.__MouseCheckoutDelayTimeoutEvent)

    #延迟事件处理
    def __MouseinDelayTimeoutEvent(self):
        if self._mouseindelay!=None:
            if self._mouseindelay.isActive():
                self._mouseindelay.stop()
        self._Colorin()

    def __MouseoutDelayTimeoutEvent(self):
        if self._mouseoutdelay!=None:
            if self._mouseoutdelay.isActive():
                self._mouseoutdelay.stop()
        self._Colorout()

    def __MouseCheckinDelayTimeoutEvent(self):
        if self._mousecheckindelay!=None:
            if self._mousecheckindelay.isActive():
                self._mousecheckindelay.stop()
        self._ColorCheckin()

    def __MouseCheckoutDelayTimeoutEvent(self):
        if self._mousecheckoutdelay!=None:
            if self._mousecheckoutdelay.isActive():
                self._mousecheckoutdelay.stop()        
        self._ColorCheckout()

    #修改事件
    def _Colorin(self,animation_:bool=True):
        '''
        鼠标进入事件

        animation_:是否启用动画
        '''
        self.mouseined.emit()

    def _Colorout(self,animation_:bool=True):
        '''
        鼠标离开事件
        
        animation_:是否启用动画
        '''
        self.mouseouted.emit()

    def _Colorpress(self,animation_:bool=True):
        '''
        鼠标按下事件
        
        animation_:是否启用动画
        '''
        pass
  
    def _ColorCheckin(self,animation_:bool=True):
        '''
        选中状态,鼠标进入事件
        
        animation_:是否启用动画
        '''
        self.mouseined.emit()

    def _ColorCheckout(self,animation_:bool=True):
        '''
        选中状态,鼠标离开事件
        
        animation_:是否启用动画
        '''
        self.mouseouted.emit()

    def _ColorDisabled(self,animation_:bool=True):
        '''
        禁用状态
        
        animation_:是否启用动画
        '''
        pass
    
class ConvenientSet:
    def SetFocusType(self,Type:int=None):
        '''
        Type:0/None 不聚焦
        Type:1      通过鼠标点击获取焦点
        Type:2      通过tab获取焦点
        Type:3      通过way1 2方式获取焦点
        Type:4      通过滑轮wheel获取焦点
        ''' 
        if Type==1:
            self.setFocusPolicy(Qt.ClickFocus)
        elif Type==2:
            self.setFocusPolicy(Qt.TabFocus)
        elif Type==3:
            self.setFocusPolicy(Qt.StrongFocus)
        elif Type==4:
            self.setFocusPolicy(Qt.WheelFocus)
        else:
            self.setFocusPolicy(Qt.NoFocus)

    def SetMousePenetration(self,Penetratio:bool):#鼠标穿透
        '''
        鼠标穿透
        '''
        self.setWindowFlag(Qt.WindowTransparentForInput,Penetratio)
        self.setAttribute(Qt.WA_TransparentForMouseEvents,Penetratio)

class CountDown:
    '''
    提供带text功能的qt控件倒计时功能

    使用方法：
    countdown_load事件,在控件加载时调用
    countdown_start事件,开始倒计时
    countdown_stop事件,强制终止倒计时
    '''
    countdowntimeouted=Signal()

    def CountDownLoad(self,Object:QWidget):
        '''
        
        '''
        self._widget=Object #缓存控件

        self._countdowntimevalue=0
        self._countdowntimethread=QTimer(self)
        self._countdowntimethread.timeout.connect(self.__CountDownTimeEvent)
        
        #缓存事件
        self._countdownmouserelease=self._widget.leaveEvent
        self._widget.leaveEvent=self.__CountDownMouseReleaseEvent
        self._countdownkeyrelease=self._widget.keyReleaseEvent
        self._widget.keyReleaseEvent=self.__CountDownKeyReleaseEvent

    def CountDownStop(self,ConnectEvent:bool=False):
        '''
        强制停止倒计时

        connect_event:触发中断事件连接槽函数
        '''
        if self._countdowntimevalue!=0:
            self._countdowntimethread.stop()
            self.setText(self._countdownbackuptext)
        if ConnectEvent:
            self.countdowntimeouted.emit()

    def CountDownStart(self,Time:int):
        '''
        开始倒计时
        
        time_:倒计时时间,单位毫秒
        '''
        if self._countdowntimevalue==0:
            self._countdowntimevalue=Time
            self._countdownbackuptext=self.text()
            self._countdowntimethread.start(10)#10ms循环一次

    def __CountDownTimeEvent(self):
        self._countdowntimevalue-=10
        if self._countdowntimevalue<=0:
            self._countdowntimethread.stop()
            self.setText(self._countdownbackuptext)
            self._countdowntimevalue=0
            self.countdowntimeouted.emit()
        else:
            self.setText(self._countdownbackuptext+"("'%.2f'%round(self._countdowntimevalue/1000,2)+"S)")

    def __CountDownMouseReleaseEvent(self,event):#鼠标松开事件
        if self._countdowntimevalue!=0:
            self.CountDownStop()
        self._countdownmouserelease(event)

    def __CountDownKeyReleaseEvent(self,event):#键盘松开事件
        if event.key()==Qt.Key_Space and self._countdowntimevalue!=0:
            self.CountDownStop()   
        self._countdownkeyrelease(event)

class ShortcutText:
    '''
    控件带有Text参数都可以使用快捷键
    '''
    shortcutpressed=Signal()
    def LoadShortcut(self):
        '''
        加载快捷键
        '''
        self._shortcut=None


    def SetShortcut_(self,Shortcut:str=None,TextFollow:bool=False):
        '''
        设置快捷键
        
        Shortcut:快捷键字符串,格式为"Ctrl+Shift+A"
        TextFollow:控件的text自动添加快捷键文本,默认不添加
        '''
        #取快捷键str文本
        _shortcuttext="" if self._shortcut==None else "("+self._shortcut.key().toString().title()+")"

        if Shortcut==None:
            if self._shortcut!=None:
                #移除快捷键
                self._shortcut.setKey(QKeySequence())
                self._shortcut=None
                #取控件的text
                _text=self.text()
                _textspilt=_text if _shortcuttext=="" else _text.split(_shortcuttext)[0]
                #设置控件的text
                self.setText(_textspilt)
        else:
            _shortcut = QKeySequence(Shortcut)
            self._shortcut = QShortcut(_shortcut, self)
            if TextFollow:
                self.setText(self.text()+self.GetShortcutName())
            else:
                self.setText(self.text())
            #绑定槽函数
            self._shortcut.activated.connect(self.shortcutpressed.emit)

    def GetShortcutName(self):
        if self._shortcut is not None:
            return "("+self._shortcut.key().toString().title()+")"
        return ""
