from enum import Enum


class GradientStyle(Enum):#渐变颜色样式
    qlineargradient="qlineargradient"#显示从起点到终点的直线渐变
    '''
    qlineargradient(spread:**, x1:*, y1:*, x2:*, y2:*, stop:0 rgba(*),.....,stop:1 rgba(*))
    '''
    qradialgradient="qradialgradient"#显示以圆心为中心的圆形渐变
    '''
    qradialgradient(spread:*, cx:*, cy:*, radius:*, fx:*, fy:*, stop:0 rgba(*),.....,stop:1 rgba(*))
    '''
    qconicalgradient="qconicalgradient"#显示围绕一个中心点的锥形渐变
    '''
    qconicalgradient(cx:*, cy:*, angle:*,stop:0 rgba(*),.....,stop:1 rgba(*))
    '''

class GradientSpread(Enum):#渐变颜色显示模式
    pad="pad"
    repeat="repeat"
    reflect="reflect"

class FontStyle(Enum):#字体样式
    normal="normal" #正常
    italic="italic" #斜体
    oblique="oblique" #斜体
    inherit="inherit" #继承自父对象

class FontWeight(Enum):#字体粗细程度
    normal="normal"
    bold="bold"

class FontSizeStyle(Enum):#字体大小样式
    auto="auto" #跟随主题
    regular="regular" #固定大小

class BorderStyle(Enum):#边框类型
    none="none"#无边框
    dotted="dotted"#点状
    dashed="dashed"#虚线
    solid="solid"#实线
    double="double"#双实线
    groove="groove"#定义 3D 凹槽边框。其效果取决于 border-color 的值
    ridge="ridge"#定义 3D 垄状边框。其效果取决于 border-color 的值
    inset="inset"#定义 3D inset 边框。其效果取决于 border-color 的值
    outset="outset"#定义 3D outset 边框。其效果取决于 border-color 的值

class TextAlign(Enum):#文本对齐类型
    top="top"#向上对齐
    bottom="bottom"#向下对齐
    left="left"#向左对齐
    right="right"#向右对齐
    center="enter"#居中

class TextDecoration(Enum):#文本样式
    none="none"#无
    underline="underline"#下滑线
    overline="overline"#上滑线
    linethrough="line-through"#删除线
