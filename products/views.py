from rest_framework import generics, status
from rest_framework.response import Response
from products.models import Product
from products.permissions import IsSeller, IsSuperUser, IsShopOwner
from products.serializers import ProductSerializer, ProductSaleStatusSerializers


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

        total_price = new_product.calculate_final_price()
        new_product.price = total_price
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


class ChangeProductSaleStatus(generics.UpdateAPIView):
    """
    Контроллер, отвечающий за снятие товара с продажи.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSaleStatusSerializers
    permission_classes = [IsShopOwner | IsSuperUser]

    def get_object(self):
        product = super().get_object()

        if product.is_active_sale:
            product.is_active_sale = False

        else:
            product.is_active_sale = True

        product.save()
        return product

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if instance.is_active_sale:
            sale_status_message = 'выведен в продажу'
        else:
            sale_status_message = 'снят с продажи'

        response_message = {
            "Product info": {'sale status': f'{instance.is_active_sale}',
                             'message': f'{instance.product_title} {sale_status_message}',
                             'status': status.HTTP_200_OK
                             }
        }

        return Response(response_message)


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
