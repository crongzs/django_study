from django.urls import path
from app11 import views

app_name = 'app11'
urlpatterns = [
    path('app11-1/', views.IndexView.as_view(), name='app11-1'),
    path('app11-2/', views.LoginView.as_view(), name='app11-2'),
    path('app11-3/', views.RegisterView.as_view(), name='app11-3'),
    path('app11-4/', views.TransferView.as_view(), name='app11-4'),
    path('app11-5/', views.LogOutView.as_view(), name='app11-5'),
    path('app11-6/', views.VirusView.as_view(), name='app11-6'),
]
