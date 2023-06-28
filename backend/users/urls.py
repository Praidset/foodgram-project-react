from django.urls import path

from .views import (
    MySubscribtionsAPIView,
    SubscribeAPIView
)

app_name = 'users'

urlpatterns = [
    path(
        'users/<int:id>/subscribe/',
        SubscribeAPIView.as_view()
    ),
    path(
        'users/subscriptions/',
        MySubscribtionsAPIView.as_view()
    ),
]
