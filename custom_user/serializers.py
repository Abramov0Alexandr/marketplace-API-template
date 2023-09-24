from rest_framework import serializers
from custom_user.models import CustomUser


class CustomUserListSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели CustomUser.
    Используется при вызове GET запросов в контроллере CustomUserListView
    """

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели CustomUser.
    Используется при вызове GET запросов в контроллере CustomUserCreateView
    password_confirmation: поле для подтверждения введенного пароля. Обработка исключений происходит в методе create.
    """

    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password_confirmation', )

    def create(self, validated_data):
        """
        :param validated_data: Данные, переданные при создании нового пользователя
        Метод переопределен для корректного создания нового пользователя.
        Пароль указанный при создании пользователя хэшируется, появляется возможность авторизации по JWT.
        :return: Создается новый экземпляр класса CustomUser
        """

        password_confirmation = validated_data.pop('password_confirmation', None)

        if password_confirmation is None:
            raise serializers.ValidationError("Поле 'password_confirmation' обязательно")

        if validated_data.get('password') != password_confirmation:
            raise serializers.ValidationError("Пароль и его подтверждение не совпадают")

        new_custom_user = CustomUser.objects.create_user(**validated_data)
        return new_custom_user
