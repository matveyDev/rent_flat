from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager
from django.core.validators import RegexValidator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=25, verbose_name='Имя')
    last_name = models.CharField(max_length=25, verbose_name='Фамилия')
    email = models.EmailField(max_length=254, unique=True, verbose_name='Email')
    phone = models.CharField(
        validators=[RegexValidator(regex='^\1?\d{9,11}$')],
        max_length=11, blank=True, verbose_name='Телефон',
        )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']