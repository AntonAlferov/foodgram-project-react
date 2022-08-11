from rest_framework import serializers

from api.models import Follow
from .models import User


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор  текущего пользователя. """

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return False

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name',
            'is_subscribed'
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей, модели User. """

    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        if self.context.get('request').user.is_authenticated:
            return Follow.objects.filter(
                user_follower=self.context.get('request').user,
                author_following=obj
            ).exists()
        return False

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'password', 'is_subscribed'
        )


class NewPasswordSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения пароля. """

    new_password = serializers.CharField()
    current_password = serializers.CharField()

    class Meta:
        model = User
        fields = ('new_password', 'current_password')

    def validate_current_password(self, value):
        if self.context.get('request').user.check_password(value):
            return value
        raise serializers.ValidationError(
                'Старый пароль не подтвержден'
            )
