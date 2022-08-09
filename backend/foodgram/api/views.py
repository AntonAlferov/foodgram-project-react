from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, mixins, permissions, status,
                            viewsets)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import FilterRecipe
from .permissions import WriteOnlyAuthorOr
from .models import (CountIngredient, Favorited, Follow, Ingredient, Recipe,
                     ShoppingCart, Tag, User)
from .serializers import (CreateRecipeSerializer, FavoritedRecipeSerializer,
                          FollowSerializer, IngredientSerializer,
                          ListRecipeSerializer, ShoppingCartRecipeSerializer,
                          TagsSerializer)
from .mixins import DeleteFavoriteShoppingCartMixin


class RecipeViewSet(viewsets.ModelViewSet):
    """ModelViewSet для обработки эндпоинта /recipes/."""

    queryset = Recipe.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        WriteOnlyAuthorOr
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterRecipe

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ListRecipeSerializer
        return CreateRecipeSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """ModelViewSet для обработки эндпоинта /ingredients/."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']


class TagsViewSet(viewsets.ModelViewSet):
    """ModelViewSet для обработки эндпоинта /tags/."""

    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class FavoritedViewSet(
        mixins.CreateModelMixin,
        DeleteFavoriteShoppingCartMixin,
        viewsets.GenericViewSet
        ):
    """ModelViewSet для обработки эндпоинта /recipes/{recipe_id}/favorite/."""

    queryset = Favorited.objects.all()
    serializer_class = FavoritedRecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ShoppingCartViewSet(
        mixins.CreateModelMixin,
        DeleteFavoriteShoppingCartMixin,
        viewsets.GenericViewSet
        ):
    """
    ModelViewSet для обработки эндпоинта /recipes/{recipe_id}/shopping_cart/.
    """

    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartRecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class APIDownloadShoppingCart(APIView):
    """APIView для обработки эндпоинта /recipes/download_shopping_cart/."""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        ingredients = CountIngredient.objects.filter(
            recipe__ShoppingCartRecipe__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit').annotate(total=Sum('amount'))
        shopping_cart = '\n'.join([
            f'{ingredient["ingredient__name"]}'
            f'({ingredient["ingredient__measurement_unit"]})'
            f' -- {ingredient["total"]}'
            for ingredient in ingredients
        ])
        filename = 'shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class SubscribeViewSet(
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
        ):
    """ModelViewSet для обработки эндпоинта /users/{recipe_id}/subscribe/."""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        if not Follow.objects.filter(
            user_follower=request.user, author_following=user
        ).exists():
            return Response(
                {"errors": "Такого пользователя нет в ваших подписках"},
                status=status.HTTP_400_BAD_REQUEST
            )
        Follow.objects.filter(
            user_follower=request.user, author_following=user
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class APISubscriptionsUser(viewsets.ModelViewSet):
    """ModelViewSet для обработки эндпоинта /users/subscriptions/."""

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        new_queryset = User.objects.filter(
            following__user_follower=self.request.user
        )
        return new_queryset
