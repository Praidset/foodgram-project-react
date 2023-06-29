from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='authors'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='subs'
    )

    class Meta:
        unique_together = ['user', 'author']
