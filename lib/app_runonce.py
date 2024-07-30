from .app_config import Conf,ConfigKey
import sys,os,psutil,win32gui,win32process,win32con


def GetHandleFromPid(pid):#根据进程pid获取窗口句柄
    '''
    根据进程pid获取窗口句柄
    '''
    _handle = None
    def callback(_hwnd, _hwndlist):
        _, _foundpid = win32process.GetWindowThreadProcessId(_hwnd)
        if _foundpid == pid and win32gui.GetParent(_hwnd) == 0 and win32gui.IsWindowVisible(_hwnd):
            _hwndlist.append(_hwnd)
    _hwndlist = []
    win32gui.EnumWindows(callback, _hwndlist)
    if _hwndlist:
        _handle=_hwndlist[0]
    return _handle

def RunOnly():#运行一次
    '''
    限制程序只能运行一此,第二次打开时会置顶显示程序
    '''
    #获取app_config缓存进程的信息
    _pid=Conf.GetValue(ConfigKey.APP_PID)
    _pidname=Conf.GetValue(ConfigKey.APP_NAME)
    
    #获取目前app运行的真实进程信息
    _runpid=os.getpid()
    _runname = psutil.Process(_runpid).name()   

    #判断是否存在app_config缓存进程的信息。
    if _pid!=None and _pidname!=None and _pid!=str(_runpid):

        #获取全部进程列表
        _pids = psutil.process_iter()

        #遍历全部进程列表
        for _piditem in _pids:

            #判断进程列表的pid和进程名称与缓存是否一致，
            if _piditem.name() == _runname and _piditem.pid== _runpid:
                
                #获取窗口句柄
                _windowhandle = GetHandleFromPid(_runpid)

                #判断是否有最小化，最小化显示
                if win32gui.IsIconic(_windowhandle):
                    win32gui.ShowWindow(_windowhandle,4)

                #置顶显示后取消置顶
                win32gui.SetWindowPos(_windowhandle, win32con.HWND_TOPMOST, 0, 0, 0, 0,win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(_windowhandle, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,win32con.SWP_SHOWWINDOW|win32con.SWP_NOSIZE|win32con.SWP_NOMOVE)

                #退出当前运行进程
                sys.exit(0)
    
    #缓存app运行的真实进程信息进app_config
    Conf.SetValue(ConfigKey.APP_PID,str(_runpid))       
    Conf.SetValue(ConfigKey.APP_NAME,str(_runname)) 
