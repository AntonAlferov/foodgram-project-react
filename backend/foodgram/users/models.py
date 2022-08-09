from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователей."""

    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    username = models.CharField(
        'Уникальный юзернейм',
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.TextField(
        'Имя',
        max_length=150,
    )
    last_name = models.TextField(
        'Фамилия',
        max_length=150,
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
