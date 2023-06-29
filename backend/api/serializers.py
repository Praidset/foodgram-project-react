from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer


from .methods import CreateUpdate
from rest_framework import serializers
from foodgram.models import (Tag, Ingredient, Recipe, Recipeingredient,
                             Favourite,
                             ShoppingCart
                             )

from users.models import CustomUser, Subscription


class TagSerializer(serializers.ModelSerializer):

    class Meta():
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta():
        model = Ingredient
        fields = ('__all__')


class CroppedRecipeListSerializer(serializers.ModelSerializer):

    class Meta():
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )

    def filter_queryset(self, request, queryset, view):
        limit = request.query_params.get('recipes_limit')
        if limit:
            return queryset[:int(limit)]
        return queryset


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
        return Subscription.objects.filter(
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


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')

    class Meta:
        model = Recipeingredient
        fields = (
            'name', 'measurement_unit', 'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True,
                                             source='recipeingredient_set')
    author = CustomUserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta():
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user.id
        return Favourite.objects.filter(user=user, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request:
            current_user = request.user
            if current_user.is_authenticated:
                return ShoppingCart.objects.filter(
                    user=current_user, recipe=obj.id).exists()
            return False


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Recipeingredient
        fields = ('id', 'amount')
        read_only_fields = ('recipe',)


class RecipeCUDSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientCreateSerializer(many=True, write_only=True)
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'author',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def validate(self, data):
        ingredients = data.get('ingredients')
        tags = data.get('tags')
        unique_check = []
        if data.get('cooking_time') < 1:
            raise serializers.ValidationError(
                'По документации время готовки не меньше минуты , СОГГУ'
            )
        if not ingredients:
            raise serializers.ValidationError(
                'Студенческий формат? В рецепте должны быть ингредиенты'
            )
        if not tags:
            raise serializers.ValidationError(
                'Нельзя добавить рецепт без тега'
            )
        for ingredient in ingredients:
            if ingredient['id'] in unique_check:
                raise serializers.ValidationError(
                    'Нельзя добавить одинаковые ингредиенты'
                )
            unique_check.append(ingredient['id'])
        return data

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        CreateUpdate(ingredients, instance=instance)
        instance.save()
        return instance

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        CreateUpdate(ingredients, recipe=recipe)
        recipe.tags.set(tags)
        return recipe

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data


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
