# Generated by Django 3.0.8 on 2020-07-30 16:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20200730_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]