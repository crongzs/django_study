from django.urls import path

from app5 import views

app_name = 'app5'

urlpatterns = [
    # ----------------------- 表单的使用流程 -----------------------
    path('forms/', views.MessageVoarView.as_view(), name='app5-1'),

    # ----------------------- 用表单验证数据是否合法 -----------------------
    path('verify/', views.VerifyView.as_view(), name='app5-2'),

    # ----------------------- 表单验证器 -----------------------
    path('validators/', views.ValidactorView.as_view(), name='app5-3'),

    # ----------------------- 自定义表单验证器 -----------------------
    path('userdefined/', views.UserdefinedView.as_view(), name='app5-4'),

    # ----------------------- 简化错误信息提取 -----------------------
    path('get-errors/', views.GetErrorView.as_view(), name='app5-5'),

    # ----------------------- ModelFrom -----------------------
    path('model-from/', views.BookView.as_view(), name='app5-6'),
    path('model-form-save/', views.add_user, name='app5-7'),
]
