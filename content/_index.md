+++
title = ""
date = 2024-10-12T20:34:58+08:00
toc = false
keywords = ["Blog","Technology","Coding","CTF","Computer Science"]
description="Sakuya's Personal Blog"
# slug = "xxx"
# draft = true
# weight = 1
+++

<style>
    /* body {
        background-color: #f0f0f0; /* 设置页面背景色 */
        color: #333; /* 可选：设置文本颜色 */
    } */
</style>

<div align="center" style="margin-top: 20vh;"> <!-- 确保居中 -->
    <h1 style="font-size: 5em; font-family: 'Times New Roman', serif; margin-bottom: 0em;">
        Sakuya's Blog
    </h1>
    <h3 style="font-size: 1.8em; font-family: 'Times New Roman', serif; margin-top: 0em;">
        Stay Hungry. Stay Foolish.
    </h3>
</div>

<hr style="width: 85% !important; border: 1px solid #d1d5db; margin: 20px auto;">

<div style="display: flex; justify-content: center; flex-wrap: wrap; row-gap: 0px; column-gap: 15px; margin-top: 0em;">
    {{< cards >}}
        <div style="min-width: 300px;"> <!-- 设置卡片最小宽度 -->
            {{< card link="/myblog" title="博客" icon="pencil" >}}
        </div>
        <div style="min-width: 300px;">
            {{< card link="/matches" title="比赛" icon="code" >}}
        </div>
    {{< /cards >}}
    {{< cards >}}
        <div style="min-width: 300px;">
            {{< card link="/misc" title="杂项" icon="light-bulb">}}
        </div>
        <div style="min-width: 300px;">
            {{< card link="/about" title="关于" icon="heart">}}
        </div>
    {{< /cards >}}
</div>
