from rest_framework import serializers
from foodgram.models import (Tags, Ingredients, Recipe, Recipe_ingredients,
                             Favourites,
                             ShoppingCard
                             )
from users.models import CustomUser, Subscriptions
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField


class TagSerializer(serializers.ModelSerializer):

    class Meta():
        model = Tags
        fields = (
            'id', 'name', 'color', 'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta():
        model = Ingredients
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
        return Subscriptions.objects.filter(
            user=user_id,
            author=author_id
        ).exists()


class RecipeCustomUserSerializer(UserSerializer):
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

    def get_is_subscribed(self, obj):
        return False


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.ingredients.name

    def get_measurement_unit(self, obj):
        return obj.ingredients.measurement_unit

    class Meta:
        model = Recipe_ingredients
        fields = (
            'name', 'measurement_unit', 'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
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
        return Favourites.objects.filter(user=user, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request:
            current_user = request.user
            if current_user.is_authenticated:
                return ShoppingCard.objects.filter(
                    user=current_user, recipe=obj.id).exists()
            return False

    def get_ingredients(self, obj):
        ingredients = Recipe_ingredients.objects.filter(recipe_id=obj.id)
        return RecipeIngredientSerializer(ingredients, many=True).data


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Recipe_ingredients
        fields = ('id', 'amount')
        read_only_fields = ('recipe',)


class RecipeCUDSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientCreateSerializer(many=True, write_only=True)
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
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
        return data

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        for ingredient in ingredients:
            ingredient_get = ingredient['id']
            amount = ingredient['amount']
            ingredientfor = Ingredients.objects.get(id=ingredient_get)
            Recipe_ingredients.objects.create(
                recipe=instance,
                ingredients=ingredientfor,
                amount=amount
            )
        instance.save()
        return instance

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            ingredient_object = ingredient['id']
            amount = ingredient['amount']
            ingredientfor = Ingredients.objects.get(id=ingredient_object)
            recipe_ingredient, created = (
                Recipe_ingredients.objects.get_or_create(
                    recipe=recipe,
                    ingredients=ingredientfor,
                    amount=amount,
                )
            )
        recipe.tags.set(tags)
        return recipe

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data
