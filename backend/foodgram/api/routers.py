from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, IngredientsViewSet
from users.views import UsersViewSet

router = DefaultRouter()

router.register('recipes', RecipeViewSet, basename='recipe')
router.register('users', UsersViewSet, basename='users')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
