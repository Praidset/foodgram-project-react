import io

from django.shortcuts import get_object_or_404
from django.http import FileResponse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny
)
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from foodgram.models import (
    Tag,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Favourite,
    ShoppingCart
)
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    TagSerializer,
    RecipeCUDSerializer,
    RecipeSerializer,
    CroppedRecipeListSerializer,
    IngredientSerializer
)
from .filters import IngredientFilter, RecipeFilter
from users.models import CustomUser, Subscription
from api.pagination import CustomPaginator
from api.serializers import SubsAuthorsListSerializer


class SubscribtionsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPaginator
    serializer_class = SubsAuthorsListSerializer

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(subs__user=user)


class SubscribeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = request.user
        try:
            author = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({
                "error": "Невозможно подписаться на то , чего не существует"},
                status=HTTP_404_NOT_FOUND)
        try:
            author.auth_token
        except CustomUser.auth_token.RelatedObjectDoesNotExist:
            return Response({"error": "Данный пользователь не авторизован"},
                            status=HTTP_401_UNAUTHORIZED)
        if Subscription.objects.filter(user=user, author=author):
            return Response({
                "error": "Вы уже подписаны на данного пользователя"},
                status=HTTP_400_BAD_REQUEST)
        Subscription.objects.create(user=user, author=author)
        serializer = SubsAuthorsListSerializer(
            author, context={'request': request})
        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        try:
            author = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({
                "error": "Невозможно отписаться от того , чего не существует"},
                status=HTTP_404_NOT_FOUND)
        try:
            author.auth_token
        except CustomUser.auth_token.RelatedObjectDoesNotExist:
            return Response({"error": "Данный пользователь не авторизован"},
                            status=HTTP_401_UNAUTHORIZED)
        try:
            subexistence = Subscription.objects.get(user=user, author=author)
        except Subscription.DoesNotExist:
            return Response({
                "error": "Вы не подписаны на данного пользователя"},
                status=HTTP_400_BAD_REQUEST)
        else:
            subexistence.delete()
            return Response(status=HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Ingredient.objects.all()
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
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_to(self, model, user, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        obj, created = model.objects.get_or_create(user=user, recipe=recipe)
        if created:
            serializer = CroppedRecipeListSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            return self.add_to(Favourite, request.user, pk)
        return self.delete_from(Favourite, request.user, pk)

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        url_path='shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def shopping_card(self, request, pk):
        if request.method == 'POST':
            return self.add_to(ShoppingCart, request.user, pk)
        return self.delete_from(ShoppingCart, request.user, pk)

    @action(
        detail=False,
        methods=('GET',),
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        shopping_cart = (
            RecipeIngredient.objects.filter(
                recipe__targeted__user=request.user
            )
            .values('ingredient__name',
                    'ingredient__measurement_unit',
                    'amount')
            .order_by('ingredient__name')
        )

        buffer = io.StringIO()

        for item in shopping_cart:
            buffer.write(f"{item['ingredient__name']}\t")
            buffer.write(f"{item['amount']}\t")
            buffer.write(f"{item['ingredient__measurement_unit']} \n")

        response = FileResponse(buffer.getvalue(), content_type='text/plain')
        response[
            'Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
        return response
