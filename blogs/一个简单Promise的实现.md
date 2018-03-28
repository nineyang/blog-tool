## 前言

`ES6`的异步处理非常方便，也非常优雅，在`GitHub`上面也有很多开源的接口，不过，`Promise`具体是怎么实现的呢？我们不妨自己动手写一个小的`demo`.

## 分析

我们首先来回顾一下`Promise`的基本用法:

    
    
    new Promise(function(resolve , reject){
    // 根据不同条件来判断执行不同的方法
    if(...){
        resolve();
    }else{
        reject();
    }
    }).then(function(){
    // this is resolve
    // do something
    } , function(){
    // this is reject
    // do something
    })

当我们在生成一个`Promise`的时候，会给他传入一个`闭包`，执行之后会根据我们的条件来决定执行哪个函数，`resolve`对应`then`中的第一个函数，`reject`对应第二个。众所周知，其实`Promise`中是有一个状态来判断当前执行到哪一步的，`PENDING`表示初始化，`FULLFILL`表示已完成，`REJECT`表示执行失败。因此，我们首先要做的第一件事情就是给他设置状态，以及我们实例化的时候需要做的准备工作:

    
    
    //定义状态
    const PENDING = 0;
    const FULLFILL = 1;
    const REJECT = 2;
    function Promise(cb){
        this.status = PENDING;
    // 用于接收传值
        this.value = '';
    // 用于存储
        this.deffers = [];
    // 通过setTimeout置于最后执行,cb.call(this)会返回一个闭包函数，剩下的两个会返回一个闭包作为参数执行
        setTimeout(cb.bind(this , this.resolve.bind(this) , this.reject.bind(this)) , 0);
    }

通过上面的初始化工作，可以帮助我们去执行我们传入的回调函数，但是问题就来了，我们现在没有`resolve`和`reject`这两个方法，因此，接下来一步就是在原型链上加上这两个方法:

    
    
    Promise.prototype = {
        constructor : Promise,
        resolve : function(value){
            this.status = FULLFILL;
            this.value = value;
            this.done();
        },
        resolve : function(value){
            this.status = REJECT;
            this.value = value;
            this.done();
        },
        done : function(){
            this.deffers.map(function(item){
                this.handler(item);
            }.bind(this));
        },
        handler : function(item){
            if(this.status == FULLFILL){
                item.success(this.value);
            }else if(this.status == REJECT){
                item.fail(this.value);
            }
        }
    }

通过上面的步骤，我们可以看到，会遍历`this.deffers`然后把其作为参数传入`this.handler`来执行，我们可以看到:`item`是有`success`和`fail`方法的，因此，这个时候我们的`then`就派上了:

    
    
    Promise.prototype.then = function(success , fail){
        this.deffers.push({
            success : success , 
            fail    : fail
        });
    }

至此，一个简单的`Promise`就得以实现了，我们可以做个简单的测试:

    
    
    new Promise(function(resolve , reject){
        resolve('nine');
    }).then(function(value){
        console.log('this is resolve , value is : ' + value);
    })

结果输出:`this is resolve , value is : nine`.  
当然，只做到这里是远远不够的，还有`then`的链式调用，`promisify` ， `all`等方法有待我们进一步实现。

本文由 [nine](https://www.hellonine.top/index.php/author/1/) 创作，采用
[知识共享署名4.0](https://creativecommons.org/licenses/by/4.0/) 国际许可协议进行许可  
本站文章除注明转载/出处外，均为本站原创或翻译，转载前请务必署名  
最后编辑时间为: Mar 21, 2018 at 04:49 pm

