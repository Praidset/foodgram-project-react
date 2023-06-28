from rest_framework import serializers
from .models import CustomUser
from foodgram.models import Recipe
from foodgram.serializers import CroppedRecipeListSerializer
from API.serializers import CustomUserSerializer
from djoser.serializers import UserCreateSerializer


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
