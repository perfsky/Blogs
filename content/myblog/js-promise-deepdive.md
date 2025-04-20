+++
title = "关于Promise的一些探究"
keywords = ["Blog","Frontend","JavaScript","Async"]
description = "关于Promise的一些探究"
date = "2025-04-20"
taxonomies = "1"
slug = "js-promise-deepdive"
+++

## 前言

对于Promise，我们都知道它是一个代表异步操作的对象。它有三种状态（pending、fulfilled、rejected），并且可以绑定回调函数来处理操作结果。但是，我最近写了一点异步请求的代码，碰到了这样的一个实现：

```js
return new Promise((resolve, reject) => {
  this.pendingResolvers.get(key).push([resolve, reject]);
});
```

它看起来没什么特别的地方。但我突然意识到，我以前可能其实根本没搞懂 Promise 是怎么“兑现承诺“的。

## Promise的实现

大部分博客中，Promise的实现都只会列出这样的用法：

```js
const promise = new Promise((resolve, reject) => {
  // 异步操作
  if (success) {
    resolve(value);
  } else {
    reject(error);
  }
}).then(result => {
  // 处理结果
}).catch(error => {
  // 处理错误
});
```

按直觉，我们会认为新建的这个Promise对象会按顺序“自动地”执行里面的异步操作，并在某个时刻完成。但实际上，`new Promise(...)`并不代表“我要开始一个异步任务，实现完之后调用`resolve()`或者`reject()`，接下来调用then()”，而是“我想要一个Promise对象，但是什么时候放东西进去，什么时候让它返回数据，由我自己决定”。也就是说，Promise对象的创建和异步操作的执行是两个独立的过程。在这个例子中：

```js
return new Promise((resolve, reject) => {
  this.pendingResolvers.get(key).push([resolve, reject]);
});
```

这段代码只是创建并返回了一个Promise对象，然后把它的`resolve()`和`reject()`方法放进了一个请求队列的数组里，没有执行任何异步操作，也没有兑现任何结果。这个Promise对象永远处于`pending`状态，直到其他地方（比如用一个`_flush()`方法对队列中的每个`[resolve, reject]`进行处理），才会改变自己的状态。此时Promise的`then()`、`catch()`都处于挂起状态，直到监听到Promise对象被兑现才会执行。

这种模式被称为deferred模式，或者“延迟对象”，先创建一个deferred，把它传出去，等什么时候操作完成了（未必是异步，并且异步操作甚至可以不在该deferred对象里面），再调用它的`resolve()`或者`reject()`来兑现承诺。这是个很有意思的点，代表很多时候Promise可以被当做一个“容器”，先传递给需要的人，等到有了东西才放进去让人使用。理解这一点之后，再回头看`then()`、`catch()`就会发现，那些都是在监听“承诺何时被兑现”，而不是在参与“异步过程的发起”。

## 代码分析

上面的代码实现的是一个`BatchRequestManager`类，它的作用是批量请求数据，并且支持缓存、去重、取消等功能。我们探讨的关键代码如下：

```js
get(key) {
    ...
    const promise = new Promise((resolve, reject) => {
        this.pendingResolvers.get(key).push([resolve, reject]);
    });
    if (!this.timer) this.timer = setTimeout(() => this._flush(), this.delay); // 启动定时器
    return promise;
}

async _flush() {
    const keys = Array.from(this.keysToFetch);
    this.keysToFetch.clear();
    this.timer = null;

    let results;
    try {
        results = await this.batchRequestFn(keys);
    } catch (err) {
        ...
        return;
    }

    for (const key of keys) {
        if (key in results) {
            const value = results[key];
            this.cache.set(key, value);
            const resolvers = this.pendingResolvers.get(key) || [];
            for (const [resolve] of resolvers) {
                resolve(value);
            }
        } else {
            const resolvers = this.pendingResolvers.get(key) || [];
            for (const [_, reject] of resolvers) {
                reject(new Error(`no data for key: ${key}`));
            }
        }
        this.pendingResolvers.delete(key);
    }
}

```

经过之前的探讨后，我们就可以理清楚这个代码的逻辑了：

1. `get(key)`中会创建一个新的Promise对象，并把它的`resolve()`和`reject()`方法放进一个请求队列中。此时这个Promise对象处于`pending`状态，并且什么也没干。
2. 接下来延迟50ms后调用`_flush()`方法。`_flush()`方法会请求队列中取出所有的key，并调用`batchRequestFn(keys)`方法批量请求数据。
3. 如果请求成功，遍历所有的key，把它们的结果放入缓存中，并调用每个key对应的Promise对象的`resolve()`方法，改变它们的状态为`fulfilled`。否则变为`rejected`。
4. 当状态变为`fulfilled`或者`rejected`时，所有监听这个Promise对象的`then()`、`catch()`方法会被调用。

## 完整代码

```js
// 有一个 requestFn(keys: string[]): Promise<Record<string, any>> 方法，每次可以批量获取多个 key 对应的数据（如批量接口：传一组 key，返回一个 key-value 对）。
// 用户可以通过 get(key: string): Promise<any> 来请求某个 key 的数据：
// 如果当前有同样的 key 正在请求中，应复用同一个 promise。意思是：
// 要使用同一个promise，对每个请求都返回这个promise的[resolve, reject]。
// 不同的 key 会被合并成一个批量请求，延迟 50ms 发出。
// 有 cancel(key: string) 方法，用于取消某个 key 的请求（如果它还没发出或者还在 pending）。
// 有缓存：如果某个 key 的数据已请求成功，应缓存，后续请求直接从缓存中取值。

class BatchRequestManager {
    constructor(batchRequestFn) {
        this.batchRequestFn = batchRequestFn;
        this.delay = 50; // 延迟时间

        this.keysToFetch = new Set(); // 收集请求的 key
        this.pendingResolvers = new Map(); // 收集请求的key对应的promise，key ->多个 Promise[resolve,reject]
        this.cache = new Map(); // 缓存结果 key -> value

        this.timer = null; // 防抖
    }

    /**
     * 获取某个 key 的数据，合并请求、去重、带缓存
     * @param {string} key
     * @returns {Promise<any>}
     */
    get(key) {
        // 复用缓存
        if (this.cache.has(key)) {
            return Promise.resolve(this.cache.get(key)); // 从缓存中获取
        }
        // 复用请求队列
        if (this.pendingResolvers.has(key)) {
            return new Promise((resolve, reject) => {
                this.pendingResolvers.get(key).push([resolve, reject]);
            });
        }
        // 新的请求
        this.keysToFetch.add(key);
        this.pendingResolvers.set(key, []);
        const promise = new Promise((resolve, reject) => {
            this.pendingResolvers.get(key).push([resolve, reject]);
        });

        if (!this.timer) this.timer = setTimeout(() => this._flush(), this.delay); // 启动定时器

        return promise;
    }

    /**
     * 取消某个 key 的请求
     * @param {string} key
     */
    cancel(key) {...}

    /**
     * 批量请求
     * @private
     */
    async _flush() {
        const keys = Array.from(this.keysToFetch);
        this.keysToFetch.clear();
        this.timer = null;

        let results;
        try {
            results = await this.batchRequestFn(keys);
        } catch (err) {
            // 出现任何失败，都会将所有的请求 reject
            for (const key of keys) {
                // 找到每个key的多个[resolve, reject]，全部 reject
                const resolvers = this.pendingResolvers.get(key) || [];
                for (const [_, reject] of resolvers) {
                    reject(err);
                }
                this.pendingResolvers.delete(key);
            }
            return;
        }

        // 请求成功，分别 resolve
        for (const key of keys) {
            if (key in results) {
                const value = results[key];
                this.cache.set(key, value);

                // 这里每个key都有多个[resolve, reject]，我们全部 resolve
                const resolvers = this.pendingResolvers.get(key) || [];
                for (const [resolve] of resolvers) {
                    resolve(value);
                }
            } else {
                const resolvers = this.pendingResolvers.get(key) || [];
                for (const [_, reject] of resolvers) {
                    reject(new Error(`no data for key: ${key}`));
                }
            }
            this.pendingResolvers.delete(key);
        }
    }
}


```