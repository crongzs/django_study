from django.urls import path

from app15 import views

app_name = 'app15'

urlpatterns = [
    path('app15-1/', views.app15_login, name='app15-1'),
    path('app15-2/', views.app15_logout, name='app15-2'),
    path('app15-3/', views.app15_login_required, name='app15-3'),
    path('app15-4/', views.app15_add_permission, name='app15-4'),
    path('app15-5/', views.app15_operate_permission, name='app15-5'),
    path('app15-6/', views.app15_add_article, name='app15-6'),
    path('app15-7/', views.app15_permission_login, name='app15-7'),
    path('app15-8/', views.app15_add_user, name='app15-8'),
    path('app15-9/', views.app15_operate_group, name='app15-9'),
    path('app15-10/', views.app15_group_permission, name='app15-10'),
    path('app15-11/', views.app15_template_permission, name='app15-11'),
]
