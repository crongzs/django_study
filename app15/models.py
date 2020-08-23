from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class App15Articls(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CharField)

    def __str__(self):
        return self.title

    # 添加权限的方式一：定义模型的时候添加权限
    class Meta:
        db_table = 'app15_article'
        permissions = [
            ('view_article', '查看文章的权限')
        ]
