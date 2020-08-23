from django.urls import path, re_path
from django.urls import converters, register_converter


class CategoryConverter(object):
    regex = r'\w+|(\w+\+\w+)+'  # 这里的正则表达式 变量名称 必须是 regex 不然Django不能识别

    def to_python(self, value):
        '''
        将 python+django+flask 处理成 ['python', 'django', 'flask']
        '''
        result = value.split('+')
        return result

    def to_url(self, value):
        '''
        将 ['python', 'django', 'flask'] 处理成 python+django+flask
        '''
        if isinstance(value, list):
            result = '+'.join(value)
            return result
        else:
            raise RuntimeError('转换URL的时候分类参数必须为list类型')


register_converter(CategoryConverter, 'cate')  # 将自定义的转换通过 register_converter 器注册到 Django 命名为 cate

from app1 import views

app_name = 'app1'

urlpatterns = [
    path('', views.index_django_study, name='django_study_index'),
    path('index/', views.index, name='index'),

    # url中传递参数给视图函数
    path('args-1/<int:id>/', views.url_args1, name='args-1'),
    path('args-2/', views.url_args2, name='args-2'),

    # url命名与url反转
    path('args-3/', views.url_args3, name='args-3'),
    path('args-4/', views.url_args4, name='args-4'),
    path('args-5/', views.url_args5, name='args-5'),

    # 实例命名空间
    path('args-6/', views.url_args6, name='args-6'),
    path('args-7/', views.url_args7, name='args-7'),

    # 使用re_path
    re_path(r're_path/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/', views.url_args8, name='re-path'),

    # url带参数反转
    path('args-9/', views.url_args9, name='args-9'),
    path('args-10/<int:id>/<int:page>/', views.url_args10, name='args-10'),

    # url携带查询字符串参数反转
    path('args-11/', views.url_args11, name='args-11'),
    path('args-12/', views.url_args12, name='args-12'),

    # 自定义path转换器
    path('args-13/<cate:categories>/', views.url_args13, name='args-13'),
    path('args-14/', views.url_args14, name='args-14'),

    # URL映射的时候指定默认参数
    path('args-15/<int:page>/', views.url_args15, name='args-15'),
    path('args-15-1/', views.url_args15, name='args-15-1'),

]
