from rest_framework import generics
from products.models import Product
from products.permissions import IsSeller, IsSuperUser, IsShopOwner
from products.serializers import ProductSerializer


class ProductCreateView(generics.CreateAPIView):
    """
    Контроллер для публикации продукта.
    Доступ к контроллеру имеется только у суперпользователя и пользователей со статусом "Продавец".
    """

    serializer_class = ProductSerializer
    permission_classes = [IsSeller | IsSuperUser]

    def perform_create(self, serializer):

        new_product = serializer.save(seller=self.request.user)
        new_product.seller = self.request.user
        new_product.save()


class ProductListView(generics.ListCreateAPIView):
    """
    Контроллер для просмотра размещенных на площадке товарах.
    Доступ к контроллеру имеется только у суперпользователя и пользователей со статусом "Продавец".
    Каждый продавец видит список только своих товаров, суперпользователь видит все размещенные товары.
    """

    serializer_class = ProductSerializer
    permission_classes = [IsSeller | IsSuperUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Product.objects.all()

        return Product.objects.filter(seller=self.request.user)


class ProductDetailView(generics.RetrieveAPIView):
    """
    Контроллер для просмотра детальной информации о товаре.
    Информацию о товаре может просмотреть только тот продавец, который разместил данный товар.
    Суперпользователь может просматривать детальную информацию всех размещенных товаров.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsShopOwner | IsSuperUser]


class ProductDeleteView(generics.DestroyAPIView):
    """
    Контроллер для удаления размещенного на площадке товара.
    Удалить товар может только тот продавец, который разместил данный товар.
    Суперпользователь может удалить любой размещенный товар.
    """

    queryset = Product.objects.all()
    permission_classes = [IsShopOwner | IsSuperUser]
