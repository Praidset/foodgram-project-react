from django.contrib import admin
from .models import CustomUser, Subscriptions

User = CustomUser


@admin.register(Subscriptions)
class AdminSubscriptions(admin.ModelAdmin):
    list_display = ('id', 'author', 'user')


@admin.register(User)
class AdminCustomUser(admin.ModelAdmin):
    list_display = ('id',
                    'username',
                    'password',
                    'email',
                    'first_name',
                    'last_name'
                    )
    list_filter = ('username', 'email',)
