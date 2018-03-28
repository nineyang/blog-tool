## 前言

最近在学着写一个基于`Koa`的`MVC`框架，在使用`koa-
router`时，发现当我在使用其提供的回调函数来执行一个`controller`下面的`action`时，意外的发现，他的`this`不见了:

    
    
    // index.js
    const route = require('koa-router')();
    const user = require('../app/controllers/User');
    
    let userObj = new user;
    
    route.get('/bb' , userObj.index);
    
    // user.js
    index(ctx, next) {
            console.log(this);
            ctx.body = 'hello api';
        }

![f8613432-e34d-4a85-b47e-5f75d7d96b72.png](https://github.com/nineyang/blog-tool/blob/master/images/f8613432-e34d-4a85-b47e-5f75d7d96b72.png)

![9e01e930-81af-4226-a2a5-3a27e1850b1d.png](https://github.com/nineyang/blog-tool/blob/master/images/9e01e930-81af-4226-a2a5-3a27e1850b1d.png)

要阐述`this`为什么会是`undefined`之前，我们先得搞清楚在什么情况下会产生`undefined`。

### this指向

在`js`中的`this`指向已经是一个老生常谈的话题，总结起来就是一句话: **this永远指向最后调用他的对象**.下面有两个例子:

    
    
    //demo1
    let aaa = function () {
        console.log(this);
    };
    aaa();
    
    
    //demo2
    'use strict';
    
    let aaa = function () {
        console.log(this);
    };
    aaa();

上面不是说了吗？最后谁调用`this`就指向谁，这里是`window`对象调用，所以这里的输出应该是`window`对象。但是很遗憾的是，在严格模式下，`this`如果是在`window`下执行，那么就是`undefined`。

![9b03bdbd-3519-479d-ae41-614ccb7e2211.png](https://github.com/nineyang/blog-tool/blob/master/images/9b03bdbd-3519-479d-ae41-614ccb7e2211.png)

所以，我有一个大胆的猜想，为什么`Koa`中的`this`是`undefined`，可能就是因为在严格模式下执行，但是这也不足以证明，所以我就大致的看了一下`Koa`的源码，`koa-
router`只是一个帮助我们把一些需要执行的函数放在`koa`的`application.js`下的`middleware`中，最终路由匹配还是由`koa`来操作的，所以我发现了如下的代码:

    
    
    // application.js
    callback() {
        const fn = compose(this.middleware);
    
        if (!this.listeners('error').length) this.on('error', this.onerror);
    
        const handleRequest = (req, res) => {
          res.statusCode = 404;
          const ctx = this.createContext(req, res);
          const onerror = err => ctx.onerror(err);
          const handleResponse = () => respond(ctx);
          onFinished(res, onerror);
          return fn(ctx).then(handleResponse).catch(onerror);
        };
    
        return handleRequest;
      }

我们可以看出，最后通过`fn(ctx)`来完成。所以，最终的执行就好比这样一种形式:

    
    
    let aaa = ()=>{
        bbb();
    };
    let bbb = function () {
        console.log(this);
    };
    aaa();

![4f1a9800-6122-4df5-9391-b821a3bc5710.png](https://github.com/nineyang/blog-tool/blob/master/images/4f1a9800-6122-4df5-9391-b821a3bc5710.png)

所以返回回调之后执行的环境是`window`下，因此才出现了`undefined`的现象。

### bind

既然问题知道了在哪里，所以也就知道该如何解决了，因此，我在重新包装`koa-
router`的路由的时候，给这个函数绑定了我给他生成的`controller`，即一个对象的实例。这样，我就可以在`controller`层做一些放心大胆的`this`操作了:

![42a5f4ea-eaca-4a17-8abb-a150b0312f55.png](https://github.com/nineyang/blog-tool/blob/master/images/42a5f4ea-eaca-4a17-8abb-a150b0312f55.png)

不过，既然聊到了这里，那我就顺便说一些我对于`bind`,`call`,`apply`的理解，如有不对的地方还望指点。

对于`bind`，官方的解释是:

> bind()方法创建一个新的函数, 当被调用时，将其this关键字设置为提供的值，在调用新函数时，在任何提供之前提供一个给定的参数序列。

解释的已经非常清晰，而我的理解是:

> bind帮我们生成一个新的函数之后，当我们在调用时，可以让他通过`this`能使用到我们所指定的对象。

好吧，其实解释的都比较晦涩，我们先来看一个小的例子:

    
    
    'use strict';
    
    let a = {
        name: 'seven',
        test: function () {
            console.log(this.name);
        }
    };
    
    let b = {
        name : 'nine'
    };
    a.test.bind(b)();

其结果:  
![e13f6cde-16b1-4660-8111-6ee02d32b01c.png](https://github.com/nineyang/blog-tool/blob/master/images/e13f6cde-16b1-4660-8111-6ee02d32b01c.png)

### call&apply

与`bind`不同的是，`call`和`apply`没有生成函数的这一过程，直接执行。而`call`和`apply`的区别在于，`call`是单个单个的传递参数，而`apply`则是以数组的形式传递参数，其实熟悉`PHP`的应该能联想到`call_user_func`和`call_user_func_array`这两个函数。

    
    
    'use strict';
    
    let a = {
        name: 'seven',
        test: function (...args) {
            console.log(args);
            console.log(this.name);
        }
    };
    
    let b = {
        name : 'nine'
    };
    a.test.bind(b)('hello' , 'nine');
    a.test.call(b , 'hello' , 'nine');
    a.test.apply(b , ['hello' , 'nine']);

其结果:  
![d493de29-f985-48ec-967b-96ba658e6e6b.png](https://github.com/nineyang/blog-tool/blob/master/images/d493de29-f985-48ec-967b-96ba658e6e6b.png)

### 箭头函数

最后提一下箭头函数，`ES5`之后，开始支持箭头函数的写法，非常方便，但是箭头函数与我们普通函数还是有一点小小的区别的，比如`this`的问题，`MDN`的解释是这样的:

> 一个箭头函数表达式的语法比一个函数表达式更短，并且不绑定自己的 this，arguments，super或
new.target。这些函数表达式最适合用于非方法函数，并且它们不能用作构造函数。

所以当我们使用如下的代码，会发现`this`是一个空对象:

    
    
    'use strict';
    let obj = {
        i: 10,
        b: () => console.log(this.i, this),
        c: function() {
            console.log( this.i, this)
        }
    };
    obj.b();
    // undefined {}
    obj.c();
    //10 obj

![3d15413c-9234-4dfc-8cd7-58a4afd9069c.png](https://github.com/nineyang/blog-tool/blob/master/images/3d15413c-9234-4dfc-8cd7-58a4afd9069c.png)

### 参考

  1. [Javascript 严格模式详解](http://www.ruanyifeng.com/blog/2013/01/javascript_strict_mode.html)

  2. [彻底理解js中this的指向](http://web.jobbole.com/85198/)

本文由 [nine](https://www.hellonine.top/index.php/author/1/) 创作，采用
[知识共享署名4.0](https://creativecommons.org/licenses/by/4.0/) 国际许可协议进行许可  
本站文章除注明转载/出处外，均为本站原创或翻译，转载前请务必署名  
最后编辑时间为: Mar 21, 2018 at 04:48 pm

