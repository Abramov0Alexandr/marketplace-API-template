from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from custom_user.models import CustomUser
from custom_user.serializers import CustomersListSerializer, VisitorSerializer, SellerSerializer


class CustomersListView(generics.ListAPIView):
    """Контроллер для отображения списка зарегистрированных пользователей."""

    serializer_class = CustomersListSerializer
    queryset = CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('is_seller', )
    permission_classes = IsAdminUser


class CustomerCreateView(generics.CreateAPIView):
    """Контроллер для регистрации новых пользователей."""

    def get_serializer_class(self):
        """
        Метод переопределен для выбора конкретного сериализатора в зависимости от переданных в POST запросе данных.
        """

        is_seller = self.request.data.get('is_seller', None)

        if is_seller:
            return SellerSerializer

        return VisitorSerializer

    def create(self, request, *args, **kwargs):
        is_seller = request.data.get('is_seller', False)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if is_seller:
                # Если выбран статус продавца, устанавливаем его
                serializer.save(is_seller=CustomUser.UserStatus.SELLER)

            else:
                # Если выбран статус посетителя, оставляем его по умолчанию
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
