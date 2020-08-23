# Django 文件上传

### 普通方式文件上传

###### 前段HTML实现

1. 在前端中，我们需要填入一个`form`标签，然后在这个`form`标签中指定`enctype="multipart/form-data"`，不然就不能上传文件。
2. 在`form`标签中添加一个`input`标签，然后指定`input`标签的`name`，以及`type="file"`。

以上两步的示例代码如下：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>普通文件上传</title>
</head>
<body>
<form action="" method="post" enctype="multipart/form-data">
    <input type="file" name="upFile">
    <input type="submit" value="submit">
</form>
</body>
</html>
```

###### 后端代码实现

app6/views.py

~~~python
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse


# ---------------- HTML + Python 普通文件上传 ----------------
class FileView1(View):

    def get(self, request):
        return render(request, 'app6/app6-1普通文件上传.html')

    def post(self, request):
        file = request.FILES.get('upFile')
        with open('/Users/ku_rong/Desktop/upFile.pdf', 'wb') as fp:
            for chunk in file.chunks():
                fp.write(chunk)

        return HttpResponse("ok")

~~~

### 指定`MEDIA_ROOT`和`MEDIA_URL`：

* 在Django中，我们一般把上传上来的问价存储在 `MEDIA_ROOT`指定的目录中
* `MEDIA_URL`指定了在浏览器上浏览上传文件的URL

### models 文件上传

在定义模型的时候，我们可以给存储文件的字段指定为`FileField`，这个`Field`可以传递一个`upload_to`参数，用来指定上传上来的文件保存到哪里。

app6/models.py

~~~python
lass UpFiles(models.Model):
    title = models.CharField(max_length=16)
    # 如果不给它指定 upload_to ，它就会自动 直接 存放字 settings.py 中 MEDIA_ROOT 指定的目录中
    # 如果给它 指定 upload_to，他就会在 MEDIA_ROOT 指定的目录中 创建这些子目录，然后将文件存放进去
    file = models.FileField(upload_to='app6/files')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'app6_file'
~~~

app6/views.py

~~~python
from app6.models import UpFiles


class FileView2(View):

    def get(self, request):
        return render(request, 'app6/app6-1普通文件上传.html')

    def post(self, request):
        file = request.FILES.get('upFile')
        title = request.POST.get('title')
        UpFiles.objects.create(title=title, file=file)

        return HttpResponse("ok")
~~~

### 配置上传文件浏览的URL

app6/urls.py

~~~python
from django.urls import path

from app6 import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'app6'

urlpatterns = [
    # 普通方式文件上传
    path('file-1/', views.FileView1.as_view(), name='app6-1'),
    # models文件上传
    path('file-2/', views.FileView2.as_view(), name='app6-2'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 设置浏览上传文件的URL地址

~~~

### 限制上传文件的扩展名

* 作用：可以将一些不安全的文件如`php、py、html`等文件过滤掉

app6/models.py

~~~python
from django.db import models
from django.core import validators


# Create your models here.


class UpFiles(models.Model):
    title = models.CharField(max_length=16)
    # 如果不给它指定 upload_to ，它就会自动 直接 存放字 settings.py 中 MEDIA_ROOT 指定的目录中
    # 如果给它 指定 upload_to，他就会在 MEDIA_ROOT 指定的目录中 创建这些子目录，然后将文件存放进去
    file = models.FileField(upload_to='app6/files',
                            validators=[validators.FileExtensionValidator(['pdf'], message='文件必须为pdf')])

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'app6_file'

~~~

app6/forms.py

```python
from django import forms

from app6.models import UpFiles


class FileForm(forms.ModelForm):
    class Meta:
        model = UpFiles
        fields = '__all__'

```

app6/views.py

```python
from app6.forms import FileForm


class FileView3(View):

    def get(self, request):
        return render(request, 'app6/app6-2models文件上传.html')

    def post(self, request):
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("successful")
        else:
            print(form.errors.get_json_data())
            return HttpResponse("fial")
```

### 图片上传

app6/models.py

~~~python

class UpImage(models.Model):
    name = models.CharField(max_length=16)
    image = models.ImageField(upload_to='app6/image')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'app6_image'
~~~

app6/forms.py

~~~python
from app6.models import UpImage


class ImageForm(forms.ModelForm):
    class Meta:
        model = UpImage
        fields = '__all__'

        error_messages = {
            'image': {
                'invalid_image': '必须为一个图片'
            }
        }
~~~

app6/views.py

~~~python
from app6.forms import ImageForm


class FileView4(View):

    def get(self, request):
        return render(request, 'app6/app6-3图片上传.html')

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("successful")
        else:
            print(form.errors.get_json_data())
            return HttpResponse("fial")
~~~

app6/urls.py

~~~python
from django.urls import path

from app6 import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'app6'

urlpatterns = [
    # 普通方式文件上传
    path('file-1/', views.FileView1.as_view(), name='app6-1'),
    # models文件上传
    path('file-2/', views.FileView2.as_view(), name='app6-2'),
    # 限制上传文件扩展名
    path('file-3/', views.FileView3.as_view(), name='app6-3'),
    # 图片上传
    path('file-4/', views.FileView4.as_view(), name='app6-4'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 设置浏览上传文件的URL地址

# 自定义一个图片浏览的URL地址
urlpatterns = urlpatterns + static('/image/', document_root='/Users/ku_rong/Pictures')
~~~

