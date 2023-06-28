import io

from django.shortcuts import get_object_or_404

from .filters import IngredientFilter, RecipeFilter
from django.http import FileResponse
from rest_framework import status
from django.db.models import Sum
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from foodgram.models import (Tags, Ingredients, Recipe, Recipe_ingredients,
                             Favourites,
                             ShoppingCard
                             )
from .permissions import IsAuthorOrReadOnly
from .serializers import (TagSerializer, RecipeCUDSerializer, RecipeSerializer,
                          CroppedRecipeListSerializer, IngredientSerializer)
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly,
                                        AllowAny)


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Tags.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return RecipeCUDSerializer
        else:
            return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_to(self, model, user, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        obj, created = model.objects.get_or_create(user=user, recipe=recipe)
        if created:
            serializer = CroppedRecipeListSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

    def delete_from(self, model, user, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        obj = get_object_or_404(model, user=user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        url_path='favorite',
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to(Favourites, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_from(Favourites, request.user, pk)

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        url_path='shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def shopping_card(self, request, pk):
        if request.method == 'POST':
            return self.add_to(ShoppingCard, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_from(ShoppingCard, request.user, pk)

    @action(
        detail=False,
        methods=('GET',),
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        shopping_cart = (
            Recipe_ingredients.objects.filter(
                recipe__targeted__user=request.user
            )
            .values('ingredients__name',
                    'ingredients__measurement_unit', )
            .annotate(amount=Sum('amount'))
            .order_by('ingredients__name')
        )

        buffer = io.StringIO()

        for item in shopping_cart:
            buffer.write(f"{item['ingredients__name']}\t")
            buffer.write(f"{item['amount']}\t")
            buffer.write(f"{item['ingredients__measurement_unit']} \n")

        response = FileResponse(buffer.getvalue(), content_type='text/plain')
        response[
            'Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
        return response
