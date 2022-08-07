from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Follow(models.Model):
    user_follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Кто подписан'

    )
    author_following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='На кого подписан'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class CountIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='RecipeCount',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='IngredientCount',
        verbose_name='Ингредиенты',
    )
    amount = models.IntegerField(
        'Количество',
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class Ingredient(models.Model):
    """Модель ингредиентов"""

    name = models.CharField('Название', max_length=200,)
    measurement_unit = models.CharField(
        'Единица измерения', max_length=16,)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name


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
    tags = models.ManyToManyField(
        'Tag',
        related_name='Tag_Ingredient',
        verbose_name='Список тегов'
        )
    image = models.ImageField(
        'Картинка, закодированная в Base64',
        upload_to='posts/',
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор'

    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

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

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Favorited(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='FavoritedUser',
        verbose_name='Имя пользователя'
    )
    is_favorited = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='FavoritedIsRecipe',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self) -> str:
        return (
            f'"{self.is_favorited.name}"'
            'в избранном у "{self.user.username}"'
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ShoppingCartUser',
        verbose_name='Имя пользователя'
    )
    is_in_shopping_cart = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ShoppingCartRecipe',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self) -> str:
        return (
            f'"{self.is_in_shopping_cart.name}"'
            'в корзине у "{self.user.username}"'
        )
