## 前言

这段时间一直在研究`Laravel`的源码，使用到了`PHP`的很多新的概念，比如`Closure`，比如`数组式访问`，于是正好研究了一下`PHP`的几个预定义接口。

### Closure(闭包)

代表一个匿名函数的类，我们所用到的匿名函数，都是`Closure`的一个实例，主要方法有:`bind` ，
`bindTo`，其实之前在[Laravel](http://www.hellonine.top/index.php/archives/6/#directory073928889396108333)第一篇的时候，是有做过一个简单的介绍的，通过阅读`Laravel`的源代码，我们发现在很多地方都是有使用到`Closure`的概念的。  
`Closure`主要有两个方法，但是殊途同归，目的都是为了把某个匿名函数绑定到某个类上面以便执行:

  1. `bindTo`  
他的参数有两个

    
    
    public Closure Closure::bindTo ( object $newthis [, mixed $newscope = 'static' ] )

`$newthis`是指需要绑定的对象，`newscope`是设置类的作用域。  
第一个参数可以设置`null`或者是一个对象的实例，主要取决于我们要在函数中操作的属性和方法是否是静态的，如果是静态的，那么第一个参数必须设置`null`，且第二个参数要设置一个类作用域:

  * example_1:

    
    
    <?php
    class A{
        private static $name = 'nine';
    }
    
    $callback = function(){
        self::$name = 'seven';
        echo self::$name;
    };
    
    $func = $callback->bindTo(null , A::class);
    $func();

输出`seven`

  * example_2:

    
    
    class A{
        private $name = 'nine';
    }
    
    $callback = function(){
        $this->name = 'seven';
        echo $this->name;
    };
    
    $a = new A;
    $func = $callback->bindTo($a);
    $func();

报错:`Cannot access private property A::$name`

  * example_3:

    
    
    <?php
    class A{
        private $name = 'nine';
    }
    
    $callback = function(){
        $this->name = 'seven';
        echo $this->name;
    };
    
    $a = new A;
    $func = $callback->bindTo($a , A::class);
    $func();

输出`seven`.

  1. 静态方法`bind`  
他的参数有两个

    
    
    public static Closure Closure::bind ( Closure $closure , object $newthis [, mixed $newscope = 'static' ] )

`$closure`是指我们需要绑定的匿名函数，`$newthis`是指需要绑定的对象，`newscope`是设置类的作用域.  
`bind`其实和`bindTo`用法一致，只不过在于使用的方式不一样而已:

  * example:

    
    
    <?php
    class A{
        private $name = 'nine';
    }
    
    $a = new A;
    $func = Closure::bind(function(){
        $this->name = 'seven';
        echo $this->name;
    } , $a , A::class);
    $func();

### ArrayAccess(数组式访问)

在`Laravel`中，经常会看到`$this['app']`这样的用法，但是我们知道，`$this`是一个对象，这种形式就好像对象用了数组的方式，具体是怎么实现的呢，主要就是当前类实现了接口`ArrayAccess`，不过需要注意的是，`ArrayAccess`的实现需要四个方法:

    
    
    <?php
    class A implements ArrayAccess{
        public $name;
        public function __construct(){
            $this->name = 'nine';
        }
        public function offsetSet($offset, $value) {
            $this->$offset = $value;
        }
        public function offsetExists($offset) {
            return isset($this->$offset);
        }
        public function offsetUnset($offset) {
            unset($this->$offset);
        }
        public function offsetGet($offset) {
            return $this->$offset;
        }
    }
    $a = new A;
    // 这里会调用offsetGet
    echo $a['name'];
    // 这里会调用offsetSet
    $a['name'] = 'seven';
    echo $a['name'];
    // 这里会调用offsetExists
    var_dump(isset($a['name']));
    // 这里会调用offsetUnset
    unset($a['name']);
    var_dump(isset($a['name']));

输出:nine seven bool(true) bool(false)  
`ArrayAccess`的优点就是可以让我们可以使用数组式的调用类的属性，但是我还是觉得`$a->name`的形式更有逼格啊......

### Traversable(遍历)

这个比较简单，主要是用来判断一个类是否可以用`foreach`来遍历:

    
    
    var_dump(new stdClass instanceof Traversable);

输出`false`.

### Iterator(迭代器)

迭代器`Iterator`的主要功能就是遍历一个对象，虽然我们通过直接遍历一个对象也可以获取他的属性，但是你要知道，能获取的只是`public`的属性，而他的`private`或者`protected`是无法获取的，所以他的主要功能在于：在我们不了解对象的结构的情况下，帮助我们去获取他的所有的属性内容(包括私有)。

  * example_1:

    
    
    <?php
    class Test implements Iterator {
        private $position = 0;
        private $array = ['nine' , 'seven'];
    
    // 该方法主要用户项目初始化
        function rewind() {
            echo __METHOD__ . PHP_EOL;
            $this->position = 0;
        }
    //用来获取当前游标所对应的值
        function current() {
            echo __METHOD__ . PHP_EOL;
            return $this->array[$this->position];
        }
    //获取当前游标
        function key() {
            echo __METHOD__ . PHP_EOL;
            return $this->position;
        }
    //下移游标
        function next() {
            echo __METHOD__ . PHP_EOL;
            ++$this->position;
        }
    //判断是否还有值
        function valid() {
            echo __METHOD__ . PHP_EOL;
            return isset($this->array[$this->position]);
        }
    }
    
    $obj = new Test;
    
    $obj->rewind();
    
    while($obj->valid()){
        echo $obj->current() . PHP_EOL;
        $obj->next();
    }
    //当然，这里其实我们也可以通过foreach的形式来获取，这里就不举例说明了。

输出:

    
    
    Test::rewind
    Test::valid
    Test::current
    nine
    Test::next
    Test::valid
    Test::current
    seven
    Test::next
    Test::valid

其执行顺序是:`rewind->volid->current->key->next->volid->current->key...`。  
当然，既然可以正序，那么我们也可以轻而易举的把结果倒序来遍历，把`next`里面的逻辑改成`--$this->position`即可，虽然说`PHP`的数组功能已经相当强大了，但是`Iterator`则会更加灵活和定制化。

### IteratorAggregate(聚合式迭代器)

聚合式迭代器`IteratorAggregate`和迭代器的功能，这个接口只需要实现一个方法即可`getIterator`：

  * example_1:

    
    
    <?php
    class Test implements IteratorAggregate {
        protected $name = 'nine';
        public $age = 18;
    
        public function getIterator(){
            return new ArrayIterator($this);
        }
    }
    
    $obj = (new Test)->getIterator();
    $obj->rewind();
    while($obj->valid()){
        echo $obj->current() . PHP_EOL;
        $obj->next();
    }

输出:18.

  * example_2:

    
    
    <?php
    class Test implements IteratorAggregate {
        private $_data;
    
        public function __construct(){
            $this->_data = ['nine' , 'seven'];
        }
    
        public function getIterator(){
            return new ArrayIterator($this->_data);
        }
    }
    
    $obj = (new Test)->getIterator();
    $obj->rewind();
    while($obj->valid()){
        echo $obj->current() . PHP_EOL;
        $obj->next();
    }

输出:nine seven。  
由此可见，最终内容取决于我们给`new ArrayIterator`注入的数组。当然，这里也可以用`foreach`来遍历，结果一样。  
其实我们去观察`ArrayIterator`的源码的时候可以发现，他继承自`Iterator`，实现了他的几个方法，所以当我们在遍历通过他返回的实例时，实际上就是在调用`rewind->valid...`这几个方法。

### Serializable(序列化)

序列化也是一个相对比较简单的接口，主要实现两个方法`serialize`以及`unserialize`即可:

    
    
    <?php
    class MyClass implements Serializable {
        private $data;
        
        public function __construct($data) {
            $this->data = $data;
        }
        
        public function serialize() {
            return serialize($this->data);
        }
        
        public function unserialize($data) {
            $this->data = unserialize($data);
        }
    }
    $a = new MyClass('hello , world');
    var_dump($a->serialize());

输出`string(21) "s:13:"hello , world";"`，这样，我们就可以在序列化的过程中做一些其他的逻辑操作了。

### Generator(生成器)

`Generator`实现了`Iterator`，但是他无法被继承，同时也生成实例。  
既然实现了`Iterator`，所以正如上文所介绍，他也就有了和`Iterator`相同的功能:`rewind->valid->current->key->next...`，`Generator`的语法主要来自于关键字`yield`。`yield`就好比一次循环的中转站，记录本次的活动轨迹，返回一个`Generator`的实例。  
`Generator`的优点在于，当我们要使用到大数据的遍历，或者说大文件的读写，而我们的内存不够的情况下，能够极大的减少我们对于内存的消耗，因为传统的遍历会返回所有的数据，这个数据存在内存上，而`yield`只会返回当前的值，不过当我们在使用`yield`时，其实其中会有一个处理`记忆体`的过程，所以实际上这是一个`用时间换空间`的办法。

  * example_1:

    
    
    $start_time = microtime(true);
    function xrange($num = 100000){
        for($i = 0 ; $i < $num ; ++ $i){
            yield $i;
        }
    }
    
    $generator = xrange();
    foreach ($generator as $key => $value) {
        echo $key . '=' . $value . PHP_EOL;
    }
    echo 'memory:' . memory_get_usage() . ' time:' . (microtime(true) - $start_time) . PHP_EOL;

输出:`memory:229056 time:0.25725412368774`.

    
    
    $start_time = microtime(true);
    function xrange2($num = 100000){
        $arr = [];
        for ($i=0; $i <$num ; ++$i) { 
            array_push($arr , $i);
        }
        return $arr;
    }
    
    $arr = xrange2();
    foreach ($arr as $key => $value) {
        # code...
    }
    echo 'memory:' . memory_get_usage() . ' time:' . (microtime(true) - $start_time);

输出:`memory:14877528 time:0.039144992828369`。

本文由 [nine](https://www.hellonine.top/index.php/author/1/) 创作，采用
[知识共享署名4.0](https://creativecommons.org/licenses/by/4.0/) 国际许可协议进行许可  
本站文章除注明转载/出处外，均为本站原创或翻译，转载前请务必署名  
最后编辑时间为: Jun 12, 2017 at 05:49 pm

