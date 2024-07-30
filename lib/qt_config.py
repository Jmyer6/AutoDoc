from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QGuiApplication,QCursor,QColor

from .app_config import Conf,ConfigKey

from enum import Enum
from typing import Union

import win32gui,win32print,win32con

class ThemeMode(Enum):#主题类型标识
    '''
    主题类型
    '''
    LIGHT = "Light" #浅色标识
    DARK = "Dark"  #深色标识
    AUTO = "Auto"  #跟随系统标识

def GetThemeMode():
    '''
    返回主题模式
    '''
    _thememode=Conf.GetValue(ConfigKey.THEME_MODE) 
    if _thememode==ThemeMode.LIGHT.value:
        return(ThemeMode.LIGHT)
    elif _thememode==ThemeMode.DARK.value:
        return(ThemeMode.DARK)
    elif _thememode==ThemeMode.AUTO.value:
        return(ThemeMode.AUTO)
    else:
        return(ThemeMode.LIGHT)
    
def GetThemeColor():
    '''
    返回主题颜色
    '''
    from .qt_color import StrToQcolor
    _themecolor=Conf.GetValue(ConfigKey.THEME_COLOR) 
    if _themecolor==None:#默认色
        return(QColor(14,145,255,255))
    else:
        return(StrToQcolor(_themecolor))

def GetThemeAlpha():
    '''
    返回主题透明度
    '''
    _themealpha=Conf.GetValue(ConfigKey.THEME_ALPHA) 
    if _themealpha==None:#默认透明度
        return(255)
    else:
        return(int(_themealpha))
    
def GetThemeImage():
    '''
    返回主题背景图路径或是颜色
    '''
    _themeimage=Conf.GetValue(ConfigKey.THEME_IMAGE) 
    if _themeimage==None:#默认没有
        return(None)
    else:
        return(_themeimage)

def GetFontName():
    '''
    返回字体名称
    '''
    _fontname=Conf.GetValue(ConfigKey.FONT_NAME) 
    if _fontname==None:#默认字体
        return("Segoe UI")
    else:
        return(_fontname)

def GetFontSize():
    '''
    返回字体大小
    '''
    _fontsize=Conf.GetValue(ConfigKey.FONT_SIZE) 
    if _fontsize==None:#默认字体大小
        return(13)
    else:
        return(int(_fontsize))

def GetScaleFactor(Default:str="1"):
    '''
    返回app缩放比例

    default:默认缩放比例,例子:"1"=100% "1.5"=150% "2"=200%
    '''
    def __GetScaling():#获取系统缩放比例
        # 获取当前显示器的设备上下文
        _hdc = win32gui.GetDC(0)
        # 获取系统的水平DPI
        _dpi_x = win32print.GetDeviceCaps(_hdc, win32con.LOGPIXELSX)
        # 释放设备上下文
        win32gui.ReleaseDC(0, _hdc)
        # 计算缩放比例
        _dpi_scale = _dpi_x / 96.0  # 96 DPI 是标准的缩放比例
        return _dpi_scale

    _factor=Conf.GetValue(ConfigKey.SCALE_FACTOR) 
    if _factor==None:
        return(Default)
    elif _factor=="follow":#和设置函数同步标识
        return str(__GetScaling())
    else:
        return(_factor)

def GetResolutionRatio(Default:QSize=QSize(800,500)):
    '''
    返回app初始分辨率

    Default:默认分辨率
    '''
    _resolution=Conf.GetValue(ConfigKey.RESOLUTION) 
    if _resolution==None:
        _size=Default
    else:#和设置函数同步格式 800 x 500
        _sizespilt=str(_resolution).split(" x ")
        _size=QSize(int(_sizespilt[0]),int(_sizespilt[1]))
    return _size

def GetLoginInfo():
    '''
    返回登录信息
    '''
    _loginsave=Conf.GetValue(ConfigKey.LOGIN_SAVE)
    _username=None
    _password=None
    _dbpath=None
    _dbport=None

    if _loginsave=="True":#和设置函数同步标识
        _username=Conf.GetValue(ConfigKey.LOGIN_USERNAME)
        _password=Conf.GetValue(ConfigKey.LOGIN_PASSWORD)
        _dbpath=Conf.GetValue(ConfigKey.LOGIN_DB_PATH)
        _dbport=Conf.GetValue(ConfigKey.LOGIN_DB_PORT)

    return(_username,_password,_dbpath,_dbport)


def SetThemeMode(ThemeMode_:ThemeMode):
    """
    设置主题模式
    """
    Conf.SetValue(ConfigKey.THEME_MODE,ThemeMode_.value)

def SetThemeColor(ThemeColor:QColor):
    """
    设置主题颜色
    """
    from .qt_color import QcolorToStr
    Conf.SetValue(ConfigKey.THEME_COLOR,QcolorToStr(ThemeColor))

def SetThemeAlpha(ThemeAlpha:int):
    """
    设置主题透明度
    """
    Conf.SetValue(ConfigKey.THEME_ALPHA,str(ThemeAlpha))

def SetThemeImage(ThemeImage:Union[str,QColor]):
    """
    设置主题图片

    ThemeImage:图片路径或颜色文本值
    """
    if isinstance(ThemeImage,QColor):#颜色文本值
        from .qt_color import QcolorToStr
        ThemeImage=QcolorToStr(ThemeImage)

    Conf.SetValue(ConfigKey.THEME_IMAGE,ThemeImage)

def SetFontName(FontName:str):
    '''
    设置字体名称
    '''
    Conf.SetValue(ConfigKey.FONT_NAME,FontName)

def SetFontSize(FontSize:int):
    '''
    设置字体大小
    '''
    Conf.SetValue(ConfigKey.FONT_SIZE,str(FontSize))

def SetScaleFactor(ScaleFactor:Union[float,str]):
    '''
    设置缩放比例

    ScaleFactor:缩放比例,例子:1.0=100% 1.5=150% 2.0=200%,"follow"跟随系统
    '''
    if isinstance(ScaleFactor,float):#浮点数
        ScaleFactor=str(ScaleFactor)

    Conf.SetValue(ConfigKey.SCALE_FACTOR,ScaleFactor)

def SetResolutionRatio(ResolutionRatio:QSize):
    '''
    设置分辨率
    '''
    Conf.SetValue(ConfigKey.RESOLUTION,str(ResolutionRatio.width())+' x '+str(ResolutionRatio.height()))

def SetLoginInfo(LoginSave:bool,UserName:str,PassWord:str,Dbpath:str,Dbport:str):
    '''
    设置登录信息

    LoginSave:是否保存登录信息
    UserName:用户名
    PassWord:密码
    Dbpath:数据库路径
    Dbport:数据库端口
    '''
    if LoginSave:
        Conf.SetValue(ConfigKey.LOGIN_SAVE,"True")
        Conf.SetValue(ConfigKey.LOGIN_USERNAME,UserName)
        Conf.SetValue(ConfigKey.LOGIN_PASSWORD,PassWord)
        Conf.SetValue(ConfigKey.LOGIN_DB_PATH,Dbpath)
        Conf.SetValue(ConfigKey.LOGIN_DB_PORT,Dbport)
    else:
        Conf.SetValue(ConfigKey.LOGIN_SAVE,"False")
   
   
def CenterShow(Widget:QWidget,Default:QSize=QSize(800,500)):
    '''
    窗口居中
    
    Widget:窗口
    Default:默认窗口大小
    '''
    #设置大小
    Widget.resize(Default)

    #取鼠标所在屏幕
    _pos=QCursor.pos()
    for _window in QGuiApplication.screens():
        _rect1,_rect2=_window.availableGeometry(),_window.geometry()
        if _pos.x()>=_rect1.x() and _pos.x()<=_rect1.x()+_rect1.width():
            break
    
    #计算窗口偏移量
    taskbarheight,taskbarheight=_rect2.height()-_rect1.height(),_rect2.width()-_rect2.width()
    
    #定位坐标
    _x=_rect1.x()+int((_rect1.width()-Widget.width()-taskbarheight)/2)
    _y=_rect1.y()+int((_rect1.height()-Widget.height()-taskbarheight)/2)
    
    #限制范围
    _x=0 if _x<0 else _x
    _y=0 if _y<0 else _y

    Widget.move(_x,_y)
    