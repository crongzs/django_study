# XSS攻击

XSS（Cross Site Script）攻击又叫做跨站脚本攻击。他的原理是用户在使用具有`XSS`漏洞的网站的时候，向这个网站提交一些恶意的代码，当用户在访问这个网站的某个页面的时候，这个恶意的代码就会被执行，从而来破坏网页的结构，获取用户的隐私信息等。

## XSS攻击场景：

比如`A网站`有一个发布帖子的入口，如果用户在提交数据的时候，提交了一段`js`代码比如：`alert("hello world");`，然后`A网站`在渲染这个帖子的时候，直接把这个代码渲染了，那么这个代码就会执行，会在浏览器的窗口中弹出一个模态对话框来显示`hello world`！如果攻击者能成功的运行以上这么一段`js`代码，那他能做的事情就有很多很多了！

## XSS攻击防御：

1. 如果不需要显示一些富文本，那么在渲染用户提交的数据的时候，直接进行转义就可以了。在`Django`的模板中默认就是转义的。也可以把数据在存储到数据库之前，就转义再存储进去，这样以后在渲染的时候，即使不转义也不会有安全问题，示例代码如下：

   ```python
    from django.template.defaultfilters import escape
    from .models import Comment
    from django.http import HttpResponse
    def comment(request):
        content = request.POST.get("content")
        escaped_content = escape(content)
        Comment.objects.create(content=escaped_content)
        return HttpResponse('success')
   ```

2. 如果对于用户提交上来的数据包含了一些富文本（比如：给字体换色，字体加粗等），那么这时候我们在渲染的时候也要以富文本的形式进行渲染，也即需要使用`safe`过滤器将其标记为安全的，这样才能显示出富文本样式。但是这样又会存在一个问题，如果用户提交上来的数据存在攻击的代码呢，那将其标记为安全的肯定是有问题的。示例代码如下：

   ```python
    # views.py
    def index(request):
        message = "<span style='color:red;'>红色字体</span><script>alert('hello world');</script>";
        return render_template(request,'index.html',context={"message":message})
   ```

   ```html
    # index.html
   ```

   那么这时候该怎么办呢？这时候我们可以指定某些标签我们是需要的（比如：span标签），而某些标签我们是不需要的（比如：script）那么我们在服务器处理数据的时候，就可以将这些需要的标签保留下来，把那些不需要的标签进行转义，或者干脆移除掉，这样就可以解决我们的问题了。这个方法是可行的，包括很多线上网站也是这样做的，在`Python`中，有一个库可以专门用来处理这个事情，那就是`sanitizer`。接下来讲下这个库的使用。

## `bleach`库：

`bleach`库是用来清理包含`html`格式字符串的库。他可以指定哪些标签需要保留，哪些标签是需要过滤掉的。也可以指定标签上哪些属性是可以保留，哪些属性是不需要的。想要使用这个库，可以通过以下命令进行安装：

```shell
pip install bleach
```

这个库最重要的一个方法是`bleach.clean`方法，`bleach.clean`示例代码如下：

```python
import bleach
from bleach.sanitizer import ALLOWED_TAGS,ALLOWED_ATTRIBUTES

@require_http_methods(['POST'])
def message(request):
    # 从客户端中获取提交的数据
    content = request.POST.get('content')

    # 在默认的允许标签中添加img标签
    tags = ALLOWED_TAGS + ['img']
    # 在默认的允许属性中添加src属性
    attributes = {**ALLOWED_ATTRIBUTES,'img':['src']}

    # 对提交的数据进行过滤
    cleaned_content=bleach.clean(content,tags=tags,attributes=attributes)

    # 保存到数据库中
    Message.objects.create(content=cleaned_content)

    return redirect(reverse('index'))
```

相关介绍如下：

1. `tags`：表示允许哪些标签。
2. `attributes`：表示标签中允许哪些属性。
3. `ALLOWED_TAGS`：这个变量是`bleach`默认定义的一些标签。如果不符合要求，可以对其进行增加或者删除。
4. `ALLOWED_ATTRIBUTES`：这个变量是`bleach`默认定义的一些属性。如果不符合要求，可以对其进行增加或者删除。

### bleach更多资料：

1. github地址： https://github.com/mozilla/bleach
2. 文档地址： https://bleach.readthedocs.io/

# clickjacking攻击：

`clickjacking`攻击又称作**点击劫持攻击**。是一种在网页中将恶意代码等隐藏在看似无害的内容（如按钮）之下，并诱使用户点击的手段。

## clickjacking攻击场景：

### 场景一：

如用户收到一封包含一段视频的电子邮件，但其中的“播放”按钮并不会真正播放视频，而是链入一购物网站。这样当用户试图“播放视频”时，实际是被诱骗而进入了一个购物网站。

### 场景二：

用户进入到一个网页中，里面包含了一个非常有诱惑力的`按钮A`，但是这个按钮上面浮了一个透明的`iframe`标签，这个`iframe`标签加载了另外一个网页，并且他将这个网页的某个按钮和原网页中的`按钮A`重合，所以你在点击`按钮A`的时候，实际上点的是通过`iframe`加载的另外一个网页的按钮。比如我现在有一个百度贴吧，想要让更多的用户来关注，那么我们可以准备以下一个页面：

```html
<!DOCTYPE html>
<html>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<head>
<title>点击劫持</title>
<style>
    iframe{
        opacity:0.01;
        position:absolute;
        z-index:2;
        width: 100%;
        height: 100%;
    }
    button{
        position:absolute;
        top: 345px;
        left: 630px;
        z-index: 1;
        width: 72px;
        height: 26px;
    }
</style>
</head>
<body>
    这个合影里面怎么会有你？
    <button>查看详情</button>
    <iframe src="http://tieba.baidu.com/f?kw=%C3%C0%C5%AE"></iframe>
</body>
</html>
页面看起来比较简陋，但是实际上可能会比这些更精致一些。当这个页面通过某种手段被传播出去后，用户如果点击了“查看详情”，实际上点击到的是关注的按钮，这样就可以增加了一个粉丝。
```

## clickjacking防御：

像以上场景1，是没有办法避免的，受伤害的是用户。而像场景2，受伤害的是百度贴吧网站和用户。这种场景是可以避免的，只要设置百度贴吧不允许使用`iframe`被加载到其他网页中，就可以避免这种行为了。我们可以通过在响应头中设置`X-Frame-Options`来设置这种操作。`X-Frame-Options`可以设置以下三个值：

1. `DENY`：不让任何网页使用`iframe`加载我这个页面。
2. `SAMEORIGIN`：只允许在相同域名（也就是我自己的网站）下使用`iframe`加载我这个页面。
3. `ALLOW-FROM origin`：允许任何网页通过`iframe`加载我这个网页。

在`Django`中，使用中间件`django.middleware.clickjacking.XFrameOptionsMiddleware`可以帮我们堵上这个漏洞，这个中间件设置了`X-Frame-Option`为`SAMEORIGIN`，也就是只有在自己的网站下才可以使用`iframe`加载这个网页，这样就可以避免其他别有心机的网页去通过`iframe`去加载了。

# SQL注入

所谓SQL注入，就是通过把SQL命令插入到表单中或页面请求的查询字符串中，最终达到欺骗服务器执行恶意的SQL命令。具体来说，它是利用现有应用程序，将（恶意的）SQL命令注入到后台数据库引擎执行的能力，它可以通过在Web表单中输入（恶意）SQL语句得到一个存在安全漏洞的网站上的数据库，而不是按照设计者意图去执行SQL语句。 比如先前的很多影视网站泄露VIP会员密码大多就是通过WEB表单递交查询字符暴出的。

## 场景：

比如现在数据库中有一个`front_user`表，表结构如下：

```python
class User(models.Model):
    telephone = models.CharField(max_length=11)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
```

然后我们使用原生`sql`语句实现以下需求：

1. 实现一个根据用户`id`获取用户详情的视图。示例代码如下：

   ```python
        def index(request):
            user_id = request.GET.get('user_id')
            cursor = connection.cursor()
            cursor.execute("select id,username from front_user where id=%s" % user_id)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            return HttpResponse('success')
   ```

   这样表面上看起来没有问题。但是如果用户传的`user_id`是等于`1 or 1=1`，那么以上拼接后的`sql`语句为：

   ```sql
    select id,username from front_user where id=1 or 1=1
   ```

   以上`sql`语句的条件是`id=1 or 1=1`，只要`id=1`或者是`1=1`两个有一个成立，那么整个条件就成立。毫无疑问`1=1`是肯定成立的。因此执行完以上`sql`语句后，会将`front_user`表中所有的数据都提取出来。

2. 实现一个根据用户的`username`提取用户的视图。示例代码如下：

   ```python
    def index(request):
        username = request.GET.get('username')
        cursor = connection.cursor()
        cursor.execute("select id,username from front_user where username='%s'" % username)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        return HttpResponse('success')
   ```

   这样表面上看起来也没有问题。但是如果用户传的`username`是`zhiliao' or '1=1`，那么以上拼接后的`sql`语句为：

   ```sql
    select id,username from front_user where username='zhiliao' or '1=1'
   ```

   以上`sql`语句的条件是`username='zhiliao'`或者是一个字符串，毫无疑问，字符串的判断是肯定成立的。因此会将`front_user`表中所有的数据都提取出来。

## sql注入防御：

以上便是`sql`注入的原理。他通过传递一些恶意的参数来破坏原有的`sql`语句以便达到自己的目的。当然`sql`注入远远没有这么简单，我们现在讲到的只是冰山一角。那么如何防御`sql`注入呢？归类起来主要有以下几点：

1. 永远不要信任用户的输入。对用户的输入进行校验，可以通过正则表达式，或限制长度；对单引号和 双"-"进行转换等。

2. 永远不要使用动态拼装

   ```
   sql
   ```

   ，可以使用参数化的

   ```
   sql
   ```

   或者直接使用存储过程进行数据查询存取。比如：

   ```python
    def index(request):
        user_id = "1 or 1=1"
        cursor = connection.cursor()
        cursor.execute("select id,username from front_user where id=%s",(user_id,))
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        return HttpResponse('success')
   ```

3. 永远不要使用管理员权限的数据库连接，为每个应用使用单独的权限有限的数据库连接。

4. 不要把机密信息直接存放，加密或者hash掉密码和敏感的信息。

5. 应用的异常信息应该给出尽可能少的提示，最好使用自定义的错误信息对原始错误信息进行包装。

## 在Django中如何防御`sql`注入：

1. 使用`ORM`来做数据的增删改查。因为`ORM`使用的是参数化的形式执行`sql`语句的。
2. 如果万一要执行原生`sql`语句，那么建议不要拼接sql，而是使用参数化的形式。

