
import winreg,sys,os,ctypes

def IsAdmin():#判断管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class WinStartup():
    '''
    程序开机启动类
    '''
    def __init__(self):
        #判断管理员权限
        if IsAdmin()==False:
            #重新启动程序
            ctypes.windll.shell32.ShellExecuteW(None,"runas", sys.executable, __file__, None, 1)
            sys.exit(0)
        self._regeditname=self.__GetRegeditName()
        self._regeditlink=r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run'

    def __GetRegeditName(self):
        (filepath, filename) = os.path.split(sys.argv[0])
        (name, suffix) = os.path.splitext(filename)
        return name

    def StartupLoad(self):#读取是否写入开机启动
        '''
        读取是否写入开机启动,写入则返回写入的路径,否则返回None
        '''
        try:
            _key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,self._regeditlink, access=winreg.KEY_ALL_ACCESS)
            _software, REG_SZ = winreg.QueryValueEx(_key, self._regeditname)
            _software = bytes(_software,encoding="utf-8").decode()
            winreg.CloseKey(_key)
            _key.Close()
        except :
            _software =None
        return(_software)

    def StartupWrite(self):#写入开机启动
        '''
        写入开机启动,成功返回True,否则返回False
        '''
        _key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,self._regeditlink, access=winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(_key,self._regeditname, 0, winreg.REG_SZ,sys.argv[0])
        winreg.CloseKey(_key)
        _key.Close()
        try:

            _key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,self._regeditlink, access=winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(_key,self._regeditname, 0, winreg.REG_SZ,sys.argv[0])
            winreg.CloseKey(_key)
            _key.Close()
            return(True)
        except :
            return(False)

    def StartupDelete(self):#取消开机启动
        '''
        取消开机启动,成功返回True,否则返回False
        '''
        try:
            _key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self._regeditlink, access=winreg.KEY_ALL_ACCESS)
            winreg.DeleteValue(_key,self._regeditname)
            winreg.CloseKey(_key)
            _key.Close()
            return(True)
        except :
            return(False)


  
