from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from .models import Recipe, Ingredient
from .serializers import RecipeSerializer, IngredientSerializer
from rest_framework import permissions
from rest_framework import filters


class RecipeViewSet(viewsets.ModelViewSet):
    """ModelViewSet для обработки эндпоинта /recipes/."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticated,)
    
#    def perform_create(self, serializer):
#        serializer.save(author=self.request.user)
#    def get_serializer_class(self):
#        if self.action in ['list', 'retrieve']:
 #           return RecipeSerializer2
 #       return RecipeSerializer



class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """ModelViewSet для обработки эндпоинта /ingredients/."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
