## 前言

前几天一个朋友咨询我关于在线聊天的事情，所以我就顺手写了一个简单的在线聊天系统。  
由于我是使用了最新版的`Laravel`，所以需要在`PHP7.0`以上的版本才可以搭建，具体的安装和使用可以参考`GitHub`。

[GitHub](https://github.com/nineyang/chat)  
[在线体验](http://chat.hellonine.top/)

## WebSocket

网页版的在线聊天一般分为两种方式，轮询和全双工。以传统的`HTTP`形式来做，`Server`没办法主动的向`Client`发送消息，而像`WebSocket`这种全双工形式则不太一样，二者保持长连接，并且能让`Server`主动的推送消息到`Client`，这就大大节省了请求资源。  
而`Swoole`非常方便的以扩展的形式集成了这些高级功能。

## 思路

建立用户，创建房间这种非常简单的业务逻辑就不再赘述，这里主要讲一下聊天的实现。  
由于`Swoole`的`WebSocket`都是单独的建立一个`PHP`进程，所以在数据共享上面我使用了`Redis`，使用`SET`来完成每个房间成员的统计，使用`HASH`来完成每个`Connect
ID`对于房间号的绑定。关于`Redis`每种类型的使用以及实现原理可以参考我之前写的这篇文章：[聊一聊Redis的数据结构](http://www.hellonine.top/index.php/archives/56/)。  
`Swoole`我以`command`的形式来处理逻辑，主要参考了这篇[文章](http://www.jianshu.com/p/4ad04f8ff907)。

 **文章首发地址：[我的博客](http://www.hellonine.top)**

## 参考

[Laravel如何优雅的使用Swoole](http://www.jianshu.com/p/4ad04f8ff907)

本文由 [nine](https://www.hellonine.top/index.php/author/1/) 创作，采用
[知识共享署名4.0](https://creativecommons.org/licenses/by/4.0/) 国际许可协议进行许可  
本站文章除注明转载/出处外，均为本站原创或翻译，转载前请务必署名  
最后编辑时间为: Mar 21, 2018 at 04:44 pm

