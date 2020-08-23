from django.db import models


# Create your models here.


class App12Comment(models.Model):
    content = models.TextField()

    class Meta:
        db_table = 'app12_comment'
