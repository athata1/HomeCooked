# Generated by Django 4.1.1 on 2023-02-23 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeCooked', '0006_post_post_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_available',
            field=models.BooleanField(default=False),
        ),
    ]