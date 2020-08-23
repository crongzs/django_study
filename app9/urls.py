from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from app9 import views

app_name = 'app9'
urlpatterns = [
    path('app9-1/', views.app9_1, name='app9-1'),
    path('app9-2/', views.app9_2, name='app9-2'),
    path('app9-2/', views.App9View1.as_view(), name='app9-2'),
    path('app9-3/', views.App9View2.as_view(), name='app9-3'),
]