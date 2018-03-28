## 前言

最近写了两个小脚本，一个应用于[Mysql](https://github.com/nineyang/fillDataForMysql)的自动填充测试数据，另外一个是[bash](https://github.com/nineyang/clearForLog)写的定期删除日志文件，两个脚本如何使用，在`GitHub`上面都有所说明，这里不再赘述，这里主要是想聊一下`Mysql`的`存储过程`以及自动填充测试数据。  
为什么要写一个自动填充测试数据的脚本？  
网上其实也有一些简单的给`Mysql`填充数据的博客，但是大多数都是针对于特定的表的特定数据来实现，写的过于简单，实用性不强，而这个脚本可以根据我们提供表的字段，来自动识别我们的字段并填充进入对应的内容，常用的结构都能够满足，当然还有进一步完善的空间。

## 存储过程

`Mysql`的存储过程可以帮助我们实现一些较为复杂的业务逻辑，就像我们在`PHP`或者其他语言中所写的逻辑一样，在`Mysql`中也同样可以执行，比如我们要循环写入1000行数据。  
不过虽然`Mysql`可以实现，但是我们更希望把业务逻辑建立在我们的业务语言上面，而`Mysql`则专注于处理数据的`CURD`，其主要原因在于我们今后在修改或者要查找到这块的业务逻辑时，会相对麻烦一些。  
因此，我更倾向于`Mysql`可以用来做一些与我们的业务逻辑无关，而又需要用到语言的逻辑性的项目，比如我在前面提到的自动填充数据。

### 形式

    
    
    delimiter $$
    drop procedure if exists test $$
    create procedure test()
    begin 
    -- do something
    end $$
    delimiter ;

这是一个自动识别表结构并填充数据的脚本，在第一行使用了`delimiter
$$`用作分隔符，因为接下来的脚本里面很多地方会使用到`;`，所以为防止过早的识别结束，暂时修改了`Mysql`默认的分隔符。  
此外，前面有`begin`和`end`包裹，用于识别开始和结束。  
暂时先不讲逻辑怎么实现的(其实逻辑也非常简单)，我们先来了解一下`Mysql`的存储过程的几个部分。  
注:通过`show create procedure your_procedure_name`可以查看创建的存储过程的代码内容。

### 变量

`Mysql`的变量分成三种:全局变量，用户变量，局部变量。

  * 局部变量

局部变量存在于我们的存储过程中，在外面无法访问:

    
    
    delimiter $$
    drop procedure if exists test $$
    create procedure test()
    begin 
        declare myName varchar(8) default 'seven';
        set myName = 'nine';
        select myName;
    end $$
    delimiter ;
    call test();

结果输出`nine`，因为在用户变量中需要`@`来声明，所以此时在外面无法使用`select myName`，否则报错。

  * 用户变量

用户变量存在于全局，但是有效期仅限于`会话`期(所以也可以叫做会话变量)，即我们下次打开`Mysql`时，变量就会消失:

    
    
    delimiter $$
    drop procedure if exists test $$
    create procedure test()
    begin 
        set @myName = 'nine';
    end $$
    delimiter ;
    call test();
    select @myName ;

输出`nine`。

当然，赋值的形式是多样的，我们也可以结合查询语句来赋值:

    
    
    select name, age from user limit 1 into @myName , @myAge;
    select @myName , @myAge;

这个时候赋值的内容就是我们表中的数据，这里需要注意的是一一对应关系，切不可一对多或者多对一。

在某些时候，我们可能需要对查询的次数进行记录，其实这个时候我们可以完全使用变量来帮我们实现:

    
    
    set @selectNum = 0;
    select * , @selectNum := @selectNum + 1 from user limit 1;

这个时候`@selectNum`的结果为2。

  * 全局变量

全局变量是设置在系统中的配置，我们可以通过`show global variables`来查看，也可以通过`set global
oneofvariable=value`来设置我们 **已经存在**
的配置，这里我特意给已经存在这几个字眼加粗，因为我在网上看到有博文说可以设置自定义的全局变量，但是我尝试了之后发现报错了，我用版本`5.5`和`5.7`都尝试过了，提示这个变量不存在。

### 参数

参数分成`IN`，`OUT`以及`INOUT`三种情况:  
其实从其字面上我们也能猜出他们的不同效果:`IN`是不会影响外面设置的结果(IN是默认方式)，`OUT`和`INOUT`是会影响到的，同时`INOUT`两边是相互影响的，我们还是以上面的`test`为例:

  * in

    
    
    set @num = 1;
    delimiter $$
    drop procedure if exists test $$
    create procedure test(num int)
    begin 
        set num = 2;    
    end $$
    delimiter ;
    call test(@num);
    select @num;

结果为1。

  * out

    
    
    set @num = 1;
    delimiter $$
    drop procedure if exists test $$
    create procedure test(OUT num int)
    begin 
        set num = 2;    
    end $$
    delimiter ;
    call test(@num);
    select @num;

结果为2。

### 语句块

[这篇文章](http://www.jianshu.com/p/7b2d74701ccd)关于语句块已经阐述的足够详细，这里不再赘述。

## 实现

代码:

    
    
    delimiter $$
    drop procedure if exists fillTable $$
    create procedure fillTable(in num int  , in tbName varchar(16))
    begin 
    -- 获取当前数据库
        select (@dbName:=database());
        set @tbName = tbName;
    -- 获取表的字段总数
        set @currSql = "select count(1) from information_schema.COLUMNS where table_name = ? and table_schema = ? into @columnSum";
        prepare stmt from @currSql;
        execute stmt using @tbName , @dbName;
        deallocate prepare stmt;
        
        set @currNum = 0;
        
    -- 这里设置随机的字符串
        set @chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
        
        while @currNum < num do 
            -- 这里设置sql后面拼接
            set @insertSql = concat("insert into " , @tbName , " values ( ");
            set @columnNum = 1;
            while @columnNum <= @columnSum do
                set @value := '';
                set @currSql = "select (@column := COLUMN_NAME) , (@length := CHARACTER_MAXIMUM_LENGTH) , (@key := COLUMN_KEY) , (@type := DATA_TYPE) from information_schema.COLUMNS where table_name = ? and table_schema = ? limit ?";
                prepare stmt from @currSql;
                execute stmt using @tbName , @dbName , @columnNum;
                deallocate prepare stmt;
                
        -- 根据类型来填充数据
                if right(@type , 3) = 'int' then
                    if @type = 'int' then
                        set @value = 'default';
                    else 
                        set @value = floor(rand() * 100);
                    end if;
                
                elseif right(@type , 4) = 'char' then
                    set @counter = 0;
                    while @counter < @length do    
                        set @value = concat(@value,substr(@chars,ceil(rand()*(length(@chars)-1)),1));  
                        set @counter = @counter + 1;
                    end while;
                    
                    set @value = concat("'" , @value , "'");
                    
                elseif @type = 'blob' or right(@type , 4) = 'text' then
                    set @counter = 0;
                     while @counter < 100 do    
                        set @value = concat(@value,substr(@chars,ceil(rand()*(length(@chars)-1)),1));  
                        set @counter = @counter + 1;
                    end while;
                    
                    set @value = concat("'" , @value , "'");
                    
                elseif @type = 'float' or @type = 'decimal' then
                    set @value = round(rand() , 2);
                else 
                    set @value = 'nine';
                end if;
                
        -- 判断这个数是否是最后一个
                if @columnNum = @columnSum then
                    set @insertSql = concat(@insertSql , @value , ' )');
                else 
                    set @insertSql = concat(@insertSql , @value , ' , ');
                end if;
                
                set @columnNum = @columnNum + 1;
            end while;
        -- 执行
            prepare stmt from @insertSql;
            execute stmt;
            deallocate prepare stmt;
            
            set @currNum = @currNum + 1;
        
        end while;
        
    end $$
    delimiter ;

其实实现这个功能的逻辑非常简单，再各个步骤里面也附上了步骤，主要是利用了系统的`information_schema.COLUMNS`表来获取我们需要的一些基本信息，主要结构如下图所示:  
![81b12bcd-e426-47e7-b7ab-1f96e034826a.png](https://github.com/nineyang/blog-tool/blob/master/images/81b12bcd-e426-47e7-b7ab-1f96e034826a.png)

## 参考

[mysql存储过程详细教程](http://www.jianshu.com/p/7b2d74701ccd)

本文由 [nine](https://www.hellonine.top/index.php/author/1/) 创作，采用
[知识共享署名4.0](https://creativecommons.org/licenses/by/4.0/) 国际许可协议进行许可  
本站文章除注明转载/出处外，均为本站原创或翻译，转载前请务必署名  
最后编辑时间为: Mar 21, 2018 at 04:49 pm

