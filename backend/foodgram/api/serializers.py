from rest_framework import serializers
from .models import Recipe, Ingredient, CountIngredient


class CountIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор колличества ингедиентов в рецепте"""

    class Meta:
        model = CountIngredient
        fields = ('ingredient', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор Рецептов"""

    ingredients = CountIngredientSerializer(source='countingredient_set', many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'cooking_time', 'author', 'ingredients')
        read_only_fields = ['author', ]

    def create(self, validated_data):
        ingredients_data = validated_data.pop('countingredient_set')
        recipe = Recipe.objects.create(author=self.context.get('request').user, **validated_data)
        for ingredient in ingredients_data:
            CountIngredient.objects.get_or_create(
                recipe=recipe,**ingredient
            )
        return recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор Ингредиентов"""
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')
