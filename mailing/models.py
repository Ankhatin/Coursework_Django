from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='имя')
    email = models.EmailField(unique=True, verbose_name='почта')
    owner = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='clients', verbose_name="пользователь", **NULLABLE)
    comment = models.CharField(max_length=200, **NULLABLE, verbose_name='комментарий')

    def __str__(self):
        return f'{self.email} ({self.name})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ['id']

        permissions = [
            ('can_disable_newsletter', 'Can disable newsletter'),
        ]


class Message(models.Model):
    topic = models.CharField(max_length=100, verbose_name='тема')
    media = models.FileField(upload_to='media/', **NULLABLE, verbose_name='медиа')
    body = models.TextField(verbose_name='сообщение')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name="пользователь", **NULLABLE)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Newsletter(models.Model):
    CREATED = 'created'
    LAUNCHED = 'launched'
    COMPLETED = 'completed'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    STATUS_SET = (
        (CREATED, 'создана'),
        (LAUNCHED, 'запущена'),
        (COMPLETED, 'завершена'),
    )
    FREQUENCY_SET = (
        (DAILY, 'раз в день'),
        (WEEKLY, 'раз в неделю'),
        (MONTHLY, 'раз в месяц'),
    )
    description = models.CharField(max_length=200, verbose_name='заголовок', **NULLABLE)
    status = models.CharField(max_length=10, choices=STATUS_SET, default=CREATED, verbose_name='статус')
    date_start = models.DateTimeField(default=timezone.now, **NULLABLE, verbose_name='дата и время отправки')
    frequency = models.CharField(max_length=15, choices=FREQUENCY_SET, verbose_name='периодичность')
    clients = models.ManyToManyField(Client, related_name='newsletters', verbose_name='клиенты')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='newsletters', verbose_name="сообщение")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='newsletters', verbose_name="пользователь", **NULLABLE)

    def __str__(self):
        return f'{self.message}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['date_start']


class Attempt(models.Model):
    date_attempt = models.DateTimeField(verbose_name='дата и время попытки')
    is_successful = models.BooleanField(default=False, verbose_name='статус попытки')
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, null=True, related_name='attempts', verbose_name='рассылка')
    response = models.CharField(max_length=100, **NULLABLE, verbose_name='ответ сервера')

    def __str__(self):
        return f'{self.newsletter}'

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    body = models.CharField(max_length=100, verbose_name='Содержание')
    preview = models.ImageField(upload_to='media/', **NULLABLE, verbose_name='Изображение')
    created_at = models.DateField(auto_now_add=True)
    count_review = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
        ordering = ['title', 'count_review']