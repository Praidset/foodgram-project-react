from rest_framework.routers import SimpleRouter
from django.urls import include, path

from .views import IngredientViewSet, RecipeViewSet, TagViewSet
from .views import SubscribtionsAPIView, SubscribeAPIView

app_name = 'users'

router = SimpleRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path(
        '',
        include(router.urls)
    ),
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
