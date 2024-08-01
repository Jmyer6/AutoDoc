
# 操作流程
1. 创建Word模板
2. 设置Word模板关键词
3. 创建Execl数据表
4. 创建Execl命名表
5. 打开软件
6. 在软件中载入Word模板
7. 在软件中设置Word模板关键词
8. 在软件中核对Word模板关键词数量
9. 在软件中载入Execl文件
10. 在软件中选择Execl数据表
11. 在软件中设置保存路径
12. 在软件中设置Word文档命名规则
13. 在软件中检查生成的路径及文件名
14. 生成文档

# Ps
下方结合实例讲解使用方法，如某一学校需要开家长会，需要给每个同学家长发送一封信通知家长。


# 1. 创建Word模板

可以使用任意的Word文档作为模板

注意：作为模板前最好自行备份一遍。

# 2. 设置Word模板关键词

在Word模板中设置与原文不一致的文本作为关键词

在下图Word实例中，关键词为[xxx],数量3

![image](https://github.com/Jmyer6/AutoDoc/blob/main/picture/1.jpg)


# 3. 创建Execl数据表

* Execl文档中任意一表都可作为数据表，只要符合下方数据规则就行。

因为Word模板中关键词数量为3，所以每列数据为3个。

这次实例中我只发给10个同学的家长，所以有10列数据，及后续会生成10个Word文档。(理论上可以无限个)

Ps. 单元格不能为空

![image](https://github.com/Jmyer6/AutoDoc/blob/main/picture/2.jpg)

# 4. 创建Execl命名表

* Execl文档中任意一表都可作为命名表，只要符合下方数据规则就行。

只能有1列数据，且数据数量和数据表中列数一致(实例中Execl数据表有10列数据)

![image](https://github.com/Jmyer6/AutoDoc/blob/main/picture/3.jpg)

# 5. 打开软件

# 6. 在软件中载入Word模板

载入方法如下
* Word文档拖动添加
* 按下“+”添加
* 手动输入添加
  
# 7. 在软件中设置Word模板关键词

输入关键词和“2步骤”设置的关键词一致

# 8. 在软件中核对Word模板关键词数量

点击“检查关键词”按钮

检查软件识别的关键词数量是否和 <a href="#id_222">步骤2</a> 设置的关键词数量一致

![image](https://github.com/Jmyer6/AutoDoc/blob/main/picture/4.jpg)

# 9. 在软件中载入Execl文件

载入方法如下
* Execl文件拖动添加
* 按下“+”添加
* 手动输入添加

# 10. 在软件中选择Execl数据表

在下拉框中选择数据表

![image](https://github.com/Jmyer6/AutoDoc/blob/main/picture/5.jpg)

# 11. 在软件中设置保存路径

设置保存路径，默认路径和 <a href="#id_666">步骤6</a> 载入Word模板路径一致

# 12. 在软件中设置Word文档命名规则

命名规则有3种类型
* 文本类型：固定文本
* 数字类型：从设置的开始数字递增
* Execl类型：Execl表中数据

Ps. 在命名规则框中可拖动切换顺序

![image](https://github.com/Jmyer6/AutoDoc/blob/main/picture/6.jpg)

# 13. 在软件中检查生成的路径及文件名

在表格中会依据 <a href="#id_1122">步骤11、步骤12</a> 设置的参数生成Word文档的预保存信息，核对是否和自己想要的一致。

![image](https://github.com/Jmyer6/AutoDoc/blob/main/picture/7.jpg)

# 14. 生成文档

在列表中勾中后，点击“运行选中”按钮，则从上到下依次生成Word文档





