import django_filters
import django_filters.rest_framework as filters
from django.db.models import Q

from foodgram.models import Recipe, Ingredient


class IngredientNameFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value:
            return qs.filter(Q(name__istartswith=value))
        return qs


class IngredientFilter(filters.FilterSet):
    name = IngredientNameFilter()

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name='author__id')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['tags', 'author']

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favby__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(
                targeted__user=self.request.user)
        return queryset
