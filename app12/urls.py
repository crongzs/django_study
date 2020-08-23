from django.urls import path
from app12 import views

app_name = 'app12'

urlpatterns = [
    path('app12-1/', views.app12_1, name='app12-1'),
    path('app12-2/', views.app12_2, name='app12-2'),
]
