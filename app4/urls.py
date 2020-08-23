from django.urls import path
from django.views.generic import TemplateView

from app4 import views

app_name = 'app4'

urlpatterns = [
    # ---------------- 限制请求 method 的装饰器 ----------------
    path('method-1/', views.method_get, name='app4-1'),
    path('method-2/', views.method_post, name='app4-2'),
    path('method-3/', views.method_get_post, name='app4-3'),

    # ---------------- 重定向 ----------------
    path('rediction-1/', views.rediction_1, name='app4-4'),
    path('rediction-2/', views.rediction_2, name='app4-5'),

    # ---------------- WSGIRequest ----------------
    path('wsgi-request/', views.wesgi_request, name='app4-6'),

    # ---------------- QueryDict对象 ----------------
    path('querydict/', views.querydict, name='app4-7'),

    # ---------------- QueryDict对象 ----------------
    path('httpresponse/', views.httpresponse, name='app4-8'),
    path('jsonresponse/', views.jsonresponse, name='app4-9'),

    # 生成csv
    path('csv1/', views.csv1, name='app4-10'),
    path('csv2/', views.csv2, name='app4-11'),
    path('csv3/', views.csv3, name='app4-12'),

    # ---------------- TemplateView ----------------
    # 如果渲染的这个模版不需要传递任何参数，那么建议在url中使用TemplateView
    path('TemplateView/', TemplateView.as_view(template_name='app4/app4-4TemplateView.html'), name='app4-13'),
    # 如果即想使用 TemplateView 又想给模版提供参数呢
    path('TemplateViewAbout/', views.TemplateViewContent.as_view(), name='app4-14'),

    # ---------------- ListView ----------------
    path('ListView/', views.ArticleListView.as_view(), name='app4-15'),

    # ---------------- 给类视图添加装饰器 ----------------
    path('ArticlesView/', views.ArticlesView.as_view(), name='app4-16'),

]
