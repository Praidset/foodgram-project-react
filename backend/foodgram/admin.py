from django.contrib import admin


from foodgram.models import (Favourites, Ingredients, Recipe,
                            Recipe_ingredients,
                            ShoppingCard, Tags)


class IngredientResource(admin.ModelAdmin):
    class Meta:
        model = Ingredients
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


@admin.register(Ingredients)
class AdminIngredient(admin.ModelAdmin):
    resource_classes = [IngredientResource]
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name', )


@admin.register(Tags)
class AdminTag(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', )


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    list_display = (
        'author', 'name', 'image', 'cooking_time', 'text', 'count_favorites',
    )
    list_filter = ('name', 'author', 'tags',)

    def count_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Recipe_ingredients)
class AdminRecipeIngredient(admin.ModelAdmin):
    list_display = ('recipe', 'ingredients', 'amount',)


@admin.register(Favourites)
class AdminFavourite(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')


@admin.register(ShoppingCard)
class AdminShoppingCart(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')
