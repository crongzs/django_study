from django.db import models


# Create your models here.


class App9User(models.Model):
    name = models.CharField(max_length=16)
    pwd = models.CharField(max_length=16)
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'app9_user'
