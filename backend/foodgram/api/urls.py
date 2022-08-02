from django.urls import path, include
from .routers import router
from users.views import APIToken, APIDeleteToken

app_name = 'api'

urlpatterns = [
   path("", include(router.urls)),
   path('auth/token/login/', APIToken.as_view(), name='token_login'),
   path('auth/token/logout/', APIDeleteToken.as_view(), name='token_logout'),
]
