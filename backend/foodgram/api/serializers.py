from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Recipe, Ingredient, CountIngredient


class CountIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор колличества ингедиентов в рецепте"""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = CountIngredient
        fields = ('id', 'amount',)
        read_only_fields = ['recipe', ]

class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор Рецептов"""

    ingredients = CountIngredientSerializer(source='recipe',many=True,)

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'cooking_time', 'author', 'ingredients')
        depth = 1

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=self.context.get('request').user, **validated_data)
        for ingredient in ingredients_data:
            CountIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
        return recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор Ингредиентов"""
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')