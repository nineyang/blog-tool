## 前言

前几天写了一个简单的`Laravel`的[dd](https://github.com/nineyang/dd)库。  
为什么自己要写一个这样的库？  
`Laravel`本身已经实现了自己的输出`dd`函数，但是我之所以要写这样一个库，一来是因为`Laravel`本身对这个库的封装没办法很好的解剖出来，另一方面，他的实现过于复杂。

## 安装方式

  1. composer 安装

    
    
    composer require nine/dd 

  1. 直接下载

clone 下来即可

## 使用

  1. 如我在[exapmle.php](https://github.com/nineyang/dd/blob/master/example.php)中所写，我们既可以直接使用:

    
    
    \dd\Dump::dump('hello,nine');

同时也可以自己封装一个`dd`函数:

    
    
    function dd($value)
    {
        \dd\Dump::dump($value);
    }
    
    dd("hello,nine");

不管是哪种方式，他都会自动的识别我们的类型来予以不同的展示效果。

此外，如果需要自己单独配置样式和新增装饰符号，可以在[conf](/src/conf)目录下根据所给的注释予以添加。

## 效果

  1. string

![d84bc944-3427-4ad8-bee4-822f6ce1775a.png](https://github.com/nineyang/blog-
tool/blob/master/images/d84bc944-3427-4ad8-bee4-822f6ce1775a.png)

  1. array

![d5f42a26-f46b-4a5f-9894-a558e8be994b.png](https://github.com/nineyang/blog-
tool/blob/master/images/d5f42a26-f46b-4a5f-9894-a558e8be994b.png)

  1. function

![9f0c4815-d1a6-4d3f-999a-0ceeb6ab49ac.png](https://github.com/nineyang/blog-
tool/blob/master/images/9f0c4815-d1a6-4d3f-999a-0ceeb6ab49ac.png)

  1. object

![2f1a3c3a-c621-46ee-97d2-ff610d245a9e.png](https://github.com/nineyang/blog-
tool/blob/master/images/2f1a3c3a-c621-46ee-97d2-ff610d245a9e.png)

## 结构

    
    
    .
    ├── Dump.php
    ├── conf
    │   ├── css.php
    │   └── decorator.php
    ├── decorator
    │   ├── DecoratorComponent.php
    │   ├── Div.php
    │   ├── P.php
    │   └── Span.php
    └── render
        ├── AbstractDump.php
        ├── DumpArray.php
        ├── DumpObject.php
        └── DumpString.php
    

以上是他的主要目录结构。

  1. 其中`Dump.php`主要是我们用来中转类型的地方，他会根据我们提供数据的不同类型，来解析并用反射类来帮我们实现中转。  
`conf`层主要是一些配置文件，`css.php`是一个样式配置文件，`decorator.php`是一个我们需要定制的装饰器，比如`=>`符号之类的。

  2. `decorator`是装饰器层，`DecoratorComonent.php`是一个装饰器基类，他的主要工作是用来初始化我们的样式表，同时提供了一些可以让我们自定义的方法，比如添加`span`装饰器，或者给这个装饰器添加一些样式等等。`Span.php`等文件主要是我们的具体装饰器，其中主要有两个方法，`wrap`方法来完善最终的输出效果，而`display`方法则是用来输出。

  3. `render`是渲染层，这里就像是一个效果加工厂，比如前面提到的`decorator`提供了一些添加样式的工具，那么这里就是用来调用这些工具的地方。`AbstractRender.php`是一个基类，里面提供了一些初始化我们前面提到的自定义装饰器符号的工具，还有包裹解析我们的数组形成数组的装饰效果(因为像对象还有函数都会用到它)，还有像`parseParams`会根据我们传入的函数(方法)的参数所形成的反射数组，来进行解析，判断他的默认值等，最终形成一个包裹好的装饰器；`display`方法主要就是获取我们的`span`之类的装饰器，然后最终调用装饰器的`display`方法来予以输出。  
而里面的诸如`DumpString.php`主要是有提供一个`render`方法来给外面的`Dump.php`使用，这几个就是会根据具体的类型来进行解析了。

## 大概思路

我们最终要实现的一个页面效果是像`Dom`节点一样，一层一层的包裹着我们最终的元素。所以我能第一时间联系到的就是`装饰器`。装饰器去生产各种`Dom`节点，为了防止生产对象的滥用，我这里也在`AbstractDump.php`文件中加入了单例的判断。当然，里面可能有许多设计的不够合理的地方，还望指正。

* * *

个人博客[地址](http://www.hellonine.top):`http://www.hellonine.top`。

本文由 [nine](https://www.hellonine.top/index.php/author/1/) 创作，采用
[知识共享署名4.0](https://creativecommons.org/licenses/by/4.0/) 国际许可协议进行许可  
本站文章除注明转载/出处外，均为本站原创或翻译，转载前请务必署名  
最后编辑时间为: Mar 21, 2018 at 04:46 pm

