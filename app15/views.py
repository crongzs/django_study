from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse

# Create your views here.


'''
django有自己的login函数，因此当我们自定义登陆视图的时候一定不能使用login



'''
from app15.forms import LoginFrom


def app15_login(request):
    if request.method == 'GET':
        return render(request, 'app15/app15-1login.html')
    else:
        form = LoginFrom(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = authenticate(request, username=username, password=password)
            if user and user.is_active:
                login(request, user)
                if remember:
                    # 设置为None表示使用全局的过期时间, 两周
                    request.session.set_expiry(None)
                else:
                    # 设置为0表示浏览器关闭就过期
                    request.session.set_expiry(0)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return HttpResponse('successful')
            else:
                return HttpResponse('fail')
        else:
            print(form.errors.get_json_data())
            return render(request, 'app15/app15-1login.html')


def app15_logout(request):
    logout(request)
    return HttpResponse('Log out')


# Django 登陆限制
@login_required(login_url='app15:app15-1')  # 要指定登陆页面
def app15_login_required(request):
    return HttpResponse('请先登录')


# ----------------------- 权限 -----------------------
from django.contrib.auth.models import Permission, ContentType
from django.contrib.auth.models import User

from app15.models import App15Articls


# 添加权限的方式二：使用代码的方式添加
def app15_add_permission(request):
    content_type = ContentType.objects.get_for_model(App15Articls)
    permission = Permission.objects.create(codename='to_like', name='点赞', content_type=content_type)
    return HttpResponse('successful')


def app15_operate_permission(request):
    user = request.user
    content_type = ContentType.objects.get_for_model(App15Articls)
    permissions = Permission.objects.filter(content_type=content_type)
    for permission in permissions:
        print(permission)

    # 一次性添加多个权限
    # user.user_permissions.set(permissions)
    # 一次性清除多个权限
    user.user_permissions.clear()
    # 添加一个权限
    # user.user_permissions.add(permissions[0])
    # 添加多个权限
    # user.user_permissions.add(*permissions)
    # 移除一个权限
    # user.user_permissions.remove(permissions[0])
    # 遗传多个权限
    # user.user_permissions.remove(*permissions)

    if user.has_perm('app15.view_article'):
        print('有权限')

    return HttpResponse("操作用户权限")


def app15_add_article(request):
    # 判断用户是否登陆
    if request.user.is_authenticated:  # 如果登陆了 request.user.is_authenticated 就会返回一个True 反之就返回一个 False
        if request.user.has_perm('app15.view_article'):
            print('hello')
            return HttpResponse('add article')
        else:
            return HttpResponse('没有权限', status=403)
    else:
        return HttpResponse('请先登录')


@permission_required('app15.view_article', raise_exception=True)  # permission_required 只有用户登陆并且具有某一权限才能访问这个视图
def app15_permission_login(request):
    return HttpResponse('hello')


def app15_add_user(request):
    ''' 创建一个用户 '''
    user = User.objects.create_user(username='ku_rong', email='sss@qq.com', password='960308')
    return HttpResponse('successful')


# ----------------------- 分组 -----------------------

from django.contrib.auth.models import Group


def app15_operate_group(request):
    # 创建组
    group = Group.objects.create(name='运营')
    # 给组添加权限
    content_type = ContentType.objects.get_for_model(App15Articls)
    permissions = Permission.objects.filter(content_type=content_type)
    group.permissions.set(permissions)
    group.save()
    return HttpResponse("Group")


def app15_user_group(request):
    ''' 给用湖添加组 '''
    user = request.user
    group = Group.objects.filter(name='运营')
    user.groups.add(group)
    return HttpResponse('group user')


def app15_group_permission(request):
    ''' 获取组的权限 '''
    user = User.objects.first()
    permissions = user.get_group_permissions()
    print('-' * 50)
    print(permissions)
    return HttpResponse('group permission')


def app15_template_permission(request):
    user = request.user
    return render(request, 'app15/app15-2user group permission.html')
