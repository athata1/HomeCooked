# Generated by Django 4.1.7 on 2023-03-01 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homeCooked', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='RecipeID', to='homeCooked.recipe', verbose_name='Recipe'),
        ),
    ]
