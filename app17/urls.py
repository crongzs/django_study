from django.urls import path

from app17 import views

app_name = 'app17'

urlpatterns = [
    path('app17-user/', views.UserView.as_view(), name='app17-user')
]
