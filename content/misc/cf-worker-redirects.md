+++
title = "关于Cloudflare workers 的重定向"
keywords = ["Blog","Cloudflare","Workers","Redirection"]
description = "关于Cloudflare workers 的重定向"
date = "2025-08-30" # !!! FIXME
taxonomies = "1"
slug = "cf-worker-redirects"
+++

## 解决方案

最近做了个React+Vite的静态页面，考虑到后续可能有自动化的一些脚本需求，所以没用Pages而是用了Workers部署。

直到我发现，在访问/featured后，刷新会提示404，这时候才发现Workers没做Pages的重定向逻辑，什么路由也没重写。

随后我参考了[文档](https://developers.cloudflare.com/workers/static-assets/redirects/)里面手动设置重定向的步骤，写了`/* /index.html 200`，但是部署报错：`Infinite loop detected in this rule.`我的想法是把所有其他请求都改写到index，或许是workers修改了机制，导致这样不成功。

可行的做法是：

```plaintext
/featured   /   200
/albums     /   200
/about      /   200
```

这样每个路由都手动写一次即可。
