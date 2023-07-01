from django.contrib import admin

from foodgram.models import (
    Recipe,
    RecipeIngredient,
    Ingredient,
    Favourite,
    ShoppingCart,
    Tag)


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    list_display = (
        'author', 'name', 'image', 'cooking_time', 'text', 'count_favorites',
    )
    list_filter = ('name', 'author', 'tags',)

    def count_favorites(self, obj):
        return obj.favorites.count()


@admin.register(RecipeIngredient)
class AdminRecipeIngredient(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)


@admin.register(Favourite)
class AdminFavourite(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')


@admin.register(ShoppingCart)
class AdminShoppingCart(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', )


class IngredientResource(admin.ModelAdmin):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    resource_classes = [IngredientResource]
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name', )
