from django.contrib.auth.models import AbstractUser
from django.db import models
from custom_user.user_manager import CustomUserManager


NULLABLE = {'blank': True, 'null': True}


class CustomUser(AbstractUser):
    """
    Расширение стандартной модели пользователя в соответствии с требованиями текущего проекта.
    """

    class VisitorStatus(models.IntegerChoices):
        """
        Вспомогательный класс для определения статуса посетителя магазина.
        По умолчанию, каждый новый пользователь имеет статус 'Посетитель'.
        """

        COMMON_USER = 0, "Посетитель"
        SELLER = 1, "Продавец"

    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)

    is_seller = models.BooleanField(choices=VisitorStatus.choices, default=VisitorStatus.COMMON_USER,
                                    verbose_name='Статус посетителя')

    is_active = models.BooleanField(default=True, verbose_name='Статус активации')

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
