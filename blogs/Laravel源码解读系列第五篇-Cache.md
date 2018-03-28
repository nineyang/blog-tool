## 前言

在我们的项目中，或多或少都会用到一些缓存机制。`Laravel`封装了一个非常方便调用的`Cache`的`Facades`，方便我们对缓存进行统一调度。

## 过程

### Facade

首先，我们可以在`config/app.php`中看到如下的相关代码(为方便查看，我省略了其他部分):

    
    
    'providers' => [
    
            Illuminate\Cache\CacheServiceProvider::class,
    
        ],
    
        'aliases' => [
    
            'Cache' => Illuminate\Support\Facades\Cache::class,
            
        ],

当我们在执行`CacheServiceProvider`这个服务提供者的时候，我们可以看到他有一个`register`方法:

    
    
    public function register()
        {
            $this->app->singleton('cache', function ($app) {
                return new CacheManager($app);
            });
    
            $this->app->singleton('cache.store', function ($app) {
                return $app['cache']->driver();
            });
    
            $this->app->singleton('memcached.connector', function () {
                return new MemcachedConnector;
            });
        }

在这个方法中帮我们实现并绑定了一个`cache`，返回`CacheManager`的一个单例。因此，当我们在下面调用`Cache`的`Facade`的时候，就帮我们返回了这个`CacheManager`的实例:

    
    
    protected static function getFacadeAccessor()
        {
            return 'cache';
        }

如果这个过程不清楚怎么实现的可以查看我之前的一篇[Facades](https://www.hellonine.top/index.php/archives/29/#directory096620026240848318).

### CacheManager

使用过`Cache`机制的朋友应该知道，我们是可以通过`Cache::put`等来执行我们的缓存的，但是我们进入到`CacheManager`，其实并没有这样的一个方法。不过，正如我在前一篇[Laravel源码解读系列第四篇-
Auth机制](https://www.hellonine.top/index.php/archives/68/)中所述，当调用一个不存在的静态方法时，最终都会执行`Facade.php`的`__callStatic`方法:

    
    
    public static function __callStatic($method, $args)
        {
            //        当继承自Facade的对象中，如果调用了一个不存在的静态方法，那么就会执行这个方法
            $instance = static::getFacadeRoot();
            //        返回一个之前在app中绑定或者注入的对象
    
            if (! $instance) {
                throw new RuntimeException('A facade root has not been set.');
            }
    
    //        然后调用该方法进行执行
            return $instance->$method(...$args);
        }

再结合`CacheManager`本身的`__call`:

    
    
    public function __call($method, $parameters)
        {
            return $this->store()->$method(...$parameters);
        }

便完成了我们的调度。

至于其他的一些方法，就是简单的调用配置获取当前应该使用的缓存机制了，有兴趣的朋友可以自行查阅:

    
    
    public function store($name = null)
        {
            $name = $name ?: $this->getDefaultDriver();
    
            return $this->stores[$name] = $this->get($name);
        }
    
        /**
         * Get a cache driver instance.
         *
         * @param  string  $driver
         * @return mixed
         */
        public function driver($driver = null)
        {
            return $this->store($driver);
        }
    
        /**
         * Attempt to get the store from the local cache.
         *
         * @param  string  $name
         * @return \Illuminate\Contracts\Cache\Repository
         */
        protected function get($name)
        {
            return isset($this->stores[$name]) ? $this->stores[$name] : $this->resolve($name);
        }
    
        /**
         * Resolve the given store.
         *
         * @param  string  $name
         * @return \Illuminate\Contracts\Cache\Repository
         *
         * @throws \InvalidArgumentException
         */
        protected function resolve($name)
        {
            $config = $this->getConfig($name);
    
            if (is_null($config)) {
                throw new InvalidArgumentException("Cache store [{$name}] is not defined.");
            }
    
            if (isset($this->customCreators[$config['driver']])) {
                return $this->callCustomCreator($config);
            } else {
                $driverMethod = 'create'.ucfirst($config['driver']).'Driver';
    
                if (method_exists($this, $driverMethod)) {
                    return $this->{$driverMethod}($config);
                } else {
                    throw new InvalidArgumentException("Driver [{$config['driver']}] is not supported.");
                }
            }
        }

 **文章首发地址：[我的博客](https://www.hellonine.top)**

本文由 [nine](https://www.hellonine.top/index.php/author/1/) 创作，采用
[知识共享署名4.0](https://creativecommons.org/licenses/by/4.0/) 国际许可协议进行许可  
本站文章除注明转载/出处外，均为本站原创或翻译，转载前请务必署名  
最后编辑时间为: Mar 21, 2018 at 04:43 pm

