from django.urls import path

from app7 import views

app_name = 'app7'
urlpatterns = [
    path('memcached1/', views.memcached1, name='app7-1'),
]
