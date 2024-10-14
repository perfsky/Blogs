+++
title = "【CTF】MISC常用工具集锦/使用方法简介"
keywords = ["Blog","Technology","CTF","Misc"]
description="一些Misc常用的工具以及使用方法总结"
date = "2024-10-14"
taxonomies = "1"
+++

## 前言

MISC题型多变而且工具繁杂，因此自己花时间整理了一份工具列表，以便日后参考用
**流畅地阅读这篇博客，你可能需要：**

- Python2.7.18 + Python3.8 + 任何一个更高版本的Python，使用conda管理
- Linux虚拟机，kali即可
- 流畅访问Google/GitHub等站点的网络

## 通用工具

### PuzzleSolver

专为misc手打造的瑞士军刀(?)，整合了多种脚本（base，字频分析，png/bmp自动修复文件头，图片盲水印等等）的带GUI的工具
仓库：[Github - PuzzleSolver](https://github.com/Byxs20/PuzzleSolver)

### [随波逐流]CTF编码工具

集成了绝大部分编码的解码/转换工具，有一键解码功能，简单题直接一把梭
[官网](http://www.1o1o.xyz/index.html)

### 010 Editor

功能强大的十六进制编辑工具，有文件模板功能，便于修改各种缺失文件头文件尾。

### binwalk

一个分析文件并提取嵌入的文件和代码的工具，可以判断源文件中包含的隐藏文件种类
仓库：[Github - binwalk](https://github.com/ReFirmLabs/binwalk)
快速入门：

```bash
binwalk -e stego.zip        #提取stego.zip
```

### steghide/stegseek

steghide隐写和配套解密工具，配合rockyou.txt食用更佳
快速入门：

```bash
stegseek [stegofile.jpg] [wordlist.txt]        #用wordlist暴力破解stegofile
stegseek --seed [stegofile.jpg]        # 分析此文件是否包含steghide内容，包含多少隐藏内容，是如何加密的
```

### CyberChef

赛博厨子，ctf编码神器，方便易用，可以下载本地离线使用
链接：[官网](https://cyberchef.org/)

### Ciphey

一个功能强大的ai全自动解密工具，输入密文后自动返回解密文本并指出加密方式（虽然不能百分百解出，但有时候试试会有奇效）
仓库：[Github - Ciphet](https://github.com/Ciphey/Ciphey)
快速入门：

```bash
ciphey -t "put_encrypted_message_here"
ciphey -f encrypted_message.txt
# 加上-q 直接给出结果
# 加上-g 只输出答案
```

## 图片隐写

### Stegsolve

常用于LSB隐写分析/内容提取、GIF查看单帧

### SilentEye

分析bmp/wav中的隐写

### OurSecret

带密码的jpg隐写工具

### Acropalypse-Multi-Tool

一个基于CVE-2023-28303和CVE-2023-21036漏洞的工具，可用于恢复截图被裁剪掉的部分数据
仓库：[Github - Acropalypse Multi Tool](https://github.com/frankthetank-music/Acropalypse-Multi-Tool)

### QR Research

二维码识别/补全软件，支持各种纠错等级和二维码种类

### QrScan

另一个二维码识别软件，特点是能批量识别并输出到csv文件中
仓库：[Github - QrScan](https://github.com/zfb132/QrScan)

### ImageMagick/gaps

多功能图像处理工具，多用于拼图，先用ImageMagick把打乱的图像拼接，再使用gaps识别并自动整理
链接（ImageMagick）：[Github - ImageMagick](https://github.com/ImageMagick/ImageMagick) & [官网](https://imagemagick.org/)
链接（gaps）：[Github - gaps](https://github.com/nemanja-m/gaps)
快速入门：

```bash
magick.exe montage *.jpg  -tile 22x2  -geometry 64x256+0+0 abc.jpg
# 将目录里的jpg文件按顺序拼成x轴22块，y轴2块的图 ，每个图块的大小为64X512像素，输出文件为abc.jpg

gaps run --image=img.png --size=xxx --save
# size填拼图各块的长宽
# 额外参数：
–generations # 遗传算法迭代次数，效果不好时适当改变
–population # 个体数量
```

## 文件隐写

### wbs4.3open

带密码的pdf隐写工具

### AOPR Forensic Edition

文档密码破解工具，支持暴力、字典、掩码等，可利用VBA后门
一个可用的学习版链接：[pcbeta](https://bbs.pcbeta.com/viewthread-1964941-1-1.html)

## 音频隐写

### Audacity

开源的音频编辑软件，可以可视化查看频谱、音轨，便于找出音频中的分析点

### DeepSound 2.0

带密码的wav隐写分析工具

### RX-SSTV

一个sstv识别工具，可将声音信息转为图像

### QSSTV

linux上的sstv接收软件，特点是可以直接读取wav音频文件里的信息，免去了外放的困扰
仓库：[Github - QSSTV](https://github.com/ON4QZ/QSSTV)

### mp3stego

正如其名，是一个命令行mp3隐写分析工具
链接：[mp3stego](https://www.petitcolas.net/steganography/mp3stego/)

## 压缩包分析

### ZipCenOp

zip伪加密修复
快速入门：

```bash
java -jar ZipCenOp.jar r fake_encrypted.zip
```

### ARCHPR

暴力破解工具，支持掩码、字典、明文攻击等手段

### bkcrack

zip明文攻击工具，和ARCHPR相比支持更多的参数
条件：1.ZipCrypto加密方式 2.已知其中某个完整的明文文件/已知明文的至少12个字节和偏移（其中又至少8字节要连续）

### hashcat

宇宙最强密码/哈希破解工具，支持多种系统，cpu/gpu/apu计算，支持多种hash算法，可破解rar、office文档、pdf等文件。

## 流量分析

### WireShark

抓包流量分析软件
快速入门：

#### mac地址/ip/端口过滤

```wireshark
eth.addr==20:dc:e6:f3:78:cc   //筛选MAC地址是20:dc:e6:f3:78:cc的数据包，包括源或者目的MAC地址
eth.src==20:dc:e6:f3:78:cc    //源MAC地址是20:dc:e6:f3:78:cc
eth.dst==20:dc:e6:f3:78:cc    //目的MAC地址是20:dc:e6:f3:78:cc

ip.addr==192.168.1.122        //筛选出IP地址是192.168.1.122的数据包，包括源IP地址或者目的IP地址
ip.src== 和ip.dst==同上

tcp.port==80         //根据TCP端口筛选数据包，包括源端口或者目的端口
tcp.dstport==80        //根据目的TCP端口筛选
tcp.srcport==80        //根据源TCP端口筛选
udp.port==4010       //根据UDP端口筛选数据包，包括源端口或者目的端口
udp.srcport==4010      //根据源UDP端口筛选
udp.dstport==4010      //根据目的UDP端口筛选
```

#### 协议筛选

常见协议：udp，tcp，arp，icmp，smtp，pop，dns，ip，ssl，http，ftp，ssh

```wireshark
http //过滤http流量
http.request.method==GET/POST
http.response
http.response.code >=400（包含错误码）
http.response.phrase == “OK”（过滤响应中的phrase）
http contains "snapshot" //过滤http头中含有指定字符
http.server contains “snapshot” //过滤http头中server字段含有指定字符
http.content_type == “text/html” //过滤content_type是text/html的http响应、post包
http.content_encoding == “gzip” //过滤content_encoding是gzip的http包
http.transfer_encoding == “chunked” //根据transfer_encoding过滤
http.content_length == 279
http.content_length_header == “279” //根据content_length的数值过滤
http.server //过滤所有含有http头中含有server字段的数据包
```

也可参考：[知乎 - Wireshark教程](https://zhuanlan.zhihu.com/p/631821119)

## MISC^2

### ntfsstreamseditor

NTFS数据流隐写

### veracrypt

磁盘加密软件，可建立虚拟磁盘并利用密码或者密钥文件进行加密，支持各种加密算法

### Cheat Engine

功能如其名，做一些游戏题的时候可以用这个走走捷径。
*不要和带反作弊的游戏一起开*

### bruteHASH

穷举指定格式的数据的HASH值，格式可以为：

- 指定明文格式
- 不限定明文格式随机字符穷举
- 自定义穷举字符集
- CTF 常见 HASH(MD4/MD5/SHA1)
- 设置 HASH 开头、结尾或包含字符串
