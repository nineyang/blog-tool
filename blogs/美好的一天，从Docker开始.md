## Docker介绍

### 介绍

`docker`作为现代化程序猿必不可少的技能(好吧，其实我也是因为公司需要...)逃...)，能极大的让我们以最小的空间成本(相对于真正的虚拟机而言)去完成我们在不同项目的环境部署。

### 镜像

镜像就好比我们所理解的虚拟机，不过这个虚拟机是一个只包含 **开发环境** 的虚拟机，或者说，一个生产环境的工厂。

### 容器

容器就好比从工厂下批量生产的产品，而我们的`开发`，正要在这个`产品`下面进行开发。当然，也有很多人会把`镜像`和`容器`的概念比作`类`和`对象`的关系。

### 优点

#### 所占空间小:

通常，我们在做虚拟机操作时，往往会给虚拟机分配不同的空间，而其中的系统，则占了其中一部分的空间，所以会造成空间的浪费，而对比于`docker`，`docker`则减少了系统`OS`部分，简而言之，就是说`docker`在让我们享有`虚拟机`功能的同时，也减少了对空间的浪费。

#### 操作方便:

`Docker`提供了大量的方便我们操作的指令，帮助我们生成镜像和容器。

#### 统一的镜像管理:

[Docker
Hub](https://hub.docker.com/)作为最大的`Docker`镜像平台，与`GitHub`类似，我们可以在上面直接找到我们想要的镜像。

* * *

## Docker基本操作

### 安装

安装就不说了，直接去[官网](https://www.docker.com/)下载。

### Docker操作

#### 拉取线上镜像

    
    
    docker pull $mirror:$tags

> `$mirror`表示拉取的镜像名，`$tags`表示标签，我们可以写版本号，例如`docker pull
centos:6.5`，如果没有写`$tags`，则会拉取`latest`，即最新版本。

#### 根据镜像生成容器

    
    
    docker run -d --name $container $mirror:$tags

> `-d`表示在后台运行，`--name
$container`是给这个容器取一个名字，如果不给也可以，镜像会自动生成一个名字，如果在本地找不到这个镜像，则会直接去线上找。另外还有`-p`，指定运行对应端口，例如:`docker
run -d -p 80:80 docker-nginx nginx`。

#### 关闭容器

    
    
    docker stop $container

#### 开始容器

    
    
    docker start $container

> `start`操作只能在已经生成容器之后

#### 删除容器

    
    
    docker rm $container

#### 删除镜像

    
    
    docker rmi $mirror

> 需要注意的是，此时必须没有容器使用这个镜像，否则无法删除，当然，这里也可以通过`IMAGE ID`来删除，可以通过`docker
images`来查看容器列表。

#### 查看当前运行容器

    
    
    docker ps

* * *

### DockerFile

#### 简介

当我们在搭建环境时，我们难免要对镜像进行操作，比如我们要给镜像安装一个扩展，或者说修改镜像的配置文件，`DockerFile`就是来解决这样一个问题的。我们在写入`DockerFile`的同时，也相当于记录了我们的操作，后续其他人查看起来也非常方便。

#### 常用指令

##### `FROM`:使用哪个镜像，例如`FROM php:7.1-fpm`

##### `RUN`:相当于在命令行执行，例如`RUN apt-get install -y libicu-dev`

##### `COPY`:复制`源目录文件`到`目标目录文件`，例如`COPY ./config/php/php.ini
/usr/local/etc/php/conf.d/`

##### `ENV`:设置环境变量，例如`ENV PHP_VERSION 7.1`，在接下来的脚本中就可以直接调用这个环境变量

[查看更多](https://yeasy.gitbooks.io/docker_practice/content/image/dockerfile/)

* * *

### docker-compose

#### 简介

如果说`DockerFile`是用来对镜像的操作，那么`docker-compose`则是对容器的操作，通常有一个`docker-
compose.yml`或者`docker-compose.yaml`文件，该文件采用的是`YAML`脚本形式。

#### 常用指令

##### `docker-compose build`根据`docker-
compose.yml`文件来构造这个容器，如果对文件进行了修改，也需要重新`build`一下

##### `docker-compose stop`停止该容器

##### `docker-compose up -d`新建并后台启动

##### `docker-compose start -d`后台启动

##### `docker-compose down`停止并删除

##### `docker-compose stop`停止

> 注：`Docker`的操作还有很多，这里只列举出常用的。

* * *

## LNMP实战

### 简介

[`LNMP`](https://github.com/nineyang/docker-for-
lnmp)包含了`mysql:5.7`，`nginx:1.1`，`php:7.1`以及`php`的相关扩展，[GitHub](https://github.com/nineyang/docker-
for-lnmp)地址:`https://github.com/nineyang/docker-for-lnmp`。

### 操作

`git clone`下来之后`cd`到该目录下并执行

    
    
    docker-compose up --build -d

#### 停止容器

    
    
    docker-compose stop

#### 重新开启容器

    
    
    docker-compose start

#### 删除容器

    
    
    docker-compose down

#### 安装php扩展

    
    
    php扩展主要根据docker提供的docker-php-ext-install来安装，非常方便

* * *

## 所遇问题

### 安装扩展库时下载失败:

    
    
    W: Failed to fetch http://mirrors.online.net/debian/dists/jessie/main/source/Sources  Hash Sum mismatch
    E: Some index files failed to download. They have been ignored, or old ones used instead.

或者类似的报错提示，在这种情况下，我们可以采取两种方式进行尝试:

#### 在`DockerFile`中修改我们的`下载来源`

    
    
    RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && \
        echo "deb http://mirrors.aliyun.com/debian/ jessie main non-free contrib" >/etc/apt/sources.list && \
        echo "deb http://mirrors.aliyun.com/debian/ jessie-proposed-updates main non-free contrib" >>/etc/apt/sources.list && \
        echo "deb-src http://mirrors.aliyun.com/debian/ jessie main non-free contrib" >>/etc/apt/sources.list && \
        echo "deb-src http://mirrors.aliyun.com/debian/ jessie-proposed-updates main non-free contrib" >>/etc/apt/sources.list

#### 修改`DNS`

将系统分配的`DNS`修改为公用的即可，`vi
/etc/resolv.conf`,参考自[该博客](http://securityer.lofter.com/post/1d0f3ee7_d0cd529)。

### 覆盖配置文件失败:

最开始我是把配置文件单独的放在一个`config`文件夹下面，然后`COPY ../config/php/php.ini
/usr/local/etc/php`，但是，会报错

    
    
    ERROR: Service 'php' failed to build: Forbidden path outside the build context: ../config/php/php.ini ()

后来，通过查资料了解到`docker`会根据`DockerFile`来确定一个`执行上下文`，简而言之就是说，服务器端的`docker`是会以当前的`DockerFile`所在的层级为根目录，所以只能找到与`DockerFile`同级或者其下目录下的文件了，至于为什么说是`服务端的docker`，那是因为`docker`的架构其实也是一个`C/S`的架构，我们所使用的指令，其实都是对`C`端的操作。

* * *

## 参考

[Docker 快速上手指南](https://segmentfault.com/a/1190000008822648)  
[使用 Docker 构建 LNMP 环境](https://segmentfault.com/a/1190000008833012)  
[基于docker的php跨平台开发环境](https://github.com/xiabin/docker-php-dev)

本文由 [nine](https://www.hellonine.top/index.php/author/1/) 创作，采用
[知识共享署名4.0](https://creativecommons.org/licenses/by/4.0/) 国际许可协议进行许可  
本站文章除注明转载/出处外，均为本站原创或翻译，转载前请务必署名  
最后编辑时间为: Mar 21, 2018 at 04:50 pm

