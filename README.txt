这是一个通过python&OpenCV实现识别真空规的读数的程序。

- 可以支持STM/PREP双路读取
- 通过UDP实现示数广播
- 提供了LabVIEW接口和示例程序

! 需要电脑默认摄像头为CCD，否则请禁用内置摄像头。
! 需要预先配置好规在CCD视野中的位置：
 a. 打开settings.conf文件
 b. [ccd_location]下的rotation代表图像逆时针旋转的角度，需要保证读数水平显示。
 c. top/bottom定义了示数区域的上线和下线，这两个数值为STM/PREP公用的。
 d. stm_left/stm_right/prep_left/prep_right为STM和PREP的示数位置的左右限。
 e. 识别框可以预留较大空间，以便程序自动定位字符，但是请保证识别框内除字符外没有其他亮点。

# 原理介绍
1. 通过CCD和识别框确定示数位置，分割出单个数字；
2. 分别检测7位数码管的7个笔画，查表确定数字。这里已经收录了“6”和“9”的两种字形；
3. 在PyQt5 based python GUI显示，并通过UDP-socket在5060端口上广播；
4. [labview] 读取数值，并显示在图像上。

3, March, 2022
@CoccaGuo

