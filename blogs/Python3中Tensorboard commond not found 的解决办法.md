我们在安装`tensorflow`的时候会依赖于`tensorboard`，但是，当我们按照网上的教程来执行:

    
    
    tensorboard --logdir=your/path

时，发现:

    
    
    command not found: tensorflow

所以就在网上找了一同答案，但是网上能找到的大多数是针对`python2`的，并且即使有`python3`的，也是之前的版本了，不过有一篇[文章](https://quickgrid.blogspot.hk/2017/05/TensorFlow-
setup-using-pip3-and-Starting-Tensorboard-in-Linux-Mint-
VirtualBox.html)虽然没能解决我的问题，但是却提供了一些基本思路，所以我是这么解决的:

  1. 

    
    
    pip3 show tensorflow

找到安装包所在的位置:

    
    
    Location: /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages
    Requires: numpy, six, tensorflow-tensorboard, wheel, protobuf

  1. 

    
    
    cd /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages && ls

发现`tensorflow`和`tensorboard`包是独立的

3.

    
    
    cd tensorboard && ls

发现并没有网上说的`tensorboard.py`文件，能用的是一个`main.py`文件

4.

    
    
    alias tensorboard='python3 /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/tensorboard/main.py' && source ~/.bash_profile

新建一个便捷的别名并更新

5.

    
    
    tensorboard --logdir=/tmp

此时已经能成功跑起来。

本文由 [nine](https://www.hellonine.top/index.php/author/1/) 创作，采用
[知识共享署名4.0](https://creativecommons.org/licenses/by/4.0/) 国际许可协议进行许可  
本站文章除注明转载/出处外，均为本站原创或翻译，转载前请务必署名  
最后编辑时间为: Mar 21, 2018 at 04:46 pm

