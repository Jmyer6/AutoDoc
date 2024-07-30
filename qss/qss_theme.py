from PySide6.QtCore import QObject,Signal,QThread,QPointF
from PySide6.QtGui import QColor

from lib import Color_,IsColorEqual,QcolorToStr,GetFontSize,GetFontName,ColorCache_,\
    GetThemeMode,ThemeMode,SetThemeMode,SetFontName,SetFontSize,SetThemeAlpha,\
    SetThemeColor,SetThemeImage

from .qss_type import GradientStyle,GradientSpread,FontSizeStyle,FontStyle,FontWeight

class GradientColorList:#渐变颜色组
    """
    Qss渐变颜色的颜色组,遵循Qss渐变类型规则

    格式[[float,Color_],[float,Color_],.....,[float,Color_]]
    """
    def __init__(self):
        super(GradientColorList, self).__init__()
        self._list=[]

    def Clear(self):
        '''
        清空列表
        '''
        self._list=[]

    def AddColor(self,Index:float,Color:Color_):
        """
        Index:0-1的小数点位置
        Color:颜色
        """
        #范围限制
        Index=0 if Index<=0 else Index
        Index=1 if Index>=1 else Index

        self._list.append([Index,Color])

    def AddColorList(self,ColorList:list):
        """
        ColorList:颜色列表,可参考AddColor函数
        """
        for color in ColorList:
            self.AddColor(color[0],color[1])

    def Equal(self,GradientColorList_):
        '''
        判断GradientColorList是否相等
        '''
        if isinstance(GradientColorList_,GradientColorList)==False:#判断类型是否为GradientColorList
            return False

        if len(self._list)!=len(GradientColorList_._list):#判断数量是否一致
            return False

        #遍历判断
        for i in range(len(self._list)):

            l1=self._list[i]
            l2=GradientColorList_._list[i]

            if len(l1)!=2 or len(l2)!=2: #判断子参数列表[float,Color_]数量是否为2
                return False

            if l1[0]!=l2[0]:
                return False
            
            if IsColorEqual(l1[1].GetColor(),l2[1].GetColor())==False:
                return False

        return True

    def GetNullColor(self):#取当前渐变颜色的透明值
        _list=[]
        for item in self._list:
            _listcache=[]
            _listcache.append(item[0])
            _listcache.append(item[1].GetNullColor())#Color_类
            _list.append(_listcache)
        return _list

class GradientColor(QObject):#渐变颜色
    '''
    Qss渐变颜色,遵循Qss渐变类型规则
    '''
    qsschanged=Signal()
    def __init__(self):
        super(GradientColor, self).__init__()
        self._style=None
        self._spread=None
        self._radius=0
        self._angle=0
        self._p1=QPointF(0,0)
        self._p2=QPointF(0,0)
        self._cp=QPointF(0,0)
        self._fp=QPointF(0,0)
        self._colorlist=None

    def LoadLine(self,FontStyle:GradientStyle,Spread:GradientSpread,x1:float,y1:float,x2:float,y2:float,ColorList:GradientColorList):
        '''
        显示从起点到终点的直线渐变
        qlineargradient(Spread:*, x1:*, y1:*, x2:*, y2:*, stop:0 rgba(*),.....,stop:1 rgba(*))
        '''
        self.SetStyle(FontStyle)
        self.SetSpread(Spread)
        self.Setp1(x1,y1)
        self.Setp2(x2,y2)
        self.SetColorlist(ColorList)
        
    def LoadRadial(self,FontStyle:GradientStyle,cx:float,cy:float,Radius:float,fx:float,fy:float,ColorList:GradientColorList):
        """
        显示以圆心为中心的圆形渐变
        qradialgradient(Spread:*, cx:*, cy:*, Radius:*, fx:*, fy:*, stop:0 rgba(*),.....,stop:1 rgba(*))
        """
        self.SetStyle(FontStyle)
        self.Setcp(cx,cy)
        self.SetRadius(Radius)
        self.Setfp(fx,fy)
        self.SetColorlist(ColorList)

    def LoadConical(self,cx:float,cy:float,Angel:float,ColorList:GradientColorList):
        '''
        #显示围绕一个中心点的锥形渐变
        qconicalgradient(cx:*, cy:*, Angle:*,stop:0 rgba(*),.....,stop:1 rgba(*))
        '''
        self.Setcp(cx,cy)
        self.SetAngle(Angel)
        self.SetColorlist(ColorList)

    def __PointFRange(func):
        def wrapper(self,x_:float,y_:float):
            lx=0 if x_<0 else x_
            lx=1 if x_>1 else x_
            ly=0 if y_<0 else y_
            ly=1 if y_>1 else y_
            return func(self,lx,ly)
        return wrapper

    def __Float_radiusRange(func):
        def wrapper(self,f_:float):
            lf=0 if f_<0 else f_
            lf=2 if f_>2 else f_
            return func(self,lf)
        return wrapper

    def __Float_angleRange(func):
        def wrapper(self,f_:float):
            lf=0 if f_<0 else f_
            lf=360 if f_>360 else f_
            return func(self,lf)
        return wrapper

    def SetStyle(self,FontStyle:GradientStyle):
        self._style=FontStyle if isinstance(FontStyle,GradientStyle) else None

    def SetSpread(self,Spread:GradientSpread):
        self._spread=Spread if isinstance(Spread,GradientSpread) else None

    @__Float_radiusRange
    def SetRadius(self,f_:float,EventConnect:bool=False):
        self._radius=f_

        if EventConnect:
            self.EventConnect()
    
    @__Float_angleRange
    def SetAngle(self,f_:float,EventConnect:bool=False):
        self._angle=f_
        
        if EventConnect:
            self.EventConnect()
 
    @__PointFRange
    def Setp1(self,x_:float,y_:float,EventConnect:bool=False):
        self._p1=QPointF(x_,y_)

        if EventConnect:
            self.EventConnect()

    @__PointFRange
    def Setp2(self,x_:float,y_:float,EventConnect:bool=False):
        self._p2=QPointF(x_,y_)

        if EventConnect:
            self.EventConnect()

    @__PointFRange
    def Setcp(self,x_:float,y_:float,EventConnect:bool=False):
        self._cp=QPointF(x_,y_)

        if EventConnect:
            self.EventConnect()
    
    @__PointFRange
    def Setfp(self,x_:float,y_:float,EventConnect:bool=False):
        self._fp=QPointF(x_,y_)

        if EventConnect:
            self.EventConnect()

    def SetColorlist(self,colorlist:GradientColorList,EventConnect:bool=False):
        self._colorlist=colorlist

        if EventConnect:
            self.EventConnect()

    def Copy(self):
        '''
        复制参数
        '''
        _gc=GradientColor()
        _gc._style=self._style
        _gc._spread=self._spread
        _gc._radius=self._radius
        _gc._angle=self._angle
        _gc._p1=self._p1
        _gc._p2=self._p2
        _gc._cp=self._cp
        _gc._fp=self._fp
        _gc._colorlist=self._colorlist
        return _gc

    def Equal(self,GradientColor_):
        '''
        判断GradientColor是否相等
        '''
        if isinstance(GradientColor_,GradientColor)==False:
            return False

        if self._style!=GradientColor_._style or\
            self._spread!=GradientColor_._spread or\
            self._radius!=GradientColor_._radius or\
            self._angle!=GradientColor_._angle or\
            self._p1!=GradientColor_._p1 or\
            self._p2!=GradientColor_._p2 or\
            self._cp!=GradientColor_._cp or\
            self._fp!=GradientColor_._fp:
            return False

        if self._colorlist.Equal(GradientColor_._colorlist)==False:
            return False
        
        return True

    def GetNullColor(self):#取当前渐变颜色的透明值
        Color=self.Copy()
        Color.SetColorlist(Color._colorlist.GetNullColor())
        return Color

    def Getqss(self):
        #初始化返回值
        _qss=""
        if self._style==GradientStyle.qlineargradient:
            if self._spread==None:
                return None 
            _qss+=self._style.value+"("
            _qss+="spread:"+self._spread.value+","
            _qss+="x1:"+str(self._p1.x())+","
            _qss+="y1:"+str(self._p1.y())+","
            _qss+="x2:"+str(self._p2.x())+","
            _qss+="y2:"+str(self._p2.y())
        elif self._style==GradientStyle.qradialgradient:
            if self._spread==None:
                return None
            _qss+=self._style.value+"("
            _qss+="spread:"+self._spread.value+","
            _qss+="cx:"+str(self._cp.x())+","
            _qss+="cy:"+str(self._cp.y())+","
            _qss+="radius:"+str(self._radius)+","
            _qss+="fx:"+str(self._fp.x())+","
            _qss+="fy:"+str(self._fp.y())
        elif self._style==GradientStyle.qconicalgradient:
            _qss+=self._style.value+"("
            _qss+="cx:"+str(self._cp.x())+","
            _qss+="cy:"+str(self._cp.y())+","
            _qss+="angle:"+str(self._angle)
        else:
            return None
        #色值
        if len(self._colorlist._list)==0:
            return None
        for color_item in self._colorlist._list:
            _qss+=",stop:"+str(color_item[0])
            _qss+=" rgba("+QcolorToStr(color_item[1].GetColor())+")"
        _qss+=")"
        return _qss

    def EventConnect(self):
        self.qsschanged.emit()


class FontSize:#新字体大小
    """
    Size:字体大小
    Shift:字体大小偏移,正数变大,负数变小
    FontStyle:跟随系统或者默认,跟随系统是忽略size参数
    Min:限制字体最小值
    Max:限制字体最大值
    """
    def __init__(self,Size:int=None,Shift:int=0,FontStyle:FontSizeStyle=FontSizeStyle.regular,Min:int=10,Max:int=100):
        self._fontstyle=FontStyle
        self._shift=Shift
        self._min=Min
        self._max=Max
        self._size=GetFontSize() if Size is None else Size
          
    def Copy(self):
        '''
        复制参数
        '''
        return FontSize(self._size,self._shift,self._fontstyle,self._min,self._max)

    def Equal(self,fontsize):
        '''
        判断FontSize是否相等
        '''
        if isinstance(fontsize,FontSize)==False:
            return False

        if self._fontstyle!=fontsize._fontstyle or\
           self._size!=fontsize._size or\
           self._shift!=fontsize._shift or\
           self._min!=fontsize._min or\
           self._max!=fontsize._max:
            return False

        return True

class Font_(QObject):#新字体类型
    '''
    FontName=字体名称
    FontSize:字体大小,详情参考Font_size
    FontStyle=字体样式,详情参考Font_style
    FontWeight=字体粗细,详情参考Font_weight
    '''
    qsschanged=Signal()
    def __init__(self,FontName:str=None,FontSize:FontSize=FontSize,FontStyle:FontStyle=FontStyle.normal,FontWeight:FontWeight=FontWeight.normal):
        super(Font_, self).__init__()
        self._fontname=FontName
        self._fontsize=FontSize
        self._fontstyle=FontStyle
        self._fontweight=FontWeight
        self._fontname=GetFontName() if FontName is None else FontName

    def SetFontName(self,FontName:str=None,EventConnect:bool=False):
        """
        字体名称
        """
        self._fontname=GetFontName() if FontName is None else FontName

        if EventConnect:
            self.EventConnect()

    def SetFontSize(self,FontSize:FontSize,EventConnect:bool=False):
        """
        字体大小,详情参考FontSize
        """
        self._fontsize=FontSize.Copy()

        if EventConnect:
            self.EventConnect()

    def SetFontStyle(self,FontStyle:FontStyle=FontStyle.normal,EventConnect:bool=False):
        """
        FontStyle=字体样式,详情参考FontStyle
        """
        self._fontstyle=FontStyle

        if EventConnect:
            self.EventConnect()

    def SetFontWeight(self,FontWeight:FontWeight=FontWeight.normal,EventConnect:bool=False):
        """
        FontWeight=字体粗细,详情参考FontWeight
        """
        self._fontweight=FontWeight

        if EventConnect:
            self.EventConnect()

    def GetFontsize(self):
        _size=None

        if isinstance(self._fontsize,FontSize):
            _size=GetFontSize() if self._fontsize._fontstyle==FontSizeStyle.auto else self._fontsize._size

            #字体大小计算偏移
            _size+=self._fontsize._shift

            #限制字体范围
            _size=self._fontsize._min if _size<self._fontsize._min else _size
            _size=self._fontsize._max if _size>self._fontsize._max else _size

        return _size

    def Getqss(self):
        _qss=""

        _qss+=self._fontstyle.value+" "
        _qss+=self._fontweight.value+" "

        #字体大小
        _size=self.GetFontsize()
        if _size!=None:
            _qss+=str(_size)+"px "

        #字体名称
        if self._fontname!=None and self._fontname!="":
            _qss+="\""+self._fontname+"\""
        else:
            _qss+="\""+GetFontName()+"\""

        return _qss

    def Copy(self):
        '''
        复制参数
        '''
        return Font_(self._fontname,self._fontsize,self._fontstyle,self._fontweight)

    def Equal(self,font):
        '''
        比较参数是否一致
        '''
        if isinstance(font,Font_)==False:
            return False

        if self._fontname!=font._fontname or\
           self._fontstyle!=font._fontstyle or\
           self._fontweight!=font._fontweight:
            return False
        
        if self._fontsize.Equal(font._fontsize)==False:
            return False

        return True

    def EventConnect(self):
        self.qsschanged.emit()

class Theme_(QObject):#主题加载
    themechanged=Signal()#主题变动事件
    colorchanged=Signal()#主题颜色变动事件
    def __init__(self,*args, **kwargs):
        super(Theme_, self).__init__(*args, **kwargs)
        self.themechanged.connect(self.__ThemeChangeEvent)

        ColorCache_.RenewColor()

    def ThemModeChange(self):
        '''
        主题模式改变事件,不适用auto模式
        '''
        if GetThemeMode()==ThemeMode.LIGHT:
            self.SetThemeMode(ThemeMode.DARK)
        elif GetThemeMode()==ThemeMode.DARK:
            self.SetThemeMode(ThemeMode.LIGHT)
        else:
            return

    def SetThemeMode(self,ThemeMode:ThemeMode):
        '''
        切换app主题
        '''
        SetThemeMode(ThemeMode)
        self.ThemeChange()

    def SetThemeColor(self,ThemeColor:QColor):
        '''
        设置app主题颜色
        '''
        SetThemeColor(ThemeColor)
        self.ThemeChange()

    def SetFontName(self,FontName:str):
        '''
        设置app字体名称
        '''
        SetFontName(FontName)
        self.ThemeChange()

    def SetFontSize(self,FontSize:int):
        '''
        设置app字体大小
        '''
        SetFontSize(FontSize)
        self.ThemeChange()
    
    def SetFont(self,FontName:str,FontSize:int):
        '''
        设置app字体
        '''
        SetFontName(FontName)
        SetFontSize(FontSize)
        self.ThemeChange()

    def SetThemeAlpha(self,ThemeAlpha:int):
        '''
        设置app主题透明度
        '''
        SetThemeAlpha(ThemeAlpha)
        self.ThemeChange()

    def SetThemeImage(self,ThemeImage:str):
        '''
        设置app主题背景图片
        '''
        SetThemeImage(ThemeImage)
        self.ThemeChange()

    def ThemeChange(self):
        self.themechanged.emit()

    def WinThemeChange(self):
        if GetThemeMode()==ThemeMode.AUTO:
            self.ThemeChange()

    def __ThemeChangeEvent(self):#颜色或主题改变事件总链接
        ColorCache_.RenewColor()
        self.colorchanged.emit()
        UpdateStyleSheet()

themes=Theme_()#定义全局

class StyleSheetmanage(QThread):
    qsschanged=Signal(QObject)
    def __init__(self):
        super(StyleSheetmanage, self).__init__()
        self._widgets = []

    def Register(self, Widget:QObject):
        if Widget not in self._widgets:
            Widget.destroyed.connect(lambda: self._widgets.remove(Widget))
            self._widgets.append(Widget)

    def UnRegister(self, Widget:QObject):
        if Widget in self._widgets:
            self._widgets.remove(Widget)

    def run(self):
        print("当前注册控件数",len(self._widgets))
        for _widget in self._widgets:
            try:
                #槽函数传递
                print(_widget)
                self.qsschanged.emit(_widget)
            except:
                self._widgets.remove(_widget)

def QssChangeEvent(Widget:QObject):
    try:
        Widget.Renewqss()
    except:
        pass


def UpdateStyleSheet():
    QssManage.start()

QssManage = StyleSheetmanage()
QssManage.qsschanged.connect(QssChangeEvent)

