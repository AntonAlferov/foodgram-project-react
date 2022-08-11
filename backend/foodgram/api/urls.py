from django.urls import include, path

from .routers import router
from .views import APIDownloadShoppingCart, APISubscriptionsUser

app_name = 'api'

urlpatterns = [
   path(
      'users/subscriptions/',
      APISubscriptionsUser.as_view({'get': 'list'}),
      name='subscriptions'
   ),
   path(
      'recipes/download_shopping_cart/',
      APIDownloadShoppingCart.as_view(),
      name='download_shopping_cart'
   ),
   path("", include(router.urls)),
   path("", include("djoser.urls")),
   path("auth/", include("djoser.urls.authtoken")),
]
