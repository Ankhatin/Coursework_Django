from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    token = models.CharField(max_length=100, verbose_name='Token', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['id']
        permissions = [
            ('can_view_users', 'Can view users\' list'),
            ('can_ban_user', 'Can ban user'),
        ]
