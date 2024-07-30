from PySide6.QtCore import Qt,QSize
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame

from ..button import ButtonBase
from ..icon import Icon

from qss import QssPlusClass,ColorStyle,BorderStyle,Font_,FontSize,GradientColor,GradientColorList,GradientSpread,GradientStyle
from lib import CountDown,ShadowEffect,Position,Color_,Animation,IntExcess


class CheckBox(ButtonBase):#菜单
    def __init__(self,Text:str,parent=None):
        super(CheckBox, self).__init__(Text=Text,objectName="CheckBox",parent=parent)
        self.SetText(Text)
        self.SetTextAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.SetIcons_(IconFrameSize=QSize(20,20),IconPosition=Position.LEFT)
        self.IconsAdd(Icon.checkbox1,QSize(20,20))
        self.IconsAdd(Icon.checkbox3,QSize(20,20))

        self.setCheckable(True)
        self.toggled.connect(self.SetCheckEvent)
        self.setMinimumHeight(28)

    def setChecked(self, arg__1: bool) -> None:
        self.SetCheckEvent(arg__1)
        return super().setChecked(arg__1)

    def SetCheckEvent(self,Check:bool):
        if Check:
            self._icon.Go(1)
        else:
            self._icon.Go(0)

    def SetTempLightqss(self):
        self._TempLightqss.SetBorderWidth(Width=0)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBackgroundColor(Color_(ColorStyle.NullColor,0))
        self._TempLightqss.Set_("outline","none")

    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()
        self._NormalLightqss.SetColor(Color_(ColorStyle.FullColor,100))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()
        self._HoverLightqss.SetColor(Color_(ColorStyle.ThemeColor,30))

    def SetCheckHoverLightqss(self):
        self._CheckHoverLightqss=self._TempLightqss.Copy()
        self._CheckHoverLightqss.SetColor(Color_(ColorStyle.ThemeColor,40))

    def SetCheckNormalLightqss(self):
        self._CheckNormalLightqss=self._TempLightqss.Copy()
        self._CheckNormalLightqss.SetColor(Color_(ColorStyle.ThemeColor,0))

    def SetDisabledLightqss(self):
        self._DisabledLightqss=self._TempLightqss.Copy()
        self._DisabledLightqss.SetColor(Color_(ColorStyle.FullColor,50))

    def SetTempDarkqss(self):
        self._TempDarkqss.SetBorderWidth(Width=0)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.SetBackgroundColor(Color_(ColorStyle.NullColor,0))
        self._TempDarkqss.Set_("outline","none")

    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempDarkqss.Copy()
        self._NormalDarkqss.SetColor(Color_(ColorStyle.FullColor,100))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempDarkqss.Copy()
        self._HoverDarkqss.SetColor(Color_(ColorStyle.ThemeColor,30))

    def SetCheckHoverDarkqss(self):
        self._CheckHoverDarkqss=self._TempDarkqss.Copy()
        self._CheckHoverDarkqss.SetColor(Color_(ColorStyle.ThemeColor,40))

    def SetCheckNormalDarkqss(self):
        self._CheckNormalDarkqss=self._TempDarkqss.Copy()
        self._CheckNormalDarkqss.SetColor(Color_(ColorStyle.ThemeColor,0))

    def SetDisabledDarkqss(self):
        self._DisabledDarkqss=self._TempDarkqss.Copy()
        self._DisabledDarkqss.SetColor(Color_(ColorStyle.FullColor,50))

      
class Round(QFrame,QssPlusClass):
    def __init__(self, *args, **kwargs):
        super(Round, self).__init__(*args, **kwargs)
        self.QssApply(self,"Round",True,False)
        self.SetMousePenetration(True)

    def SetColor(self,Color:Color_,Animation:bool=True):
        _color=GradientColor()
        _color.SetStyle(GradientStyle.qradialgradient)
        _color.SetSpread(GradientSpread.pad)
        _color.Setcp(0.5,0.5)
        _color.Setfp(0.5,0.5)
        _color.SetRadius(0.5)

        _colorlist=GradientColorList()
        _colorlist.AddColor(0.6,Color)
        _colorlist.AddColor(0.7,Color_(Color.GetColor(),FixAlpha=0))

        _color.SetColorlist(_colorlist)

        if Animation:
            self.qss.SetBackgroundColor(_color,True)
        elif Animation==False:
            self.qss.SetBackgroundColor(_color)   
            self._qssplus.ApplyQss()

class RoundFrame(QFrame,QssPlusClass):
    def __init__(self, *args, **kwargs):
        super(RoundFrame, self).__init__(*args, **kwargs)
        self.QssApply(self,"RoundFrame",True,False)
        self.SetMousePenetration(True)
        self._check=False

        self._handle=Round(self)
        self._handle.move(0,0)

        self.setFixedSize(32,18)
        self._handle.setFixedSize(self.height(),self.height())

        self._ani=Animation(0)
        self._ani.Animationed.connect(self.__MoveEvent)

        self._handleani=Animation(0)
        self._handleani.Animationed.connect(self.__SizeHandleEvent)
        
        self.__SetColor(False)

    def __MoveEvent(self,Value:int):
        self._handle.move(IntExcess(0,self.width()-self._handle.width(),Value),0)

    def __SizeHandleEvent(self,Value:int):
        _add=3
        if self._check:
            self._handle.move(IntExcess(self.width()-self.height(),self.width()-self.height()-_add,Value),0)
        self._handle.setFixedSize(self.height()+int(_add/100*Value),self.height())      

    def __SetColor(self,Animation:bool=True):
        if self._check:
            _bordercolor=Color_(ColorStyle.FullThemeColor,0)
            _bccolor=Color_(ColorStyle.FullThemeColor,0)
            _color=Color_(ColorStyle.Light)
        else:
            _bordercolor=Color_(ColorStyle.FullColor,50)
            _bccolor=Color_(ColorStyle.FullColor,0)
            _color=Color_(ColorStyle.FullColor,100)

        self.qss.SetBorderWidth(Width=1)
        self.qss.SetBorderRadius(Radius=int(self.height()/2))
        self.qss.SetBorderStyle(Style=BorderStyle.solid)
        self.qss.SetBorderColor(Color=_bordercolor)

        if Animation:
            self.qss.SetBackgroundColor(_bccolor,True)
        elif Animation==False:
            self.qss.SetBackgroundColor(_bccolor)   
            self._qssplus.ApplyQss()

        self._handle.SetColor(_color,Animation)
 
    def SetCheck(self,Check:bool):
        self._check=Check
        if Check:
            self._ani.GoValue(100)
        else:
            self._ani.GoValue(0)

        self.__SetColor()
            
class CheckRoundBox(ButtonBase):#菜单
    def __init__(self,Text:str,parent=None):
        self._round=None
        super(CheckRoundBox, self).__init__(Text=Text,objectName="CheckRoundBox",parent=parent)
        self.SetText(Text)
        self.SetTextAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self._round=RoundFrame()
        self.SetLeftWidget(self._round)

        self.setCheckable(True)
        self.toggled.connect(self._round.SetCheck)
        self.setMinimumHeight(28)

        self.SetFocusType(0)

    def SetTempLightqss(self):
        self._TempLightqss.SetBorderWidth(Width=0)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBackgroundColor(Color_(ColorStyle.NullColor,0))
        self._TempLightqss.Set_("outline","none")

    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()
        self._NormalLightqss.SetColor(Color_(ColorStyle.FullColor,100))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()
        self._HoverLightqss.SetColor(Color_(ColorStyle.ThemeColor,30))

    def SetCheckHoverLightqss(self):
        self._CheckHoverLightqss=self._TempLightqss.Copy()
        self._CheckHoverLightqss.SetColor(Color_(ColorStyle.ThemeColor,40))

    def SetCheckNormalLightqss(self):
        self._CheckNormalLightqss=self._TempLightqss.Copy()
        self._CheckNormalLightqss.SetColor(Color_(ColorStyle.ThemeColor,0))

    def SetDisabledLightqss(self):
        self._DisabledLightqss=self._TempLightqss.Copy()
        self._DisabledLightqss.SetColor(Color_(ColorStyle.FullColor,50))

    def SetTempDarkqss(self):
        self._TempDarkqss.SetBorderWidth(Width=0)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.SetBackgroundColor(Color_(ColorStyle.NullColor,0))
        self._TempDarkqss.Set_("outline","none")

    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempDarkqss.Copy()
        self._NormalDarkqss.SetColor(Color_(ColorStyle.FullColor,100))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempDarkqss.Copy()
        self._HoverDarkqss.SetColor(Color_(ColorStyle.ThemeColor,30))

    def SetCheckHoverDarkqss(self):
        self._CheckHoverDarkqss=self._TempDarkqss.Copy()
        self._CheckHoverDarkqss.SetColor(Color_(ColorStyle.ThemeColor,40))

    def SetCheckNormalDarkqss(self):
        self._CheckNormalDarkqss=self._TempDarkqss.Copy()
        self._CheckNormalDarkqss.SetColor(Color_(ColorStyle.ThemeColor,0))

    def SetDisabledDarkqss(self):
        self._DisabledDarkqss=self._TempDarkqss.Copy()
        self._DisabledDarkqss.SetColor(Color_(ColorStyle.FullColor,50))

    def _Colorin(self, animation_: bool = True):
        if self._round!=None:
            self._round._handleani.GoValue(100)
        return super()._Colorin(animation_)
    
    def _Colorout(self, animation_: bool = True):
        if self._round!=None:
            self._round._handleani.GoValue(0)
        return super()._Colorout(animation_)
    
    def _ColorCheckin(self, animation_: bool = True):
        if self._round!=None:
            self._round._handleani.GoValue(100)
        return super()._ColorCheckin(animation_)
    
    def _ColorCheckout(self, animation_: bool = True):
        if self._round!=None:
            self._round._handleani.GoValue(0)
        return super()._ColorCheckout(animation_)

            

    



        


  