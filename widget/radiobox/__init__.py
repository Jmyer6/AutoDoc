from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame

from ..button import ButtonBase

from qss import ColorStyle,Color_,BorderStyle,QssPlusClass,ConvenientSet,\
        GradientColor,GradientColorList,GradientSpread,GradientStyle

class RadioIcon(QFrame,QssPlusClass,ConvenientSet):#菜单
    def __init__(self,*args, **kwargs):
        super(RadioIcon, self).__init__(*args, **kwargs)
        self.QssApply(self,"RadioIcon",True,False)
        self.SetMousePenetration(True)#鼠标穿透

    def Setqss(self):
        self._backgroundColor=GradientColor()
        self._backgroundColor.SetStyle(GradientStyle.qradialgradient)
        self._backgroundColor.SetSpread(GradientSpread.pad)
        self._backgroundColor.Setcp(0.5,0.5)
        self._backgroundColor.Setfp(0.5,0.5)
        self._backgroundColor.SetRadius(0.5)

        __backgroundColorList=GradientColorList()
        __backgroundColorList.AddColor(0.6,Color_(ColorStyle.NullColor,100))
        __backgroundColorList.AddColor(0.7,Color_(ColorStyle.FullColor,100))
        __backgroundColorList.AddColor(0.8,Color_(ColorStyle.FullColor,100))
        __backgroundColorList.AddColor(0.9,Color_(ColorStyle.NullColor,100))  
        self._backgroundColor.SetColorlist(__backgroundColorList)  
        
        self.qss.SetBackgroundColor(self._backgroundColor)

class RadioBox(ButtonBase):#菜单
    def __init__(self,Text:str,parent=None):
        super(RadioBox, self).__init__(Text=Text,objectName="RadioButton",EventFollow=False,parent=parent)
        self.setMinimumHeight(24)
        self.RadioCheck=False

        self.SetTextAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self._radio=RadioIcon(self)
        self._radio.setFixedSize(20,20)
        self.SetLeftWidget(self._radio)
        self.setCheckable(True)
        self.toggled.connect(self.SetCheck)

        self.MouseEventLoad(self)
        
    def Setqss(self):
        self.qss.Set_("outline","none")
        self.qss.SetBorderWidth(Width=0)
        self.qss.SetBorderStyle(BorderStyle.solid)
        self.qss.SetBackgroundColor(Color_(ColorStyle.NullColor,50))

    def resizeEvent(self, event) -> None:
        self._radio.move(7,2)
        self._radio.setFixedSize(self.height()-4,self.height()-4)
        return super().resizeEvent(event)

    def _Colorin(self, animation_: bool = True):
        if self._evevtfollow==False and self.RadioCheck==False:
            __backgroundColorList=GradientColorList()
            __backgroundColorList.AddColor(0.5,Color_(ColorStyle.NullColor,100))
            __backgroundColorList.AddColor(0.6,Color_(ColorStyle.FullColor,100))
            __backgroundColorList.AddColor(0.8,Color_(ColorStyle.FullColor,100))
            __backgroundColorList.AddColor(0.9,Color_(ColorStyle.NullColor,100))    

            self._radio._backgroundColor.SetColorlist(__backgroundColorList,True)

    def _Colorout(self, animation_: bool = True):
        if self._evevtfollow==False and self.RadioCheck==False:
            __backgroundColorList=GradientColorList()
            __backgroundColorList.AddColor(0.6,Color_(ColorStyle.NullColor,100))
            __backgroundColorList.AddColor(0.7,Color_(ColorStyle.FullColor,100))
            __backgroundColorList.AddColor(0.8,Color_(ColorStyle.FullColor,100))
            __backgroundColorList.AddColor(0.9,Color_(ColorStyle.NullColor,100))    

            self._radio._backgroundColor.SetColorlist(__backgroundColorList,True)

    def _ColorCheckin(self, animation_: bool = True):
        if self._evevtfollow==False and self.RadioCheck==True:
            __backgroundColorList=GradientColorList()
            __backgroundColorList.AddColor(0.4,Color_(ColorStyle.NullThemeColor,100))
            __backgroundColorList.AddColor(0.5,Color_(ColorStyle.ThemeColor,0))
            __backgroundColorList.AddColor(0.8,Color_(ColorStyle.ThemeColor,0))
            __backgroundColorList.AddColor(0.9,Color_(ColorStyle.NullThemeColor,100))    

            self._radio._backgroundColor.SetColorlist(__backgroundColorList,True)
 
    def _ColorCheckout(self, animation_: bool = True):
        if self._evevtfollow==False and self.RadioCheck==True:
            __backgroundColorList=GradientColorList()
            __backgroundColorList.AddColor(0.4,Color_(ColorStyle.NullThemeColor,100))
            __backgroundColorList.AddColor(0.5,Color_(ColorStyle.ThemeColor,0))
            __backgroundColorList.AddColor(0.8,Color_(ColorStyle.ThemeColor,0))
            __backgroundColorList.AddColor(0.9,Color_(ColorStyle.NullThemeColor,100))    

            self._radio._backgroundColor.SetColorlist(__backgroundColorList,True)
   
    def _ColorDisabled(self, animation_: bool = True):
        if self._evevtfollow==False:
            __backgroundColorList=GradientColorList()
            __backgroundColorList.AddColor(0.6,Color_(ColorStyle.NullColor,50))
            __backgroundColorList.AddColor(0.7,Color_(ColorStyle.FullColor,50))
            __backgroundColorList.AddColor(0.8,Color_(ColorStyle.FullColor,50))
            __backgroundColorList.AddColor(0.9,Color_(ColorStyle.NullColor,50))    

            self._radio._backgroundColor.SetColorlist(__backgroundColorList,True)

    def SetCheck(self,Check:bool):
        if Check and self.parent() is not None:
            self.RadioCheck=True
            list_=self.parent().findChildren(RadioBox,"RadioButton")
            for btn_ in list_:
                if  btn_ != self:
                    btn_._mouse=False
                    btn_._check=False
                    btn_._fouce=False
                    btn_.RadioCheck=False
                    btn_.setChecked(False)
                    btn_._Colorout()
            


           


