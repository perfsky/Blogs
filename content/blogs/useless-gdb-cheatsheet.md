+++
title = "看了也不会的GDB CheatSheet"
keywords = ["Debug","CTF","Cyber Security"]
description = "Use(less) GDB CheatSheet"
date = "2024-05-23"
taxonomies = "1"
slug = "useless-gdb-cheatsheet"
+++

## 基本命令

### 1. disassemble

输出当前函数的汇编代码

默认为AT&T格式，用`set disassembly-flavor intel`来改为Intel汇编格式

可以用`layout asm`，在上方代码区显示汇编码

### 2. run

用`run`（简写r）开始执行程序，直到遇到断点停止。也可用Ctrl+C手动中断。执行过程再次使用run即可重启程序。

### 3. continue

触发断点或者用Ctrl+C中断后，用`continue`（简写c）继续，程序会执行直到遇到另一个断点。

### 4. break

用`break`（简写b）添加断点。

```bash
## 在函数名为functionname的入口处添加一个断点（比如main）
break functionname
## 在当前文件行号为LineNo处添加一个断点
break LineNo
## 在filename文件行号为LineNo处添加一个断点
break filename:LineNo
```

### 5. tbreak

`tbreak`和`break`用法相同，不过用此命令添加的断点触发一次之后即被删除。

### 6. info break/enable/disable/delete

`info break`查看添加的所有断点

`enable/disable + 断点编号`可启用/禁用断点。若不加编号，默认对所有断点进行处理

`delete + 断点编号`永久删除断点。若不加编号，默认对所有断点进行处理

### 7. backtrace/frame

`backtrace (bt)`查看当前线程的调用堆栈

`frame + 堆栈编号`可切换到其他堆栈

### 8. list

`list (l)`查看当前断点附近的代码。一般显示断点前后10行代码

`list + [加号]` 向下显示10行代码， list+[减号] 向上显示10行代码

### 9. print/ptype

- print

`print (p)` 可方便输出/修改变量的值

同时支持输出表达式（解引用*，算术+-*/，打印错误码对应文字信息`strerror(errno)` ）

`print variable = value` 即可修改变量的值

`print /format variable` 指定输出格式

- ptype

`ptype variable` 输出变量类型（支持结构体）

### 10. info/thread

`info`用于查看各种信息，比如

`info thread` 查看所有线程

`info args` 查看当前函数的参数值

`thread + 线程编号` 切换到指定线程

### 11. next/step/until/finish/return/jump

`next (n)`跳到下一行（单步步过step over，遵循代码逻辑）

`step (s)`会进入函数内部（单步步入step into）

`until (u) + <lineno>` 直接执行到行数停止

`return <value>` 直接让函数用value返回值返回

`jump <lineno/location>` 直接跳到行数或者函数地址（不停止，需要自行设置断点）

> GDB空行直接回车默认为执行最近一次的命令。

### 12. set args/show args

在使用run命令之前，使用`set args`命令行参数来指定.

可以使用文件，也可以直接輸入參數。有空格可以用雙引號包裹起來。

清除参数，用`set args`不加参数即可

### 13. watch/display

watch监视一个变量或者一段内存，如果发生变化就会中断。会产生一个watch point 观察点（数据断点）

display监视变量或者内存值，每次 gdb 中断下来都会自动输出这些被监视变量或内存的值

`nfo display`查看当前已经监视了哪些值，使用`delete display`清除全部被监视的变量，使用`delete display + 编号`移除对指定变量的监视

### 14. dir

gcc/g++编译出来的可执行程序并不包含完整源码，在不同环境里调试时可能不能匹配，dir可以让被调试的可执行程序匹配源代码

```bash
# 加一个源文件路径到当前路径的前面,指定多个路径为源码目录，可以使用引号”:”
dir SourcePath1:SourcePath2:SourcePath
```

`show dir`可以查看当前设置的源码路径

dir不加参数则初始化搜索路径为空

## 参考

[GDB常用命令详解——利用GDB调试Redis](https://cppguide.cn/pages/68d9ed/#_2-5-1-gdb%E5%B8%B8%E7%94%A8%E8%B0%83%E8%AF%95%E5%91%BD%E4%BB%A4%E6%A6%82%E8%A7%88%E5%92%8C%E8%AF%B4%E6%98%8E)

[GDB 备忘清单 & gdb cheatsheet & Quick Reference](https://quickref.cn/docs/gdb.html)

[CheatSheet PDF](G[DB-cheat-sheet.pdf](https://www.sourceware.org/gdb/download/onlinedocs/refcard.pdf))
