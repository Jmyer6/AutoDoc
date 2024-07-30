from PySide6.QtXml import QDomDocument
from PySide6.QtGui import QImage,QPixmap,Qt,QPainter,QIconEngine,QTransform,QIcon
from PySide6.QtCore import QRect,QRectF,QFile,QSize,QByteArray
from PySide6.QtSvg import QSvgRenderer

import os

from lib import QcolorAlpha
from qss import Color_
from typing import Union

from .svg_date import Icon

#缓存svg的base64格式

class SvgIcon(QIconEngine):#QIcon
    '''
    Icon_: Icon:内置svg图标,str:svg,icon,png文件路径
    Color:svg颜色
    Angle:svg旋转角度

    使用方法:SvgIcon(icon,color,angle).getpixmap(size) 
    '''
    def __init__(self,Icon_:Union[Icon,str],Color:Color_=None,Angle:int=None):
        super().__init__()      
        self._icontype=None
        self._color=Color
        self._angle=Angle
        self.__GetIcon(Icon_)

    def __GetIcon(self,Icon_):
        dom = QDomDocument()

        if isinstance(Icon_,str):#文本格式
            if os.path.exists(Icon_)==False:#判断路径
                self._icontype=None
                return
            if Icon_.lower().endswith('.svg'):
                self._icontype="svg"
                f = QFile(Icon_)
                f.open(QFile.ReadOnly)
                dom.setContent(f.readAll())
                f.close()
                self._icon = dom.toString()
            elif Icon_.lower().endswith('.ico'):
                self._icontype="ico"
                self._icon = Icon_
            elif Icon_.lower().endswith('.png'):
                self._icontype="png"
                self._icon = Icon_
            else:
                self._icontype=None
                return
        elif isinstance(Icon_,Icon):#图标格式
            self._icontype="svg"
            dom.setContent(QByteArray().fromBase64(Icon_.value[0].encode()))
            self._icon = dom.toString()
        else:
            self._icontype=None
            return
        
    def pixmap(self, size, mode, state):
        if self._icontype!=None:
            #画svg
            pixmap=self.__DrawPixmap(size)
            #换色
            pixmap=self.__ChangeColor(pixmap)
            #旋转
            pixmap=self.__Rotate(pixmap)
            return pixmap

    def __DrawPixmap(self,size):
        if self._icontype=="ico" or self._icontype=="png":
            return QPixmap(self._icon) 
        
        if self._icontype=="svg":
            #根据大小创建image
            _image = QImage(size, QImage.Format_ARGB32)
            #设置image全透明
            _image.fill(Qt.transparent)
            #转换pixmap
            _pixmap = QPixmap.fromImage(_image, Qt.NoFormatConversion)
            _painter = QPainter(_pixmap)
            _rect = QRect(0, 0, size.width(), size.height())
            #画svg
            _renderer = QSvgRenderer(self._icon.encode())
            _renderer.render(_painter, QRectF(_rect))
            #画结束
            _painter.end()
            return _pixmap

    def __ChangeColor(self,pixmap:QPixmap):
        if self._color==None:
            return pixmap
        #转换image格式
        _image=pixmap.toImage()
        #遍历image色块
        Color=self._color.GetColor()
        for x in range(_image.width()):
            for y in range(_image.height()):
                pcolor = _image.pixelColor(x, y).alpha() 
                if pcolor > 0:
                    _image.setPixelColor(x, y, QcolorAlpha(Color,pcolor)) #修改色块颜色
        return QPixmap.fromImage(_image, Qt.NoFormatConversion)

    def __Rotate(self,pixmap:QPixmap):
        if self._angle==None:
            return pixmap
        _tran=QTransform()
        _tran.rotate(self._angle)
        _tranpicture=pixmap.transformed(_tran,Qt.SmoothTransformation)
        #区图片居中位置
        x_s=int((_tranpicture.width()-pixmap.width())/2)
        y_s=int((_tranpicture.height()-pixmap.height())/2)
        return _tranpicture.copy(x_s, y_s, pixmap.width(),pixmap.height())

    def geticon(self):
        return QIcon(self)
    
    def getpixmap(self,Size:QSize):
        return QIcon(self).pixmap(Size)

