# Generated by Django 3.0.3 on 2020-02-26 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app3', '0006_auto_20200226_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='filterarticle',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]