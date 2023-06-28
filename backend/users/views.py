from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    )
from rest_framework.permissions import IsAuthenticated
from .pagination import CustomPaginator
from .serializers import (
                          SubsAuthorsListSerializer,
                          )
from .models import CustomUser, Subscriptions


class MySubscribtionsAPIView(generics.ListAPIView):
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
        except Exception:
            return Response({
                "error": "Невозможно подписаться на то , чего не существует"},
                status=HTTP_404_NOT_FOUND)
        try:
            author.auth_token
        except Exception:
            return Response({"error": "Данный пользователь не авторизован"},
                            status=HTTP_401_UNAUTHORIZED)
        if Subscriptions.objects.filter(user=user, author=author):
            return Response({
                "error": "Вы уже подписаны на данного пользователя"},
                status=HTTP_400_BAD_REQUEST)
        Subscriptions.objects.create(user=user, author=author)
        serializer = SubsAuthorsListSerializer(
            author, context={'request': request})
        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        try:
            author = CustomUser.objects.get(id=id)
        except Exception:
            return Response({
                "error": "Невозможно отписаться от того , чего не существует"},
                status=HTTP_404_NOT_FOUND)
        try:
            author.auth_token
        except Exception:
            return Response({"error": "Данный пользователь не авторизован"},
                            status=HTTP_401_UNAUTHORIZED)
        try:
            a = Subscriptions.objects.get(user=user, author=author)
        except Exception:
            return Response({
                "error": "Вы не подписаны на данного пользователя"},
                            status=HTTP_400_BAD_REQUEST)
        else:
            a.delete()
            return Response(status=HTTP_204_NO_CONTENT)
