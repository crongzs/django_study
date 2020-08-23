from django.urls import path

from app16 import views

app_name = 'app16'

urlpatterns = [
    path("app16-1/", views.article_list, name='app16-1')
]
