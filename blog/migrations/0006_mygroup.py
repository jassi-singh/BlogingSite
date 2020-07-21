# Generated by Django 3.0.3 on 2020-07-17 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_auto_20200717_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mygroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mygroups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
