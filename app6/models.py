from django.db import models
from django.core import validators


# Create your models here.


class UpFiles(models.Model):
    title = models.CharField(max_length=16)
    # 如果不给它指定 upload_to ，它就会自动 直接 存放字 settings.py 中 MEDIA_ROOT 指定的目录中
    # 如果给它 指定 upload_to，他就会在 MEDIA_ROOT 指定的目录中 创建这些子目录，然后将文件存放进去
    file = models.FileField(upload_to='app6/files',
                            validators=[validators.FileExtensionValidator(['pdf'], message='文件必须为pdf')])

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'app6_file'


class UpImage(models.Model):
    name = models.CharField(max_length=16)
    image = models.ImageField(upload_to='app6/image')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'app6_image'
