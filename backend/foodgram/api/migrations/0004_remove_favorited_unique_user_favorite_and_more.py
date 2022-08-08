# Generated by Django 4.0.6 on 2022-08-07 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_countingredient_unique_recipe_ingredient_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorited',
            name='unique_user_favorite',
        ),
        migrations.RenameField(
            model_name='favorited',
            old_name='is_favorited',
            new_name='favorite',
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Имя'),
        ),
        migrations.AddConstraint(
            model_name='favorited',
            constraint=models.UniqueConstraint(fields=('user', 'favorite'), name='unique_user_favorite'),
        ),
    ]