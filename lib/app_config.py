import sys,os,sqlite3
from enum import Enum
from typing import Union

#数据库名称
DataBaseName="\\config.Jmyer"
'''
在当前目录创建一个sqlite数据库,创建config表含name(char(255)),和value(char(255))2列数据。
'''

class ConfigKey(Enum):
    '''
    默认数据key
    '''
    THEME_MODE="thememode"
    THEME_COLOR="themecolor"
    THEME_ALPHA="themealpha"
    THEME_IMAGE="themeimage"

    FONT_NAME="fontname"
    FONT_SIZE="fontsize"

    SCALE_FACTOR="scalefactor"
    RESOLUTION="resolution"

    APP_PID="apppid"
    APP_NAME="appname"

    COLOR_LIST="colorlist"
    IMAGE_LIST="imagelist"

    HOTKEY_OPENWINDOW="hotkeyopenwindow"

    LOGIN_USERNAME="loginusername"
    LOGIN_PASSWORD="loginpassword"
    LOGIN_DB_PATH="logindbpath"
    LOGIN_DB_PORT="logindbport"
    LOGIN_SAVE="loginsave"

def GetLink():#获取当前目录
    '''
    获取当前目录
    '''
    if hasattr(sys, '_MEIPASS'):
        _path = os.path.dirname(os.path.realpath(sys.executable))
    else:
        _path= os.path.split(os.path.abspath( __file__))[0]
    return (_path.replace('\\','/'))

def GetDataBaseLink():#判断sqlite是否存在
    '''
    获取数据库路径,不含数据库名称

    存在返回路径,不存在返回None
    '''
    _link =GetLink()+DataBaseName
    _filelink, _file= os.path.split(_link)
    if os.path.exists(_link):#sqlite存在，返回sqlite路径
        return _link
    if not os.path.exists(_filelink):#不存在目录,创建目录
        os.mkdir(_filelink)
    return None

def CreateDataBase():#创建数据库
    '''
    创建数据库
    '''
    _link=GetDataBaseLink()
    if _link==None:
        #创建sqlite数据库并连接
        _conn = sqlite3.connect(GetLink()+DataBaseName)
        _cur = _conn.cursor()
        #不存在创建表
        _sql='CREATE table IF NOT EXISTS config (name char(512),value char(255))'
        _cur.execute(_sql)
        _conn.commit()
        #关闭连接
        _cur.close()
        _conn.close()

def GetValue(Key:str,Vague:bool=False,Number:bool=True):#获取值
    '''
    获取值

    Key:值的标识
    Vague:模糊搜索
    Number:返回第一个参数或者列表参数
    '''
    #vague 模糊
    _link=GetDataBaseLink()
    if _link==None:
        return None
    
    _conn = sqlite3.connect(_link)
    _cur = _conn.cursor()
    if Vague:
        _sql= 'SELECT value FROM config WHERE name like "%'+Key+'%"'
    else:
        _sql= 'SELECT value FROM config WHERE name="'+Key+'"'
    _conn.commit()
    _cur.execute(_sql)

    if Number:
        _values=_cur.fetchall()
    else:
        _values=_cur.fetchone()
    
    _cur.close()
    _conn.close()

    if not _values:
        return None

    if Number:
        return _values
    else:
        return _values[0]

def ChangeValue(Key:str,Value:str,Vague:bool=False):
    """
    修改值

    Key:值的标识
    Value:修改值
    Vague:模糊搜索
    Number:返回第一个参数或者列表参数
    """
    _link=GetDataBaseLink()
    if _link!=None:
        _conn = sqlite3.connect(_link)
        _cur = _conn.cursor()
        if Vague:
            _sql= 'INSERT INTO config SET value = "'+Value+'" WHERE name like "%'+Key+'%"'
        else:
            _sql= 'UPDATE config SET value = "'+Value+'" WHERE name="'+Key+'"'
        _cur.execute(_sql) 
        _conn.commit()
        _cur.close()
        _conn.close()
        return "successful"
    else:
        return None

def InsertValue(Key:str,Value:str):
    """
    插入值

    Key:值的标识
    Value:修改值
    """
    _link=GetDataBaseLink()
    if _link!=None:
        _conn = sqlite3.connect(_link)
        _cur = _conn.cursor()
        _sql= 'INSERT INTO config VALUES ("'+Key+'","'+Value+'")'
        _cur.execute(_sql) 
        _conn.commit()
        _cur.close()
        _conn.close()
        return "successful"
    else:
        return None

class Config():
    """
    app配置集
    """
    def __init__(self):
        CreateDataBase()

    def GetValue(self,Key:Union[ConfigKey,str]):
        '''
        获取值

        Key:值的标识 [ConfigKey:默认Key值的标识 , str:自定义Key值的标识 ]
        '''
        _key=Key.value if isinstance(Key,ConfigKey) else Key
        
        return GetValue(_key,Number=False)

    def SetValue(self,Key:Union[ConfigKey,str],Value:str):
        '''
        设置值

        Key:值的标识 [ConfigKey:默认Key值的标识 , str:自定义Key值的标识 ]
        Value:值
        '''
        _key=Key.value if isinstance(Key,ConfigKey) else Key

        if GetValue(_key)==None:
            InsertValue(_key,Value)
        else:
            ChangeValue(_key,Value)

Conf=Config()