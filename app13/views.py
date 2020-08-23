from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Create your views here.


def app13_1(request):
    ''' 创建用户 '''

    name = request.POST.get('name')
    pwd = request.POST.get('pwd')

    # 创建用户一定要使用 create_user() 方法。否则将不会对密码password 加密
    User.objects.create_user(username=name, password=pwd)
    # 创建 superuser
    User.objects.create_superuser(username=name, password=pwd)

    return HttpResponse('create user')


def app13_2(request):
    ''' 用户登陆验证 '''
    name = request.POST.get('name')
    pwd = request.POST.get('pwd')

    # authenticate 验证用户名密码是否匹配，返回一个 user对象
    user = authenticate(request, username=name, password=pwd)

    if user:
        print('login successful')
    else:
        print('fail')

    return HttpResponse('authenticate')


# ----------- 扩展User模型 一对一关联 -----------

def app13_one_to_on_authenticate(phone, password):
    ''' 使用一对一关联扩展的时候 用扩展字段电话号码和密码做用户登陆时的验证 '''
    user = User.objects.filter(extension__phone=phone).first()
    if user:
        is_corrent = user.check_password(password)
        if is_corrent:
            return user
        else:
            return None
    else:
        return None


# ----------- 扩展User模型 继承AbstractUser -----------
def app13_3(request):
    ''' 使用继承 AbstractUser 做User扩展的时候 进行用户登陆验证'''
    phone = request.POST.get('phone')
    pwd = request.POST.get('pwd')

    # 因为设置了 USERNAME_FIELD = 'phone' 所以 username=phone
    user = authenticate(request, username=phone, password=pwd)

    if user:
        print('login successful')
    else:
        print('fail')

    return HttpResponse('authenticate')

# ----------- 扩展User模型 继承AbstractUser -----------
