from .models import CountIngredient


def bulk_create_count_ingredient(recipe, ingredients_data):
    ingredient_list = [
        CountIngredient(
            recipe=recipe,
            **ingredient
        )
        for ingredient in ingredients_data
    ]
    CountIngredient.objects.bulk_create(ingredient_list)
