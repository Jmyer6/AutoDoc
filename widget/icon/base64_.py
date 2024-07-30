from PySide6.QtWidgets import QApplication,QFileDialog
import sys,os,base64

def to_py(list):

    with open(f'widget\icon\svg_date.py', 'w+') as w:
        w.write("from enum import Enum\n\n")
        w.write("class Icon(Enum):\n")

        for i in list:
            (filepath_, filename_) = os.path.split(i)
            (name_, suffix_) = os.path.splitext(filename_)

            with open(i, 'rb') as r:
                b64str = base64.b64encode(r.read())

            w.write("    "+name_+" = \""+b64str.decode()+"\",\n")

        
if __name__ == '__main__':
    app =QApplication(sys.argv)
    links=QFileDialog.getOpenFileNames(None, "请选择要添加的文件","D:\\python\\code\\words\\icon\\svg", ";All Files (*)")
    to_py(links[0])
