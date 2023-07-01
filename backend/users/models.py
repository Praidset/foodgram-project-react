from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, verbose_name='Почта')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    username = models.CharField(max_length=150,
                                unique=True,
                                verbose_name='Ник')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subs',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [UniqueConstraint(
            fields=['user', 'author'],
            name='unique_user_subscriptions')]
