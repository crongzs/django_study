from django.db import models


# Create your models here.

class App16Artivle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    ts_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'app16_article'
