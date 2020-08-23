# Memcached

##### mac memcached 安装使用

###### 安装

~~~shell
brew install memcached
~~~

######使用brew 安装好memcached 可以使用如下方式启动start、停止stop、重启restart

第一种方式

~~~shell
brew services start memcached
~~~

第二种方式

~~~shell
/usr/local/bin/memcached -u memcache -m 1024 -p 11222 start
~~~

##### linux memcached 安装使用

安装

~~~shell
sudo apt install memcached
~~~

启动

第一种方式

~~~shell
service memcached start
~~~

第二种方式

~~~shell
/usr/bin/memcached -u memcache -m 1024 -p 11222 start
~~~

##### 参数选项

- `-d`：这个参数是让`memcached`在后台运行。
- `-m`：指定占用多少内存。以`M`为单位，默认为`64M`。
- `-p`：指定占用的端口。默认端口是`11211`。
- `-l`：别的机器可以通过哪个ip地址连接到我这台服务器。如果是通过`service memcached start`的方式，那么只能通过本机连接。如果想要让别的机器连接，就必须设置`-l 0.0.0.0`。

如果想要使用以上参数来指定一些配置信息，那么不能使用`service memcached start`，而应该使用`/usr/bin/memcached`的方式来运行。比如`/usr/bin/memcached -u memcache -m 1024 -p 11222 start`。

##### telnet 登陆 memcached

telnet 127.0.0.1[ip地址] 11211[端口]

##### 基本操作及语法

添加数据

~~~shell
set username 0[是否需要压缩] 60[超时时间] 4[字符长度]
rong
STORED
~~~

~~~shell
add username 0[是否需要压缩] 60[超时时间] 6[字符长度]
kurong
STORED
~~~

`set`和`add`的区别：`add`是只负责添加数据，不会去修改数据。如果添加的数据的`key`已经存在了，则添加失败，如果添加的`key`不存在，则添加成功。而`set`不同，如果`memcached`中不存在相同的`key`，则进行添加，如果存在，则替换。

获取数据

~~~shell
get username
VALUE username 0 4
rong
END
~~~

删除数据

delete 删除memcached中的一个键值对

~~~shell
delete username
DELETED
~~~

flush_all 

删除memcached中的所有键值对

~~~shell
flush_all
OK
~~~

incr

给memcached中的数字值添加数字

~~~shell
set age 0 120 2
18
STORED

incr age[key] 2[添加值]
20
~~~

decr

给memcached中的数字值减去数字

~~~shell
set age 0 120 2
18
STORED
decr age[key] 6[添加值]
12
~~~

### python 操作memcached

安装：`python-memcached`：`pip install python-memcached`

~~~python
import memcache

# 连接之前保证memcache服务已经启动
mc = memcache.Client(["127.0.0.1:11211"], debug=True)  # 列表中添加memcache服务器的IP以及端口， debug=True以便查看错误信息

# 设置一个值
mc.set("username", "Rong", time=120)

# 一次设置多个值
mc.set_multi({"email": "123@qq.com", "phone": "13145203487"}, time=120)

# 获取值
id = mc.get("id")
print(id)

# 删除
mc.delete("username")

# 自增
mc.incr("age", delta=10)  # delta 是增加的数值，如果没有定义，那么默认增加1

# 自减
mc.decr("age", delta=10)  # delta 是减少的数值，如果没有定义，那么默认减少1

~~~

### memcached安全机制

`memcached`的操作不需要任何用户名和密码，只需要知道`memcached`服务器的ip地址和端口号即可。因此`memcached`使用的时候尤其要注意他的安全性。这里提供两种安全的解决方案。分别来进行讲解：

1. 使用`-l`参数设置为只有本地可以连接：这种方式，就只能通过本机才能连接，别的机器都不能访问，可以达到最好的安全性。
2. 使用防火墙，关闭`11211`端口，外面也不能访问。

```shell
  ufw enable # 开启防火墙
  ufw disable # 关闭防火墙
  ufw default deny # 防火墙以禁止的方式打开，默认是关闭那些没有开启的端口
  ufw deny 端口号 # 关闭某个端口
  ufw allow 端口号 # 开启某个端口
```

### Django中使用memcached

~~~python
# 缓存

# 更改 Django memcached 默认的 key值设置规则
def KEY_FUNCTION(key, key_prefix, version):
    return 'django:' + key


CACHES = {
    'default': {
        # memcached
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_FUNCTION': lambda key, key_prefix, version: 'django:' + key
        # 'KEY_FUNCTION': KEY_FUNCTION,
    }
}

'''
Memcached 的一个出色功能是它能够在多个服务器上共享缓存。这意味着您可以在多台计算机上运行 Memcached 守护程序，
程序会视这组计算机为单个缓存，而无需在每台机器上复制缓存值。要使用此功能，需要在 LOCATION 中包含所有服务器的地址，
可以是分号或者逗号分隔的字符串，也可以是一个列表。

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            '172.19.26.240:11211',
            '172.19.26.242:11211',
        ]
    }
}

在这个示例中，缓存通过端口 11211 的 IP 地址 172.19.26.240 、 172.19.26.242 运行的 Memcached 实例共享：
'''
~~~

app7/views.py

~~~python
from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse
from django.core.cache import cache


def memcached1(request):
    cache.set("username", "ku_rong", 120)  # key value timeout
    username = cache.get("username")
    return HttpResponse("username: %s" % username)

~~~

