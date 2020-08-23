from django import forms

from app11.models import App11User


class APP11Form1(forms.ModelForm):
    pwd1 = forms.CharField(max_length=16, min_length=6)

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('pwd')
        pwd1 = cleaned_data.get('pwd1')
        if pwd1 != pwd:
            raise forms.ValidationError("The two passwords don't match")
        return cleaned_data

    class Meta:
        model = App11User
        fields = ['name', 'pwd', 'phone']


class APP11Form2(forms.ModelForm):
    class Meta:
        model = App11User
        fields = ['name', 'pwd']


class APP11Form3(forms.Form):
    phone = forms.CharField(max_length=16)
    money = forms.FloatField()
