from PySide6.QtCore import QPoint,QPointF,QRect,QRectF,QSize


def IntExcess(Start:int,End:int,ExcessValue:int=0,ExcessMax:int=100):
    '''
    数值int过度
        
    Start:起始值
    End:目标值
    ExcessValue:过度当前位置
    ExcessMax:过度最大值

    算法:Start到End分成ExcessMax份,ExcessValue为当前第几份的值
    '''
    return int(Start+int((End-Start)/ExcessMax*ExcessValue))

def FloatExcess(Start:float,End:float,ExcessValue:int=0,ExcessMax:int=100):
    '''
    数值float过度
        
    Start:起始值
    End:目标值
    ExcessValue:过度当前位置
    ExcessMax:过度最大值
    
    算法:Start到End分成ExcessMax份,ExcessValue为当前第几份的值
    '''
    return Start+(End-Start)/ExcessMax*ExcessValue

def QPointExcess(Start:QPoint,End:QPoint,ExcessValue:int=0,ExcessMax:int=100):
    '''
    坐标过度
        
    Start:起始值
    End:目标值
    ExcessValue:过度当前位置
    ExcessMax:过度最大值
    
    算法:Start到End分成ExcessMax份,ExcessValue为当前第几份的值
    '''
    return QPoint(IntExcess(Start.x(),End.x(),ExcessValue,ExcessMax),IntExcess(Start.y(),End.y(),ExcessValue,ExcessMax))

def QPointfExcess(Start:QPointF,End:QPointF,ExcessValue:int=0,ExcessMax:int=100):
    '''
    坐标float过度
        
    Start:起始值
    End:目标值
    ExcessValue:过度当前位置
    ExcessMax:过度最大值
    
    算法:Start到End分成ExcessMax份,ExcessValue为当前第几份的值
    '''
    return QPointF(FloatExcess(Start.x(),End.x(),ExcessValue,ExcessMax),FloatExcess(Start.y(),End.y(),ExcessValue,ExcessMax))

def QRectExcess(Start:QRect,End:QRect,ExcessValue:int=0,ExcessMax:int=100):
    '''
    矩形过度
        
    Start:起始值
    End:目标值
    ExcessValue:过度当前位置
    ExcessMax:过度最大值
    
    算法:Start到End分成ExcessMax份,ExcessValue为当前第几份的值
    '''
    return QRect(IntExcess(Start.x(),End.x(),ExcessValue,ExcessMax),\
                    IntExcess(Start.y(),End.y(),ExcessValue,ExcessMax),\
                    IntExcess(Start.width(),End.width(),ExcessValue,ExcessMax),\
                    IntExcess(Start.height(),End.height(),ExcessValue,ExcessMax))

def QRectfExcess(Start:QRectF,End:QRectF,ExcessValue:int=0,ExcessMax:int=100):
    '''
    矩形float过度
        
    Start:起始值
    End:目标值
    ExcessValue:过度当前位置
    ExcessMax:过度最大值
    
    算法:Start到End分成ExcessMax份,ExcessValue为当前第几份的值
    '''
    return QRectF(FloatExcess(Start.x(),End.x(),ExcessValue,ExcessMax),\
                    FloatExcess(Start.y(),End.y(),ExcessValue,ExcessMax),\
                    FloatExcess(Start.width(),End.width(),ExcessValue,ExcessMax),\
                    FloatExcess(Start.height(),End.height(),ExcessValue,ExcessMax)
    ) 

def QSizeExcess(Start:QSize,End:QSize,ExcessValue:int=0,ExcessMax:int=100):
    '''
    大小过度
        
    Start:起始值
    End:目标值
    ExcessValue:过度当前位置
    ExcessMax:过度最大值
    
    算法:Start到End分成ExcessMax份,ExcessValue为当前第几份的值
    '''
    return QSize(IntExcess(Start.width(),End.width(),ExcessValue,ExcessMax),\
                    IntExcess(Start.height(),End.height(),ExcessValue,ExcessMax))

def Range360(Number:int):
    '''
    数值限制在0-360内
    '''
    while Number > 359:
        Number=Number-360
    while Number < 0:
        Number=Number+360
    return Number