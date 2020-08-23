from django.urls import path

from app3 import views

app_name = 'app3'

urlpatterns = [
    # Django 使用原生 sql 语句操作数据库
    path('sql/', views.to_do_sql, name='app3-1'),

    # Django 使用原生 sql 语句搭建图书管理系统
    # 图书首页
    path('sql-1/', views.to_do_sql1, name='app3-2'),
    # 添加图书
    path('sql-2/', views.to_do_sql2, name='app3-3'),
    # 图书详情
    path('sql-3/<int:id>/', views.to_do_sql3, name='app3-4'),
    # 删除图书
    path('sql-4/', views.to_do_sql4, name='app3-5'),

    # ORM 外键与表关系
    path('orm1/', views.orm1, name='app3-6'),
    path('prm5/', views.orm5, name='app3-7'),  # 一对一
    path('prm6/', views.orm6, name='app3-8'),  # 多对多
    path('prm7/', views.orm7, name='app3-9'),  # 多对多

    # ORM 查询
    path('filter1/', views.orm_filter1, name='app3-11'),
    path('filter2/', views.orm_filter2, name='app3-12'),
    path('filter3/', views.orm_filter3, name='app3-13'),
    path('filter4/', views.orm_filter4, name='app3-14'),
    path('filter5/', views.orm_filter5, name='app3-15'),
    path('filter6/', views.orm_filter6, name='app3-16'),
    path('filter7/', views.orm_filter7, name='app3-17'),
    path('filter8/', views.orm_filter8, name='app3-18'),
    path('filter9/', views.orm_filter9, name='app3-19'),
    path('filter10/', views.orm_filter10, name='app3-20'),
    path('filter11/', views.orm_filter11, name='app3-21'),

    # 聚合函数
    path('filter12/', views.orm_filter12, name='app3-22'),
    path('filter13/', views.orm_filter13, name='app3-23'),
    path('filter14/', views.orm_filter14, name='app3-24'),
    path('filter15/', views.orm_filter15, name='app3-25'),
    path('filter16/', views.orm_filter16, name='app3-26'),
    path('filter17/', views.orm_filter17, name='app3-27'),
    path('filter18/', views.orm_filter18, name='app3-28'),

    # QuerySet API 详解
    path('queryset1/', views.queryset1, name='app3-31'),
    path('queryset2/', views.queryset2, name='app3-32'),
    path('queryset3/', views.queryset3, name='app3-33'),
    path('queryset4/', views.queryset4, name='app3-34'),
    path('queryset5/', views.queryset5, name='app3-35'),
    path('queryset6/', views.queryset6, name='app3-36'),
    path('queryset7/', views.queryset7, name='app3-37'),
    path('queryset8/', views.queryset8, name='app3-38'),
    path('queryset9/', views.queryset9, name='app3-39'),
    path('queryset10/', views.queryset10, name='app3-40'),
]
