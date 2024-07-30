from PySide6.QtCore import QPoint
from PySide6.QtGui import QColor,QTextCharFormat,QFont, QColor
from PySide6.QtWidgets import QTextEdit

from ..menu import LineEditMenu
from ..scrollbar import VScrollDelegate

from qss import BorderStyle,Color_,ColorStyle,QssPlusClass,Font_,FontSize

from docx import Document

class TextEdit(QTextEdit,QssPlusClass):
    def __init__(self,*args, **kwargs):
        super(TextEdit, self).__init__(*args, **kwargs)
        self.QssApply(self,"TextEdit",True,False)

        self.MouseEventLoad(self)
        self.SetClickFunciton(False)

        self._vscorll=VScrollDelegate(self)

    def Setqss(self):
        self.qss.SetBackgroundColor(Color=Color_(ColorStyle.NullColor,0))
        self.qss.SetColor(Color_(ColorStyle.FullColor,100))

        self.qss.SetFont(Font_(FontSize=FontSize(Shift=0,Min=10,Max=16)))

        self.qss.SetBorderWidth(Width=1)
        self.qss.SetBorderStyle(Style=BorderStyle.solid)
        self.qss.SetBorderRadius(Radius=5)
        self.qss.SetBorderColor(Color=Color_(ColorStyle.FullColor,10))
        self.qss.SetBorderColor(ColorBottom=Color_(ColorStyle.FullColor,20))

    def _Colorin(self,animation_:bool=True):
        self.qss.SetBorderColor(Color=Color_(ColorStyle.ThemeColorBackground,40))
        self.qss.SetBorderColor(ColorBottom=Color_(ColorStyle.ThemeColorBackground,40),EventConnect=True)

    def _Colorout(self,animation_:bool=True):
        self.qss.SetBorderColor(Color=Color_(ColorStyle.FullColor,10))
        self.qss.SetBorderColor(ColorBottom=Color_(ColorStyle.FullColor,20),EventConnect=True)

    def contextMenuEvent(self, e):
        self.SetMenu()
        LineEditMenu(self).ExecPos(e.globalPos()+QPoint(0,10),Opacity=True,MoveMultiple=0.3,Duration=300)
       
class WordTextEdit(TextEdit):
    def __init__(self,*args, **kwargs):
        super(WordTextEdit, self).__init__(*args, **kwargs)
        self.isReadOnly(True)

    def LoadWord(self,Link:str):
        doc = Document(Link)
        cursor = self.textCursor()

        for para in doc.paragraphs:
            for run in para.runs:
                self.__InsertText(cursor, run)
            cursor.insertBlock()

    def __InsertText(self, cursor, run):
        char_format = QTextCharFormat()
        if run.bold:
            char_format.setFontWeight(QFont.Bold)
        else:
            char_format.setFontWeight(QFont.Normal)
        if run.italic:
            char_format.setFontItalic(True)
        if run.underline:
            char_format.setFontUnderline(True)
        if run.font.size:
            char_format.setFontPointSize(run.font.size)
        else:
            char_format.setFontPointSize(10)
        if run.font.name:
            font = QFont(run.font.name)
            char_format.setFont(font)
        if run.font.color and run.font.color.rgb:
            color = run.font.color.rgb
            char_format.setForeground(QColor(color[0], color[1], color[2]))

        cursor.setCharFormat(char_format)
        cursor.insertText(run.text)




    
