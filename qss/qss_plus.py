from PySide6.QtCore import QObject,Signal,QEasingCurve
from PySide6.QtGui import QColor

from lib import Animation,Color_,ColorCache_,IntExcess,FloatExcess,QcolorExcess,QcolorToStr,IsColorEqual,GetFontSize

from .qss_theme import Font_,GradientColor,GradientColorList,FontSize,QssManage,themes
from .qss_type import BorderStyle,TextAlign,TextDecoration

from typing import Union

class QssStyle(QObject):#qss类型
    '''
    Qss类型
    '''
    qsschanged=Signal()#qss改变触发事件
    def __init__(self):
        super(QssStyle, self).__init__()
        self._qsslist={}

    def EventConnect(self):
        self.qsschanged.emit()

    def Set_(self,ItemName:str,Value:Union[str,int,Color_,Font_,GradientColor,BorderStyle,TextDecoration,TextAlign],EventConnect:bool=False):
        '''
        ItemName:qss的名称,如color,background-color等
        Value:ItemName的值
        EventConnet:触发qss事件
        '''
        if Value==None:
            self._qsslist.pop(ItemName)
        else:
            self._qsslist[ItemName]=Value

        if EventConnect:
            self.EventConnect()

    def Copy(self):
        '''
        复制参数
        '''
        _qss=QssStyle()

        for _key, _value in self._qsslist.items():
            if isinstance(_value,Font_) or isinstance(_value,GradientColor):
                _v=_value.Copy()
                _qss.Set_(_key,_v)
            else:
                _qss.Set_(_key,_value)

        return _qss

    def SetColor(self,Color:Union[Color_,GradientColor]=None,EventConnect:bool=False):
        """
        Color:none、Color_、GradientColor
        EventConnect:触发qss事件
        """
        if isinstance(Color,GradientColor):
            Color.qsschanged.connect(self.EventConnect)

        self.Set_("color",Color,EventConnect)
    
    def SetBackgroundColor(self,Color:Union[Color_,GradientColor]=None,EventConnect:bool=False):
        """
        Color:none、Color_、GradientColor
        EventConnect:触发qss事件
        """
        if isinstance(Color,GradientColor):
            Color.qsschanged.connect(self.EventConnect)

        self.Set_("background-color",Color,EventConnect)

    def SetBorderWidth(self,
                        WidthTop:int=None,
                        WidthRight:int=None,
                        WidthBottom:int=None,
                        WidthLeft:int=None,
                        Width:int=None,
                        EventConnect:bool=False):
        '''
        设置边框宽度
        WidthTop:上边框宽度
        WidthRight:右边框宽度
        WidthBottom:下边框宽度
        WidthLeft:左边框宽度
        Width:四边框宽度,设置此参数后忽略WidthTop,WidthRight,WidthBottom,WidthLeft
        EventConnect:触发qss事件
        '''
        if Width!=None:
            self.Set_("border-top-width",Width)
            self.Set_("border-right-width",Width)
            self.Set_("border-bottom-width",Width)
            self.Set_("border-left-width",Width)    
        else:
            if WidthTop!=None:
                self.Set_("border-top-width",WidthTop)
            if WidthRight!=None:
                self.Set_("border-right-width",WidthRight)
            if WidthBottom!=None:
                self.Set_("border-bottom-width",WidthBottom)
            if WidthLeft!=None:
                self.Set_("border-left-width",WidthLeft)

        #触发qss事件
        if EventConnect:
            self.EventConnect()

    def SetBorderStyle(self,
                         StyleTop:BorderStyle=None,
                         StyleRight:BorderStyle=None,
                         StyleBottom:BorderStyle=None,\
                         StyleLeft:BorderStyle=None,
                         Style:BorderStyle=None,
                         EventConnect:bool=False):

        '''
        设置边框类型
        StyleTop:上边框类型
        StyleRight:右边框类型
        StyleBottom:下边框类型
        StyleLeft:左边框类型
        Style:四边框类型,设置此参数后忽略StyleTop,StyleRight,StyleBottom,StyleLeft
        EventConnect:触发qss事件
        '''
        if Style!=None:
            self.Set_("border-top-style",Style)
            self.Set_("border-right-style",Style)
            self.Set_("border-bottom-style",Style)
            self.Set_("border-left-style",Style)
        else:
            if StyleTop!=None:
                self.Set_("border-top-style",StyleTop)
            if StyleRight!=None:
                self.Set_("border-right-style",StyleRight)
            if StyleBottom!=None:
                self.Set_("border-bottom-style",StyleBottom)
            if StyleLeft!=None:
                self.Set_("border-left-style",StyleLeft)
        
        #触发qss事件
        if EventConnect:
            self.EventConnect()

    def SetBorderColor(self,
                          ColorTop:str=None,
                          ColorRight:str=None,
                          ColorBottom:str=None,\
                          ColorLeft:str=None,
                          Color:str=None,
                          EventConnect:bool=False):
        
        '''
        设置边框颜色
        ColorTop:上边框颜色
        ColorRight:右边框颜色
        ColorBottom:下边框颜色
        ColorLeft:左边框颜色
        Color:四边框颜色,设置此参数后忽略ColorTop,ColorRight,ColorBottom,ColorLeft
        EventConnect:触发qss事件
        '''
        if Color!=None:
            self.Set_("border-top-color",Color)
            self.Set_("border-right-color",Color)
            self.Set_("border-bottom-color",Color)
            self.Set_("border-left-color",Color)
        else:
            if ColorTop!=None:
                self.Set_("border-top-color",ColorTop)
            if ColorRight!=None:
                self.Set_("border-right-color",ColorRight)
            if ColorBottom!=None:
                self.Set_("border-bottom-color",ColorBottom)
            if ColorLeft!=None:
                self.Set_("border-left-color",ColorLeft)
            
        #触发qss事件
        if EventConnect:
            self.EventConnect()

    def SetBorderRadius(self,
                          RadiusTopLeft:int=None,
                          RadiusTopRight:int=None,
                          RadiusBottomLeft:int=None,
                          RadiusBottomRight:int=None,
                          Radius:int=None,
                          EventConnect:bool=False):
        '''
        设置边框圆角
        RadiusTopLeft:左上角圆角
        RadiusTopRight:右上角圆角
        RadiusBottomLeft:左下角圆角
        RadiusBottomRight:右下角圆角
        Radius:四边框圆角,设置此参数后忽略RadiusTopLeft,RadiusTopRight,RadiusBottomLeft,RadiusBottomRight
        EventConnect:触发qss事件
        '''
        if Radius!=None:
            self.Set_("border-top-left-radius",Radius)
            self.Set_("border-top-right-radius",Radius)
            self.Set_("border-bottom-left-radius",Radius)
            self.Set_("border-bottom-right-radius",Radius)     
        else:
            if RadiusTopLeft!=None:
                self.Set_("border-top-left-radius",RadiusTopLeft)
            if RadiusTopRight!=None:
                self.Set_("border-top-right-radius",RadiusTopRight)
            if RadiusBottomLeft!=None:
                self.Set_("border-bottom-left-radius",RadiusBottomLeft)
            if RadiusBottomRight!=None:
                self.Set_("border-bottom-right-radius",RadiusBottomRight)
            
        #触发qss事件
        if EventConnect:
            self.EventConnect()
         
    def SetFont(self,Font:Font_=None,EventConnect:bool=False):
        """
        Font:字体类型,详情参考Font_
        EventConnect:触发qss事件
        """
        if isinstance(Font,Font_):
            Font.qsschanged.connect(self.EventConnect)

        self.Set_("font",Font,EventConnect)

    def SetTextDecoration(self,TextDecoration:TextDecoration=None,EventConnect:bool=False):
        """
        TextDecoration:文本类型,详情参考TextDecoration
        event_connet:触发qss事件
        """
        self.Set_("text-decoration",TextDecoration,EventConnect)

    def SetTextAlign(self,TextAlign:TextAlign=None,EventConnect:bool=False):
        """
        TextAlign:文本对齐类型,详情参考TextAlign
        EventConnect:触发qss事件
        """
        self.Set_("text-align",TextAlign,EventConnect)
   
    def SetPadding(self,
                    PaddingTop:int=None,
                    PaddingRight:int=None,
                    PaddingBottom:int=None,
                    PaddingLeft:int=None,
                    Padding:int=None,
                    EventConnect:bool=False):
        """
        设置内边距
        PaddingTop:上边距
        PaddingRight:右边距
        PaddingBottom:下边距
        PaddingLeft:左边距

        Padding:四边距,设置此参数后忽略PaddingTop,PaddingRight,PaddingBottom,PaddingLeft

        event_connet:触发qss事件
        """
        if Padding!=None:
            self.Set_("padding-top",Padding)
            self.Set_("padding-right",Padding)
            self.Set_("padding-bottom",Padding)
            self.Set_("padding-left",Padding)
        else:
            if PaddingTop!=None:
                self.Set_("padding-top",PaddingTop)
            if PaddingRight!=None:
                self.Set_("padding-right",PaddingRight)
            if PaddingBottom!=None:
                self.Set_("padding-bottom",PaddingBottom)
            if PaddingLeft!=None:
                self.Set_("padding-left",PaddingLeft)

        #触发qss事件
        if EventConnect:
            self.EventConnect()

    def SetMargin(self,
                    MarginTop:int=None,
                    MarginRight:int=None,
                    MarginBottom:int=None,
                    MarginLeft:int=None,
                    Margin:int=None,
                    EventConnect:bool=False):
        """
        设置外边距
        MarginTop:上边距
        MarginRight:右边距  
        MarginBottom:下边距
        MarginLeft:左边距
        
        Margin:四边距,设置此参数后忽略MarginTop,MarginRight,MarginBottom,MarginLeft
        
        event_connet:触发qss事件
        """
        if Margin!=None:
            self.Set_("margin-top",Margin)
            self.Set_("margin-right",Margin)
            self.Set_("margin-bottom",Margin)
            self.Set_("margin-left",Margin)
            
        else:
            if MarginTop!=None:
                self.Set_("margin-top",MarginTop)
            if MarginRight!=None:
                self.Set_("margin-right",MarginRight)
            if MarginBottom!=None:
                self.Set_("margin-bottom",MarginBottom)
            if MarginLeft!=None:
                self.Set_("margin-left",MarginLeft)
            
        #触发qss事件
        if EventConnect:
            self.EventConnect()

    def Getqss(self):
        #qss初始化
        _qss=""

        for _key,_value in self._qsslist.items():
            if _value==None:
                continue

            if isinstance(_value,int):
                _qss+=_key+":"+str(_value)+"px"
            elif isinstance(_value,str):
                _qss+=_key+":"+_value
            elif isinstance(_value,Color_):
                _qss+=_key+":rgba("+QcolorToStr(_value.GetColor())+")"
            elif isinstance(_value,GradientColor):
                _qss+=_key+":"+_value.Getqss()
            elif isinstance(_value,Font_):
                _qss+=_key+":"+_value.Getqss()
            elif isinstance(_value,BorderStyle):
                _qss+=_key+":"+_value.value
            elif isinstance(_value,TextAlign):
                _qss+=_key+":"+_value.value
            elif isinstance(_value,TextDecoration):
                _qss+=_key+":"+_value.value

            _qss+=";"

        return _qss

class QssPlus(QObject):#屎山
    '''
    Widget:控件
    ObjectName:控件名称
    EasingCurve:动画曲线
    Duration:动画持续时间
    '''
    colorchanged=Signal(QColor)
    colorbackgroundchanged=Signal(QColor)
    fontsizechanged=Signal(int)
    def __init__(self,Widget:QObject,ObjectName:str,EasingCurve:QEasingCurve=QEasingCurve.OutQuad,Duration:int=500):
        super(QssPlus, self).__init__()
        #应用并缓存qss标题
        Widget.setObjectName(ObjectName)
        self.qss_title_=Widget.metaObject().className()+"#"+ObjectName
        #缓存控件
        self._widget=Widget
        #qss创建
        self.qss=QssStyle()
        self.qss.qsschanged.connect(self.__AppltQaaAnimation)
        #qss备份
        self._qssbackup=None
        #qss过度
        self._qssexcess=None
        #创建动画
        self._animation=Animation(0,EasingCurve=EasingCurve,Duration=Duration)
        self._animation.Animationed.connect(self.__AnimationEvent)
        #终止事件
        themes.colorchanged.connect(self._animation.Stop)
        Widget.destroyed.connect(lambda: self._animation.Stop())#某些事件会在close并行运行报错，必须暂停动画

    def Register(self,Register_:bool):#注册控件
        '''
        注册控件,主题更改时刷新qss
        '''
        if Register_:
            QssManage.Register(self._widget)
        else:
            QssManage.UnRegister(self._widget)

    def UpDateQss(self,Qss:QssStyle=None,Animation:bool=True):#更换新的qss_style
        '''
        Qss:新的颜色组,详情参考QssStyle
        Animation:动画效果开关
        '''
        if isinstance(Qss,QssStyle)==False:
            return
        
        #复制备份
        self._qssbackup=self.qss.Copy()
        #应用
        self.qss=Qss.Copy()
        self.qss.qsschanged.connect(self.__AppltQaaAnimation)
        self._qssexcess=None

        #刷新效果
        if Animation:#动画模式
            self.__AppltQaaAnimation()
        else:#无动画模式
            self.ApplyQss()

    def ApplyQss(self):#应用qss，无过度效果
        """
        应用qss,无动画效果
        """
        self._widget.setStyleSheet(self.QssTitle(self.qss.Getqss()))
        #复制备份
        self._qssbackup=self.qss.Copy()
        #过度清空
        self._qssexcess=None
        #槽函数传递
        self.QssConnectEvent()

    def GetColor(self):
        '''
        获取当前QssStyle的qss_color
        '''
        if self._animation.IsRun():
            if self._qssexcess!=None:
                _color=self._qssexcess._qsslist.get("color")
            else:
                _color=self.qss._qsslist.get("color")
        else:
            _color=self.qss._qsslist.get("color")

        if isinstance(_color,Color_):
            return _color.GetColor()
        
        return ColorCache_._color.Color
    
    def GetBackgroundColor(self):
        '''
        获取当前QssStyle的qss_backgroundcolor
        '''
        if self._animation.IsRun():
            if self._qssexcess!=None:
                _color=self._qssexcess._qsslist.get("background")
            else:
                _color=self.qss._qsslist.get("background")
        else:
            _color=self.qss._qsslist.get("background")

        if isinstance(_color,Color_):
            return _color.GetColor()
        
        return ColorCache_._color.ColorBackground
    
    def GetFontSize(self):
        '''
        获取当前QssStyle的qss_fontsize
        '''
        if self._animation.IsRun():
            if self._qssexcess!=None:
                _font=self._qssexcess._qsslist.get("font")
            else:
                _font=self.qss._qsslist.get("font")
        else:
            _font=self.qss._qsslist.get("font")

        if isinstance(_font,Font_):
            return _font.GetFontsize()
        
        return GetFontSize()

    def __AppltQaaAnimation(self):#应用qss,带动画效果
        '''
        应用qss,带动画效果
        '''
        #暂停动画事件
        self._animation.Stop()

        #存在过度qss，同步到备份qss中
        if self._qssexcess!=None:
            self._qssbackup=self._qssexcess.Copy()
            #过度清空
            self._qssexcess=None
            
        if self.__QssCompare(self.qss,self._qssbackup)==False:#两个qss不一样
            #补全参数
            self.__qss_completion__(self.qss,self._qssbackup)

            self._qssexcess=QssStyle()
            #开始动画
            self._animation.SetValue(0)
            self._animation.GoValue(100)
        else:
            self.ApplyQss()

    def __AnimationEvent(self,Value:int=0):#动画事件
        #按进度生成新qss，并缓存新qss
        self._qssexcess=self.__QssExcess(self._qssbackup,self.qss,Value).Copy()
        #应用qss
        self._widget.setStyleSheet(self.QssTitle(self._qssexcess.Getqss()))

        # print(self.QssTitle(self._qssexcess.Getqss()))
        #槽函数传递
        self.QssConnectEvent()

    def __QssCompare(self,Qss1:QssStyle,Qss2:QssStyle):#qss比较

        if len(Qss1._qsslist)!=len(Qss2._qsslist):#数量不一样
            return False

        if set(Qss1._qsslist.keys()) != set(Qss2._qsslist.keys()):#数量一致,但key值不一致
            return False

        #数量一致,key值一致,判断value是否一致

        for _key,_value in Qss1._qsslist.items():#遍历其中一个字典
            _valuecache=Qss2._qsslist.get(_key)

            if type(_value) != type(_valuecache):#判断value是否为同一个类型
                return False

            #类型判断
            if isinstance(_value,int) or\
               isinstance(_value,str) or\
               isinstance(_value,BorderStyle) or\
               isinstance(_value,TextAlign) or\
               isinstance(_value,TextDecoration) :
                if _value!=_valuecache:
                    return False
            
            elif isinstance(_value,Color_):
                if IsColorEqual(_value.GetColor(),_valuecache.GetColor())==False:
                    return False

            elif isinstance(_value,GradientColor) or\
                 isinstance(_value,Font_):
                if _value.Equal(_valuecache)==False:
                    return False
                
        return True

    def __QssExcess(self,Qssold:QssStyle,Qssnew:QssStyle,Value:int=0):#动画事件的过渡计算
        '''
        Qssold向Qssnew过度,Value 0-100
        '''
        def __ValueJudge(Value:int):#固定值判断
            """
            文本类型参数无法过度，在整个过度阶段的一半时候进行变换。
            """
            if Value>50:
                return True
            return False

        def __FontExcess(Fontold:Font_,Fontnew:Font_,Value:int=0):#字体过度
            #创建临时字体类型
            _font=Font_()
            _fontsize=FontSize()

            #固定值判断
            if __ValueJudge(Value):
                _font.SetFontName(Fontnew._fontname)
                _font.SetFontWeight(Fontnew._fontweight)
                _font.SetFontStyle(Fontnew._fontstyle)
                _fontsize._fontstyle=Fontnew._fontsize._fontstyle
            else:
                _font.SetFontName(Fontold._fontname)
                _font.SetFontWeight(Fontold._fontweight)
                _font.SetFontStyle(Fontold._fontstyle)
                _fontsize._fontstyle=Fontold._fontsize._fontstyle

            _fontsize._size=IntExcess(Fontold._fontsize._size,Fontnew._fontsize._size,Value)
            _fontsize._shift=IntExcess(Fontold._fontsize._shift,Fontnew._fontsize._shift,Value)
            _fontsize._min=IntExcess(Fontold._fontsize._min,Fontnew._fontsize._min,Value)
            _fontsize._max=IntExcess(Fontold._fontsize._max,Fontnew._fontsize._max,Value)

            _font.SetFontSize(_fontsize)

            return _font

        def __GradientColorExcess(GradientColorold:GradientColor,GradientColornew:GradientColor,Value:int=0,CompletionWay:bool=True):#渐变颜色过度
            '''
            CompletionWay:补全方式,True为向后补全,False为向前补全
            '''
            #创建临时颜色渐变类型
            _color=GradientColor()
            _colorlist=GradientColorList()

            #固定值判断
            if __ValueJudge(Value):
                _color.SetStyle(GradientColornew._style)
                _color.SetSpread(GradientColornew._spread)
            else:
                _color.SetStyle(GradientColorold._style)
                _color.SetSpread(GradientColorold._spread)

            _color.SetRadius(FloatExcess(GradientColorold._radius,GradientColornew._radius,Value))
            _color.SetAngle(FloatExcess(GradientColorold._angle,GradientColornew._angle,Value))

            _color.Setp1(FloatExcess(GradientColorold._p1.x(),GradientColornew._p1.x(),Value),FloatExcess(GradientColorold._p1.y(),GradientColornew._p1.y(),Value))
            _color.Setp2(FloatExcess(GradientColorold._p2.x(),GradientColornew._p2.x(),Value),FloatExcess(GradientColorold._p2.y(),GradientColornew._p2.y(),Value))
            _color.Setcp(FloatExcess(GradientColorold._cp.x(),GradientColornew._cp.x(),Value),FloatExcess(GradientColorold._cp.y(),GradientColornew._cp.y(),Value))
            _color.Setfp(FloatExcess(GradientColorold._fp.x(),GradientColornew._fp.x(),Value),FloatExcess(GradientColorold._fp.y(),GradientColornew._fp.y(),Value))

            #补全列表
            l1=len(GradientColornew._colorlist._list)
            l2=len(GradientColorold._colorlist._list)
            if l1>l2:
                for i in range(int(l1-l2)):
                    if CompletionWay:
                        GradientColorold._colorlist._list.insert(0,GradientColorold._colorlist._list[0])
                    else:
                        GradientColorold._colorlist._list.append(0,GradientColorold._colorlist._list[-1])
            elif l1<l2:
                for i in range(int(l2-l1)):
                    if CompletionWay:
                        GradientColornew._colorlist._list.insert(0,GradientColornew._colorlist._list[0])
                    else:
                        GradientColornew._colorlist._list.append(0,GradientColornew._colorlist._list[-1])

            #列表
            for i in range(len(GradientColornew._colorlist._list)):
                _colorlist.AddColor(FloatExcess(GradientColorold._colorlist._list[i][0],GradientColornew._colorlist._list[i][0],Value),
                                    Color_(QcolorExcess(GradientColorold._colorlist._list[i][1].GetColor(),GradientColornew._colorlist._list[i][1].GetColor(),str(Value)+"%"))
                                    )

            _color.SetColorlist(_colorlist)

            return _color

        def __TranGradient(Color:Color_,GradientColor:GradientColor):#非Color_转Gradient_color_
            _gradientcolor=GradientColor.Copy()

            _gradientcolorlist=GradientColorList()
            for _item in _gradientcolor._colorlist._list:
                _gradientcolorlist.AddColor(_item[0],Color)

            _gradientcolor.SetColorlist(_gradientcolorlist)

            return _gradientcolor

        #创建临时qss
        _qss=QssStyle()

        for _key,_value in Qssnew._qsslist.items():
            _valuecache=Qssold._qsslist.get(_key)

            if isinstance(_value,int):
                _qss.Set_(_key,IntExcess(_valuecache,_value,Value))

            elif isinstance(_value,str) or isinstance(_value,BorderStyle) or isinstance(_value,TextDecoration) or isinstance(_value,TextAlign):
                if __ValueJudge(Value):
                    _qss.Set_(_key,_value)
                else:
                    _qss.Set_(_key,_valuecache)

            elif isinstance(_value,Font_):
                _qss.Set_(_key,__FontExcess(_valuecache,_value,Value))

            elif isinstance(_value,Color_) and isinstance(_valuecache,Color_):
                _qss.Set_(_key,Color_(QcolorExcess(_valuecache.GetColor(),_value.GetColor(),str(Value)+"%")))
            elif isinstance(_value,Color_) and isinstance(_valuecache,GradientColor): 
                _qss.Set_(_key,__GradientColorExcess(_valuecache,__TranGradient(_value,_valuecache),Value))
            elif isinstance(_value,GradientColor) and isinstance(_valuecache,Color_): 
                _qss.Set_(_key,__GradientColorExcess(__TranGradient(_valuecache,_value),_value,Value))
            elif isinstance(_value,GradientColor) and isinstance(_valuecache,GradientColor): 
                _qss.Set_(_key,__GradientColorExcess(_valuecache,_value,Value))

        #颜色返回槽函数

        return _qss
   
    def __qss_completion__(self,Qss1:QssStyle,Qss2:QssStyle):#qss补全
        '''
        假如qss的属性中有color,而qss_backup中没有color属性,则在qss_backup中插入补全参数qss_color的color完成透明值,同时也作用相反,qss_backup也会补全qss

        补全前
         qss="text{Color:rgba(255,255,255,255),padding-left:10px}"                       
         qss_backup="text{background-Color:rgba(255,255,255,255)}"

        补全后
         qss="text{Color:rgba(255,255,255,255),background-Color:rgba(255,255,255,0),padding-left:10px}"
         qss_backup="text{Color:rgba(255,255,255,0),background-Color:rgba(255,255,255,255),padding-left:0px}"
        '''

        def DefaultValue(Value:Union[str,int,Color_,Font_,GradientColor,BorderStyle,TextDecoration,TextAlign]):
            if isinstance(Value,int):
                return 0
            elif isinstance(Value,str) or isinstance(Value,Font_) or isinstance(Value,BorderStyle) or isinstance(Value,TextDecoration) or isinstance(Value,TextAlign):
                return Value
            elif isinstance(Value,Color_) or isinstance(Value,GradientColor):
                return Value.GetNullColor()

        #生成临时字典,代替qss_new
        _qss=Qss1._qsslist.copy()
        for _key, _value in Qss2._qsslist.items():
            if _key in _qss:
                continue  # 如果键已存在，跳过该键值对
            else:
                _qss[_key] = DefaultValue(_value)

        for _key, _value in Qss1._qsslist.items():
            if _key in Qss2._qsslist.copy():
                continue  # 如果键已存在，跳过该键值对
            else:
                Qss2._qsslist[_key] = DefaultValue(_value)

        Qss1._qsslist=_qss.copy()

    def QssConnectEvent(self):#各参数的槽函数修改事件汇总
        #颜色
        self.colorchanged.emit(self.GetColor())
        
        #背景颜色
        self.colorbackgroundchanged.emit(self.GetBackgroundColor())
        
        #字体大小
        self.fontsizechanged.emit(self.GetFontSize())

    def QssTitle(self,_qss:str):#返回带标题的qss
        return self.qss_title_+"{"+_qss+"}"
