from PySide6.QtCore import QSize,QSize,Qt,QPoint,QEasingCurve,Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLineEdit,QHBoxLayout,QFileDialog

from ..button import ButtonBase
from ..icon import Icon,IconView,IconViews
from ..menu import LineEditMenu

from qss import BorderStyle,Color_,ColorStyle,QssPlusClass,GradientColor,\
    GradientSpread,GradientStyle,GradientColorList,Font_,FontSize
from lib import Position

from typing import Union

class LineEditButton(ButtonBase):
    '''
    普通按钮
    '''
    def __init__(self,*args, **kwargs):
        super(LineEditButton, self).__init__(*args, **kwargs)
        self.SetFocusType(2)
        self.setFixedSize(20,20)
        #设置鼠标样式
        self.setCursor(Qt.ArrowCursor)

    def SetTempLightqss(self):
        self._TempLightqss.SetBorderWidth(Width=0)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBorderRadius(Radius=3)
        self._TempLightqss.Set_("outline","none")

    def SetTempDarkqss(self):
        self._TempDarkqss.SetBorderWidth(Width=0)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.SetBorderRadius(Radius=3)
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

class LineEdit(QLineEdit,QssPlusClass):
    loadlinked=Signal(str)
    def __init__(self,*args, **kwargs):
        super(LineEdit, self).__init__(*args, **kwargs)
        self.QssApply(self,"LineEdit",True,False)

        self._icon=None
        self._iconPosition=Position.LEFT  #只支持left、right
        self._iconPadding=0

        self._closeButton=None  #删除按钮标识
        self._closePadding=0    
        
        self._addlinkButton=None  #添加链接按钮标识
        self._addlinkPadding=0

        self._passwordButton=None  #密码按钮标识
        self._passwordPadding=0

        #右边图标,适用后续combobox情况,一般加载箭头
        self._rightIcon=None  
        self._rightIconPadding=0

        self.__SetLayout()
        self.MouseEventLoad(self)
        self.SetClickFunciton(False)
        self.__SetPadding()

        self.textChanged.connect(self.__ShowCloseButton)

    def __SetLayout(self):
        self.setFixedHeight(26)
        self.layouts=QHBoxLayout()
        self.layouts.setContentsMargins(6,0,3,0)
        self.layouts.setSpacing(1)
        self.layouts.addStretch(1)
        self.setLayout(self.layouts)
     
    def Setqss(self):
        self._backgroundcolor=GradientColor()
        self._backgroundcolor.SetStyle(GradientStyle.qlineargradient)
        self._backgroundcolor.SetSpread(GradientSpread.pad)
        self._backgroundcolor.Setp1(0.5,0)
        self._backgroundcolor.Setp2(0.5,1)
        _colorlist=GradientColorList()
        _colorlist.AddColor(0,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(0.94,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(0.95,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(1,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        self._backgroundcolor.SetColorlist(_colorlist)

        self.qss.SetBackgroundColor(self._backgroundcolor)
        self.qss.SetColor(Color_(ColorStyle.FullColor,100))

        self.qss.SetFont(Font_(FontSize=FontSize(Shift=0,Min=10,Max=16)))

        self.qss.SetBorderWidth(Width=1)
        self.qss.SetBorderStyle(Style=BorderStyle.solid)
        self.qss.SetBorderRadius(Radius=5)
        self.qss.SetBorderColor(Color=Color_(ColorStyle.FullColor,10))
        self.qss.SetBorderColor(ColorBottom=Color_(ColorStyle.FullColor,20))

    def __SetPadding(self):
        _paddingLeft=5
        _paddingRight=5

        self.layouts.setContentsMargins(6,0,3,0)

        _widget=self

        if self._closeButton is not None:
            _paddingRight+=self._closePadding
            self.layouts.insertWidget(-1,self._closeButton)
            self.setTabOrder(_widget,self._closeButton)
            _widget=self._closeButton
            self._closeButton.show()

        if self._addlinkButton is not None:
            _paddingRight+=self._addlinkPadding
            self.layouts.insertWidget(-1,self._addlinkButton)
            self.setTabOrder(_widget,self._addlinkButton)
            _widget=self._closeButton
            self._addlinkButton.show()

        if self._passwordButton is not None:
            _paddingRight+=self._passwordPadding
            self.layouts.insertWidget(-1,self._passwordButton)
            self.setTabOrder(_widget,self._passwordButton)
            _widget=self._closeButton
            self._passwordButton.show()

        if self._icon is not None:
            if self._iconPosition==Position.LEFT:
                _paddingLeft+=self._iconPadding
                self.layouts.insertWidget(0,self._icon)
                self._icon.show()
            elif self._iconPosition==Position.RIGHT:
                _paddingRight+=self._iconPadding
                self.layouts.insertWidget(-1,self._icon)
                self._icon.show()
        
        if self._rightIcon is not None:
            self.layouts.setContentsMargins(6,0,5,0)
            _paddingRight+=self._rightIconPadding
            self.layouts.insertWidget(-1,self._rightIcon)
            self.setTabOrder(_widget,self._rightIcon)
            _widget=self._closeButton
            self._rightIcon.show()

        self.qss.SetPadding(PaddingLeft=_paddingLeft,PaddingRight=_paddingRight)
        self._qssplus.ApplyQss()

    def _Colorin(self,animation_:bool=True):
        self.__ShowCloseButton()

        _colorlist=GradientColorList()
        _colorlist.AddColor(0,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(0.94,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(0.95,Color_(ColorStyle.ThemeColorBackground,20,Rshift=-10,Bshift=3))
        _colorlist.AddColor(1,Color_(ColorStyle.ThemeColorBackground,20,Rshift=-10,Bshift=3))

        self._backgroundcolor.SetColorlist(_colorlist,True)

    def _Colorout(self,animation_:bool=True):
        self.__ShowCloseButton()

        _colorlist=GradientColorList()
        _colorlist.AddColor(0,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(0.94,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(0.95,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))
        _colorlist.AddColor(1,Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))

        self._backgroundcolor.SetColorlist(_colorlist,True)

    def _ColorDisable(self,animation_:bool=True):
        _colorlist=GradientColorList()
        _colorlist.AddColor(0,Color_(ColorStyle.FullColor,20,Rshift=-10,Bshift=3))
        _colorlist.AddColor(0.94,Color_(ColorStyle.FullColor,20,Rshift=-10,Bshift=3))
        _colorlist.AddColor(0.95,Color_(ColorStyle.FullColor,20,Rshift=-10,Bshift=3))
        _colorlist.AddColor(1,Color_(ColorStyle.FullColor,20,Rshift=-10,Bshift=3))

        self.qss.SetColor(Color_(ColorStyle.FullColor,50))
        self._backgroundcolor.SetColorlist(_colorlist,True)

    def contextMenuEvent(self, e):
        self.SetMenu()
        LineEditMenu(self).ExecPos(e.globalPos()+QPoint(0,10),Opacity=True,MoveMultiple=0.3,Duration=300)
       
    def SetIcon_(self, 
                 Icon_:Union[Icon,str]=None,
                 IconSize:QSize=QSize(16,16),
                 IconFrameSize:QSize=None,
                 IconPosition:Position=Position.LEFT,
                 IconAngle:int=None):
        '''
        设置单图标,如已经设置多图标会直接替换

        Icon_: Icon:内置svg图标,str:svg,icon,png文件路径,None为删除图标
        IconSize:图标大小
        IconFrameSize:图标边框大小,None为和图标大小
        IconPosition:图标位置,只支持LEFT、RIGHT
        IconAngle:图标旋转角度

        图标颜色,跟随按钮color值
        '''

        if Icon_ is None:
            if self._icon is not None:#删除图标
                self._icon.deleteLater()
                self._qssplus.colorchanged.disconnect(self.__IconColorChangeEvent)
                self._icon=None
                self._iconPadding=0

            self.__SetPadding()
            return
        
        if self._icon is None:
            #图标颜色
            _iconcolor=Color_(self._qssplus.GetColor())
            self._qssplus.colorchanged.connect(self.__IconColorChangeEvent)
            #加载图标
            self._icon=IconView(Icon_,_iconcolor,IconSize,IconAngle,self)
            self._icon.SetMousePenetration(True)
        elif isinstance(self._icon,IconViews):
            #删除原有多图标
            self._icon.deleteLater()
            #图标颜色
            _iconcolor=Color_(self._qssplus.GetColor())
            #加载图标
            self._icon=IconView(Icon_,_iconcolor,IconSize,IconAngle,self)
            self._icon.SetMousePenetration(True)
        else:
            self._icon.SetIcon(Icon_)
            self._icon.SetIconSize(IconSize)
            self._icon.SetIconAngle(IconAngle)
        
        if IconFrameSize is None:
            self._icon.setFixedSize(IconSize)
        else:
            self._icon.setFixedSize(IconFrameSize)

        #同步参数
        self._iconPosition=IconPosition
        #设置图标位置
        self._iconPadding=self._icon.width()+3
        self.__SetPadding()

    def SetIcons_(self,  
                 Open:bool=True,
                 IconFrameSize:QSize=QSize(16,16),
                 IconPosition:Position=Position.LEFT,
                 MovePosition:Position=Position.NONE,
                 Opacity:bool=False,
                 EasingCurve:QEasingCurve=QEasingCurve.InSine,
                 Duration:int = 600):
        
        '''
        设置多图标,如已经设置单图标会直接替换

        Open:True为打开图标,False为关闭图标
        IconFrameSize:图标框大小
        IconPosition:图标位置,只支持LEFT、RIGHT
        MovePosition:图标移动位置
        Opacity:图标是否透明
        EasingCurve:图标切换动画
        Duration:图标切换动画持续时间

        图标颜色,跟随按钮color值

        图标加载
        self.IconsAdd()

        图标切换
        self._icon.next/self._icon.before/self._icon.go(index)
        '''
        if Open == False:
            if self._icon is not None:#删除图标
                self._icon.deleteLater()
                self._qssplus.colorchanged.disconnect(self.__IconColorChangeEvent)
                self._icon=None
                self._iconPadding=0
            
            self.__SetPadding()
            return
        
        if self._icon is None:
            #加载图标
            self._icon=IconViews(MovePosition,Opacity,EasingCurve,Duration,self)
            self._qssplus.colorchanged.connect(self.__IconColorChangeEvent)
            self._icon.SetMousePenetration(True)
        elif isinstance(self._icon,IconView):
            #删除单图标
            self._icon.deleteLater()
            self._icon=IconViews(MovePosition,Opacity,EasingCurve,Duration,self)
            self._icon.SetMousePenetration(True)
        else:
            self._icon.SetAnimationType(EasingCurve,Duration)
            self._icon._moveposition=MovePosition
            self._icon._opacity=Opacity

        self._icon.setFixedSize(IconFrameSize)

        #同步参数
        self._iconPosition=IconPosition
        #插入控件
        if self._iconPosition==Position.LEFT:
            self.layouts.insertWidget(0,self._icon)
        elif self._iconPosition==Position.RIGHT:
            self.layouts.insertWidget(-1,self._icon)

        self._iconPadding=self._icon.width()+8
        self.__SetPadding()
 
    def IconsAdd(self,Icon_:Union[Icon,str],Size:QSize=QSize(16,16),Angle:int=None):
        '''
        Icon_: Icon:内置svg图标,str:svg,icon,png文件路径
        Size:图标大小
        Angle:图标旋转角度

        图标颜色,跟随按钮color值
        '''
        if self._icon is None:
            return
        
        if isinstance(self._icon,IconViews):
            _iconcolor=Color_(self._qssplus.GetColor())
            self._icon.AddIcon(Icon_,_iconcolor,Size,Angle)   

    def __IconColorChangeEvent(self,Color:QColor):
        '''
        只适用Icon为IconView的情况
        '''
        if isinstance(self._icon,IconView) or isinstance(self._icon,IconViews):
            self._icon.SetIconColor(Color_(Color))  
    
    def SetCloseButton(self,Show:bool=True):
        '''
        设置清空按钮
        Show:是否显示
        '''
        if Show and self._closeButton==None:
            self._closeButton=LineEditButton()
            self._closeButton.SetIcon_(Icon.close,QSize(12,12))
            self._closeButton.setToolTip("删除")
            self._closeButton.clicked.connect(lambda: self.setText(""))
            self._closePadding=20
        elif Show==False and self._closeButton!=None:
            self._closeButton.deleteLater()
            self._closeButton=None
            self._closePadding=0

        self.__SetPadding()

    def __ShowCloseButton(self,):
        if self.text()!="" and self.isReadOnly()==False:
            self.SetCloseButton()
        else:
            self.SetCloseButton(False)

    def SetAddLink(self,Title:str,Link:str,Filter:str,File:bool=False,Show:bool=True):
        '''
        设置添加路径按钮

        Title:文件浏览器标题
        Link:文件浏览器默认路径  
        Filter:文件浏览器过滤器

        Filter格式:Images (*.png *.xpm *.jpg);;Text files (*.txt);;XML files (*.xml)
        '''
        if Show and self._addlinkButton==None:
            self._addlinkTitle=Title
            self._addlinkLink=Link
            self._addlinkFilter=Filter
            self._addlinkFile=File

            self._addlinkButton=LineEditButton()
            self._addlinkButton.SetIcon_(Icon.add,QSize(12,12))
            self._addlinkButton.setToolTip("载入路径")
            self._addlinkButton.clicked.connect(self.__LoadLink)
            self._addlinkPadding=20
        elif Show==False and self._addlinkButton!=None:
            self._addlinkButton.deleteLater()
            self._addlinkButton=None
            self._addlinkPadding=0

        self.__SetPadding()

    def __LoadLink(self):
        if self._addlinkFile:#文件夹
            path = QFileDialog.getExistingDirectory(self,
                    self._addlinkTitle,
                    self._addlinkLink)
            if path != "":
                self.setText(path)
                self.loadlinked.emit(path)

        else: #文件
            path, ok = QFileDialog.getOpenFileName(self,
                    self._addlinkTitle,
                    self._addlinkLink,
                    self._addlinkFilter)
            if ok:
                self.setText(path)
                self.loadlinked.emit(path)

    def SetPasswordMode(self,Show:bool=True):
        '''
        设置密码模式按钮

        Show:是否显示
        '''
        if Show and self._passwordButton==None:
            self._passwordButton=LineEditButton()
            self._passwordButton.SetIcons_(True,QSize(12,12))
            self._passwordButton.IconsAdd(Icon.eyehide,QSize(12,12))
            self._passwordButton.IconsAdd(Icon.eyeshow,QSize(12,12))
            self._passwordButton.setToolTip("显示密码")
            self._passwordButton.clicked.connect(self.__PasswordModeChange)
            self.setEchoMode(QLineEdit.Password)
    
            self._passwordPadding=20
        elif Show==False and self._passwordButton!=None:
            self._passwordButton.deleteLater()
            self._passwordButton=None
            self._passwordPadding=0

        self.__SetPadding()

    def __PasswordModeChange(self):
        if self.echoMode()==QLineEdit.Password:
            self._passwordButton._icon.Go(1)
            self.setEchoMode(QLineEdit.Normal)
            self._passwordButton.setToolTip("隐藏密码")
        elif self.echoMode()==QLineEdit.Normal:
            self._passwordButton._icon.Go(0)
            self.setEchoMode(QLineEdit.Password)
            self._passwordButton.setToolTip("显示密码")

    def ReSetIcon(self,Icon_:Union[Icon,str],Index:int=None):
        '''
        设置图标名称

        Icon_: Icon:内置svg图标,str:svg,icon,png文件路径
        Index:图标索引,必须索引

        Index:Icon为IconViews特有,IconView忽略此参数
        '''
        if isinstance(self._icon,IconView):
            self._icon.SetIcon(Icon_)
        elif isinstance(self._icon,IconViews):
            self._icon.SetIcon(Icon_,Index) 

    def ReSetIconSize(self,IconSize:QSize,Index:int=None):
        '''
        设置图标大小

        IconSize:图标大小
        Index:图标索引,None是所有图标

        Index:Icon为IconViews特有,IconView忽略此参数
        '''
        if isinstance(self._icon,IconView):
            self._icon.SetIconSize(IconSize)
        elif isinstance(self._icon,IconViews):
            self._icon.SetIconSize(IconSize,Index) 
           
    def ReSetIconAngle(self,IconAngle:int,Index:int=None):
        '''
        设置图标旋转角度

        IconAngle:图标旋转角度
        Index:图标索引,None是所有图标

        Index:Icon为IconViews特有,IconView忽略此参数
        '''
        if isinstance(self._icon,IconView):
            self._icon.SetIconAngle(IconAngle)
        elif isinstance(self._icon,IconViews):
            self._icon.SetIconAngle(IconAngle,Index) 

    def ReSetIconFrameSize(self,IconFrameSize:QSize):

        '''
        设置图标边框大小
        '''

        self._icon.setFixedSize(IconFrameSize)

        #设置图标位置
        self._iconPadding=self._icon.width()+3
        self.__SetPadding()

    def ReSetIconPosition(self,IconPosition:Position):
        '''
        设置图标位置,只能left、right
        '''
        self._iconPosition=IconPosition
        self.__SetPadding()
    
    def SetRightIcon(self, 
                 Icon_:Union[Icon,str]=None,
                 IconSize:QSize=QSize(16,16),
                 IconAngle:int=None):
        '''
        设置右边图标
        Icon_: Icon:内置svg图标,str:svg,icon,png文件路径
        IconSize:图标大小
        IconAngle:图标旋转角度

        图标颜色,跟随按钮color值
        '''
        if Icon_ is None:
            if self._rightIcon is not None:#删除图标
                self._rightIcon.deleteLater()
                self._rightIcon=None
                self._rightIconPadding=0
            
            self.__SetLayout()
            return
        
        if self._rightIcon is None:
            #加载图标
            self._rightIcon=LineEditButton()
            self._rightIcon.SetIcon_(Icon_,IconSize,IconAngle=IconAngle)

        self._rightIcon.setFixedSize(QSize(20,20))
        #同步参数
        self._rightIconPadding=self._rightIcon.width()+3

        self.__SetPadding()




    
