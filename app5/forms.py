from django import forms
from django.core import validators


# ------------------ 表单使用流程 ------------------
class MessageBoardForm(forms.Form):
    title = forms.CharField(max_length=100, min_length=2, error_messages={'required': '必填项不能为空'}, label='标签')
    # label 指定label 名称
    content = forms.CharField(widget=forms.Textarea, error_messages={'required': '必填项不能不填'}, label='内容')
    # error_messages 指定错误信息
    email = forms.EmailField(error_messages={'required': '字符格式不匹配'}, label='邮箱')
    reply = forms.BooleanField(required=False, label='是否需要回复')


# ------------------ 用表单验证数据是否合法 ------------------
class VerifyForm(forms.Form):
    email = forms.EmailField(error_messages={'invalid': '不是一个有效的邮箱地址', 'required': '请输入邮箱'})
    price = forms.FloatField(error_messages={'invalid': '请输入一个价格', 'required': '请输入价格'})
    path = forms.URLField(error_messages={'invalid': '请输入一个url', 'required': '请输入url'})


# ------------------ 表单中的验证器 ------------------
class ValidactorsForm(forms.Form):
    email = forms.CharField(validators=[validators.EmailValidator(message='请输入正确的邮箱格式')])
    phone = forms.CharField(validators=[validators.RegexValidator(r'1[35678]\d{9}', message='请输入一个手机号码')])


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
        # de

        # 定义错误消息
        error_messages = {
            'name': {'max_length': '最多不能超过十个字符'},
            'page': {'required': 'page不能为空'}
        }


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
