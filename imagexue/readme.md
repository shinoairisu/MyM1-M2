# 绘制图形学作业

## 用法

在main中编写想要的形状

python main 就会生成ppm图片

## 画布方向

![](https://github.com/shinoairisu/MyM1-M2/blob/main/imagexue/%E5%8E%9F%E7%90%86.png)

## APIs

### makeBall_opaq

绘制一个漫反射球体，具体看writer.py的源码，很容易看懂。

参数：

position 位置

r 半径

color 颜色,可以为random

ks:镜面反射系数 小于1

b:镜面反射指数 大于1的整数

![](https://github.com/shinoairisu/MyM1-M2/blob/main/imagexue/image/1.png)

### makeBall_mirror

制作一个镜面球

position 位置

r 半径

### makeBall_transparent

制作一个透明球

ks:镜面反射系数 小于1

b:镜面反射指数 大于1的整数

kt:透明系数 小于1

n：折射率 大于1的小数

### drawLine

使用某个球画一条线

ball:球的类别 op mr tr ran  漫反射 镜面 透明 随机

from: 起始点

to: 结束点

z: 所在平面

number: 用多少个球来填充线段

color：球的颜色 可以是一个list，也可以是random。

ks:镜面反射系数 小于1

b:镜面反射指数 大于1的整数

kt:透明系数 小于1

n：折射率 大于1的小数

ks=0.6,b=10,kt=0.5,n=1.5

支持使用随机球组成线以及随机颜色的球组成线。

![](https://github.com/shinoairisu/MyM1-M2/blob/main/imagexue/image/2.png)![](https://github.com/shinoairisu/MyM1-M2/blob/main/imagexue/image/3.png)

### drawSin

用球画sin，同样支持随机球类型与随机球颜色。

![](https://github.com/shinoairisu/MyM1-M2/blob/main/imagexue/image/4.png)

### drawCic

用球画圆，同样支持随机球类型与随机球颜色。

![](https://github.com/shinoairisu/MyM1-M2/blob/main/imagexue/image/5.png)

### outAndRend

最终输出，会直接输出为一张ppm。

参数

outputmap：一张准备输出的图(实际上一个list)

bg: 背景色

size:图像长边大小

resolution:长短边比例

picname:输出图片名

mapname:输出图片指令文件名

