from django.urls import path

from app8 import views

app_name = 'app8'
urlpatterns = [
    path('cookie1/', views.cookie1, name='app8-1'),
    path('cookie2/', views.cookie2, name='app8-2'),
    path('cookie3/', views.cookie3, name='app8-3'),

    path('session1/', views.session1, name='app8-4'),
    path('session2/', views.session2, name='app8-5'),
    path('session3/', views.session3, name='app8-6'),
]
