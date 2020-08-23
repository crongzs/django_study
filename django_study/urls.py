"""django_study URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from app1 import inclued_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('app1.urls')),

    # ------------- URL与视图 -------------
    path('app1/', include('app1.urls', namespace='app1-a')),
    # 实例命名空间: 同一个app1下出现了两个实例app1、app1-1
    path('app1-1/', include('app1.urls', namespace='app1-b')),
    # 将 子URL 放到 include 中
    path('app1-2/', include([
        path('include/', inclued_views.app1_inclued, name='include_path')
    ])),

    # ------------- URL与视图 -------------
    path('app2/', include('app2.urls')),

    # ------------- Django 数据库 -------------
    path('app3/', include('app3.urls')),

    # ------------- Django 视图高级 -------------
    path('app4/', include('app4.urls')),

    # ------------- Django 状态码错误处理 -------------
    path('error/', include('error.urls')),

    # ------------- Django 表单 -------------
    path('app5/', include('app5.urls')),

    # ------------- Django 文件上传 -------------
    path('app6/', include('app6.urls')),

    # ------------- Django 缓存 -------------
    path('app7/', include('app7.urls')),

    # ------------- Django cookie 和 session -------------
    path('app8/', include('app8.urls')),

    # ------------- Django 上下文处理器 -------------
    path('app9/', include('app9.urls')),

    # ------------- Django 中间件 -------------
    path('app10/', include('app10.urls')),

    # ------------- Django CSRF攻击 -------------
    path('app11/', include('app11.urls')),

    # ------------- Django XXS攻击 -------------
    path('app12/', include('app12.urls')),

    # ------------- Django 验证和授权（一） -------------
    path('app13/', include('app13.urls')),

    # ------------- Django rest_framework -------------
    path('app14/', include('app14.urls')),

    # ------------- Django 验证和授权（二） -------------
    path('app15/', include('app15.urls')),

    # ------------- 页面显示Markdown -------------
    path('app16/', include('app16.urls')),

    # ------------- Django 日志 -------------
    path('app17/', include('app17.urls')),

    # ------------- Django 信号 -------------
    path('app18/', include('app18.urls')),

    # ------------- FastDFS -------------
    path('app19/', include('app19.urls')),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from app14.urls import router as app14

restful_url = [
    path('api/app14/', include(app14.urls)),
]

urlpatterns = urlpatterns + restful_url
