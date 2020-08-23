from django.urls import path

from app2 import views

app_name = 'app2'

urlpatterns = [
    # 模版渲染的两种方式
    path('template1/', views.template1, name='app2-1'),
    path('template2/', views.template2, name='app2-2'),

    # 模版变量的使用
    path('template3/', views.template3, name='app2-3'),

    # for标签的使用
    path('template4/', views.template4, name='app2-4'),

    # with标签的使用
    path('template5/', views.template5, name='app2-5'),

    # url标签的使用
    path('template6/', views.template6, name='app2-6'),
    path('template7/<str:id>/<int:page>/', views.template7, name='app2-7'),
    path('template8/', views.template8, name='app2-8'),

    # autoescape标签的使用
    path('template9/', views.template9, name='app2-9'),

    # verbatim标签的使用
    path('template10/', views.template10, name='app2-10'),

    # 常见的模版顾虑器
    path('template11/', views.template11, name='app2-11'),

    # 自定义模版过滤器
    path('template12/', views.template12, name='app2-12'),

    # 模版优化-引入模版
    path('template13/', views.template13, name='app2-13'),

    # 模版优化-模版继承
    path('template14/', views.template14, name='app2-14'),

    # 加载静态文件
    path('template15/', views.template15, name='app2-15'),
    path('template16/', views.template16, name='app2-16'),

]
