from rest_framework import serializers

from api.models import Follow

from .models import User


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор  текущего пользователя. """

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
        if Follow.objects.filter(
            user_follower=self.context.get('request').user,
            author_following=obj
        ).exists():
            return True
        return False

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name',
            'password', 'is_subscribed'
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class ObtainTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токена. """

    email = serializers.EmailField(required=True)
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'password')


class NewPasswordSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения пароля. """

    new_password = serializers.CharField()
    current_password = serializers.CharField()

    class Meta:
        model = User
        fields = ('new_password', 'current_password')
