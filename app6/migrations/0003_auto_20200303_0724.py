# Generated by Django 3.0.3 on 2020-03-02 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app6', '0002_auto_20200303_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upfiles',
            name='file',
            field=models.FileField(upload_to='app6/files'),
        ),
    ]