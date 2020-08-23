from django import forms

from app9.models import App9User


class App9From1(forms.ModelForm):
    pwd1 = forms.CharField(max_length=16, min_length=6)

    def clean(self):
        clean_data = super().clean()
        pwd1 = clean_data.get('pwd1')
        pwd = clean_data.get('pwd')
        if pwd1 != pwd:
            raise forms.ValidationError('两次密码不一致')
        else:
            return clean_data

    class Meta:
        model = App9User
        fields = '__all__'


class App9Form2(forms.ModelForm):
    class Meta:
        model = App9User
        fields = ['name', 'pwd']
