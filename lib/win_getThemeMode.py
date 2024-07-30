def GetWindowThememode(): #获取系统主题
    '''
    True:深色模式
    False:浅色模式
    '''
    try:
        import winreg
    except ImportError:
        return False
    
    _registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    _regkeypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    try:
        _reg_key = winreg.OpenKey(_registry, _regkeypath)
    except FileNotFoundError:
        return False

    for i in range(1024):
        try:
            _valuename, _value, _ = winreg.EnumValue(_reg_key, i)
            if _valuename == 'AppsUseLightTheme':
                return _value == 0
        except OSError:
            break
    return False