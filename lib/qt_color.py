from PySide6.QtGui import QColor
from typing import Union

from .qt_config import GetThemeMode,GetThemeColor,GetThemeAlpha,ThemeMode
from .win_getThemeMode import GetWindowThememode

from enum import Enum

ColorLight = QColor(255,255,255,255)
ColorDark = QColor(0,0,0,255)

class ColorStyle(Enum):#颜色样式
    '''
    颜色类型

    Dark:#深色主题色
    Light:#浅色主题色

    Color:0-100渐变值,0背景色-100前景色,带透明通道
    ThemeColor:0-100渐变值,0主题色-100前景色,带透明通道
    ThemeColorBackground:0-100渐变值,0主题色-100背景色,带透明通道

    '''
    Dark="Dark"#深色主题色
    Light="Light"#浅色主题色

    Color="Color"#0-100渐变值,0背景色-100前景色,带透明通道
    ThemeColor="ThemeColor"#0-100渐变值,0前景色-100主题色,带透明通道
    ThemeColorBackground="ThemeColorBackground"#0-100渐变值,0主题色-100背景色,带透明通道

    FullColor="FullColor"#0-100渐变值,0背景色-100前景色,透明通道为255
    FullThemeColor="FullThemeColor"#0-100渐变值,0前景色-100主题色,透明通道为255
    FullThemeColorBackground="FullThemeColorBackground"#0-100渐变值,0主题色-100背景色,透明通道为255

    NullColor="NullColor"#0-100渐变值,0背景色-100前景色,透明通道为0
    NullThemeColor="NullThemeColor"#0-100渐变值,0前景色-100主题色,透明通道为0
    NullThemeColorBackground="NullThemeColorBackground"#0-100渐变值,0主题色-100背景色,透明通道为0
  
class Color_:#新颜色样式，用于定位颜色
    '''
    请严格按照下方格式使用,否则运行错误或无法获取到颜色值

    Color:str,1个参数,格式"255,255,255,255"
    Color:int,4个参数,格式255,255,255,255
    Color:QColor,1个参数,格式QColor(255,255,255,255),或者ColorStyle.Dark,ColorStyle.Light
    Color:渐变色,2个参数,格式ColorStyle,index(0背景色-100前景色)
    Color:双重渐变色str格式,3个参数,格式str1,str2,Value。Value为过渡值int 0-255 或 str "0%"-"100%"
    Color:双重渐变色Color格式,3个参数,格式Color1,Color2,Value。Value为过渡值int 0-255 或 str "0%"-"100%"
    Color:双重渐变色QColor格式,3个参数,格式QColor1,QColor2,Value。Value为过渡值int 0-255 或 str "0%"-"100%"
    Color:双重渐变色ColorStyle格式,5个参数,格式ColorStyle1,index1,ColorStyle2,index2,Value。Value为过渡值int 0-255 或 str "0%"-"100%"

    Alpha:透明度,范围0-255,不会覆盖原颜色值的透明层,计算公式为原颜色值的透明层/255*aplha,如rgba(255,255,255,100)定义alpha为100,则get_color颜色为rgba(255,255,255,39)
    FixAlpha:直接覆盖原颜色值的透明层。

    Rshift:R通道偏移量,范围-255-255,默认为0
    Gshift:G通道偏移量,范围-255-255,默认为0
    Bshift:B通道偏移量,范围-255-255,默认为0
    '''

    def __init__(self,*Color,Alpha:int=255,FixAlpha:int=None,Rshift:int=0,Gshift:int=0,Bshift:int=0):
        super(Color_, self).__init__()
        super(Color_, self).__init__()
        self._color=Color
        self._alpha=Alpha
        self._fixalpha=FixAlpha
        
        self._rshift=Rshift
        self._gshift=Gshift
        self._bshift=Bshift

    def __GetColorfromColorStyle(self,ColorStyle_:ColorStyle,index:int):
        if ColorStyle_==ColorStyle.Dark:
            _color = ColorDark
        elif ColorStyle_==ColorStyle.Light:
            _color = ColorLight
            
        elif ColorStyle_==ColorStyle.Color:
            _color = ColorCache_._color[index]
        elif ColorStyle_==ColorStyle.ThemeColor:
            _color = ColorCache_._themecolor[index]
        elif ColorStyle_==ColorStyle.ThemeColorBackground:
            _color = ColorCache_._themecolorbcackground[index]

        elif ColorStyle_==ColorStyle.FullColor:
            _color = QcolorAlpha(ColorCache_._color[index],255)
        elif ColorStyle_==ColorStyle.FullThemeColor:
            _color = QcolorAlpha(ColorCache_._themecolor[index],255)
        elif ColorStyle_==ColorStyle.FullThemeColorBackground:
            _color = QcolorAlpha(ColorCache_._themecolorbcackground[index],255)

        elif ColorStyle_==ColorStyle.NullColor:
            _color = QcolorAlpha(ColorCache_._color[index],0)
        elif ColorStyle_==ColorStyle.NullThemeColor:
            _color = QcolorAlpha(ColorCache_._themecolor[index],0)
        elif ColorStyle_==ColorStyle.NullThemeColorBackground:
            _color = QcolorAlpha(ColorCache_._themecolorbcackground[index],0)

        else:
            return None
        
        return _color

    def GetColor(self):#取当前颜色
        '''
        从缓存中获取颜色值,返回Qcolor
        '''
        if len(self._color)==0:#参数数量为0
            return None
        
        Color=self._color[0]#取标识值

        if len(self._color)==1:#参数数量为1
            if isinstance(Color,str):
                _color = StrToQcolor(Color)
            elif isinstance(Color,QColor):
                _color = Color
            elif isinstance(Color,ColorStyle):
                if Color==ColorStyle.Dark:
                    _color = ColorDark
                elif Color==ColorStyle.Light:
                    _color = ColorLight
            else:
                return None
        
        if len(self._color)==2:#参数数量为2
            if not isinstance(Color,ColorStyle):
                return None
            
            _color=self.__GetColorfromColorStyle(Color,self._color[1])
            
        if len(self._color)==3:#参数数量为3
            if isinstance(Color,str):
                _color = QcolorExcess(StrToQcolor(self._color[0]),StrToQcolor(self._color[1]),self._color[2])
            elif isinstance(Color,QColor):
                _color = QcolorExcess(self._color[0],self._color[1],self._color[2])
            else:
                return None

        if len(self._color)==4:#参数数量为4
            if isinstance(Color,int):
                _color = QColor(self._color[0],self._color[1],self._color[2],self._color[3])
            else:
                return None
            
        if len(self._color)==5:#参数数量为5
            if not isinstance(Color,ColorStyle):
                return None
            
            _color1=self.__GetColorfromColorStyle(self._color[0],self._color[1])
            _color2=self.__GetColorfromColorStyle(self._color[2],self._color[3])
            _color = QcolorExcess(_color1,_color2,self._color[4])
            

        #色值偏移
        _colorR=_color.red()+self._rshift
        _colorG=_color.green()+self._gshift
        _colorB=_color.blue()+self._bshift
        
        #限制范围
        if _colorR<0:_colorR=0
        if _colorR>255:_colorR=255
        if _colorG<0:_colorG=0
        if _colorG>255:_colorG=255
        if _colorB<0:_colorB=0  
        if _colorB>255:_colorB=255

        #透明层
        if self._fixalpha!=None:#直接覆盖原颜色值的透明层
            _colorA=self._fixalpha
        else:
            _colorA=int(_color.alpha()/255*self._alpha)
        
        return QColor(_colorR,_colorG,_colorB,_colorA)

    def GetNullColor(self):#取透明颜色
        '''
        忽略其他参数,强制取颜色透明层为0的颜色值
        '''
        _color=self.GetColor()
        return QcolorAlpha(_color,0)

    def GetFullColor(self):#取不透明颜色
        '''
        忽略其他参数,强制取颜色透明层为255的颜色值
        '''
        _color=self.GetColor()
        return QcolorAlpha(_color,255)

class Color_list(list):#color列表类,缓存颜色列表
    """
    颜色列表:背景色到前景色的0-100渐变值

    self.Color:前景色
    self.ColorBackground:背景色
    """
    def __init__(self,Color:Color_,ColorBackground:Color_):
        self.RenewColor(Color,ColorBackground)
    
    def RenewColor(self,Color:Color_,ColorBackground:Color_):#刷新颜色
        '''
        刷新颜色
        '''
        #清空
        self.clear()

        #颜色文本格式转Qcolor
        self.Color=Color.GetColor()
        self.ColorBackground=ColorBackground.GetColor()

        #缓存
        self.append(self.ColorBackground)
        self.append(self.Color)

        #渐变缓存
        for i in range(1,100):
            _color=QcolorExcess(self.ColorBackground,self.Color,str(i)+"%")
            self.insert(i,_color)
  
class ColorCache:
    '''
    颜色值缓存,根据主题情况刷新3个颜色列表Color_list

    self._color:0-100渐变值,0背景色-100前景色
    self._themecolor:0-100渐变值,0前景色-100主题色
    self._themecolorbcackground:0-100渐变值,0背景色-100主题色
    '''
    def RenewColor(self):#刷新当前主题颜色
        _thememode=GetThemeMode()
        _themealpha=GetThemeAlpha()
        _themecolor=GetThemeColor()

        #判断主题
        if _thememode==ThemeMode.AUTO:
            _mode=ThemeMode.DARK if GetWindowThememode() else ThemeMode.LIGHT
        else:
            _mode=_thememode
        
        #颜色缓存

        print(_mode)

        if _mode==ThemeMode.LIGHT:#亮
            self._color=Color_list(Color_(ColorDark),Color_(QcolorAlpha(ColorLight,_themealpha)))
        elif _mode==ThemeMode.DARK:#暗
            self._color=Color_list(Color_(ColorLight),Color_(QcolorAlpha(ColorDark,_themealpha)))

        self._themecolor=Color_list(Color_(self._color.Color),Color_(_themecolor))
        self._themecolorbcackground=Color_list(Color_(self._color.ColorBackground),Color_(_themecolor))
       
ColorCache_=ColorCache()
  
def IsColorStr(Color:str):
    """
    判断颜色是否文本格式  "255,255,255,255"
    """
    if not isinstance(Color,str):
        return(False)
    
    try:
        _colors=Color.split(",")
    except:
        return(False)
    
    if len(_colors)!=4:#不是颜色,rgba总共4位
        return(False)
    
    for _color in _colors:
        if str(_color).isdigit==False:#判断是否为数字
            return(False)
        if int(_color) >255 or int(_color)<0:#超出色值范围
            return(False)
        
    return(True)

def IsColorEqual(Color1:QColor,Color2:QColor):
    """
    判断颜色是否一致
    """
    if Color1.red()!=Color2.red():
        return False
    elif Color1.green()!=Color2.green():
        return False
    elif Color1.blue()!=Color2.blue():
        return False
    elif Color1.alpha()!=Color2.alpha():
        return False
    return True

def StrToQcolor(ColorStr:str):
    '''
    颜色文本格式转换QColor

    ColorStr:颜色文本格式,例"255,255,255,255"
    '''
    if IsColorStr(ColorStr):
        _color=str(ColorStr).split(",")
        return(QColor(int(_color[0]),int(_color[1]),int(_color[2]),int(_color[3])))
    return None

def QcolorToStr(Color:QColor):
    '''
    QColor转换颜色文本格式
    '''
    if isinstance(Color,QColor):
        return("{},{},{},{}".format(str(Color.red()),str(Color.green()),str(Color.blue()),str(Color.alpha())))
    else:
        return None

def QcolorExcess(Color1:QColor,Color2:QColor,Value:Union[int,str]):
    '''
    计算颜色过渡值
    
    Color1:颜色1
    Color2:颜色2
    Value:过渡值,int 0-255 或 str "0%"-"100%"
    '''
    def Cal(Int1:int,Int2:int,Value:int):
        '''
        过渡计算V
        '''
        _int=Int1-int((Int1-Int2)/255*Value) if Int1>Int2 else Int1+int((Int2-Int1)/255*Value)
        return _int

    if isinstance(Value,str):
        Value=int(int(Value.split("%")[0])/100*255)
    if isinstance(Value,int):
        if Value>255 or Value<0:
            return None

    _R=Cal(Color1.red(),Color2.red(),Value)
    _G=Cal(Color1.green(),Color2.green(),Value)
    _B=Cal(Color1.blue(),Color2.blue(),Value)
    _A=Cal(Color1.alpha(),Color2.alpha(),Value)

    #qss bug a值为1时背景会触发纯黑色
    if _A==1:
        _A=0

    return(QColor(_R,_G,_B,_A))

def QcolorAlpha(Color:QColor,Alpha:int):
    '''
    修改颜色的透明值
    '''
    if Alpha>255 or Alpha<0:
        return None
    return QColor(Color.red(),Color.green(),Color.blue(),Alpha)

def QcolorOpposite(Color=QColor):
    '''
    颜色反色
    '''
    return QColor(255-Color.red(),255-Color.green(),255-Color.blue(),Color.alpha())

def QcolorOpposit2(Color=QColor):
    '''
    颜色反色,不完全反色,另类算法
    '''
    _red=int((255-Color.red()/1.2)*1.2)
    _red=255 if _red>255 else _red
    _red=0 if _red<0 else _red

    _blue=int((255-Color.blue()/1.5)*1.5)
    _blue=255 if _blue>255 else _blue
    _blue=0 if _blue<0 else _blue

    _green=int((255-Color.red()/1.8)*1.8)
    _green=255 if _green>255 else _green
    _green=0 if _green<0 else _green

    return QColor(_red,_green,_blue,Color.alpha())
