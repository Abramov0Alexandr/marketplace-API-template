from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from custom_user.models import CustomUser
from custom_user.serializers import CustomUserListSerializer, CustomUserCreateSerializer


class CustomUserListView(generics.ListAPIView):
    """Контроллер для отображения списка зарегистрированных пользователей"""

    serializer_class = CustomUserListSerializer
    queryset = CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('is_seller', )


class CustomUserCreateView(generics.CreateAPIView):
    """Контроллер для регистрации новых пользователей"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserCreateSerializer
