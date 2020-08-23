from django import forms
from django.contrib.auth.models import User


class LoginFrom(forms.ModelForm):
    remember = forms.IntegerField(required=False)  # required=False 设定某个字段是否为必须的，在这里非必须
    username = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['password']
