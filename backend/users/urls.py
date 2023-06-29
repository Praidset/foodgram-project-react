from django.urls import path

from .views import (
    SubscribtionsAPIView,
    SubscribeAPIView
)

app_name = 'users'

urlpatterns = [
    path(
        'users/<int:id>/subscribe/',
        SubscribeAPIView.as_view(),
        name='to_subscribe'
    ),
    path(
        'users/subscriptions/',
        SubscribtionsAPIView.as_view(),
        name='my_subscriptions'
    ),
]
