from PySide6.QtCore import Signal,QPoint,Qt,QSize,QObject,QEasingCurve,QRect
from PySide6.QtGui import QColor, QKeyEvent, QResizeEvent
from PySide6.QtWidgets import QPushButton,QHBoxLayout,QVBoxLayout,QWidget

from qss import QssPlusClass,ColorStyle,BorderStyle,Font_,FontSize
from lib import CountDown,ShadowEffect,Position,Color_,GetFontName,QcolorToStr

from typing import Union

from ..tooltip import ToolTipFilter
from ..icon import IconView,IconViews,Icon
from ..label import LabelNormal,ShortCutLabel

class ButtonBase(QPushButton,QssPlusClass,CountDown):
    def __init__(self,Text:str="",objectName:str="button",EventFollow: bool = True,parent=None):
        super(ButtonBase, self).__init__(parent=parent)
        #安装事件筛选
        self.installEventFilter(ToolTipFilter(self))
        #倒计时事件初始化
        self.CountDownLoad(self)
        #控件加载
        self._text=None
        self._textCache=self.text()  #文本缓存
        self._textAlignment=Qt.AlignCenter

        self._icon=None
        self._iconFrameSize=None
        self._iconPosition=Position.NONE  #只支持None、left、right、top、bottom
        self._iconPositionShift=0  #icon的偏移量
        self._iconClickMove=True
        self._iconClickPosition=None
        
        #右边图标,适用于menu,list情况,一般加载箭头
        self._rightIcon=None  
        self._rightIconSize=None
        self._rightIconShift=0  #icon的偏移量

        self._shortCut=None
        self._shortCutCache=""  #快捷键缓存

        self._spacing=0 #控件的间隔
        
        #给radiobox或者checkbox加载显示控件
        self._leftWidget=None
        self._leftWidgetShift=0

        self._rightWidget=None
        self._rightWidgetShift=0
        
        #字体跟随
        self._fontfollow=False
        self._fonttext=GetFontName()

        self.QssApply(self,objectName,True,EventFollow)

        #空格事件
        self.mousepressed.connect(self.__PressEvent)
        self.mousereleaseed.connect(self.__ReleaseEvent)
        self.keypressed.connect(self.__PressEvent)
        self.keyreleaseed.connect(self.__ReleaseEvent)

        self.__SetLayout()
        self.SetText(Text)
    
    def __SetLayout(self):
        _shortkeyShift=5 #快捷键的偏移量

        # print(self._icon,self._shortCut,self._rightIcon)
        
        #图标、快捷键、右图标、左控件都没有加载
        if self._icon==None and self._shortCut is None and self._rightIcon is None and self._leftWidget is None and self._rightWidget is None:

            if self._text is not None:#删除文本控件
                self._text.deleteLater()
                self._text=None

            self.setText(self._textCache)

            return
        
        #优先级 右图标>左控件>图标>快捷键>文本

        #可用区域
        _UseGeometry=QRect(0,0,self.width(),self.height())
        
        #右图标加载
        if self._rightIcon is not None:
            self._rightIcon.setFixedSize(self._rightIconSize)
            self._rightIcon.move(_UseGeometry.width()-self._rightIcon.width()-self._rightIconShift,\
                                 int((_UseGeometry.height()-self._rightIcon.height())/2))
            self._rightIcon.show()

            #重新计算可用区域
            _UseGeometry=QRect(_UseGeometry.x(),_UseGeometry.y(),self._rightIcon.x(),self.height())
        
        #左控件加载
        if self._leftWidget is not None:
            self._leftWidget.move(self._leftWidgetShift,int((_UseGeometry.height()-self._leftWidget.height())/2))
            self._leftWidget.show()
        
            #重新计算可用区域
            _UseGeometry=QRect(self._leftWidget.x()+self._leftWidget.width(),_UseGeometry.y(),_UseGeometry.width(),_UseGeometry.height())

        #右控件加载
        if self._rightWidget is not None:
            self._rightWidget.move(_UseGeometry.width()-self._rightWidget.width()-self._rightWidgetShift,\
                                 int((_UseGeometry.height()-self._rightWidget.height())/2))
            self._rightWidget.show()
        
            #重新计算可用区域
            _UseGeometry=QRect(_UseGeometry.x(),_UseGeometry.y(),self._rightWidget.x(),self.height())

        #图标加载
        if self._icon is not None:
            if self._iconPosition==Position.NONE:#铺满显示,后续不加载快捷键和文本
                if self._leftWidget is not None:
                    self._icon.move(_UseGeometry.x()+self._spacing,_UseGeometry.y())
                else:
                    self._icon.move(_UseGeometry.x(),_UseGeometry.y())

                if self._rightIcon is not None:
                    self._icon.setFixedSize(_UseGeometry.width()-self._icon.x()-self._spacing,_UseGeometry.height())
                else:   
                    self._icon.setFixedSize(_UseGeometry.width()-self._icon.x(),_UseGeometry.height())
  
            else:

                self._icon.setFixedSize(self._iconFrameSize)

                if self._iconPosition==Position.LEFT:#靠左显示
                    self._icon.move(_UseGeometry.x()+self._iconPositionShift,int((_UseGeometry.height()-self._icon.height())/2))

                    #重新计算可用区域
                    _UseGeometry=QRect(self._icon.x()+self._icon.width(),_UseGeometry.y(),_UseGeometry.width(),_UseGeometry.height())

                elif self._iconPosition==Position.RIGHT:#靠右显示
                    self._icon.move(_UseGeometry.width()-self._icon.width()-self._iconPositionShift,int((_UseGeometry.height()-self._icon.height())/2))

                    #重新计算可用区域
                    _UseGeometry=QRect(_UseGeometry.x(),_UseGeometry.y(),self._icon.x(),_UseGeometry.height())

                elif self._iconPosition==Position.TOP:#靠上显示
                    self._icon.move(_UseGeometry.x()+int((_UseGeometry.width()-_UseGeometry.x()-self._icon.width())/2),_UseGeometry.y()+self._iconPositionShift)

                    #重新计算可用区域
                    _UseGeometry=QRect(_UseGeometry.x(),_UseGeometry.y()+self._iconPositionShift,_UseGeometry.width(),_UseGeometry.height())
 
                elif self._iconPosition==Position.BOTTOM:#靠下显示
                    self._icon.move(_UseGeometry.x()+int((_UseGeometry.width()-_UseGeometry.x()-self._icon.width())/2),
                                    _UseGeometry.height()-self._icon.height()-self._iconPositionShift)

                    #重新计算可用区域
                    _UseGeometry=QRect(_UseGeometry.x(),_UseGeometry.y(),_UseGeometry.width(),self._icon.y())
         
            self._icon.show()
              
        #快捷键
        if self._shortCut is not None:
            if self._icon is not None and self._iconPosition==Position.NONE:
                self._shortCutCache=self.GetShortCutName()
                self.SetShortCut(None)
            else:
                self._shortCut.move(_UseGeometry.width()-self._shortCut.width()-_shortkeyShift,\
                                    int(_UseGeometry.y()+(_UseGeometry.height()-_UseGeometry.y()-self._shortCut.height())/2))
                
                self._shortCut.show()
                
                _UseGeometry=QRect(_UseGeometry.x(),_UseGeometry.y(),self._shortCut.x(),_UseGeometry.height())

        #文本
        if self._icon is not None and self._iconPosition==Position.NONE:
            if self._text is None :
                return
            else:
                self._text.deleteLater()
                self._text=None
                self.setText(self._textCache)
        else:
            if self._text is None :
                self.__AddText()

            self._text.move(_UseGeometry.x()+self._spacing,_UseGeometry.y()+self._spacing)

            self._text.setFixedSize(_UseGeometry.width()-self._text.x()-self._spacing,_UseGeometry.height()-self._text.y()-self._spacing)
            self.setText(self._textCache)
            self._text.show()

    def __PressEvent(self):
        if self._text is not None:
            self._text.move(self._text.pos()+QPoint(1,1))
        if self._icon is not None and self._iconClickMove:
            if self._iconClickPosition==None:
                self._icon.move(self._icon.pos()+QPoint(1,1))
            elif self._iconClickPosition==Position.LEFT:
                self._icon.move(self._icon.pos()-QPoint(1,0))
            elif self._iconClickPosition==Position.TOP:
                self._icon.move(self._icon.pos()-QPoint(0,1))
            elif self._iconClickPosition==Position.RIGHT:
                self._icon.move(self._icon.pos()+QPoint(1,0))
            elif self._iconClickPosition==Position.BOTTOM:
                self._icon.move(self._icon.pos()+QPoint(0,1))
        if self._shortCut is not None:
            self._shortCut.move(self._shortCut.pos()+QPoint(1,1))
 
    def __ReleaseEvent(self):
        if self._text is not None:
            self._text.move(self._text.pos()-QPoint(1,1))
        if self._icon is not None and self._iconClickMove:
            if self._iconClickPosition==None:
                self._icon.move(self._icon.pos()-QPoint(1,1))
            elif self._iconClickPosition==Position.LEFT:
                self._icon.move(self._icon.pos()+QPoint(1,0))
            elif self._iconClickPosition==Position.TOP:
                self._icon.move(self._icon.pos()+QPoint(0,1))
            elif self._iconClickPosition==Position.RIGHT:
                self._icon.move(self._icon.pos()-QPoint(1,0))
            elif self._iconClickPosition==Position.BOTTOM:
                self._icon.move(self._icon.pos()-QPoint(0,1))
        if self._shortCut is not None:
            self._shortCut.move(self._shortCut.pos()-QPoint(1,1))

    def SetShadow(self,Shadow:bool=True):
        '''
        设置阴影
        
        Shadow:是否显示阴影
        '''
        if Shadow:
            self.shadow=ShadowEffect(Color_(ColorStyle.FullColor,20),10,QPoint(0,2))
        else:
            self.shadow=None
        self.setGraphicsEffect(self.shadow)
  
    def SetSpacing(self,Spacing:int=0):
        '''
        设置控件的间隔
        
        Spacing:间隔大小
        '''
        self._spacing=Spacing
        self.__SetLayout()

    def SetShortCut(self,ShortCut:str=None):
        '''
        设置快捷键

        ShortCut:快捷键文本,例如Ctrl+A,None为删除快捷键
        '''
        if ShortCut is None:
            if self._shortCut is not None: #删除快捷键
                self._shortCut.SetShortcut_(None)
                self._shortCut.deleteLater()
                self._shortCut=None
            self.__SetLayout()
            return
        
        if self._icon is not None and self._iconPosition==Position.NONE:
            self._shortCutCache=ShortCut
            return
        
        if ShortCut is not None and self._shortCut is None:
            self._shortCut=ShortCutLabel(ShortCut,self)

            self._shortCut.shortcutpressed.connect(self.clicked.emit)
        elif ShortCut is not None and self._shortCut is not None:
            self._shortCut.SetShortcut_(ShortCut)

        self._shortCutCache="" 

        self.__SetLayout()

    def GetShortCutName(self):
        '''
        获取快捷键文本
        '''
        if self._shortCut is not None:
            return self._shortCut._shortCut.key().toString().title()
        return ""
           
    def SetIcon_(self, 
                 Icon_:Union[Icon,str]=None,
                 IconSize:QSize=QSize(16,16),
                 IconFrameSize:QSize=None,
                 IconPosition:Position=Position.NONE,
                 IconPositionShift:int=5,
                 IconAngle:int=None):
        '''
        设置单图标,如已经设置多图标会直接替换

        Icon_: Icon:内置svg图标,str:svg,icon,png文件路径,None为删除图标
        IconSize:图标大小
        IconFrameSize:图标框大小,None为和图标大小
        IconPosition:图标位置,只支持NONE、LEFT、RIGHT、TOP、BOTTOM,NONE是不显示文本
        IconPositionShift:图标位置偏移IconPosition.NONE忽略此参数
        IconAngle:图标旋转角度

        图标颜色,跟随按钮color值
        '''

        if Icon_ is None:
            if self._icon is not None:#删除图标
                self._icon.deleteLater()
                self._qssplus.colorchanged.disconnect(self.__IconColorChangeEvent)
                self._icon=None
            if self._shortCutCache!="" and self._shortCut is None:
                self.SetShortCut(self._shortCutCache)
            self.__SetLayout()
            return
        
        if self._icon is None:
            #图标颜色
            _iconcolor=Color_(self._qssplus.GetColor())
            self._qssplus.colorchanged.connect(self.__IconColorChangeEvent)
            #加载图标
            self._icon=IconView(Icon_,_iconcolor,IconSize,IconAngle,self)
            self._icon.SetMousePenetration(True)
        elif isinstance(self._icon,IconViews):
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

        #同步参数

        if IconFrameSize is not None:
            self._iconFrameSize=IconFrameSize
        elif self._iconFrameSize is None:
            self._iconFrameSize=IconSize
 
        self._iconPosition=IconPosition
        self._iconPositionShift=IconPositionShift

        self.__SetLayout()

    def __IconColorChangeEvent(self,Color:QColor):
        '''
        只适用Icon为IconView的情况
        '''
        if isinstance(self._icon,IconView) or isinstance(self._icon,IconViews):
            self._icon.SetIconColor(Color_(Color))

    def SetIcons_(self,  
                 Open:bool=True,
                 IconFrameSize:QSize=QSize(16,16),
                 IconPosition:Position=Position.NONE,
                 IconPositionShift:int=5,
                 MovePosition:Position=Position.NONE,
                 Opacity:bool=False,
                 EasingCurve:QEasingCurve=QEasingCurve.InSine,
                 Duration:int = 600):
        
        '''
        设置多图标,如已经设置单图标会直接替换

        Open:True为打开图标,False为关闭图标
        IconFrameSize:图标框大小
        IconPosition:图标位置,只支持NONE、LEFT、RIGHT、TOP、BOTTOM,NONE是不显示文本
        IconPositionShift:图标位置偏移IconPosition.NONE忽略此参数
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
            if self._shortCutCache!="" and self._shortCut is None:
                self.SetShortCut(self._shortCutCache)
            self.__SetLayout()
            return
        
        if self._icon is None:
            #加载图标
            self._icon=IconViews(MovePosition,Opacity,EasingCurve,Duration,self)
            self._qssplus.colorchanged.connect(self.__IconColorChangeEvent)
            self._icon.SetMousePenetration(True)
        elif isinstance(self._icon,IconView):
            self._icon.deleteLater()
            self._icon=IconViews(MovePosition,Opacity,EasingCurve,Duration,self)
            self._icon.SetMousePenetration(True)

        #同步参数
        self._iconFrameSize=IconFrameSize
        self._iconPosition=IconPosition
        self._iconPositionShift=IconPositionShift

        self.__SetLayout()

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

    def SetIconColorFollow(self,IconColorFollow:bool=True,Index:int=None):
        '''
        设置图标被disable时颜色是否跟随

        IconColorFollow:开启跟随icon颜色,关闭不跟随
        Index:图标索引,None是所有图标,
        
        Index:Icon为IconViews特有,IconView忽略此参数

        '''
        if isinstance(self._icon,IconView):
            self._icon.SetIconColorFollow(IconColorFollow)
        elif isinstance(self._icon,IconViews):
            self._icon.SetIconColorFollow(IconColorFollow,Index) 

    def SetIconClickMove(self,ClickMove:bool=True):
        '''
        设置图标被点击时是否移动

        ClickMove:开启移动,关闭不移动
        '''
        self._iconClickMove=ClickMove

    def SetIconClickPositon(self,ClickPosition:Position=None):
        '''
        设置图标被点击时移动位置

        ClickPosition:图标被点击时移动位置,只能设置None、left、right、top、bottom
        '''
        self._iconClickPosition=ClickPosition

    def SetIconClickPositonShift(self,ClickPositionShift:Position):
        '''
        设置图标被点击时移动位置偏移

        ClickPositionShift:图标被点击时移动位置偏移
        '''
        self._iconClickPositionShift=ClickPositionShift

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
        self._iconFrameSize=IconFrameSize
        self.__SetLayout()

    def ReSetIconPosition(self,IconPosition:Position):
        '''
        设置图标位置
        '''
        self._iconPosition=IconPosition
        if IconPosition!=Position.NONE and self._shortCutCache!="" and self._shortCut is None:
            self.SetShortCut(self._shortCutCache)
        self.__SetLayout()
    
    def ReSetIconPositionShift(self,IconPositionShift:int):
        '''
        设置图标位置偏移
        '''
        self._iconPositionShift=IconPositionShift
        self.__SetLayout()

    def SetRightIcon(self, 
                 Icon_:Union[Icon,str]=None,
                 IconSize:QSize=QSize(16,16),
                 IconPositionShift:int=5,
                 IconAngle:int=None):
        '''
        设置右边图标
        Icon_: Icon:内置svg图标,str:svg,icon,png文件路径
        IconSize:图标大小
        IconPositionShift:图标位置偏移IconPosition.NONE忽略此参数
        IconAngle:图标旋转角度

        图标颜色,跟随按钮color值
        '''

        if Icon_ is None:
            if self._rightIcon is not None:#删除图标
                self._rightIcon.deleteLater()
                self._qssplus.colorchanged.disconnect(self.__RightIconColorChangeEvent)
                self._rightIcon=None
            if self._shortCutCache!="" and self._shortCut is None:
                self.SetShortCut(self._shortCutCache)
            self.__SetLayout()
            return
        
        if self._rightIcon is None:
            #图标颜色
            _iconcolor=Color_(self._qssplus.GetColor())
            self._qssplus.colorchanged.connect(self.__RightIconColorChangeEvent)
            #加载图标
            self._rightIcon=IconView(Icon_,_iconcolor,IconSize,IconAngle,self)
            self._rightIcon.SetMousePenetration(True)
        else:
            self._rightIcon.SetIcon(Icon_)
            self._rightIcon.SetIconSize(IconSize)
            self._rightIcon.SetIconAngle(IconAngle)

        #同步参数
        self._rightIconSize=IconSize
        self._rightIconShift=IconPositionShift

        self.__SetLayout()

    def SetLeftWidget(self,Widget:QWidget,LeftWidgetShift:int=5):
        '''
        加载左边控件
        '''
        if Widget is not None:
            Widget.setParent(self)

        if  self._leftWidget is not None:
            self._leftWidget.deleteLater()

        self._leftWidget=Widget
        self._leftWidgetShift=LeftWidgetShift
        self.__SetLayout()

    def SetRigthWidget(self,Widget:QWidget,RightWidgetShift:int=5):
        '''
        加载左边控件
        '''
        if Widget is not None:
            Widget.setParent(self)

        if  self._rightWidget is not None:
            self._rightWidget.deleteLater()
            
        self._rightWidget=Widget
        self._rightWidgetShift=RightWidgetShift
        self.__SetLayout()

    def SetTextAlignment(self,TextAlignment):
        '''
        设置文本对齐方式
        '''
        self._textAlignment=TextAlignment
        if self._text is not None:
            self._text.setAlignment(self._textAlignment)

    def __RightIconColorChangeEvent(self,Color:QColor):
        '''
        只适用Icon为IconView的情况
        '''
        if isinstance(self._rightIcon,IconView):
            self._rightIcon.SetIconColor(Color_(Color))
  
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__SetLayout()
        return super().resizeEvent(event)
    
    def __AddText(self):
        self.setText("")
        self._text=LabelNormal(self._textCache,self)
        self._text.setAlignment(self._textAlignment)

    def SetText(self, text: str) -> None:
        self._textCache=text
        self.setText(text)
    
    def setText(self, text: str) -> None:
        if self._text is not None:
            self._text.setText(text)
            self._text.adjustSize()
            return super().setText("")
        if self._icon is not None and self._iconPosition==Position.NONE:
            return super().setText("")
        return super().setText(text)
    
    def text(self) -> str:
        if self._text is not None:
            return self._text.text()
        return super().text()

class ButtonNormal(ButtonBase):
    '''
    普通按钮
    '''
    def __init__(self,Text:str="",parent=None):
        super(ButtonNormal, self).__init__(Text=Text,objectName="ButtonNormal",parent=parent)

    def SetTempLightqss(self):
        self._TempLightqss.SetFont(Font_(FontSize=FontSize(Shift=0,Min=10,Max=20)))
        self._TempLightqss.SetBorderWidth(Width=1)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBorderRadius(Radius=5)
        self._TempLightqss.SetBorderColor(Color=Color_(ColorStyle.FullColor,10))
        self._TempLightqss.SetBorderColor(ColorBottom=Color_(ColorStyle.FullColor,20))
        self._TempLightqss.SetPadding(Padding=5)
        self._TempLightqss.Set_("outline","none")

    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()

        self._NormalLightqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._NormalLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,2,Rshift=-10,Bshift=3))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()

        self._HoverLightqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._HoverLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,7,Rshift=-10,Bshift=3))

    def SetPressLightqss(self):
        self._PressLightqss=self._TempLightqss.Copy()

        self._PressLightqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._PressLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,12,Rshift=-10,Bshift=3))
        self._PressLightqss.SetPadding(6,5,5,6)

    def SetCheckHoverLightqss(self):
        self._CheckHoverLightqss=self._TempLightqss.Copy()

        self._CheckHoverLightqss.SetColor(Color_(ColorStyle.Light))
        self._CheckHoverLightqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,10))

    def SetCheckNormalLightqss(self):
        self._CheckNormalLightqss=self._TempLightqss.Copy()

        self._CheckNormalLightqss.SetColor(Color_(ColorStyle.Light))
        self._CheckNormalLightqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,100))

    def SetDisabledLightqss(self):
        self._DisabledLightqss=self._TempLightqss.Copy()

        self._DisabledLightqss.SetColor(Color_(ColorStyle.FullColor,50))
        self._DisabledLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,20))

    def SetTempDarkqss(self):
        self._TempDarkqss.SetFont(Font_(FontSize=FontSize(Shift=0,Min=10,Max=20)))
        self._TempDarkqss.SetBorderWidth(Width=1)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.SetBorderRadius(Radius=5)
        self._TempDarkqss.SetBorderColor(Color=Color_(ColorStyle.FullColor,10))
        self._TempDarkqss.SetBorderColor(ColorBottom=Color_(ColorStyle.FullColor,20))
        self._TempDarkqss.SetPadding(Padding=5)
        self._TempDarkqss.Set_("outline","none")

    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempDarkqss.Copy()

        self._NormalDarkqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._NormalDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,5))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempDarkqss.Copy()

        self._HoverDarkqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._HoverDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,10))

    def SetPressDarkqss(self):
        self._PressDarkqss=self._TempDarkqss.Copy()

        self._PressDarkqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._PressDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,15))
        self._PressDarkqss.SetPadding(6,5,5,6)

    def SetCheckHoverDarkqss(self):
        self._CheckHoverDarkqss=self._TempDarkqss.Copy()

        self._CheckHoverDarkqss.SetColor(Color_(ColorStyle.Dark))
        self._CheckHoverDarkqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,10))

    def SetCheckNormalDarkqss(self):
        self._CheckNormalDarkqss=self._TempDarkqss.Copy()

        self._CheckNormalDarkqss.SetColor(Color_(ColorStyle.Dark))
        self._CheckNormalDarkqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,100))

    def SetDisabledDarkqss(self):
        self._DisabledDarkqss=self._TempDarkqss.Copy()

        self._DisabledDarkqss.SetColor(Color_(ColorStyle.FullColor,50))
        self._DisabledDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,20))
      
class ButtonTheme(ButtonBase):
    '''
    主题按钮
    '''
    def __init__(self,Text:str="",parent=None):
        super(ButtonTheme, self).__init__(Text=Text,objectName="ButtonTheme",parent=parent)

    def SetTempLightqss(self):
        self._TempLightqss.SetFont(Font_(FontSize=FontSize(Shift=0,Min=10,Max=20)))
        self._TempLightqss.SetBorderWidth(Width=1)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBorderRadius(Radius=5)
        self._TempLightqss.SetBorderColor(Color=Color_(ColorStyle.FullThemeColor,10))
        self._TempLightqss.SetBorderColor(ColorBottom=Color_(ColorStyle.FullThemeColor,20))
        self._TempLightqss.SetPadding(Padding=5)
        self._TempLightqss.Set_("outline","none")

    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()

        self._NormalLightqss.SetColor(Color_(ColorStyle.Light))
        self._NormalLightqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,0))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()

        self._HoverLightqss.SetColor(Color_(ColorStyle.Light))
        self._HoverLightqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,10))

    def SetPressLightqss(self):
        self._PressLightqss=self._TempLightqss.Copy()

        self._PressLightqss.SetColor(Color_(ColorStyle.Light))
        self._PressLightqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,5))
        self._PressLightqss.SetPadding(6,5,5,6)

    def SetCheckHoverLightqss(self):
        self._CheckHoverLightqss=self._TempLightqss.Copy()

        self._CheckHoverLightqss.SetColor(Color_(ColorStyle.Light))
        self._CheckHoverLightqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,20))

    def SetCheckNormalLightqss(self):
        self._CheckNormalLightqss=self._TempLightqss.Copy()

        self._CheckNormalLightqss.SetColor(Color_(ColorStyle.Light))
        self._CheckNormalLightqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,10))

    def SetDisabledLightqss(self):
        self._DisabledLightqss=self._TempLightqss.Copy()

        self._DisabledLightqss.SetColor(Color_(ColorStyle.FullColor,50))
        self._DisabledLightqss.SetBackgroundColor(Color_(ColorStyle.FullThemeColor,20))

    def SetTempDarkqss(self):
        self._TempDarkqss.SetFont(Font_(FontSize=FontSize(Shift=0,Min=10,Max=20)))
        self._TempDarkqss.SetBorderWidth(Width=1)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.SetBorderRadius(Radius=5)
        self._TempDarkqss.SetBorderColor(Color=Color_(ColorStyle.FullThemeColor,10))
        self._TempDarkqss.SetBorderColor(ColorBottom=Color_(ColorStyle.FullThemeColor,20))
        self._TempDarkqss.SetPadding(Padding=5)
        self._TempDarkqss.Set_("outline","none")

    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempDarkqss.Copy()

        self._NormalDarkqss.SetColor(Color_(ColorStyle.Light))
        self._NormalDarkqss.SetBackgroundColor(Color_(ColorStyle.ThemeColor,0))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempDarkqss.Copy()

        self._HoverDarkqss.SetColor(Color_(ColorStyle.Light))
        self._HoverDarkqss.SetBackgroundColor(Color_(ColorStyle.ThemeColor,10))

    def SetPressDarkqss(self):
        self._PressDarkqss=self._TempDarkqss.Copy()

        self._PressDarkqss.SetColor(Color_(ColorStyle.Light))
        self._PressDarkqss.SetBackgroundColor(Color_(ColorStyle.ThemeColor,5))
        self._PressDarkqss.SetPadding(6,5,5,6)

    def SetCheckHoverDarkqss(self):
        self._CheckHoverDarkqss=self._TempDarkqss.Copy()

        self._CheckHoverDarkqss.SetColor(Color_(ColorStyle.Light))
        self._CheckHoverDarkqss.SetBackgroundColor(Color_(ColorStyle.ThemeColor,20))

    def SetCheckNormalDarkqss(self):
        self._CheckNormalDarkqss=self._TempDarkqss.Copy()

        self._CheckNormalDarkqss.SetColor(Color_(ColorStyle.Light))
        self._CheckNormalDarkqss.SetBackgroundColor(Color_(ColorStyle.ThemeColor,10))

    def SetDisabledDarkqss(self):
        self._DisabledDarkqss=self._TempDarkqss.Copy()

        self._DisabledDarkqss.SetColor(Color_(ColorStyle.FullColor,50))
        self._DisabledDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,20))

class ButtonTransparent(ButtonBase):
    '''
    透明按钮
    '''
    def __init__(self,Text:str="",parent=None):
        super(ButtonTransparent, self).__init__(Text=Text,objectName="ButtonTransparent",parent=parent)

    def SetTempLightqss(self):
        self._TempLightqss.SetBorderWidth(Width=1)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBorderRadius(Radius=5)
        self._TempLightqss.SetBorderColor(Color=Color_(ColorStyle.FullColor,10))
        self._TempLightqss.SetBorderColor(ColorBottom=Color_(ColorStyle.FullColor,20))
        self._TempLightqss.Set_("outline","none")
  
    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()

        self._NormalLightqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._NormalLightqss.SetBorderColor(Color=Color_(ColorStyle.NullColor,10))
        self._NormalLightqss.SetBorderColor(ColorBottom=Color_(ColorStyle.NullColor,20))
        self._NormalLightqss.SetBackgroundColor(Color_(ColorStyle.NullColor,0,Rshift=-10,Bshift=3))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()

        self._HoverLightqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._HoverLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,7,Rshift=-10,Bshift=3))


    def SetPressLightqss(self):
        self._PressLightqss=self._TempLightqss.Copy()

        self._PressLightqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._PressLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,10,Rshift=-10,Bshift=3))
        self._PressLightqss.SetPadding(1,0,0,1)

    def SetCheckHoverLightqss(self):
        self._CheckHoverLightqss=self._TempLightqss.Copy()

        self._CheckHoverLightqss.SetColor(Color_(ColorStyle.Light))
        self._CheckHoverLightqss.SetBackgroundColor(Color_(ColorStyle.ThemeColor,20))

    def SetCheckNormalLightqss(self):
        self._CheckNormalLightqss=self._TempLightqss.Copy()

        self._CheckNormalLightqss.SetBorderColor(Color=Color_(ColorStyle.NullColor,10))
        self._CheckNormalLightqss.SetBorderColor(ColorBottom=Color_(ColorStyle.NullColor,20))
        self._CheckNormalLightqss.SetColor(Color_(ColorStyle.Light))
        self._CheckNormalLightqss.SetBackgroundColor(Color_(ColorStyle.ThemeColor,10))

    def SetDisabledLightqss(self):
        self._DisabledLightqss=self._TempLightqss.Copy()

        self._DisabledLightqss.SetColor(Color_(ColorStyle.FullColor,50))
        self._DisabledLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,20))

    def SetTempDarkqss(self):
        self._TempDarkqss.SetBorderWidth(Width=1)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.SetBorderRadius(Radius=5)
        self._TempDarkqss.SetBorderColor(Color=Color_(ColorStyle.FullColor,10))
        self._TempDarkqss.SetBorderColor(ColorBottom=Color_(ColorStyle.FullColor,20))
        self._TempDarkqss.Set_("outline","none")
  
    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempDarkqss.Copy()

        self._NormalDarkqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._NormalDarkqss.SetBorderColor(Color=Color_(ColorStyle.NullColor,10))
        self._NormalDarkqss.SetBorderColor(ColorBottom=Color_(ColorStyle.NullColor,20))
        self._NormalDarkqss.SetBackgroundColor(Color_(ColorStyle.NullColor,0))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempDarkqss.Copy()

        self._HoverDarkqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._HoverDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,10))

    def SetPressDarkqss(self):
        self._PressDarkqss=self._TempDarkqss.Copy()

        self._PressDarkqss.SetColor(Color_(ColorStyle.FullColor,100))
        self._PressDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,15))
        self._PressDarkqss.SetPadding(1,0,0,1)

    def SetCheckHoverDarkqss(self):
        self._CheckHoverDarkqss=self._TempDarkqss.Copy()

        self._CheckHoverDarkqss.SetColor(Color_(ColorStyle.Dark))
        self._CheckHoverDarkqss.SetBackgroundColor(Color_(ColorStyle.ThemeColor,20))

    def SetCheckNormalDarkqss(self):
        self._CheckNormalDarkqss=self._TempDarkqss.Copy()

        self._CheckNormalDarkqss.SetBorderColor(Color=Color_(ColorStyle.NullColor,10))
        self._CheckNormalDarkqss.SetBorderColor(ColorBottom=Color_(ColorStyle.NullColor,20))
        self._CheckNormalDarkqss.SetColor(Color_(ColorStyle.Dark))
        self._CheckNormalDarkqss.SetBackgroundColor(Color_(ColorStyle.ThemeColor,10))

    def SetDisabledDarkqss(self):
        self._DisabledDarkqss=self._TempDarkqss.Copy()

        self._DisabledDarkqss.SetColor(Color_(ColorStyle.FullColor,50))
        self._DisabledDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,20))
