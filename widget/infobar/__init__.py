from PySide6.QtCore import QSize,QTimer,Signal,QObject,QPoint,QRect,QEvent,QEasingCurve
from PySide6.QtGui import QColor,QGuiApplication,QCursor
from PySide6.QtWidgets import QHBoxLayout

from enum import Enum
from typing import Union

from qss import Color_,ColorStyle,Font_,FontSize,FontWeight,BorderStyle
from lib import Position,ColorCache_,ShadowEffect

from ..button import ButtonBase
from ..label import LabelNormal
from ..showway import PopupInfo
from ..icon import Icon,IconView

class InfoType(Enum):
    """ Info bar icon """
    INFORMATION = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

InfoColor=QColor(0, 159, 170,255)
SuccessColor=QColor(15,123,15,255)
WarningColor=QColor(157,93,0,255)
ErrorColor=QColor(196,43,28,255)
        
InfoBackgroundColor=QColor(245,249,251,255)
SuccessBackgroundColor=QColor(223,246,221,255)
WarningBackgroundColor=QColor(255,244,206,255)
ErrorBackgroundColor=QColor(253,231,233,255)

class TitleLabel(LabelNormal):
    def __init__(self, *args, **kwargs):
        super(TitleLabel, self).__init__(*args, **kwargs)

    def Setqss(self):
        self.qss.SetColor(Color_(0,0,0,255))
        self.font_=Font_(FontSize=FontSize(Shift=0,Min=10,Max=16),FontWeight=FontWeight.bold)
        self.qss.SetFont(self.font_)
        self.qss.SetPadding(3,4,4,3)
   
class NormalLabel(LabelNormal):
    def __init__(self, *args, **kwargs):
        super(NormalLabel, self).__init__(*args, **kwargs)
        self.SetMaxWidth(400)
    
    def Setqss(self):
        self.qss.SetColor(Color_(0,0,0,255))
        self.font_=Font_(FontSize=FontSize(Shift=0,Min=10,Max=16))
        self.qss.SetFont(self.font_)
        self.qss.SetPadding(3,4,4,3)

class CloseBtn(ButtonBase):
    def __init__(self,ShowType:Union[InfoType,str],parent=None):
        self._showtype=ShowType
        super(CloseBtn, self).__init__(objectName="CloseBtn",EventFollow=False,parent=parent)
        #设置大小
        self.setFixedSize(20,20)
        #设置可聚焦
        self.SetFocusType(0)
        #设置图标
        self.SetIcon_(Icon.close,QSize(12,12))
        #加载事件
        self.MouseEventLoad(self)
        self.SetClickFunciton(False)

    def Setqss(self):
        self.qss.SetBorderWidth(Width=0)
        self.qss.SetBorderStyle(Style=BorderStyle.solid)
        self.qss.SetBorderRadius(Radius=5)
        self.qss.Set_("outline","none")
        self.qss.SetColor(Color_(ColorStyle.Dark))
        self.qss.SetBackgroundColor(self.__GetBackgroundColor(0))

    def _Colorin(self, animation_: bool = True):
        self.qss.SetBackgroundColor(self.__GetBackgroundColor(),True)
        
    def _Colorout(self, animation_: bool = True):
        self.qss.SetBackgroundColor(self.__GetBackgroundColor(0),True)

    def __GetBackgroundColor(self,Alpha:int=255):
        _bccolor=Color_(ColorStyle.Light).GetColor()

        if self._showtype==InfoType.INFORMATION or self._showtype==InfoType.INFORMATION.value:
            _color=Color_(InfoColor,_bccolor,"80%",FixAlpha=Alpha)
        elif self._showtype==InfoType.SUCCESS or self._showtype==InfoType.SUCCESS.value:
            _color=Color_(SuccessColor,_bccolor,"80%",FixAlpha=Alpha)
        elif self._showtype==InfoType.WARNING or self._showtype==InfoType.WARNING.value:
            _color=Color_(WarningColor,_bccolor,"80%",FixAlpha=Alpha)
        elif self._showtype==InfoType.ERROR or self._showtype==InfoType.ERROR.value:
            _color=Color_(ErrorColor,_bccolor,"80%",FixAlpha=Alpha)
        return _color

class InfoWidget(PopupInfo):
    infoclosed=Signal(QObject,bool)
    def __init__(self, ShowType:Union[InfoType,str], Title: str="", Text: str="",isClose=True,ExistTime=500,parent=None):
        super(InfoWidget,self).__init__(parent=parent)
        if self.parent()!=None:
            self.raise_()
            self.SetWindowNormal()
        else:
            #设置tool类型
            self.SetWindowTool()
        #存在变量
        self._exist=True
        self._closeState=False

        #布局
        self._layout=QHBoxLayout()
        self._layout.setSpacing(5)
        self._layout.setContentsMargins(0,0,0,0)
        self._showframe.layouts.setContentsMargins(5,5,5,5)
        self._showframe.layouts.addLayout(self._layout)
        
        #图标
        if ShowType==InfoType.INFORMATION or ShowType==InfoType.INFORMATION.value:
            self._icon=IconView(Icon.info,Color_(InfoColor),QSize(16,16))
            self._showframe.qss.SetBackgroundColor(Color_(InfoBackgroundColor))
        elif ShowType==InfoType.SUCCESS or ShowType==InfoType.SUCCESS.value:
            self._icon=IconView(Icon.success,Color_(SuccessColor),QSize(16,16))
            self._showframe.qss.SetBackgroundColor(Color_(SuccessBackgroundColor))
        elif ShowType==InfoType.WARNING or ShowType==InfoType.WARNING.value:
            self._icon=IconView(Icon.warning,Color_(WarningColor),QSize(16,16))
            self._showframe.qss.SetBackgroundColor(Color_(WarningBackgroundColor))
        elif ShowType==InfoType.ERROR or ShowType==InfoType.ERROR.value:
            self._icon=IconView(Icon.error,Color_(ErrorColor),QSize(16,16))
            self._showframe.qss.SetBackgroundColor(Color_(ErrorBackgroundColor))
        self._showframe.qss.SetBorderRadius(Radius=5)
        self._showframe._qssplus.ApplyQss()

        self._icon.setFixedSize(QSize(16,16))
        self._layout.addWidget(self._icon)

        #标题
        self._titleLabel=TitleLabel()
        self._titleLabel.setText(Title)
        self._layout.addWidget(self._titleLabel)

        #内容
        self._textLabel=NormalLabel()
        self._textLabel.setText(Text)
        self._layout.addWidget(self._textLabel)

        #关闭按钮
        if isClose:
            self._closebtn=CloseBtn(ShowType)
            self._layout.addWidget(self._closebtn)
            self._closebtn.clicked.connect(self.__CloseEvent)
        else:
            self._layout.setContentsMargins(0,0,10,0)

        self.closed.connect(self.__CloseStateChange)

        #阴影
        self._shadow=ShadowEffect(Color_(ColorStyle.FullColor,30),15,QPoint(0,2))
        self._showframe.setGraphicsEffect(self._shadow)
        
        #关闭事件
        QTimer.singleShot(ExistTime,self.__CloseEvent)
   
    def __SetExist(self,_exist:bool):
        self._exist=_exist
        self.infoclosed.emit(self,True)

    def __CloseEvent(self):
        if self._closeState==False:
            self._closeState=True
            self.__SetExist(False)
    
    def __CloseStateChange(self):
        self._closeState=True
  
class Info(QObject):#继承QThread
    def __init__(self,Position_:Position=Position.TOP,ExistTime:int=7000,ShiftPoint:QPoint=QPoint(0,0),parent=None):
        '''
        Position_ 显示位置,不能lefe、right、none、center
        ExistTime 存在时间
        Shift 偏移高度
        parent 父窗口
        '''
        super(Info,self).__init__(parent=parent)
        self._infoList=[]
        self._existTime=ExistTime
        self._closeTime=300
        self._shiftPoint=ShiftPoint
        self._position=Position_
        self.runs=False
        self.__CalStartPoint()

        if parent is not None:
            parent.installEventFilter(self)
    
    def __CalStartPoint(self):
        '''
        计算高度
        '''
        #判断是否有父窗口
        if self.parent()==None:
            #取坐标所在屏幕
            pos_=QCursor.pos()
            for window in QGuiApplication.screens():
                rect=window.availableGeometry()
                if pos_.x()>=rect.x() and pos_.x()<=rect.x()+rect.width():
                    break
        else:
            #获取父窗口大小坐标
            _parenrRect=self.parent().geometry()
            rect=QRect(0,0,_parenrRect.width(),_parenrRect.height())

        if self._position== Position.TOP or self._position== Position.TOP_LEFT or \
            self._position== Position.TOP_RIGHT or self._position== Position.LEFT_TOP or \
            self._position== Position.RIGHT_TOP: 

            self.height_=0


        elif self._position== Position.BOTTOM or self._position== Position.BOTTOM_LEFT or \
            self._position== Position.BOTTOM_RIGHT or self._position== Position.LEFT_BOTTOM or \
            self._position== Position.RIGHT_BOTTOM: 
    
            self.height_=rect.height()

    def ShowInfo(self,
                 ShowType:Union[InfoType,str],
                 Title:str="",
                 Text: str="",
                 isClose:bool=True,
                 ShowTime:int=500,\
                 MoveMultiple:float=1,
                 Mouse:bool=False):
        '''
        ShowType:info类型
        Title:标题
        Text:内容
        isClose:关闭按钮
        ShowTime:显示事件
        MoveMultiple:位置弹出系数
        Mouse:鼠标穿透
        '''
        info=InfoWidget(ShowType,Title,Text,isClose,self._existTime,parent=self.parent())

        #计算位置
        h=0
        for item in self._infoList:
            h+=item.height()
        #info加入
        self._infoList.append(info)
        #关闭事件绑定
        info.infoclosed.connect(self.__Close)
        #显示
        info.Exec(h,self._position,Duration=ShowTime,Opacity=True,ShiftPoint=self._shiftPoint,MoveMultiple=MoveMultiple,Mouse=Mouse)

        if self.runs:
            self.RenewPos(False)

    def __Close(self,object,FirstPos:bool=False):
        if self.runs==False:
            self.runs=True#关闭动画标识打开
            if self._position== Position.TOP or self._position== Position.TOP_LEFT or \
               self._position== Position.TOP_RIGHT or self._position== Position.LEFT_TOP or \
               self._position== Position.RIGHT_TOP: 

                object.Close(Position.TOP,QEasingCurve.InQuad,self._closeTime,True,1,lambda: self.__Delete(object))

            elif self._position== Position.BOTTOM or self._position== Position.BOTTOM_LEFT or \
                 self._position== Position.BOTTOM_RIGHT or self._position== Position.LEFT_BOTTOM or \
                 self._position== Position.RIGHT_BOTTOM: 

                object.Close(Position.BOTTOM,QEasingCurve.InQuad,self._closeTime,True,1,lambda: self.__Delete(object))
         
            # self.RenewPos(FirstPos)

    def __Delete(self,object):
        #list中删除item，删除立马消失，需要等动画完成执行。
        self._infoList.remove(object)
        object.close()
        #删除动画执行完毕变量
        self.runs=False
        if len(self._infoList)!=0:#list还有item
            self.RenewPos()
            if self._infoList[0]._exist==False:
                self.__Close(self._infoList[0])

    def RenewPos(self,FirstPos:bool=True):#刷新位置
        '''
        FirstPos:是否包含第一个
        '''
        if self.runs and FirstPos:
            return
        
        _start=0 if FirstPos==True else 1#执行关闭动画时忽略list的第一个item

        _parenrRect=self.parent().geometry()
        rect=QRect(0,0,_parenrRect.width(),_parenrRect.height())

        h=0
        if len(self._infoList)!=0:
            for i in range(_start,len(self._infoList)):
                x_,y_=0,0

                if self._position==Position.LEFT:
                    x_=rect.x()+self._shiftPoint.x()
                    y_=rect.y()+int((rect.height()-self._infoList[i].height())/2)+self._shiftPoint.y()
                elif self._position==Position.TOP:
                    x_=rect.x()+int((rect.width()-self._infoList[i].width())/2)+self._shiftPoint.x()
                    y_=rect.y()+self._shiftPoint.y()
                elif self._position==Position.RIGHT:
                    x_=rect.x()+rect.width()-self._infoList[i].width()-self._shiftPoint.x()
                    y_=rect.y()+int((rect.height()-self._infoList[i].height())/2)+self._shiftPoint.y()
                elif self._position==Position.BOTTOM:
                    x_=rect.x()+int((rect.width()-self._infoList[i].width())/2)+self._shiftPoint.x()
                    y_=rect.x()+rect.height()-self._infoList[i].height()-self._shiftPoint.y()
                elif self._position==Position.TOP_LEFT or self._position==Position.LEFT_TOP:
                    x_=rect.x()+self._shiftPoint.x()
                    y_=rect.y()+self._shiftPoint.y()
                elif self._position==Position.TOP_RIGHT or self._position==Position.RIGHT_TOP:
                    x_=rect.x()+rect.width()-self._infoList[i].width()-self._shiftPoint.x()
                    y_=rect.y()+self._shiftPoint.y()
                elif self._position==Position.BOTTOM_LEFT or self._position==Position.LEFT_BOTTOM:
                    x_=rect.x()+self._shiftPoint.x()
                    y_=rect.x()+rect.height()-self._infoList[i].height()-self._shiftPoint.y()
                elif self._position==Position.BOTTOM_RIGHT or self._position==Position.RIGHT_BOTTOM:
                    x_=rect.x()+rect.width()-self._infoList[i].width()-self._shiftPoint.x()
                    y_=rect.x()+rect.height()-self._infoList[i].height()-self._shiftPoint.y()
                elif self._position==Position.CENTER or self._position==Position.NONE:
                    x_=rect.x()+int((rect.width()-self._infoList[i].width())/2)+self._shiftPoint.x()
                    y_=rect.y()+int((rect.height()-self._infoList[i].height())/2)+self._shiftPoint.y()

                if self._position==Position.LEFT or self._position==Position.TOP or self._position==Position.RIGHT or \
                    self._position==Position.TOP_LEFT or self._position==Position.LEFT_TOP or self._position==Position.TOP_RIGHT or \
                        self._position==Position.RIGHT_TOP:
                    
                    point_=QPoint(x_,y_+h)
                
                elif self._position==Position.BOTTOM or self._position==Position.BOTTOM_LEFT or self._position==Position.LEFT_BOTTOM or \
                    self._position==Position.BOTTOM_RIGHT or self._position==Position.RIGHT_BOTTOM:

                    point_=QPoint(x_,y_-h)

                self._infoList[i].Move(point_)
                h+=self._infoList[i].height()

    def eventFilter(self, obj, e: QEvent):
        if obj == self.parent() and e.type() == 14:
            self.RenewPos()
        return super().eventFilter(obj, e)

 
#self.ee.showinfo(InfoType.SUCCESS,"123","asdasdaf",False,500,self)
#self.ee=_infoList(QPoint(100,100),False,4000,parent=self)

