from rest_framework import serializers
from custom_user.models import CustomUser


class CustomersListSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели CustomUser.
    Используется при вызове GET запросов в контроллере CustomUserListView
    """

    class Meta:
        model = CustomUser
        fields = '__all__'


class VisitorSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели CustomUser.
    Используется при регистрации ОБЫЧНЫХ пользователей в контроллере CustomUserCreateView.
    :password_confirmation: поле для подтверждения введенного пароля. Обработка исключений происходит в методе create.
    """

    password_confirmation = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    patronymic = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'patronymic', 'email', 'password', 'password_confirmation', )

    def create(self, validated_data):
        """
        :param validated_data: Данные, переданные при создании нового пользователя.
        Метод переопределен для корректного создания нового пользователя.
        Пароль указанный при создании пользователя хэшируется, появляется возможность авторизации по JWT.
        :return: Создается новый экземпляр класса CustomUser.
        """

        password_confirmation = validated_data.pop('password_confirmation', None)

        if password_confirmation is None:
            raise serializers.ValidationError("Поле 'password_confirmation' обязательно")

        if validated_data.get('password') != password_confirmation:
            raise serializers.ValidationError("Пароль и его подтверждение не совпадают")

        new_common_user = CustomUser.objects.create_user(**validated_data)
        return new_common_user


class SellerSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели CustomUser.
    Используется при регистрации пользователей со статусом ПРОДАВЕЦ.
    При вызове данного сериализатора устанавливается необходимость указывать следующие поля:
    :shop_name: Название магазина, поле обязательно к заполнению.
    :product_images: Изображения товара, поле является необязательным.
    """

    shop_name = serializers.CharField()
    product_images = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('shop_name', 'product_images', 'email', )

    def create(self, validated_data):
        new_seller = CustomUser.objects.create_user(**validated_data)
        return new_seller
