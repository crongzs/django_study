from django import forms

from app6.models import UpFiles


class FileForm(forms.ModelForm):
    class Meta:
        model = UpFiles
        fields = '__all__'


from app6.models import UpImage


class ImageForm(forms.ModelForm):
    class Meta:
        model = UpImage
        fields = '__all__'

        error_messages = {
            'image': {
                'invalid_image': '必须为一个图片'
            }
        }
