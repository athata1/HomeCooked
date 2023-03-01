# Generated by Django 4.1.7 on 2023-02-28 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeCooked', '0016_user_image_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_sys_tags',
            field=models.CharField(default='', max_length=200, verbose_name='system tags'),
        ),
        migrations.AddField(
            model_name='post',
            name='post_user_tags',
            field=models.CharField(default='', max_length=200, verbose_name='user tags'),
        ),
    ]
