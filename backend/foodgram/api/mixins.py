from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe


class DeleteFavoriteShoppingCartMixin:
    """Миксин удаления из списка покупок и избранного"""

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if not self.queryset.filter(
            user=request.user, recipe=recipe
        ).exists():
            return Response(
                {"errors": "Такой рецепт не добавлен"},
                status=status.HTTP_400_BAD_REQUEST
            )
        obj = get_object_or_404(
            self.queryset, user=user, recipe=recipe
        )
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
