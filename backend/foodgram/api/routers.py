from rest_framework.routers import DefaultRouter

from .views import (FavoritedViewSet, IngredientsViewSet, RecipeViewSet,
                    ShoppingCartViewSet, SubscribeViewSet, TagsViewSet)
from users.views import UsersViewSet

router = DefaultRouter()


router.register(r'recipes/(?P<recipe_id>\w+)/favorite',
                FavoritedViewSet, basename='favorite')
router.register(r'recipes/(?P<recipe_id>\w+)/shopping_cart',
                ShoppingCartViewSet, basename='shoppingcart')
router.register(r'users/(?P<user_id>\w+)/subscribe',
                SubscribeViewSet, basename='subscribe')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('users', UsersViewSet, basename='users')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')
