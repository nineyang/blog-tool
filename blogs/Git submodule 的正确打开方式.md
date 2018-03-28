## 前言

通常，我们在项目中经常会有许多公用的代码块，如果直接大批量的复制，显得不便于管理，而`Git`有一个[子模块](https://git-
scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E5%AD%90%E6%A8%A1%E5%9D%97)给我们提供了极大的便利。  
我也在`GitHub`上面建立了两个简单的`demo`方便详细了解。  
[父级](https://github.com/nineyang/parent)  
[子级](https://github.com/nineyang/submodule)

## 使用

### 新建子模块

新建子模块需要分成两部分，一方面是创建子模块的人的流程，另一方面是团队其他使用子模块的人。

#### 初始化子模块

我们可以通过

    
    
    git submodule add your_submodule_url

来新建一个我们所需要的子模块，正如下图所示:

![762d9921-ff8a-4031-b2bf-32d4696f511b.png](https://github.com/nineyang/blog-
tool/blob/master/images/762d9921-ff8a-4031-b2bf-32d4696f511b.png)

不过这里需要阐明的是，当我们在父级新建了一个子模块时， **父级并不包含子模块的代码**
，而是有一个7位数的字符串来指向子模块所对应的位置，其实通过对比这串字符串和我们子模块的提交记录，我们可以很清晰的得到一个结论：这个字符串就是代表的子模块的提交记录。

![企业微信截图_0e78d5d4-460a-49f0-8c23-467636101cd8.png](https://github.com/nineyang/blog-
tool/blob/master/images/企业微信截图_0e78d5d4-460a-49f0-8c23-467636101cd8.png)

![企业微信截图_75b44176-abf2-49a7-a429-2bcd01dbaf49.png](https://github.com/nineyang/blog-
tool/blob/master/images/企业微信截图_75b44176-abf2-49a7-a429-2bcd01dbaf49.png)

#### 下拉子模块

当团队其他人使用有包含子模块的项目时，我们又可以分成两种情况，一种是还没有`clone`过项目，另外一种是已经有了本地的项目。  
对于第一种情况，我们可以直接使用:

    
    
    git clone your_project_url --recursive

这个指令会在初始化父类项目的同时，也会把子模块的代码递归拉取到你的本地。

此外，当你的项目已经存在于本地了，而其他人提交了一个新的子模块，那么你可以使用:

    
    
    git submodule init

加上

    
    
    git submodule update

来拉取一个新的子模块，需要注意的是，执行`git submodule update`的时候才会真正拉取你的子模块代码。

![企业微信截图_8dc1f6d0-7eb7-445b-81e1-ba6997b43938.png](https://github.com/nineyang/blog-
tool/blob/master/images/企业微信截图_8dc1f6d0-7eb7-445b-81e1-ba6997b43938.png)

### 更新子模块

正如我们在创建子模块中所述，其实我们在更新子模块的时候也需要分成两个部分去阐述，一部分是`push`的人，一部分是`pull`的人。

#### push

刚才我们已经在本地新建了一个`parent_2`的项目，现在我们需要在这个本地仓库中更新子模块再提交到线上仓库中，我们需要做的是先在子模块中切到`master`或者一个新的分支，提交上去之后再回到父类更新子模块的指针。

![企业微信截图_2da4f577-6bc1-4e77-81de-f0e22c06b429.png](https://github.com/nineyang/blog-
tool/blob/master/images/企业微信截图_2da4f577-6bc1-4e77-81de-f0e22c06b429.png)

![企业微信截图_408c3fbb-7dc9-47e8-b0c4-f8399f992938.png](https://github.com/nineyang/blog-
tool/blob/master/images/企业微信截图_408c3fbb-7dc9-47e8-b0c4-f8399f992938.png)

正如上图所示，我们更新了父类对应子模块的指针，然后我们把本地的父类推送到线上去。

#### pull

当其他人`pull`线上的父类之后，如果有人更新了对应的指针，那么会有这样的一个提示:

![企业微信截图_8212f57d-75b6-42e7-ab33-bf606ee76789.png](https://github.com/nineyang/blog-
tool/blob/master/images/企业微信截图_8212f57d-75b6-42e7-ab33-bf606ee76789.png)

这个时候我们需要做的是什么呢？聪明的朋友可能已经想到，联系到我们在上面所说， **父级记录的是子模块的指针** 。所以此时我们执行:

    
    
    git submodule update

即可完成我们的更新。

![企业微信截图_70757ae4-abcd-48ef-
becd-a678cd74b8b5.png](https://github.com/nineyang/blog-
tool/blob/master/images/企业微信截图_70757ae4-abcd-48ef-becd-a678cd74b8b5.png)

本文由 [nine](https://www.hellonine.top/index.php/author/1/) 创作，采用
[知识共享署名4.0](https://creativecommons.org/licenses/by/4.0/) 国际许可协议进行许可  
本站文章除注明转载/出处外，均为本站原创或翻译，转载前请务必署名  
最后编辑时间为: Mar 21, 2018 at 04:43 pm

