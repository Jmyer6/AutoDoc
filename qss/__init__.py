from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QEasingCurve

from .qss_plus import QssPlus,QssStyle
from .qss_theme import themes,GradientColorList,GradientColor,Font_,FontSize,QssManage

from .qss_type import GradientSpread,GradientStyle,FontSizeStyle,FontStyle,\
    FontWeight,BorderStyle,TextAlign,TextDecoration

from lib import MouseEvent,ConvenientSet,GetThemeMode,ThemeMode,GetWindowThememode,Color_,ColorStyle

class QssPlusEvent():
    def QssPlusEventLoad(self):
        #模板
        self._TempLightqss=QssStyle()
        self._TempDarkqss=QssStyle()
        #正常
        self._NormalLightqss=QssStyle()
        self._NormalDarkqss=QssStyle()
        #点燃
        self._HoverLightqss=QssStyle()
        self._HoverDarkqss=QssStyle()
        #按下
        self._PressLightqss=QssStyle()
        self._PressDarkqss=QssStyle()
        #禁用
        self._DisabledLightqss=QssStyle()
        self._DisabledDarkqss=QssStyle()
        #选中正常
        self._CheckNormalLightqss=QssStyle()
        self._CheckNormalDarkqss=QssStyle()
        #选中点燃
        self._CheckHoverLightqss=QssStyle()
        self._CheckHoverDarkqss=QssStyle()

        self.SetTempLightqss()
        self.SetTempDarkqss()

        self.SetNormalLightqss() if self.IsThemeMode() else self.SetNormalDarkqss()

    def SetTempLightqss(self):
        '''
        浅色模板样式
        '''
        pass

    def SetTempDarkqss(self):
        '''
        深色模板样式
        '''
        pass

    def SetNormalLightqss(self):
        '''
        浅色正常样式
        '''
        pass

    def SetNormalDarkqss(self):
        '''
        深色正常样式
        '''
        pass
  
    def SetHoverLightqss(self):
        '''
        浅色点燃样式
        '''
        pass

    def SetHoverDarkqss(self):
        '''
        深色点燃样式
        '''
        pass

    def SetPressLightqss(self):
        '''
        浅色按下样式
        '''
        pass
    
    def SetPressDarkqss(self):
        '''
        深色按下样式
        '''
        pass

    def SetDisabledLightqss(self):
        '''
        浅色禁用样式
        '''
        pass

    def SetDisabledDarkqss(self):
        '''
        深色禁用样式
        '''
        pass

    def SetCheckNormalLightqss(self):
        '''
        浅色选中正常样式
        '''
        pass
    
    def SetCheckNormalDarkqss(self):
        '''
        深色选中正常样式
        '''
        pass

    def SetCheckHoverLightqss(self):
        '''
        浅色选中点燃样式
        '''
        pass

    def SetCheckHoverDarkqss(self):
        '''
        深色选中点燃样式
        '''
        pass

    def IsThemeMode(self):
        '''
        判断主题模式
        True:浅色
        False:深色
        '''
        _thememode=GetThemeMode()
        #判断主题
        if _thememode==ThemeMode.AUTO:
            _mode=ThemeMode.DARK if GetWindowThememode() else ThemeMode.LIGHT
        else:
            _mode=_thememode

        if _mode==ThemeMode.LIGHT:
            return True
        else:
            return False
 
class QssPlusClass(MouseEvent,ConvenientSet,QssPlusEvent):
    '''
    QssPlus多继承类

    QssApply函数在init中应用  
    '''
    def QssApply(self,
                 Widget:QWidget,
                 ObjectName:str,
                 Register:bool=True,
                 EventFollow:bool=True,
                 EasingCurve:QEasingCurve=QEasingCurve.OutQuad,
                 Duration:int=500):
        """
        加载qss_plus环境,多继承后类中有set_qss函数,建议全部qss修改都存放在set_qss函数中
        Widget:控件
        ObjectName:控件名
        Register:注册控件,注册后跟随主题颜色变动而变动
        EventFollow:是否开启事件跟随
        EasingCurve:动画类型,详情参考QEasingCurve
        Duration:动画运行时间,单位毫秒

        event_open不打开操作self.qss改变显示效果
        event_open打开需要分别操作所对应的显示效果
    
        self._NormalLightqss  浅色主题正常显示
        self._NormalDarkqss   深色主题正常显示
        self._HoverLightqss   浅色主题鼠标悬浮
        self._HoverDarkqss    深色主题鼠标悬浮
        self._PressLightqss   浅色主题按下
        self._PressDarkqss    深色主题按下
        self._DisabledLightqss 浅色主题禁用
        self._DisabledDarkqss  深色主题禁用
        self._CheckNormalLightqss 浅色主题选中正常
        self._CheckNormalDarkqss  深色主题选中正常
        self._CheckHoverLightqss  浅色主题选中点燃
        self._CheckHoverDarkqss   深色主题选中点燃

        菜单功能,需要每次打开菜单时运行self.set_menu()
        """
        self._qssplus=QssPlus(Widget,ObjectName,EasingCurve,Duration)
        self.qss=self._qssplus.qss

        #动画事件覆盖加载
        self.SetEasingCurve()
        self.SetDuration()
        
        if Register:
            self._qssplus.Register(Register)

        self._evevtfollow=EventFollow

        if EventFollow:
            #加载鼠标事件
            self.MouseEventLoad(Widget)
            #加载qssplus事件
            self.QssPlusEventLoad()
            #应用qss
            self.Renewqss()
    
        else:
            #应用qss
            self.Setqss()
            self._qssplus.ApplyQss()

    def Renewqss(self):
        '''
        重新加载qss
        '''
        if self._evevtfollow:
            if self._check and self._fouce:
                self._ColorCheckin(False)
            elif self._check and self._fouce==False:
                self._ColorCheckout(False)
            if self._check==False and self._fouce:
                self._Colorin(False)
            elif self._check==False and self._fouce==False:
                self._Colorout(False)
        else:
            self._qssplus.ApplyQss()

    def Setqss(self):
        '''
        全部qss修改都存放在这个函数中
        '''
        pass

    def SetEasingCurve(self,EasingCurve:QEasingCurve=QEasingCurve.OutQuad):
        '''
        设置动画类型,详情参考QEasingCurve
        '''
        self._qssplus._animation.SetEasingCurve(EasingCurve)

    def SetDuration(self,Duration:int=500):
        '''
        设置动画运行时间,单位毫秒
        '''
        self._qssplus._animation.SetDuration(Duration)
    
    def _Colorin(self, animation_: bool = True):
        if self._evevtfollow:

            if self.IsThemeMode():
                self.SetHoverLightqss()
                self._qssplus.UpDateQss(self._HoverLightqss,animation_)
            else:
                self.SetHoverDarkqss()
                self._qssplus.UpDateQss(self._HoverDarkqss,animation_)

        return super()._Colorin(animation_)
    
    def _Colorout(self, animation_: bool = True):
        if self._evevtfollow:

            if self.IsThemeMode():
                self.SetNormalLightqss()
                self._qssplus.UpDateQss(self._NormalLightqss,animation_) 
            else:
                self.SetNormalDarkqss()
                self._qssplus.UpDateQss(self._NormalDarkqss,animation_)  

        return super()._Colorout(animation_)

    def _Colorpress(self, animation_: bool = True):
        if self._evevtfollow:

            if self.IsThemeMode():
                self.SetPressLightqss()
                self._qssplus.UpDateQss(self._PressLightqss,False)
            else:
                self.SetPressDarkqss()
                self._qssplus.UpDateQss(self._PressDarkqss,False)

        return super()._Colorpress(animation_)

    def _ColorCheckin(self, animation_: bool = True):
        if self._evevtfollow:

            if self.IsThemeMode():
                self.SetCheckHoverLightqss()
                self._qssplus.UpDateQss(self._CheckHoverLightqss,animation_)
            else:
                self.SetCheckHoverDarkqss()
                self._qssplus.UpDateQss(self._CheckHoverDarkqss,animation_)
        
        return super()._ColorCheckin(animation_)
    
    def _ColorCheckout(self, animation_: bool = True):
        if self._evevtfollow:

            if self.IsThemeMode():
                self.SetCheckNormalLightqss()
                self._qssplus.UpDateQss(self._CheckNormalLightqss,animation_)
            else:
                self.SetCheckNormalDarkqss()
                self._qssplus.UpDateQss(self._CheckNormalDarkqss,animation_)
        
        return super()._ColorCheckout(animation_)
    
    def _ColorDisabled(self, animation_: bool = True):
        if self._evevtfollow:

            if self.IsThemeMode():
                self.SetDisabledLightqss()
                self._qssplus.UpDateQss(self._DisabledLightqss,animation_)
            else:
                self.SetDisabledDarkqss()
                self._qssplus.UpDateQss(self._DisabledDarkqss,animation_)
                

        return super()._ColorDisabled(animation_)



