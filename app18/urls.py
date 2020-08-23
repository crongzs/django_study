from django.urls import path

from app18 import views

app_name = 'app18'

urlpatterns = [
    path('self-siganl1/', views.test_signal, name='self-siganl1'),
    path('self-siganl2/', views.test_request_log, name='self-siganl2')
]
