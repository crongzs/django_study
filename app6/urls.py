from django.urls import path

from app6 import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'app6'

urlpatterns = [
    # 普通方式文件上传
    path('file-1/', views.FileView1.as_view(), name='app6-1'),
    # models文件上传
    path('file-2/', views.FileView2.as_view(), name='app6-2'),
    # 限制上传文件扩展名
    path('file-3/', views.FileView3.as_view(), name='app6-3'),
    # 图片上传
    path('file-4/', views.FileView4.as_view(), name='app6-4'),
    # 文件下载
    path('file-5/', views.FileUploadView.as_view(), name='app6-5'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 设置浏览上传文件的URL地址

# 自定义一个图片浏览的URL地址
urlpatterns = urlpatterns + static('/image/', document_root='/Users/ku_rong/Pictures')