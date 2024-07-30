from PySide6.QtCore import QEvent,Signal,Qt
from PySide6.QtGui import QCloseEvent, QResizeEvent, QShowEvent, QWheelEvent
from PySide6.QtWidgets import QWidget

from qss import QssPlusClass,BorderStyle,Color_,ColorStyle,Font_,FontSize
from lib import QcolorToStr

from ..button import ButtonBase
from ..scrollbar import Scroll

from .draglist import DragList,DragItem
from .namerule import NameRuleList
from .tasklist import TaskList

import math

class TextList(QWidget,QssPlusClass):
    checked=Signal(int,str)
    showed=Signal()
    hided=Signal()
    def __init__(self,parent=None,scrollparent=None):
        super(TextList,self).__init__(parent=parent)

        self._itemheight=32
        self._itemspacing=2
        self._itemcount=None #None为跟随self.height设置item数量,可设置固定数量
        self._itemcountCache=0 #数量缓存
        self._heightfollow=True #固定数量时高度跟随

        self._textlist=[]  #数据数组
        self._itemlist=[]  #控件数组

        self._index=0
        self._check=None

        self._listwidget=QWidget(self)
        self._listwidget.move(0,0)
        self._overheight=0

        self._endfouce=None
        self._startfouce=None
        self._foucewidget=None

        self._fontfollow=False

        if scrollparent==None:
            self._scroll=Scroll(Qt.Vertical,self)
        else:
            self._scroll=Scroll(Qt.Vertical,scrollparent)
        self._scroll.valuechanged.connect(self.__ScrollValueChanged)
  
        self.QssApply(self,"TextList",True,False)

        self.window().installEventFilter(self)

    def Clear(self):
        self._textlist=[]  #数据数组
        self._itemlist=[]  #控件数组

        self._index=0
        self._check=None
        
    def Setqss(self):
        self.qss.SetBackgroundColor(Color_(ColorStyle.FullColor,0))
        self.qss.SetBorderRadius(Radius=5)
        return super().Setqss()

    def SetCheck(self,Check:int):
        self._check=Check
        self.checked.emit(Check,self._textlist[Check])

        for i in range(len(self._itemlist)):
            if i!=Check-self._index:
                self.__ItemCheck(i,False)
            else:
                self.__ItemCheck(i,True)

    def check(self):
        return self._check

    def ShowIndex(self):
        if self._check!=None:
            self._index=self._check

            self._scroll.SetValue(self._check*self._itemheight)

            self.__RenewItemText()

    def Addtext(self,Text:str):
        self._textlist.append(Text)
        if self.isHidden()==False:
            self.__RenewItemText()#刷新可以优化
            self.__RenewScrollRange()

    def Addtexts(self,Texts:list[str]):
        for text in Texts:
            self.Addtext(text)

    def SetItemHeight(self, Height:int):
        '''
        设置item高度
        '''
        self._itemheight=Height
        self.Adjust()

    def SetItemSpacing(self, Spacing:int):
        '''
        设置item间距
        '''
        self._itemspacing=Spacing
        self.Adjust()

    def SetItemCount(self,Count:int=None):
        '''
        设置item数量
        Count:数量
        '''
        self._itemcount=Count
        self.Adjust()

    def SetHeightFollow(self, Open:bool=True):
        '''
        设置当item数量固定时,list组件高度跟随
        '''
        self._heightfollow=Open
        self.Adjust()

    def SetFontNameFollow(self, Open:bool=True):
        self._fontfollow=Open

        for _item in self._itemlist:
                _item.SetFontNameFollow(Open)

    def __ItemClickEvent(self,Index:int):
        if self._index>len(self._textlist)-self._itemcountCache:
            _index=len(self._textlist)-self._itemcountCache
        else:
            _index=self._index

        self.SetCheck(_index+Index)

    def Adjust(self):
        '''
        调整高度或者item
        '''
        _l=len(self._textlist)#取数据量

        if _l==0:
            return

        if self._itemcount is None:#跟随高度设置item数量
            _h=self.height() 
            _itemcount=math.ceil(_h/(self._itemheight+self._itemspacing))

            if _l<_itemcount:
                self.__RenewItem(_l)
            else:
                self.__RenewItem(_itemcount)
             
        else:                      #跟随item数量设置高度 
            if _l<self._itemcount:
                _itemcount=_l
            else:
                _itemcount=self._itemcount

            if self._heightfollow:
                _h=_itemcount*(self._itemheight+self._itemspacing)-self._itemspacing
                if _h>0:
                    self.setFixedHeight(_h)
                    self._scroll.ScrollSizeAdjust()

            self.__RenewItem(_itemcount)

    def __RenewItem(self,Count:int):
        """
        加载item
        """
        self._itemcountCache=Count#缓存
        self.__RenewScrollRange()

        _l=len(self._itemlist)

        if _l<Count:#小了新增
            for i in range(_l,Count):
                _item=TextListItem(Index=i,parent=self._listwidget)
                _item.focusin.connect(self.__ItemFocusIn)
                _item.checked.connect(self.__ItemClickEvent)

                if self._fontfollow:
                    _item.SetFontNameFollow(self._fontfollow)

                _item.show() #显示
                self._itemlist.append(_item)

        elif _l>Count:#大了删除
            for i in range(Count, _l):
                self._itemlist[i].deleteLater()
                self._itemlist.pop(i)

        
        _h=self._itemheight*Count+self._itemspacing*(Count-1)
        if _h>0:
            self._listwidget.setFixedSize(self.width(),_h)

        #调整位置
        _y=0
        for item in self._itemlist:
            if isinstance(item,TextListItem):
                item.setFixedSize(self.width(),self._itemheight)
                item.move(0, _y)
                _y+=item.height()+self._itemspacing
           
    def __RenewItemText(self):
        """
        加载item
        """
        if self._index>len(self._textlist)-self._itemcountCache:
            _index=len(self._textlist)-self._itemcountCache
        else:
            _index=self._index

        for i in range(len(self._itemlist)):
            if _index+i==self._check and self._itemlist[i].isChecked()==False:
                self.__ItemCheck(i,True)
            elif _index+i!=self._check and self._itemlist[i].isChecked()==True:
                self.__ItemCheck(i,False)
            # print(len(self._textlist),self._index,self._index+i)
            self._itemlist[i].SetText(self._textlist[_index+i])

    def __ItemCheck(self,Index:int,Checked:bool):
        if Checked:
            self._itemlist[Index].setChecked(True)
            self._itemlist[Index].SetCheckScroll(True)
            self._itemlist[Index]._mouse=True
            self._itemlist[Index]._check=True
            self._itemlist[Index]._fouce=True
            self._itemlist[Index]._ColorCheckin()
        else:
            self._itemlist[Index].setChecked(False)
            self._itemlist[Index].SetCheckScroll(False)
            self._itemlist[Index]._mouse=False
            self._itemlist[Index]._check=False
            self._itemlist[Index]._fouce=False
            if self._itemlist[Index].hasFocus():
                self._itemlist[Index]._Colorin()
            else:
                self._itemlist[Index]._Colorout()

    def __RenewScrollRange(self):
        _overheight=self._listwidget.height()-self.height()

        if _overheight<0:#计算超出值，如为负数则为0
            _overheight=0

        self._scroll.SetScrollValueRange(0,
            (len(self._textlist)-self._itemcountCache)*self._itemheight+_overheight)
        
        #设置超出范围标记
        if _overheight>0:
            self._overheight=(len(self._textlist)-self._itemcountCache)*self._itemheight
        else:
            self._overheight=0

    def __ScrollValueChanged(self,value:int):
        _value=value
        if self._overheight!=0:
            if value>self._overheight:
                self._listwidget.move(0,-(value-self._overheight))
                _value=self._overheight
            else:
                self._listwidget.move(0,0)

        self._index=math.floor(_value/self._itemheight)
        self.__RenewItemText()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.Adjust()
        self.__RenewScrollRange()
        return super().resizeEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        self._scroll.deleteLater()
        return super().closeEvent(event)

    def showEvent(self, event: QShowEvent) -> None:
        self.Adjust()
        self.__RenewItemText()
        self.showed.emit()
        return super().showEvent(event)

    def hideEvent(self, event) -> None:
        self.hided.emit()
        return super().hideEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.angleDelta().y() != 0:
            self._scroll.wheelEvent(event)
        return super().wheelEvent(event)

    def eventFilter(self, obj, e: QEvent):
        if e.type() == QEvent.KeyRelease and (e.key() == Qt.Key_Down or e.key() == Qt.Key_Left):
            if self._endfouce:
                self.__AddHideFocusWidget(False)
                if self._itemlist[-1].hasFocus()==False:
                    self._index+=1
                    if self._index==len(self._textlist)-self._itemcountCache:
                        self._itemlist[-1].setFocus()
                        self.__AddHideFocusWidget()
                        self._endfouce=None
                    else:
                        self._itemlist[-1].setFocus()
                    self.__RenewItemText()
                    self._scroll.ScrollHandleMove(self._index*self._itemheight,True,False,False)

        elif e.type() == QEvent.KeyRelease and (e.key() == Qt.Key_Up or e.key() == Qt.Key_Right):
            if self._startfouce:
                self.__AddHideFocusWidget(True)
                if self._itemlist[0].hasFocus()==False:
                    self._index-=1
                    if self._index==0:
                        self.__AddHideFocusWidget()
                        self._startfouce=None
                    else:
                        self._itemlist[0].setFocus()
                    self.__RenewItemText()
                    self._scroll.ScrollHandleMove(self._index*self._itemheight,True,False,False)

        return super().eventFilter(obj, e)

    def __ItemFocusIn(self):
        if self._itemlist[0].hasFocus() and self._index>0:
            self._startfouce=True
        elif self._itemlist[-1].hasFocus() and self._index<len(self._textlist)-self._itemcountCache:
            self._endfouce=True
        else:
            self._startfouce=None
            self._endfouce=None
            self.__AddHideFocusWidget()

    def __AddHideFocusWidget(self,Open:bool=None):
        '''
        添加一个隐藏控件,临时焦点过渡
        open:   
            True:  上
            False: 下
            None:  清除
        '''
        if Open is not None:
            if self._foucewidget==None:
                self._foucewidget=TextListItem(parent=self._listwidget)
                self._foucewidget.setFixedSize(10,10)
                self._foucewidget.move(-100,100)
                self._foucewidget.show()
            if Open:
                self.setTabOrder(self._foucewidget,self._itemlist[0])
                #刷新聚焦顺序
                for i in range(len(self._itemlist)-1):
                    self.setTabOrder(self._itemlist[i],self._itemlist[i+1])

            elif Open==False:
                self.setTabOrder(self._itemlist[-1],self._foucewidget)
        elif Open is None:
            if self._foucewidget!=None:
                self._foucewidget.close()
                self._foucewidget=None

                if self._startfouce:
                    self.focusPreviousChild()

class TextListItem(ButtonBase):#菜单按钮
    moved=Signal()
    checked=Signal(int)
    def __init__(self,Text:str="",Index:int=None,parent=None):
        super(TextListItem,self).__init__(Text=Text,objectName="TextListItem",parent=parent)
        self._checkscoll=None
        self._index=Index

        #设置鼠标move事件跟随
        self.setMouseTracking(True)
        #设置可选中
        self.setCheckable(True)
        #设置选中事件
        self.clicked.connect(lambda: self.checked.emit(self._index))
        #设置鼠标move事件跟随
        self.setMouseTracking(True)

    def mouseMoveEvent(self, arg__1) -> None:
        self.moved.emit()
        return super().mouseMoveEvent(arg__1)

    def SetFontNameFollow(self,Open:bool=True):
        self._fontfollow=Open

    def SetText(self, text: str) -> None:

        self._fonttext=text
        self.setToolTip(text)

        self.SetTempDarkqss()
        self.SetTempLightqss()

        if (self._mouse or self._fouce) and self._check:
            self._ColorCheckin()
        elif (self._mouse or self._fouce) and self._check==False:
            self._Colorin()
        elif (self._mouse or self._fouce)==False and self._check:
            self._ColorCheckout()
        elif (self._mouse or self._fouce)==False and self._check==False:
            self._Colorout()

        return super().SetText(text)

    def SetCheckScroll(self,Open:bool=True):
        if Open:
            if self._checkscoll==None:
                self._checkscoll=QWidget(self)
                self._checkscoll.setObjectName("checkscoll")
                self._checkscoll.setAttribute(Qt.WA_TransparentForMouseEvents)
                self._checkscoll.setWindowFlag(Qt.WindowTransparentForInput)
                self._checkscoll.setFixedSize(4,int(self.height()/8*4))
                self._checkscoll.move(7,int((self.height()-self._checkscoll.height())/2))
                self._checkscoll.setStyleSheet("QWidget#checkscoll{background-color:rgba("+QcolorToStr(Color_(ColorStyle.ThemeColor,0).GetColor())+");border-radius:1px;margin:1px}")
                self._checkscoll.show()
        else:
            if self._checkscoll!=None:
                self._checkscoll.deleteLater()
                self._checkscoll=None

    def resizeEvent(self, event: QResizeEvent) -> None:
        if self._checkscoll!=None:
            self._checkscoll.setFixedSize(4,int(self.height()/8*4))
            self._checkscoll.move(7,int((self.height()-self._checkscoll.height())/2))
        return super().resizeEvent(event)

    def SetTempLightqss(self):
        if  self._fontfollow:
            self._TempLightqss.SetFont(Font_(self._fonttext,FontSize=FontSize(Shift=2,Min=5,Max=20)))
        else:
            self._TempLightqss.SetFont(Font_(FontSize=FontSize(Shift=0,Min=5,Max=20)))

        self._TempLightqss.SetColor(Color=Color_(ColorStyle.Dark))
        self._TempLightqss.SetBorderWidth(Width=1)
        self._TempLightqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempLightqss.SetBorderRadius(Radius=5)
        self._TempLightqss.SetBorderColor(Color=Color_(ColorStyle.NullColor,10))
        self._TempLightqss.SetBorderColor(ColorBottom=Color_(ColorStyle.NullColor,20))
        self._TempLightqss.SetMargin(1,2,1,2)
        self._TempLightqss.SetPadding(0,10,0,10)
        self._TempLightqss.Set_("outline","none")
  
    def SetNormalLightqss(self):
        self._NormalLightqss=self._TempLightqss.Copy()
        self._NormalLightqss.SetBackgroundColor(Color_(ColorStyle.NullColor,0,Rshift=-10,Bshift=3))

    def SetHoverLightqss(self):
        self._HoverLightqss=self._TempLightqss.Copy()
        self._HoverLightqss.SetBackgroundColor(Color_(ColorStyle.FullColor,7,Rshift=-10,Bshift=3))

    def SetCheckHoverLightqss(self):
        self._CheckHoverLightqss=self._TempLightqss.Copy()
        self._CheckHoverLightqss.SetBackgroundColor(Color_(ColorStyle.ThemeColorBackground,85))

    def SetCheckNormalLightqss(self):
        self._CheckNormalLightqss=self._TempLightqss.Copy()
        self._CheckNormalLightqss.SetBackgroundColor(Color_(ColorStyle.ThemeColorBackground,84))

    def SetTempDarkqss(self):
        if  self._fontfollow:
            self._TempDarkqss.SetFont(Font_(self._fonttext,FontSize=FontSize(Shift=0,Min=10,Max=20)))
        else:
            self._TempDarkqss.SetFont(Font_(FontSize=FontSize(Shift=0,Min=10,Max=20)))

        self._TempDarkqss.SetColor(Color=Color_(ColorStyle.Light))
        self._TempDarkqss.SetBorderWidth(Width=1)
        self._TempDarkqss.SetBorderStyle(Style=BorderStyle.solid)
        self._TempDarkqss.SetBorderRadius(Radius=5)
        self._TempDarkqss.SetBorderColor(Color=Color_(ColorStyle.NullColor,10))
        self._TempDarkqss.SetBorderColor(ColorBottom=Color_(ColorStyle.NullColor,20))
        self._TempDarkqss.SetMargin(1,2,1,2)
        self._TempDarkqss.SetPadding(0,10,0,10)
        self._TempDarkqss.Set_("outline","none")

    def SetNormalDarkqss(self):
        self._NormalDarkqss=self._TempDarkqss.Copy()
        self._NormalDarkqss.SetBackgroundColor(Color_(ColorStyle.NullColor,0))

    def SetHoverDarkqss(self):
        self._HoverDarkqss=self._TempDarkqss.Copy()
        self._HoverDarkqss.SetBackgroundColor(Color_(ColorStyle.FullColor,10))

    def SetCheckHoverDarkqss(self):
        self._CheckHoverDarkqss=self._TempDarkqss.Copy()
        self._CheckHoverDarkqss.SetBackgroundColor(Color_(ColorStyle.ThemeColorBackground,75))

    def SetCheckNormalDarkqss(self):
        self._CheckNormalDarkqss=self._TempDarkqss.Copy()
        self._CheckNormalDarkqss.SetBackgroundColor(Color_(ColorStyle.ThemeColorBackground,74))

    def leaveEvent(self, event) -> None:
        self.clearFocus()
        return super().leaveEvent(event)

    def focusOutEvent(self, arg__1) -> None:
        if self._mouse or self._fouce:
            self._mouse=False
            self._fouce=False
            if self._check:
                self._ColorCheckout()
            else:
                self._Colorout()
        return super().focusOutEvent(arg__1)
    
    def mouseMoveEvent(self, arg__1) -> None:
        if self._mouse==False or self._fouce==False:
            self.setFocus()
        return super().mouseMoveEvent(arg__1)




       
    

