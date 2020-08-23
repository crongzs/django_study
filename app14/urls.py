from django.urls import path

from rest_framework import routers

from app14 import views

router = routers.DefaultRouter()

app_name = 'app14'

urlpatterns = [
    path('app14-1/', views.merchant1, name='app14-1'),
    path('app14-2/', views.merchant2, name='app14-2'),
    path('app14-3/', views.category1, name='app14-3'),
    path('app14-4/', views.goods1, name='app14-4'),
    path('app14-5/', views.MerchantAPIView.as_view(), name='app14-5'),
    path('app14-6/<int:pk>/', views.MerchantAPIView.as_view(), name='app14-6'),
    path('app14-9/', views.token_view, name='app14-8')
]

router.register('app14-7', views.MerchantModelViewSet, basename='app14-7')  # basename 后期做url反转的时候需要
router.register('app14-8', views.MerchantModelViewSet01, basename='app14-8')  # basename 后期做url反转的时候需要
router.register('app14-10', views.MerchantModelViewSet02, basename='app14-10')  # basename 后期做url反转的时候需要
router.register('app14-11', views.MerchantModelViewSet03, basename='app14-11')  # basename 后期做url反转的时候需要
router.register('app14-12', views.MerchantModelViewSet04, basename='app14-12')  # basename 后期做url反转的时候需要

urlpatterns += router.urls
