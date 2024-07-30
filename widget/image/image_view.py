import os,math

from PySide6.QtGui import  QCloseEvent, QPainter, QPixmap, QWheelEvent,QPainterPath
from PySide6.QtCore import QRectF,QSize,Qt,QEasingCurve,Signal,QRect,QPoint
from PySide6.QtWidgets import QGraphicsItem,QGraphicsPixmapItem,QGraphicsScene,\
    QLabel,QGraphicsView,QFrame,QHBoxLayout

from qss import QssPlusClass,Color_,ColorStyle,BorderStyle,TextAlign,GradientColor,\
    GradientColorList,GradientSpread,GradientStyle,QssManage
from lib import ShadowEffect,ConvenientSet,Animation,Position
from icon import GetLink
from typing import Union

from ..button import ButtonTransparent,ButtonNormal
from ..icon.icon_view import IconView,Icon
from ..label import LabelNormal
from ..frame import MoveFrame,MaskFrame
from ..showway import Popup_
from ..window import WindowsFramelessWindow

def GetRadiusPath(PixmapRect:QRect,ImageRadius:QRect):
    path = QPainterPath()
    
    #取图像长宽最小值
    _min=PixmapRect.width() if PixmapRect.width()<PixmapRect.height() else PixmapRect.height()
    _min=math.ceil(_min/2)

    #限制圆角不超出范围
    lt=ImageRadius.x() if ImageRadius.x()<_min else _min
    rt=ImageRadius.y() if ImageRadius.y()<_min else _min
    lb=ImageRadius.width() if ImageRadius.width()<_min else _min
    rb=ImageRadius.height() if ImageRadius.height()<_min else _min

    path.moveTo(PixmapRect.topLeft().x() + lt, PixmapRect.topLeft().y() + lt)

    if lt==0:
        path.lineTo(PixmapRect.topLeft())
    else:
        path.arcTo(QRect(PixmapRect.topLeft(), QSize(lt * 2, lt * 2)), 90, 90)

    if lb==0:
        path.lineTo(PixmapRect.bottomLeft())
    else:
        path.arcTo(QRect(QPoint(PixmapRect.x(), PixmapRect.height() - lb * 2), QSize(lb * 2, lb * 2)), 180, 90)

    if rb==0:
        path.lineTo(PixmapRect.bottomRight()+QPoint(1,0))
    else:
        path.arcTo(QRect(QPoint(PixmapRect.width() - rb * 2, PixmapRect.height() - rb * 2), QSize(rb * 2, rb * 2)), 270, 90)

    if rt==0:
        path.lineTo(PixmapRect.topRight()+QPoint(1,0))
    else:
        path.arcTo(QRect(QPoint(PixmapRect.topRight().x() - rt * 2+1, PixmapRect.topRight().y()), QSize(rt * 2, rt * 2)), 0, 90)

    path.lineTo(PixmapRect.topLeft().x() + lt, PixmapRect.topLeft().y())

    return path

def SetImageRadius(Pixmap:QPixmap,Size:QSize,ImageRadius:QRect):
    '''
    设置image 圆角

    Pixmap:图片缓存
    Size:图片大小
    ImageRadius:圆角大小,QRect(左上角,右上角,左下角,右下角)
    '''
    # 加载图片
    pixmap = Pixmap.scaled(Size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation,Qt.IgnoreAspectRatio)

    # 绘制圆角图片
    roundpixmap = QPixmap(pixmap.size())
    roundpixmap.fill(Qt.transparent)
    painter = QPainter(roundpixmap)
    painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
    painter.setClipPath(GetRadiusPath(pixmap.rect(),ImageRadius))
    painter.drawPixmap(0, 0, pixmap)
    painter.end()

    # 设置为标签背景
    return roundpixmap

class ImageTool(MoveFrame,QssPlusClass):
    '''
    图像按钮组

    LoadShow:初次加载是否显示
    EasingCurve:动画曲线,参考函数QEasingCurve
    Duration:动画时间
    '''
    def __init__(self, 
                 LoadShow:bool=True,\
                 EasingCurve:QEasingCurve=QEasingCurve.OutQuad,\
                 Duration:int = 300,\
                 parent=None):
        super(ImageTool, self).__init__(LoadShow=LoadShow,EasingCurve=EasingCurve,Duration=Duration,parent=parent)
        self.QssApply(self,"ImageTool",True,False)
        self.__SetLayout()

    def Setqss(self):
        self.qss.SetBorderWidth(Width=1)
        self.qss.SetBorderStyle(Style=BorderStyle.solid)
        self.qss.SetBorderRadius(Radius=5)
        self.qss.SetBorderColor(Color=Color_(ColorStyle.FullColor,20))
        self.qss.SetBackgroundColor(Color_(ColorStyle.FullColor,0,FixAlpha=150))
        return super().Setqss()
   
    def __SetLayout(self):
        self._btnlayouts=QHBoxLayout()
        self._btnlayouts.setSpacing(3)
        self._btnlayouts.setContentsMargins(3,3,3,3)
        self.layouts.addLayout(self._btnlayouts)

        self._zoomout=None
        self._zoomin=None
        self._zoomlabel=None
        self._rotateright=None
        self._rotateleft=None
        self._zoomadapt=None
        self._zoom1_1=None
        self._close=None
        self._fullsize=None

    def SetZoomOut(self,Open:bool=True):
        if Open and self._zoomout==None:
            self._zoomout=ButtonTransparent()
            self._zoomout.setToolTip("放大")
            self._zoomout.setFixedSize(28,25)
            self._zoomout.SetIcon_(Icon.zoom1)
            self.__ReNewLayout()
        elif not Open and self._zoomout!=None:
            self._zoomout.deleteLater()
            self._zoomout=None

    def SetZoomIn(self,Open:bool=True):
        if Open and self._zoomin==None:
            self._zoomin=ButtonTransparent()
            self._zoomin.setToolTip("缩小")
            self._zoomin.setFixedSize(28,25)
            self._zoomin.SetIcon_(Icon.zoom2)
            self.__ReNewLayout()
        elif not Open and self._zoomin!=None:
            self._zoomin.deleteLater()
            self._zoomin=None

    def SetZoomLabel(self,Open:bool=True):
        if Open and self._zoomlabel==None:
            self._zoomlabel=LabelNormal()
            self._zoomlabel.setFixedSize(45,25)
            self.__ReNewLayout()
        elif not Open and self._zoomlabel!=None:
            self._zoomlabel.deleteLater()
            self._zoomlabel=None

    def SetRotateRight(self,Open:bool=True):
        if Open and self._rotateright==None:
            self._rotateright=ButtonTransparent()
            self._rotateright.setToolTip("顺时针旋转90度")
            self._rotateright.setFixedSize(28,25)
            self._rotateright.SetIcon_(Icon.rotate1,QSize(20,20),QSize(20,20))
            self.__ReNewLayout()
        elif not Open and self._rotateright!=None:
            self._rotateright.deleteLater()
            self._rotateright=None

    def SetRotateLeft(self,Open:bool=True):
        if Open and self._rotateleft==None:
            self._rotateleft=ButtonTransparent()
            self._rotateleft.setToolTip("逆时针旋转90度")
            self._rotateleft.setFixedSize(28,25)
            self._rotateleft.SetIcon_(Icon.rotate2,QSize(20,20),QSize(20,20))
            self.__ReNewLayout()
        elif not Open and self._rotateleft!=None:
            self._rotateleft.deleteLater()
            self._rotateleft=None

    def SetZoomAdapt(self,Open:bool=True):
        if Open and self._zoomadapt==None:
            self._zoomadapt=ButtonTransparent()
            self._zoomadapt.setToolTip("缩放以适应")
            self._zoomadapt.setFixedSize(28,25) 
            self._zoomadapt.SetIcon_(Icon.size1,QSize(20,20),QSize(20,20))
            self.__ReNewLayout()
        elif not Open and self._zoomadapt!=None:
            self._zoomadapt.deleteLater()
            self._zoomadapt=None

    def SetZoom1_1(self,Open:bool=True):
        if Open and self._zoom1_1==None:
            self._zoom1_1=ButtonTransparent()
            self._zoom1_1.setToolTip("缩放到实际大小")  
            self._zoom1_1.setFixedSize(28,25)
            self._zoom1_1.SetIcon_(Icon.size2,QSize(20,20),QSize(20,20))
            self.__ReNewLayout()
        elif not Open and self._zoom1_1!=None:  
            self._zoom1_1.deleteLater()
            self._zoom1_1=None

    def SetClose(self,Open:bool=True):
        if Open and self._close==None:
            self._close=ButtonTransparent()
            self._close.setToolTip("关闭")
            self._close.setFixedSize(28,25)
            self._close.SetIcon_(Icon.close)
            self.__ReNewLayout()
        elif not Open and self._close!=None:
            self._close.deleteLater()
            self._close=None

    def SetFullSize(self,Open:bool=True):
        if Open and self._fullsize==None:
            self._fullsize=ButtonNormal()
            self._fullsize.setToolTip("全屏")
            self._fullsize.setFixedSize(28,25)  
            self._fullsize.SetIcon_(Icon.fullscreen,QSize(20,20),QSize(20,20))
            self.__ReNewLayout()
        elif not Open and self._fullsize!=None:
            self._fullsize.deleteLater()
            self._fullsize=None

    def __ReNewLayout(self):
        if self._zoomlabel is not None:
            self._btnlayouts.addWidget(self._zoomlabel) 
        if self._zoomout is not None:
            self._btnlayouts.addWidget(self._zoomout)
        if self._zoomin is not None:
            self._btnlayouts.addWidget(self._zoomin)
        if self._rotateright is not None:
            self._btnlayouts.addWidget(self._rotateright)
        if self._rotateleft is not None:            
            self._btnlayouts.addWidget(self._rotateleft)
        if self._zoomadapt is not None:
            self._btnlayouts.addWidget(self._zoomadapt)
        if self._zoom1_1 is not None:
            self._btnlayouts.addWidget(self._zoom1_1)   
        if self._close is not None:
            self._btnlayouts.addWidget(self._close)   
        if self._fullsize is not None:
            self.layouts.addWidget(self._fullsize)

    def __ShowFullSize(self,show:bool=True):
        if show:
            self._btnlayouts.setSpacing(0)
            self._btnlayouts.setContentsMargins(0,0,0,0)
            self.qss.SetBorderColor(Color=Color_(ColorStyle.FullColor,20,FixAlpha=0))
            self.qss.SetBackgroundColor(Color_(ColorStyle.FullColor,0,FixAlpha=0),EventConnect=True)
        else:
            self._btnlayouts.setSpacing(3)
            self._btnlayouts.setContentsMargins(3,3,3,3)
            self.qss.SetBorderColor(Color=Color_(ColorStyle.FullColor,20))
            self.qss.SetBackgroundColor(Color_(ColorStyle.FullColor,0,FixAlpha=150),EventConnect=True)

    def SetButtonMode(self,Mode:int):
        '''
        设置按钮

        分为2种图片浏览模式,一种是带鼠标动作,一种是纯浏览

        1:只带全屏按钮,用于纯浏览模式显示带鼠标动作的浏览模式
        2:不含关闭按钮和全屏按钮,纯鼠标动作浏览模式
        3:含关闭按钮,不含全屏按钮,鼠标动作浏览模式退回纯浏览模式
        4:全部不显示
        '''
        if Mode==1:
            self.__ShowFullSize(True) 
        else:
            self.__ShowFullSize(False)

        if Mode==1:#只显示全屏按钮
            self.SetZoomOut(False)
            self.SetZoomIn(False)
            self.SetZoomLabel(False)
            self.SetRotateLeft(False)
            self.SetRotateRight(False)
            self.SetZoomAdapt(False)
            self.SetZoom1_1(False)
            self.SetClose(False)
            self.SetFullSize(True)
            self.setFixedSize(30,30) 
        elif Mode==2:
            self.SetZoomOut(True)
            self.SetZoomIn(True)
            self.SetZoomLabel(True)
            self.SetRotateRight(True)
            self.SetRotateLeft(True)
            self.SetZoomAdapt(True)
            self.SetZoom1_1(True)
            self.SetClose(False) 
            self.SetFullSize(False)
            self.setFixedSize(250,35) 
        elif Mode==3:
            self.SetZoomOut(True)
            self.SetZoomIn(True)
            self.SetZoomLabel(True)
            self.SetRotateRight(True)
            self.SetRotateLeft(True)
            self.SetZoomAdapt(True)
            self.SetZoom1_1(True)
            self.SetClose(True) 
            self.SetFullSize(False)
            self.setFixedSize(250,35)
            self.setFixedSize(280,35) 
        elif Mode==4:
            self.SetZoomOut(False)
            self.SetZoomIn(False)
            self.SetZoomLabel(False)
            self.SetRotateRight(False)
            self.SetRotateLeft(False)
            self.SetZoomAdapt(False)
            self.SetZoom1_1(False)
            self.SetClose(False)
            self.SetFullSize(False)
 
class ImageViewBase(QFrame,ConvenientSet):
    '''
    纯图片浏览

    IamgeLink:图片路径,picture文件夹内可直接应用文件名,如123.png
    FollowSize:图片大小跟随,开启跟随控件大小,关闭原图片等比例
    ImageRadius:图片圆角化,QRect(左上角,右上角,左下角,右下角)
    '''
    def __init__(self,IamgeLink:str=None,FollowSize:bool=False,ImageRadius:QRect=None,parent=None):
        super(ImageViewBase,self).__init__(parent=parent)
        #设置图片
        self._image=QLabel(self)
        #设置图片跟随label大小
        self._image.setScaledContents(True)
        #显示类型,跟随大小
        self._followsize=FollowSize
        #图片大小
        self._imagegeometry=None
        #图片圆角化
        self._imageradius=ImageRadius

        # self.setStyleSheet("QFrame{background:rgba(255,0,0,255);border:0px;padding:0px;margin:0px;}")

        self.SetIamge(IamgeLink)

    def SetFollowSize(self,FollowSize:bool=False):
        """
        设置图片大小跟随

        FollowSize:图片大小跟随,开启跟随控件大小,关闭原图片等比例
        """
        self._followsize=FollowSize
        self.resize(self.size())
    
    def GetImageName(self):
        '''
        返回图片名称
        '''
        return self._imagename

    def GetImageLink(self):
        '''
        返回图片路径
        '''
        return self._imagelink

    def SetIamge(self,IamgeLink:str):
        '''
        重新加载图片路径

        picture_link:图片路径,picture文件夹内可直接应用文件名,如123.png
        '''
        self._image.setScaledContents(True)
        
        #判断路径
        if  os.path.exists(IamgeLink):
            link_=IamgeLink
        elif os.path.exists(GetLink()+"\\picture\\"+IamgeLink):
            link_=GetLink()+"\\picture\\"+IamgeLink
        else:
            self._imagename=None
            self._imagelink=None
            return
          
        (filepath_, filename_) = os.path.split(link_)
        (name_, suffix_) = os.path.splitext(filename_)

        self._imagename=name_
        self._imagelink=link_

        self.__ImageSizeEvent()

    def __CalSize(self):
        '''
        计算图片大小
        '''
        w_=self.width()
        h_=self.height()
        pw_=self._image.pixmap().width()
        ph_=self._image.pixmap().height()

        x=0 if pw_==0 or ph_==0 or h_==0 else int(pw_/(ph_/h_))
        y=0 if ph_==0 or pw_==0 or w_==0 else int(ph_/(pw_/w_))

        if ph_>pw_:
            if x>w_:
                new_w,new_h=w_,y
            else:
                new_w,new_h=x,h_
        elif ph_<pw_:
            if y>h_:
                new_w,new_h=x,h_
            else:
                new_w,new_h=w_,y
        else:
            if w_>h_:
                new_w,new_h=h_,h_
            else:
                new_w,new_h=w_,w_

        return QSize(new_w,new_h)

    def __ImageSizeEvent(self):
        if self.isHidden():
            True

        if self._followsize:
            self._image.move(0,0)
            self._image.setFixedSize(self.width(),self.height())
        else:
            self._image.setFixedSize(self.__CalSize())
            self._image.move(int((self.width()-self._image.width())/2),int((self.height()-self._image.height())/2))

        self._imagegeometry=self._image.geometry()

        if self._imageradius==None:
            self._image.setPixmap(QPixmap(self._imagelink))
        else:
            self.__SetImageRadius(SetImageRadius(QPixmap(self._imagelink),self.__CalSize(),self._imageradius))

    def resizeEvent(self, a0) -> None:
        self.__ImageSizeEvent()
        return super().resizeEvent(a0)

    def SetAdjust(self):
        '''
        图片浏览会根据图片大小自适应
        '''
        _size=self.__CalSize()
        self.SetFollowSize(True)
        self.setFixedSize(_size)
    
class ImageView(ImageViewBase):
    '''
    图片浏览

    IamgeLink:图片路径,picture文件夹内可直接应用文件名,如123.png
    FollowSize:图片大小跟随,开启跟随控件大小,关闭原图片等比例
    ImageRadius:图片圆角化,QRect(左上角,右上角,左下角,右下角)

    SetEnterMove:鼠标进入图片放大功能 
    SetPopupView:图片弹窗预览功能
    ShowMaxWindow:图片全屏预览功能
    '''
    def __init__(self,
                 IamgeLink:str=None,
                 FollowSize:bool=False,
                 ImageRadius:QRect=None,
                 parent=None):
        super(ImageView,self).__init__(IamgeLink=IamgeLink,FollowSize=FollowSize,ImageRadius=ImageRadius,parent=parent)
        self._entermoveAnimation=None
        self._entermoveMovesize=0
        self._PopupViewIamgeSize=None
        self._PopupViewWindow=None
        self._maxFunction=False
        self._maxbutton=None

    def SetEnterMove(self,MoveSize:int=0,EasingCurve:QEasingCurve=QEasingCurve.InOutCirc,Duration:int = 200):
        '''
        MoveSize:图片移动距离,鼠标进入图片会移动,0表示不移动
        EasingCurve:动画曲线
        Duration:动画持续时间
        '''

        self._entermoveMovesize=MoveSize
        if MoveSize!=0:
            self._entermoveAnimation=Animation(0,EasingCurve,Duration)
            self._entermoveAnimation.Animationed.connect(self.__MoveSizeEvent)
        else:
            self._entermoveAnimation=None

    def __MoveSizeEvent(self,value:int):
        self._image.move(self._imagegeometry.x()-int(self._entermoveMovesize/100*value),\
                         self._imagegeometry.y()-int(self._entermoveMovesize/100*value))
        self._image.setFixedSize(self._imagegeometry.width()+int(self._entermoveMovesize/100*value*2),\
                            self._imagegeometry.height()+int(self._entermoveMovesize/100*value*2))

    def SetPopupView(self,IamgeSize:QSize=None,ShowName:bool=False,NameAlign_:TextAlign=None,Text:str=None,TextAlign:TextAlign=None):
        '''
        IamgeSize:图片大小
        ShowName:是否显示图片名称
        NameAlign_:图片名称文本对齐方式,只接受left、center、right
        Text:图片描述文本
        TextAlign:图片描述文本对齐方式,只接受left、center、right
        '''
        self._PopupViewIamgeSize=IamgeSize
        self._PopupViewShowName=ShowName
        self._PopupViewShowNameNameAlign=NameAlign_
        self._PopupViewText=Text
        self._PopupViewTextAlign=TextAlign
        self._PopupViewWindow=None
   
    def SetMaxWindow(self,Max:bool=True):
        """
        全屏显示
        """
        self._maxFunction=Max

        if Max:
            self._maxbutton=ImageTool(False,parent=self)
            self._maxbutton.SetButtonMode(1)
            self._maxbutton._fullsize.clicked.connect(self.ShowMaxWindow)
            self._maxbutton.Hide()
        else:
            self._maxbutton=None

    def ShowMaxWindow(self):
        #加载阴影窗口
        if isinstance(self.window(),WindowsFramelessWindow):
            _fullwindow=MaskFrame(parent=self.window().userFrame)
        else:
            _fullwindow=MaskFrame(parent=self.window())
        _imagewindow=ImageViewPlus(self._imagelink,False,_fullwindow)
        #大小同步
        _imagewindow.setGeometry(0,0,_fullwindow.width(),_fullwindow.height())
        _fullwindow.sizechangeed.connect(lambda: _imagewindow.setGeometry(0,0,_fullwindow.width(),_fullwindow.height()))
        #显示
        _fullwindow.Show()
        #关闭事件连接
        _imagewindow.closed.connect(_fullwindow.deleteLater)

    def enterEvent(self, event) -> None:
        if self._entermoveMovesize!=0:
            self._entermoveAnimation.GoValue(100)
        if self._PopupViewIamgeSize!=None:
            self._PopupViewWindow=ImagePopup(self.GetImageLink(),\
                                             self._PopupViewIamgeSize,\
                                             self._PopupViewShowName,\
                                             self._PopupViewShowNameNameAlign,\
                                             self._PopupViewText,\
                                             self._PopupViewTextAlign)
            self._PopupViewWindow.ExecWindowOut(self,QPoint(5,self._image.y()),Position.RIGHT_TOP)
        if self._maxFunction:
            self._maxbutton.move(self.width()-self._maxbutton.width()-10,self._image.y()+10)
            self._maxbutton.Show()

        return super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        if self._entermoveMovesize!=0:
            self._entermoveAnimation.GoValue(0)
        if self._PopupViewWindow!=None:
            self._PopupViewWindow.Close(Position.NOW,Duration=300)
        if self._maxFunction:
            self._maxbutton.Hide()
        return super().leaveEvent(event)

    def resizeEvent(self, event):
        if self._maxbutton!=None:
            self._maxbutton.move(self.width()-self._maxbutton.width()-10,self._image.y()+10)
        return super().resizeEvent(event)

class ImagePopup(Popup_):
    '''
    popup方式显示图片

    Image:可以Icon类或文本路径类的图标或图片
    IamgeSize:图片大小
    ShowName:是否显示图片名称
    NameAlign_:图片名称文本对齐方式,只接受left、center、right
    Text:图片描述文本
    TextAlign:图片描述文本对齐方式,只接受left、center、right
    '''
    def __init__(self,Image:Union[Icon,str],IamgeSize:QSize=QSize(500,400),ShowName:bool=False,NameAlign_:TextAlign=None,Text:str=None,TextAlign_:TextAlign=None,parent=None):
        super(ImagePopup, self).__init__(parent=parent)
        #设置窗口样式
        self.SetWindowTool()
        #阴影
        self._shadow=ShadowEffect(Color_(ColorStyle.Color,100,Alpha=70),13,QPoint(0,0))
        self._showframe.setGraphicsEffect(self._shadow)
        
        if isinstance(Image,Icon):
            _icon=IconView(Image,Color_(ColorStyle.Color,100),IamgeSize)
            _icon.SetMousePenetration(True)
            _name=_icon.Icon.GetIconName()
            self._showframe.layouts.addWidget(_icon)
        else:
            if ShowName==False and  Text==None:
                _picture=ImageView(Image,ImageRadius=QRect(5,5,5,5))
            else:
                _picture=ImageView(Image,ImageRadius=QRect(5,5,0,0))
                #重设布局参数
                self._showframe.layouts.setContentsMargins(0,0,0,8)
                self._showframe.layouts.setSpacing(5)
            _picture.SetMousePenetration(True)
            _picture.setFixedSize(IamgeSize)
            _picture.SetAdjust()
            _name=_picture.GetImageName()
            self._showframe.layouts.addWidget(_picture,1)

        if ShowName:
            _picturename=LabelNormal()
            _picturename.setFixedWidth(IamgeSize.width())
            _picturename.setText(_name)

            if NameAlign_==TextAlign.left:
                _align=Qt.AlignLeft
            elif NameAlign_==TextAlign.center:
                _align=Qt.AlignHCenter
            elif NameAlign_==TextAlign.right:
                _align=Qt.AlignRight
            else:
                _align=Qt.AlignHCenter

            _picturename.setAlignment(_align)
            self._showframe.layouts.addWidget(_picturename)

        if Text:
            _text=LabelNormal()
            _text.setFixedWidth(IamgeSize.width())
            _text.setText(Text)
            if TextAlign_==TextAlign.left:
                _align=Qt.AlignLeft
            elif TextAlign_==TextAlign.center:
                _align=Qt.AlignHCenter
            elif TextAlign_==TextAlign.right:
                _align=Qt.AlignRight
            else:
                _align=Qt.AlignLeft

            _text.setAlignment(_align)
            self._showframe.layouts.addWidget(_text)

        #修改qss
        if ShowName==False and Text==None:
            _backgroundcolor=Color_(0,0,0,0)
        else:
            _backgroundcolor=GradientColor()
            _backgroundcolor.SetStyle(GradientStyle.qlineargradient)
            _backgroundcolor.SetSpread(GradientSpread.pad)
            _backgroundcolor.Setp1(0.5,0)
            _backgroundcolor.Setp2(0.5,1)

            _backgroundcolorlist=GradientColorList()
            _backgroundcolorlist.AddColor(0,Color_(0,0,0,0))
            _backgroundcolorlist.AddColor(0.2,Color_(ColorStyle.Color,0))
            _backgroundcolorlist.AddColor(1,Color_(ColorStyle.Color,0))

            _backgroundcolor.SetColorlist(_backgroundcolorlist)

        self._showframe.qss.SetBackgroundColor(_backgroundcolor)
        self._showframe._qssplus.ApplyQss()

class ImageViewPlus(QGraphicsView):
    """
    图片浏览

    ImageLink:图片链接
    ViewMode:True:纯浏览模式,False:全屏预览模式
    """
    closed=Signal()
    def __init__(self,ImageLink:str,ViewMode:bool=True,parent=None):
        super(ImageViewPlus, self).__init__(parent=parent)
        self._rotationAngle = 0   #旋转角度缓存
        self._zoomInTimes = 0     #当前放大倍数
        self._maxZoomInTimes = 40 #最大放大倍数
        self._fileName=None       #image名称  
        self._mode=ViewMode           #按钮显示模式

        self.pixmap = QPixmap()
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
        self.graphicsScene = QGraphicsScene()
        self.displayedImageSize = QSize(0, 0)

        self.setImage(ImageLink)

        self._btn=ImageTool(False,parent=self)

        if self._mode:
            self._btn.SetButtonMode(2)
        else:
            self._btn.SetButtonMode(3)

        self.__ButtonMove()
        self.__ButtonEvent()
        self.__LabelEvent()

        self.__initWidget()

    def __ButtonMove(self):
        self._btn.move(int((self.width()-self._btn.width())/2),self.height()-60)

    def __ButtonEvent(self):
        self._btn._zoomin.clicked.connect(lambda: self.shrinkPicture())
        self._btn._zoomout.clicked.connect(lambda: self.enlargePicture())
        self._btn._rotateright.clicked.connect(lambda: self.rotateClockwise(90))
        self._btn._rotateleft.clicked.connect(lambda: self.rotateClockwise(-90))
        self._btn._zoomadapt.clicked.connect(self.setAdaptation)
        self._btn._zoom1_1.clicked.connect(self.setOriginalSize)
        self._btn._close.clicked.connect(self.___fullwindowclose_event)

    def __LabelEvent(self):
        self._btn._zoomlabel.setText(str(100+self._zoomInTimes*10)+"%")

    def ___fullwindowclose_event(self):
        self.closed.emit()

    def __initWidget(self):
        """
        初始化小部件
        :return:
        """
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # 隐藏水平滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # 隐藏垂直滚动条
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)  # 以鼠标所在位置为锚点进行缩放
        self.pixmapItem.setTransformationMode(Qt.TransformationMode.SmoothTransformation)  # 平滑转型
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)  # 平滑像素图变换

        self.setStyleSheet("QGraphicsView{background:rgba(0,0,0,150);border:0px;padding:0px;margin:0px;}")
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.graphicsScene.addItem(self.pixmapItem)
        self.setScene(self.graphicsScene)

    def setImage(self, _fileName: str):
        """
        设置显示的图片
        :param _fileName:
        :return:
        """
        self.resetTransform()
        del self.pixmap
        self._fileName = _fileName
        self.pixmap = QPixmap(_fileName)
        self.pixmapItem.setPixmap(self.pixmap)
        self._zoomInTimes = 0
        # 调整图片大小
        self.setSceneRect(QRectF(self.pixmap.rect()))
        ratio = self.__getScaleRatio()
        self.displayedImageSize = self.pixmap.size() * ratio
        if ratio < 1:
            self.fitInView(self.pixmapItem, Qt.KeepAspectRatio)
        self.pixmapItem.setTransformOriginPoint(self.pixmapItem.boundingRect().center())

    def setOriginalSize(self):
        """
        设置 1:1 大小
        :return:
        """
        self.resetTransform()
        self.setSceneRect(QRectF(self.pixmap.rect()))
        self.__setDragEnabled(self.__isEnableDrag())
        self._zoomInTimes = self.getZoomInTimes(self.pixmap.width())

        self.__LabelEvent()

    def setAdaptation(self):
        """
        缩放以适应
        :return:
        """
        self.setSceneRect(QRectF(self.pixmap.rect()))
        self.fitInView(self.pixmapItem, Qt.KeepAspectRatio)
        self.__setDragEnabled(False)
        self._zoomInTimes = 0

        self.__LabelEvent()

    def rotationAngle(self):
        return self._rotationAngle

    def rotateClockwise(self, stepSize: int = 90):
        """
        顺时针旋转
        :param stepSize: 步长，旋转角度
        :return:
        """
        if self._fileName is None:
            return
        self._rotationAngle = self._rotationAngle + stepSize
        self.__rotation(self._rotationAngle)

    def __rotation(self, stepSize: int):
        """
        指定图片中心并旋转
        :return:
        """
        self.pixmapItem.setTransformOriginPoint(self.pixmapItem.boundingRect().center())  # 指定图片旋转中心点
        self.pixmapItem.setRotation(stepSize)
        self.setAdaptation()

    def __isEnableDrag(self):
        """
        根据图片的尺寸决定是否启动拖拽功能
        :return:
        """
        v = self.verticalScrollBar().maximum() > 0
        h = self.horizontalScrollBar().maximum() > 0
        return v or h

    def __setDragEnabled(self, isEnabled: bool):
        """
        设置拖拽是否启动
        :param isEnabled: bool
        :return:
        """
        if isEnabled:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        else:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)

    def __getScaleRatio(self):
        """
        获取显示的图像和原始图像的缩放比例
        :return:
        """
        if self.pixmap.isNull():
            return 1

        pw = self.pixmap.width()
        ph = self.pixmap.height()
        rw = min(1, self.width() / pw)
        rh = min(1, self.height() / ph)
        return min(rw, rh)

    def enlargePicture(self, anchor=QGraphicsView.AnchorUnderMouse):
        """
        放大图片
        :return:
        """
        if self._zoomInTimes == self._maxZoomInTimes:
            return
        self.setTransformationAnchor(anchor)
        self._zoomInTimes += 1
        self.scale(1.1, 1.1)
        self.__setDragEnabled(self.__isEnableDrag())

        # 还原 anchor
        self.setTransformationAnchor(self.ViewportAnchor.AnchorUnderMouse)

        self.__LabelEvent()

    def shrinkPicture(self, anchor=QGraphicsView.AnchorUnderMouse):
        """
        缩小图片
        :return:
        """
        if self._zoomInTimes == 0 and not self.__isEnableDrag():
            return

        self.setTransformationAnchor(anchor)

        self._zoomInTimes -= 1

        # 原始图像的大小
        pw = self.pixmap.width()
        ph = self.pixmap.height()

        # 实际显示的图像宽度
        w = self.displayedImageSize.width() * 1.1 ** self._zoomInTimes
        h = self.displayedImageSize.height() * 1.1 ** self._zoomInTimes

        if pw > self.width() or ph > self.height():
            # 在窗口尺寸小于原始图像时禁止继续缩小图像比窗口还小
            if w <= self.width() and h <= self.height():
                self.fitInView(self.pixmapItem)
            else:
                self.scale(1 / 1.1, 1 / 1.1)
        else:
            # 在窗口尺寸大于图像时不允许缩小的比原始图像小
            if w <= pw:
                self.resetTransform()
            else:
                self.scale(1 / 1.1, 1 / 1.1)

        self.__setDragEnabled(self.__isEnableDrag())

        # 还原 anchor
        self.setTransformationAnchor(self.ViewportAnchor.AnchorUnderMouse)

        self.__LabelEvent()

    def getZoomInTimes(self, width: int, step: int = 100):
        for i in range(0, self._maxZoomInTimes):
            if width - self.displayedImageSize.width() * 1.1 ** i <= step:
                return i
        return self._maxZoomInTimes

    def fitInView(self, item: QGraphicsItem, mode=Qt.AspectRatioMode.KeepAspectRatio):
        """
        缩放场景使其适应窗口大小
        :param item:
        :param mode:
        :return:
        """
        super().fitInView(item, mode)
        self.displayedImageSize = self.__getScaleRatio() * self.pixmap.size()
        self._zoomInTimes = 0

    def resizeEvent(self, event):
        if self._zoomInTimes > 0:
            return
        # 调整图片大小
        ratio = self.__getScaleRatio()
        self.displayedImageSize = self.pixmap.size() * ratio
        if ratio < 1:
            self.fitInView(self.pixmapItem, Qt.KeepAspectRatio)
        else:
            self.resetTransform()

        self.__ButtonMove()

    def resetTransform(self):
        """
        重置变换
        :return:
        """
        self._zoomInTimes = 0
        self.__setDragEnabled(False)
        super().resetTransform()

    def wheelEvent(self, e: QWheelEvent):
        """
        滚动鼠标滚轮缩放图片
        :param e:
        :return:
        """
        if self._mode:
            return
        if e.angleDelta().y() > 0:
            self.enlargePicture()
        else:
            self.shrinkPicture()
    
    def enterEvent(self, event):
        """
        鼠标进入事件
        """
        self._btn.Show()

    def leaveEvent(self, event):
        """
        鼠标离开事件
        """
        self._btn.Hide()
    