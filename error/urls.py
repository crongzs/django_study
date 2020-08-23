from django.urls import path

from error import views

app_name = 'error'

urlpatterns = [
    path('403/', views.error_403, name='403'),
    path('405/', views.error_405, name='405'),
]
