from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer

from .models import (CountIngredient, Favorited, Follow, Ingredient, Recipe,
                     ShoppingCart, Tag)


class CountIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингедиентов в рецепте"""

    id = serializers.IntegerField(source='ingredient_id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = CountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор Рецептов при создании"""

    image = Base64ImageField()
    ingredients = CountIngredientSerializer(source='RecipeCount', many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, required=True, queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
                'id', 'ingredients', 'tags', 'image',
                'name', 'text', 'cooking_time', 'author'
        )
        read_only_fields = ['author', ]

    def create(self, validated_data):
        ingredients_data = validated_data.pop('RecipeCount')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=self.context.get('request').user, **validated_data
        )
        recipe.tags.set(tags)
        for ingredient in ingredients_data:
            CountIngredient.objects.get_or_create(
                recipe=recipe, **ingredient
            )
        return recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор Ингредиентов"""
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор Тегов"""

    class Meta:
        model = Tag
        fields = '__all__'


class ListRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор Рецептов при просмотре"""

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        if Favorited.objects.filter(
            user=self.context.get('request').user, is_favorited=obj
        ).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        if ShoppingCart.objects.filter(
            user=self.context.get('request').user, is_in_shopping_cart=obj
        ).exists():
            return True
        return False

    author = UserSerializer()
    ingredients = CountIngredientSerializer(
        source='RecipeCount', many=True, read_only=True
    )
    tags = TagsSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name', 'is_favorited',
            'is_in_shopping_cart', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ['author', ]


class FavoritedRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор Добавления рецепта в избранное"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time')
        read_only_fields = ['id', 'name', 'cooking_time']

    def create(self, validated_data):
        is_favorited = self.context['view'].kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=is_favorited)
        if Favorited.objects.filter(
            user=self.context.get('request').user, is_favorited=recipe
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже есть в избранном'
            )
        Favorited.objects.create(
            user=self.context.get('request').user, is_favorited=recipe
        )
        return recipe


class ShoppingCartRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор Добавления рецепта в корзину"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time')
        read_only_fields = ['id', 'name', 'cooking_time']

    def create(self, validated_data):
        is_in_shopping_cart = self.context['view'].kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=is_in_shopping_cart)
        if ShoppingCart.objects.filter(
            user=self.context.get('request').user, is_in_shopping_cart=recipe
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже есть в корзине'
            )
        ShoppingCart.objects.create(
            user=self.context.get('request').user, is_in_shopping_cart=recipe
        )
        return recipe


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор добавления пользователя в подписки"""

    recipes = ShoppingCartRecipeSerializer(
        source='recipe', many=True, read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        return obj.recipe.count()

    def get_is_subscribed(self, obj):
        if Follow.objects.filter(
            user_follower=self.context.get('request').user,
            author_following=obj
        ).exists():
            return True
        return False

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )
        read_only_fields = [
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        ]

    def create(self, validated_data):
        author_following = self.context['view'].kwargs.get('user_id')
        author_following = get_object_or_404(User, id=author_following)
        if Follow.objects.filter(
            user_follower=self.context.get('request').user,
            author_following=author_following
        ).exists():
            raise serializers.ValidationError(
                'Пользователь уже есть в подписках'
            )
        Follow.objects.create(
            user_follower=self.context.get('request').user,
            author_following=author_following
        )
        return author_following
