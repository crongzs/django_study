from django.urls import path
from app10 import views

app_name = 'app10'

urlpatterns = [
    path('app10-1/', views.IndexView.as_view(), name='app10-1'),
    path('app10-2/', views.SiginView.as_view(), name='app10-2'),
]
