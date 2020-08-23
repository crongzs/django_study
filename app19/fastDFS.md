# FastDFS

fastdfs：提供文件上传下载的服务，实现海量存储，存储扩展方便，避免存储内容相同的文件

tracker server作用：负载均衡和调度，追踪或者调度服务器

storage server作用：文件存储，客户端上传的文件最终存储在storage服务器上。

Storage server 组内是互为备份的，组之间存储的文件是不一样的

storage server 会对文件的内容取一个hash值作为文件的名字保存

### 文件上传下载的流程：

client上传下载的时候需要取请求tracker server，tracker server 查询可用的storage server 向client返回可用的storage server的ip和端口号，client直接访问这个storage server 的ip和端口号 将文件传给这个storage server，storage server将文件存储后向client返回一个file_id。

下载时，client请求tracker server ，tracker server找到这个文件所在的storage server向cliemt返回它的ip和port，client直接访问这个storage server获取文件。

### Mac安装FastDFS

* 安装xcode-select

  ~~~bash
  # 终端输入然后安装
  xcode-select --install
  ~~~

* 下载安装依赖包

  [libfastcommon](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fhappyfish100%2Flibfastcommon.git)

  [FastDFS](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Fhappyfish100%2Ffastdfs.git)

  ~~~bash
  ku-rongdeMacBook-Pro:libfastcommon-master ku_rong$ pwd
  /Users/ku_rong/Downloads/libfastcommon-master
  ku-rongdeMacBook-Pro:libfastcommon-master ku_rong$ ./make.sh 
  ku-rongdeMacBook-Pro:libfastcommon-master ku_rong$ sudo ./make.sh install
  ~~~

  ~~~bash
  ku-rongdeMacBook-Pro:fastdfs-master ku_rong$ pwd
  /Users/ku_rong/Downloads/fastdfs-master
  ku-rongdeMacBook-Pro:fastdfs-master ku_rong$ ./make.sh 
  ku-rongdeMacBook-Pro:fastdfs-master ku_rong$ sudo ./make.sh install
  ~~~

* 配置跟踪服务器tracker server

  1.拷贝tracker配置文件

  ~~~bash
  sudo cp /etc/fdfs/tracker.conf.sample /etc/fdfs/tracker.conf
  ~~~

  2.在`/home/python/`目录中创建目录 `fastdfs/tracker`

  ~~~bash
  mkdir -p /home/python/fastdfs/tracker/
  ~~~

  3.编辑`/etc/fdfs/tracker.conf`配置文件

  ~~~bash
  sudo vim /etc/fdfs/tracker.conf
  ~~~

  4.修改其中的base_path

  ~~~bash
   base_path=/home/python/fastdfs/tracker
  ~~~

  

* 配置存储服务器storage server









## Mac系统下实现 FastDFS 文件的上传 与下载

> 在 Mac 下通过 Docker + FastDFS + Nginx 是不能够实现的
>  原因在于：虽然Docker中有network host模式，但是Docker是通过虚拟化的Linxu主机网络作为Host网络，所以无法使用Mac主机的网络，因此Docker中 FastDFS 无法链接到Mac 找不到storage下的资源。
>  解决办法：本机编译FastDFS实现文件的上传与下载。

#### 准备

> 1. 关闭mac的系统保护：Mac对关键目录进行了保护（例如：/bin, /usr/bin等）
>     `1. 重启系统，重启的过程中按住Command+R进入Recovery模式；`
>     `2. 从菜单中选择“终端”或“Terminal”进入命令行模式；`
>     `3. 输入命令csrutil disable关闭保护模式，然后输入reboot重启系统即可。`
> 2. 下载 libfastcommon，文件格式：zip,通过github下载
> 3. 下载 fastdfs，文件格式：zip,通过github下载
> 4. home 路径下的/Python/fastdfs/tracker 需要创建 **`sudo mkdir -p /Python/fastdfs/tracker`**
> 5. 查询本机ip地址  **`ifconfig`**

**注意：** **第一个坑：** **`mkdir: test: Operation not supported`**
 **解决:** * 执行sudo vim /etc/auto_master，注释掉/home选项。 **`允许`** --> **重启电脑**

![img](https:////upload-images.jianshu.io/upload_images/911921-b02517a4177ccf51.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

image.png


**参考链接：**[mkdir: test: Operation not supported](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.jiweichengzhu.com%2Farticle%2F7d5f8e54182d45c5b04655cd5e83dc0c)

image.png

## FastDFS 文件上传

##### 配置跟踪服务器 Tracker

> 1. 准备：libfastcommon-master.zip/fastdfs-master.zip 解压缩到 桌面；文件夹名称为libfastcommon-master/fastdfs-master
>
> 2. 移动文件夹到 
>
>    ```
>    /usr/local
>    ```
>
>    ；
>
>    1. `cd Desktop`
>    2. `sudo mv libfastcommon-master /usr/local`
>    3. `sudo mv fastdfs-master /usr/local`
>
> 3. ```
>    cd /usr/local/libfastcommon-master
>    ```
>
>    1. `./make.sh`           # 编译
>    2. `./make.sh install`    # 安装
>
> 4. 配置 跟踪服务器 tracker
>     `1. sudo cp /etc/fdfs/tracker.conf.sample /etc/fdfs/tracker.conf`
>     `2. 编辑配置文件`tracker.conf`
>     `3. `sudo vi /etc/fdfs/tracker.conf`
>     `4. 修改其中的bash_path`
>     `base_path=/home/Python/fastdfs/tracker`

##### 配置跟踪服务器 Storage

> 1. 拷贝storage配置文件
>     `sudo cp /etc/fdfs/storage.conf.sample /etc/fdfs/storage.conf`
> 2. 在/home/Python/fastdfs/ 目录下创建目录 **`storage`**
>     mkdir /home/Python/fastdfs/storage
> 3. 编辑配置文件`storage.conf`
> 4. 修改其中的 base_path, store_path0,tracker_server
>     `base_path=/home/Python/fastdfs/storage`
>     `store_path0=/home/Python/fastdfs/storage`
>     `tracker_server=Mac的IP地址:22122`
> 5. 启动 tracker & storage
>     `sudo /usr/bin/fdfs_trackerd /etc/fdfs/tracker.conf restart`
>     `sudo /usr/bin/fdfs_storaged /etc/fdfs/storage.conf restart`

> 1. 检查是否启动成功
>     `ps aux | grep fdfs`
>
> > ```
> > root 1699 0.0 0.4 4366520 66828 ?? S 9:21下午 0:02.77 /usr/bin/fdfs_storaged /etc/fdfs/storage.conf restart`
> >  `root 1694 0.0 0.0 4314496 992 ?? S 9:20下午 0:02.71 /usr/bin/fdfs_trackerd /etc/fdfs/tracker.conf restart`
> >  `lofoer 4055 0.0 0.0 4268056 812 s001 S+ 1:09上午 0:00.00 grep fdfs
> > ```

**注意：**
 **第二个坑：** **`root 用户`** **暂时不影响，下面会说到**

1. 上述显示，则表示启动成功

#### 测试上传

##### 配置client文件

> 1. 拷贝client配置文件
>     `sudo cp /etc/fdfs/client.confi.sample /etc/fdfs/client.conf`

> 1. 修改client配置文件
>     `sudo vi /etc/fdfs/client.conf`

> 1. 修改内容
>     `base_path=/home/Python/fastdfs/tracker tracker_server=Mac的IP地址:22122`

> 1. 上传文件测试
>     `fdfs_upload_file /etc/fdfs/client.conf 要上传文件的路径`

**如果返回类似group1/M00/00/00/wKgCZl0OIFWAZOVMAABwSY4nz_Q55.jpeg的文件id则说明文件上传成功。**

> **查看文件：**
>  `cd /home/Python/fastdfs/storage/data/00/00wKgCZl0OIFWAZOVMAABwSY4nz_Q55.jpg`

**查找**



```shell
sudo find . -name 'wKgCZl0OIFWAZOVMAABwSY4nz_Q55.jpg'
```

#### FastDFS + Nginx 文件下载

##### 准备

1. 下载fastdfs-nginx-module-master.zip

2. 下载nginx-1.17.5.tar.gz

3. 分别解压缩到桌面，然后移动到 **`/usr/local`**

4. 在 /usr/local下创建一个 **nginx文件夹**

   

   ```shell
   cd /usr/loca/nginx-1.17.5
   
   ./configure \
   > --prefix=/usr/local/nginx\
   > --add-module=/usr/local/fastdfs-nginx-module-master/src
   ```

   **添加fastdfs-nginx模块**

5. 编译并安装
    **`make && make install`**

**注意：**
 **第三个坑：** **`这里会出现问题 make: \**\* No rule to make target build, needed by default. Stop.`**

**重要：**
 **因为缺少安装先决条件**

1. Command Line Tools
    所以装完系统后，不管用不用Xcode 都得安装上，其次要安装 Command Line Tools
2. GCC - GUN编译器集合
3. PCRE 库
4. zlib 库
5. OpenSSL库

使用Homebrew来进行安装

再尝试下：**`make && make install`**

##### 配置nginx

1. 修改 mod_fastdfs.conf 配置

   `sudo vi /usr/local/fastdfs-nginx-master/src/mod_fastdfs.conf`

   

   ```shell
   #======修改以下内容========
   base_path=/home/Python/fastdfs/storage  #保存日志的路径
   tracker_server=本地IP:22122  #track_server配置的服务端口
   url_have_group_name=true        #url中是否包含group名称
   store_path0=/home/Python/fastdfs/storage  #指定文件存储路径（必须和storage.conf配置相同）
   ```

2. 拷贝配置文件`/usr/local/fastdfs-nginx-master/src/mod_fastdfs.conf` **至** `/etc/fdfs/mod_fastdfs.conf`

   ![img](https:////upload-images.jianshu.io/upload_images/911921-260c20b0acdf9d8a.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

   image.png

   

1. http.conf & mime.types
    通过 sudo find . -name 'http.conf'找到 http.conf & mime.types 的全路径
    拷贝到 /etc/fdfs/http.conf ； /etc/fdfs/mime.types

   ![img](https:////upload-images.jianshu.io/upload_images/911921-f24bdf477c232ea6.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

   image.png

1. 编辑 nginx.conf 文件

   `sudo vi /usr/local/nginx/conf/nginx.conf`

   

   ```shell
   server {
               listen       8989;
               server_name  172.20.10.2;
               location /group1/M00/  { 
           root /home/Python/fastdfs/storage/data/;
                   ngx_fastdfs_module;
               }
               error_page   500 502 503 504  /50x.html;
               location = /50x.html {
               root   html;
               }
           }
   ```

   ![img](https:////upload-images.jianshu.io/upload_images/911921-1a94b660994c577f.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

   image.png

😍**注意：这里的root就是上文中的root用户**

##### 启动 Nginx

**1. 启动 nginx**
 `shell /usr/local/nginx/sbin/nginx`

**2. 查看是否启动**
 `shell ps aux | grep nginx`

**3. 查看nginx是否能够显示**

```cpp
**`http://172.20.10.2:8989`**
```

**4. 查看上传成功的文件**
 `http://172.20.10.2:8989/ group1/M00/00/00/CtM3BVnij5-AQyvAAAHc1z_-Xc4112.jpg`

**5. 使用lsof 来查看被占用的端口**

**`sudo lsof -i -n -P | grep 8989`**

**`sudo lsof -i -n -P | grep nginx`**

**6. 强制杀死进程**
 **`sudo kill -9 进程号`**

**注意：通过强制杀死进程可处理该问题**
 **`关于nginx启动失败 [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)`**



作者：我叫小灿灿
链接：https://www.jianshu.com/p/a4e6dbfd2a8a
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。