# Generated by Django 3.0.3 on 2020-07-18 06:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0007_post_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='mygroup',
            name='member',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
