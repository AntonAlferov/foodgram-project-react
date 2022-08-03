from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )


class CountIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='Recipe_count',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='Ingredient_count',
        verbose_name='Ингредиенты',
    )
    amount = models.IntegerField(
        'Количество',
    )


class Ingredient(models.Model):
    """Модель ингредиентов"""

    name = models.CharField('Название', max_length=200,)
    measurement_unit = models.CharField(
        'Единица измерения', max_length=16,)


class Recipe(models.Model):
    """Модель рецептов"""

    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='Recipe_Ingredient',
        through='CountIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Список ингредиентов'
    )
    name = models.CharField('Название', max_length=200,)
    text = models.TextField('Описание',)
    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)', validators=[MinValueValidator(1), ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор'

    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(max_length=200,)
    color = models.CharField(max_length=7,)
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name='slug'
    )

    def __str__(self) -> str:
        return self.name
