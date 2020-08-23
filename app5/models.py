from django.db import models
from django.core import validators


# Create your models here.


class FormUser(models.Model):
    name = models.CharField(max_length=6)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'form_user'


class FormBook(models.Model):
    name = models.CharField(max_length=10)
    page = models.IntegerField()
    # 在模型类中添加验证器
    price = models.FloatField(validators=[validators.MaxValueValidator(limit_value=1000)])

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'form_book'


class FormUser2(models.Model):
    name = models.CharField(max_length=16)
    pwssword = models.CharField(max_length=16)
    phone = models.CharField(max_length=11,
                             validators=[validators.RegexValidator(r'1[35678]\d{9}', message='请输入一个手机号码')])

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'form_user2'
