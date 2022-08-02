from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, status, viewsets
from .models import User
from .serializers import (
    UserSerializer, ObtainTokenSerializer, NewPasswordSerializer
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404


class UsersViewSet(viewsets.ModelViewSet):
    """ModelViewSet для обработки эндпоинта /users/."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny,)

    @action(
        methods=['get', ],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def get_account_information(self, request):
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post', ],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='set_password',
    )
    def post(self, request):
        serializer = NewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.check_password(
            serializer.validated_data['current_password']
            ):
            user = get_object_or_404(User, id=request.user.id)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class APIToken(APIView):
    """APIView для получения токена"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(
                email=serializer.validated_data['email']
            )
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if user.check_password(serializer.validated_data['password']):
            token = AccessToken.for_user(user)
            return Response(
                {'auth_token': str(token)},
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class APIDeleteToken(APIView):
    """APIView для удаления токена"""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            Response(status=status.HTTP_401_UNAUTHORIZED)
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
