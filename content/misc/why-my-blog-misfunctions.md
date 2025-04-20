+++
title = "高版本Hugo的一个注意事项"
keywords = ["Blog","Hugo","Bug"]
description = "关于Promise的一些探究"
date = "2025-04-20"
taxonomies = "1"
slug = "why-my-blog-misfunctions"
+++

## 起因

之前一直用的是Hugo 0.126.1版本，并且我的一个博客子页面放在文件夹`/blogs`下。最近换了电脑，顺带升级到最新的Hugo版本，编译的时候发现生成的网页在/blogs下会出现显示错位的问题。排查一番发现，新版本的Hugo会默认将生成的所有网页创建一个副本放在`/blogs`下，和我的子页面冲突了。

## 解决方案

解决方案是将`/blogs`文件夹重命名为其他名字，比如`/myblog`，然后执行`hugo --gc`重新生成。
