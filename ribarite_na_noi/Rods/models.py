from django.contrib.auth.models import User
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator,
                                    MinLengthValidator,
                                    )
from django.db import models


class Rod(models.Model):
    ROD_TYPE_CHOICES = (
        ("", "Избери тип"),
        ("Мач", "Мач"),
        ("Телемач", "Телемач"),
        ("Телескоп", "Телескоп"),
        ("Спининг", "Спининг"),
        ("Друг", "Друг"),
    )

    ROD_ACTION_CHOICES = (
        ("", "Избери акция"),
        ("1-5", "1-5"),
        ("1-8", "1-8"),
        ("5-12", "5-12"),
        ("10-27", "10-27"),
        ("20-40", "20-40"),
        ("10-50", "10-50"),
        ("40-80", "40-80"),
        ("Друг", "Друг"),
    )

    ROD_TYPE_MAX_LENGTH = 12

    MIN_ROD_LENGTH = 0.5
    MAX_ROD_LENGTH = 14

    MIN_ROD_GUIDES = 3
    MAX_ROD_GUIDES = 14

    MIN_ROD_NAME_LENGTH = 3
    MAX_ROD_NAME_LENGTH = 20

    MAX_ACTION_LENGTH = 10

    MAX_COLOR_LENGTH = 15

    rod_type = models.CharField(
        max_length=ROD_TYPE_MAX_LENGTH,
        null=False,
        blank=False,
        choices=ROD_TYPE_CHOICES,
        verbose_name="Тип",
    )

    length = models.FloatField(
        null=False,
        blank=False,
        validators=(
            MinValueValidator(MIN_ROD_LENGTH),
            MaxValueValidator(MAX_ROD_LENGTH),
        ),
        verbose_name="Дължина",
    )

    guides = models.PositiveIntegerField(
        null=False,
        blank=False,
        validators=(
            MinValueValidator(MIN_ROD_GUIDES),
            MaxValueValidator(MAX_ROD_GUIDES),
        ),
        verbose_name="Брой Водачи",
    )

    rod_name = models.CharField(
        null=False,
        blank=False,
        max_length=MAX_ROD_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_ROD_NAME_LENGTH),
        ),
        verbose_name="Име на модел",
    )

    action = models.CharField(
        null=False,
        blank=False,
        max_length=MAX_ACTION_LENGTH,
        choices=ROD_ACTION_CHOICES,
        verbose_name="Акция",
    )

    color = models.CharField(
        null=False,
        blank=False,
        max_length=MAX_COLOR_LENGTH,
        validators=(
            MinLengthValidator(3),
        ),
        verbose_name="Цвят",
    )

    price = models.FloatField(
        null=False,
        blank=False,
        validators=(
            MinValueValidator(10),
            MaxValueValidator(2500),
        ),
        verbose_name="Цена",
    )

    image = models.URLField(
        null=True,
        blank=True,
        verbose_name="Снимка URL",
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )

    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   )
