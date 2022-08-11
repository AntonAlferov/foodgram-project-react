from rest_framework.pagination import PageNumberPagination

from .models import CountIngredient


def bulk_create_count_ingredient(recipe, ingredients_data):
    """Функция сохрания ингредиентов в рецепте через bulk_create"""

    ingredient_list = [
        CountIngredient(
            recipe=recipe,
            **ingredient
        )
        for ingredient in ingredients_data
    ]
    CountIngredient.objects.bulk_create(ingredient_list)


class RecipePagination(PageNumberPagination):
    """Пагинатор рецептов"""

    page_size_query_param = 'limit'
