from django.db import models


# Create your models here.


class MethodArticle(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    price = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'method_article'


class ViewArticel(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'view_article'
