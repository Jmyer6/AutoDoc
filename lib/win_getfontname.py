def SpiltName(Name:str):
    '''
    去除字体多余字符
    '''
    Name=Name.split(" (TrueType)")
    Name=Name[0].split(" & ")
    Name=Name[0].split(" (")
    for i in range(30):
        Name=Name[0].split(" "+str(i)+",")  
    return Name[0]

def CheckName(Name:str):
    '''
    因为某些系统字体会在qt中报错,去除这些报错字体

    错误大致为  DirectWrite: CreateFontFaceFromHDC() failed (指示输入文件 (例如字体文件) 中的错误。) for QFontDef(Family="Small Fonts", pointsize=11.25, pixelsize=13, styleHint=5, weight=400, stretch=100, hintingPreference=0) LOGFONT("Small Fonts", lfWidth=0, lfHeight=-13) dpi=96
    '''
    if Name=="MS Sans Serif":
        return False
    elif Name=="Modern":
        return False
    elif Name=="MS Serif":
        return False
    elif Name=="Roman":
        return False
    elif Name=="Script":
        return False
    elif Name=="Small Fonts":
        return False
    return True

def GetFontNameList():
    try:
        import winreg
    except ImportError:
        return False
    
    _fontNamelist = []
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts')
        for  i in range(winreg.QueryInfoKey(key)[1]):
            name, value, type= winreg.EnumValue(key, i)
            _name=SpiltName(name)
            if CheckName(_name):
                _fontNamelist.append(_name)
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts')
        for  i in range(winreg.QueryInfoKey(key)[1]):
            name, value, type= winreg.EnumValue(key, i)
            _name=SpiltName(name)
            if CheckName(_name):
                _fontNamelist.append(_name)
        _fontNamelist.sort()
    except:
        pass

    return _fontNamelist