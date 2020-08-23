# Django 表单

Django 中的表单丰富了传统HTML表单，有两点作用

* 渲染HTML模版
* 表单验证数据是否合法

### Form表单的使用流程

* 定义一个表单

首先我们在后台服务器定义一个表单类，继承自`django.forms.Form`

```python
from django import forms


class MessageBoardForm(forms.Form):
    title = forms.CharField(max_length=100, min_length=2, error_messages={'required': '必填项不能为空'}, label='标签')
    # label 指定label 名称
    content = forms.CharField(widget=forms.Textarea, error_messages={'required': '必填项不能不填'}, label='内容')
    # error_messages 指定错误信息
    email = forms.EmailField(error_messages={'required': '字符格式不匹配'}, label='邮箱')
    reply = forms.BooleanField(required=False, label='是否需要回复')
```

* 定义视图

然后在视图中，根据是`GET`还是`POST`请求来做相应的操作。如果是`GET`请求，那么返回一个空的表单，如果是`POST`请求，那么将提交上来的数据进行校验。

在使用`GET`请求的时候，我们传了一个`form`给模板，那么以后模板就可以使用`form`来生成一个表单的`html`代码。在使用`POST`请求的时候，我们根据前端上传上来的数据，构建一个新的表单，这个表单是用来验证数据是否合法的，如果数据都验证通过了，那么我们可以通过`cleaned_data`来获取相应的数据。

```python
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import HttpResponse

from app5.forms import MessageBoardForm


class MessageVoarView(View):

    def get(self, request):
        form = MessageBoardForm()
        return render(request, 'app5/app5-1forms.html', context={'form': form})

    def post(self, request):
        form = MessageBoardForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            email = form.cleaned_data.get('email')
            reply = form.cleaned_data.get('reply')
            return HttpResponse('successful')
        else:
            print(form.errors.get_json_data())
            return HttpResponse('fail')
```

* 编写模版

我们在最外面给了一个`form`标签，然后在里面使用了`table`标签来进行美化，在使用`form`对象渲染的时候，使用的是`table`的方式，当然还可以使用`ul`的方式（`as_ul`），也可以使用`p`标签的方式（`as_p`），并且在后面我们还加上了一个提交按钮。这样就可以生成一个表单了

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Forms</title>
</head>
<body>
<form action="" method="post">
    <table>
        {{ form.as_table }}
        <tr>
            <td></td>
            <td><input type="submit" value="submit"></td>
        </tr>
    </table>
</form>
</body>
</html>
```

### 用表单验证数据是否合法

app5/forms.py

~~~python
# ------------------ 用表单验证数据是否合法 ------------------
class VerifyForm(forms.Form):
    email = forms.EmailField(error_messages={'invalid': '不是一个有效的邮箱地址', 'required': '请输入邮箱'})
    price = forms.FloatField(error_messages={'invalid': '请输入一个价格', 'required': '请输入价格'})
    path = forms.URLField(error_messages={'invalid': '请输入一个url', 'required': '请输入url'})
~~~

app5/views.py

~~~python
# ---------------- 用表单验证数据是否合法 ----------------

from app5.forms import VerifyForm


class VerifyView(View):
    def get(self, request):
        return render(request, 'app5/app5-2verify.html')

    def post(self, request):
        form = VerifyForm(request.POST)
        if form.is_valid():
            return HttpResponse('suucessful')
        else:
            print('----------error----------')
            print(form.errors.get_json_data())
            return HttpResponse('fail')
~~~

app5/urls.py

~~~python
from django.urls import path

from app5 import views

app_name = 'app5'

urlpatterns = [
  	# ----------------------- 用表单验证数据是否合法 -----------------------
    path('verify/', views.VerifyView.as_view(), name='app5-2'),
]

~~~

templates/app5/app5-2verify.html

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Verify</title>
</head>
<body>
<form action="" method="post">
    <input type="text" name="email">
    <input type="text" name="price">
    <input type="text" name="path">
    <input type="submit" value="submit">
</form>
</body>
</html>
~~~

### 表单中的验证器

在验证某个字段的时候，可以传递一个`validators`参数用来指定验证器，进一步对数据进行过滤。验证器有很多，但是很多验证器我们其实已经通过这个`Field`或者一些参数就可以指定了。比如`EmailValidator`，我们可以通过`EmailField`来指定，比如`MaxValueValidator`，我们可以通过`max_value`参数来指定。以下是一些常用的验证器：

1. `MaxValueValidator`：验证最大值。
2. `MinValueValidator`：验证最小值。
3. `MinLengthValidator`：验证最小长度。
4. `MaxLengthValidator`：验证最大长度。
5. `EmailValidator`：验证是否是邮箱格式。
6. `URLValidator`：验证是否是`URL`格式。
7. `RegexValidator`：如果还需要更加复杂的验证，那么我们可以通过正则表达式的验证

app5/forms.py

~~~python
# ------------------ 表单中的验证器 ------------------
class ValidactorsForm(forms.Form):
    email = forms.CharField(validators=[validators.EmailValidator(message='请输入正确的邮箱格式')])
    phone = forms.CharField(validators=[validators.RegexValidator(r'1[35678]\d{9}', message='请输入一个手机号码')])
~~~

app5/views.py

~~~python
# ---------------- 使用表单验证器 ----------------

from app5.forms import ValidactorsForm


class ValidactorView(View):
    def get(self, request):
        return render(request, 'app5/app5-3validators.html')

    def post(self, request):
        form = ValidactorsForm(request.POST)
        if form.is_valid():
            return HttpResponse('successful')
        else:
            print(form.errors.get_json_data())
            return HttpResponse('fail')
~~~

app5/urls.py

~~~python
from django.urls import path

from app5 import views

app_name = 'app5'

urlpatterns = [
		# ----------------------- 表单验证器 -----------------------
    path('validators/', views.ValidactorView.as_view(), name='app5-3'),
]


~~~

templates/app5/app5-3valdators.html

~~~html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>validators</title>
</head>
<body>
<form action="" method="post">
    <input type="text" name="email">
    <input type="text" name="phone">
    <input type="submit" value="submit">
</form>
</body>
</html>
~~~

### 自定义表单验证器

* 针对某一个字段

  对某个字段进行自定义的验证方式是，定义一个方法，这个方法的名字定义规则是：`clean_fieldname`。如果验证失败，那么就抛出一个验证错误。

* 针对多个字段

  需要针对多个字段进行验证，那么可以重写`clean`方法。

app5/models.py

~~~python
class FormUser(models.Model):
    name = models.CharField(max_length=6)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'form_user'
~~~

app5/forms.py

~~~python
# ------------------ 自定义表单验证器 ------------------
from app5.models import FormUser


class UserdefinedForm(forms.Form):
    name = forms.CharField(max_length=6)
    phone = forms.CharField(validators=[validators.RegexValidator(r'1[35678]\d{9}', message='请输入一个手机号码')])
    pwd1 = forms.CharField(max_length=10, min_length=6)
    pwd2 = forms.CharField(max_length=10, min_length=6)

    # 如果要专门针对某个字段进行验证，那么就定义一个方法 方法名称为 clean_ + 字段名，如 clean_phone
    # 当视图中调用 is_valid() 方法时， 会自动调用 这种以 clean_ 开头 加字段名的方法
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        exists = FormUser.objects.filter(phone=phone).exists()
        if exists:
            raise forms.ValidationError(message='此号码已注册')
        else:
            # 如果验证没问题，一定要将字段返回
            return phone

    # 验证多个字段，重写clean() 方法
    def clean(self):
        # 如果来到了clean方法，说明之前的每一个字段都验证成功了
        # super().clean()
        # pwd1 = self.cleaned_data.get('pwd1')
        # pwd2 = self.cleaned_data.get('pwd2')
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get('pwd1')
        pwd2 = cleaned_data.get('pwd2')
        if pwd2 != pwd1:
            raise forms.ValidationError(message='两次密码不一致')
        return cleaned_data
~~~

app5/views.py

~~~py
# ---------------- 自定义表单验证器 ----------------
from app5.forms import UserdefinedForm
from app5.models import FormUser


class UserdefinedView(View):
    def get(self, request):
        return render(request, 'app5/app5-4userdefined.html')

    def post(self, request):
        form = UserdefinedForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            phone = form.cleaned_data.get('phone')
            FormUser.objects.create(name=name, phone=phone)
            return HttpResponse('successful')
        else:
            print(form.errors.get_json_data())
            return HttpResponse('fail')
~~~

### 提取错误信息



app5/forms.py

```python
# ------------------ 简化错误信息提取 ------------------
class GetErrorsForm(forms.Form):
    name = forms.CharField(max_length=6)
    phone = forms.CharField(validators=[validators.RegexValidator(r'1[35678]\d{9}', message='请输入一个手机号码')])
    pwd1 = forms.CharField(max_length=10, min_length=6)
    pwd2 = forms.CharField(max_length=10, min_length=6)

    # 如果要专门针对某个字段进行验证，那么就定义一个方法 方法名称为 clean_ + 字段名，如 clean_phone
    # 当视图中调用 is_valid() 方法时， 会自动调用 这种以 clean_ 开头 加字段名的方法
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        exists = FormUser.objects.filter(phone=phone).exists()
        if exists:
            raise forms.ValidationError(message='此号码已注册')
        else:
            # 如果验证没问题，一定要将字段返回
            return phone

    # 验证多个字段，重写clean() 方法
    def clean(self):
        # 如果来到了clean方法，说明之前的每一个字段都验证成功了
        # super().clean()
        # pwd1 = self.cleaned_data.get('pwd1')
        # pwd2 = self.cleaned_data.get('pwd2')
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get('pwd1')
        pwd2 = cleaned_data.get('pwd2')
        if pwd2 != pwd1:
            raise forms.ValidationError(message='两次密码不一致')
        return cleaned_data

    # 定义一个获取错误信息的方法
    def get_errors(self):
        errors = self.get_json_data()
        news_errors = {}
        for key, message_dicts in errors.items():
            messages = []
            for message_dict in message_dicts:
                message = message_dict['message']
                messages.append(message)
            news_errors[key] = messages
        return news_errors


# 如果要多个表单复用这个方法，可以把它封装近一个公共类中, 其他表单类直接继承这个类
class GetMessageBaseFrom(forms.Form):
    def get_errors(self):
        errors = self.get_json_data()
        news_errors = {}
        for key, message_dicts in errors.items():
            messages = []
            for message_dict in message_dicts:
                message = message_dict['message']
                messages.append(message)
            news_errors[key] = messages
        return news_errors


# 继承公共类，这样就可以使用 get_errors 方法了
class GetMessageTestFrom(GetMessageBaseFrom):
    pass
```

### ModelForm

app5/models.py

~~~python
class FormBook(models.Model):
    name = models.CharField(max_length=10)
    page = models.IntegerField()
    # 在模型类中添加验证器
    price = models.FloatField(validators=[validators.MaxValueValidator(limit_value=1000)])

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'form_book'
~~~

app5/forms.py

~~~python
# ------------------ ModelFrom ------------------
from app5.models import FormBook


class BookFrom(forms.ModelForm):
    # 可以向模型类中添加验证器，也可以自定义验证

    # 自定义验证
    def clean_page(self):
        page = self.cleaned_data.get('page')
        if page >= 500:
            raise forms.ValidationError('页数过大，不能超过500')
        else:
            return page

    class Meta:
        model = FormBook
        # fields = '__all__' 将模型中的所有字段复制过来进行验证
        fields = '__all__'

        # fields = ['name', 'page'] 将需要验证的字段放入类表中进行验证
        # fields = ['name', 'page']

        # 除了个别字段不需要验证，其它字段都要验证，可以用 exclude 将不需要验证的字段排除
        # exclude = ['price', 'page']

        # 定义错误消息
        error_messages = {
            'name': {'max_length': '最多不能超过十个字符'},
            'page': {'required': 'page不能为空'}
        }
~~~

app5/views.py

~~~python
# ---------------- ModelForm ----------------
from app5.forms import BookFrom


class BookView(View):
    def get(self, request):
        return HttpResponse('ModelForm')

    def post(self, request):
        form = BookFrom(request.POST)
        if form.is_valid():
            return HttpResponse('successful')
        else:
            print(form.errors.get_json_data())
            return HttpResponse('fail')
~~~

###### savr()

`ModelForm`还有`save`方法，可以在验证完成后直接调用`save`方法，就可以将这个数据保存到数据库中了。

~~~python
form = MyForm(request.POST)
if form.is_valid():
    form.save()
    return HttpResponse('succes')
else:
    print(form.get_errors())
    return HttpResponse('fail')
~~~

这个方法必须要在`clean`没有问题后才能使用，如果在`clean`之前使用，会抛出异常。另外，我们在调用`save`方法的时候，如果传入一个`commit=False`，那么只会生成这个模型的对象，而不会把这个对象真正的插入到数据库中。比如表单上验证的字段没有包含模型中所有的字段，这时候就可以先创建对象，再根据填充其他字段，把所有字段的值都补充完成后，再保存到数据库中。

app5/models.py

~~~python
class FormUser2(models.Model):
    name = models.CharField(max_length=16)
    pwssword = models.CharField(max_length=16)
    phone = models.CharField(max_length=11,
                             validators=[validators.RegexValidator(r'1[35678]\d{9}', message='请输入一个手机号码')])

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'form_user2'
~~~

app5/forms.py

~~~python
from app5.models import FormUser2


class User2Form(forms.ModelForm):
    pwd1 = forms.CharField(max_length=16, min_length=6)
    pwd2 = forms.CharField(max_length=16, min_length=6)

    def clean(self):
        clean_data = super().clean()
        pwd1 = clean_data.get('pwd1')
        pwd2 = clean_data.get('pwd2')
        if pwd1 != pwd2:
            raise forms.ValidationError('两次输入密码不一致')
        else:
            return clean_data

    class Meta:
        model = FormUser2
        exclude = ['pwssword']
~~~

app5/viees.py

~~~pyton
@require_POST
def add_user(request):
    ''' ModelForm 的 save() 方法 '''
    form = User2Form(request.POST)
    if form.is_valid():
        # 这样直接使用 save()方法 必须要保证表单中的fields字段列表中的数据满足 模型中的所有字段需求，也就是 __all__
        # form.save()
        # 如果 forms 中的 fields 不能满足 models 中的需求，那么就在save 方法中 添加参数 commit=False
        pwd = form.cleaned_data.get('pwd1')
        user = form.save(commit=False)
        user.password = pwd
        user.save()
        return HttpResponse('successful')
    else:
        print(form.errors.get_json_data())
        return HttpResponse('fail')
~~~

