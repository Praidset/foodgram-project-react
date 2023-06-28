from rest_framework import serializers
from .models import CustomUser, Subscriptions
from foodgram.models import Recipe
from foodgram.serializers import CroppedRecipeListSerializer
from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta():
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, instance):
        user_id = self.context['request'].user.id
        author_id = instance.id
        return Subscriptions.objects.filter(
            user=user_id,
            author=author_id
            ).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Создание пользователя"""

    class Meta():
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )


class SubsAuthorsListSerializer(serializers.ModelSerializer):
    "Список отслеживаемых авторов"
    is_subscribed = serializers.BooleanField(default=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta():
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()

    def get_recipes(self, obj):
        limit = self.context.get('request').query_params.get('recipes_limit')
        if limit is not None:
            recipes = Recipe.objects.all()[:int(limit)]
        else:
            recipes = Recipe.objects.all()
        return CroppedRecipeListSerializer(recipes, many=True).data
