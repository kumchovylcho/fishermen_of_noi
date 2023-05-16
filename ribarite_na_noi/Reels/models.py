from django.contrib.auth.models import User
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator,
                                    MinLengthValidator,
                                    )
from django.db import models


class Reel(models.Model):
    SIZE_CHOICES = (
        ('', 'Избери размер'),
        ("1000", "1000"),
        ("2000", "2000"),
        ("3000", "3000"),
        ("4000", "4000"),
        ("5000", "5000"),
        ("6000", "6000"),
        ("7000", "7000"),
        ("8000", "8000"),
        ("Друг", "Друг"),
    )

    GEAR_RATIO_CHOICES = (
        ('', 'Пред.число'),
        ("4.2:1", "4.2:1"),
        ("4.9:1", "4.9:1"),
        ("5:1", "5:1"),
        ("5.2:1", "5.2:1"),
        ("5.3:1", "5.3:1"),
        ("5.4:1", "5.4:1"),
        ("6.1:1", "6.1:1"),
        ("6.2:1", "6.2:1"),
        ("4.9:1", "4.9:1"),
        ("4.9:1", "4.9:1"),
        ("Друг", "Друг"),
    )

    MODEL_MIN_LENGTH = 4
    MODEL_MAX_LENGTH = 30
    MODEL_ERROR_MSG = f"Не съществува модел с толкова кратко име, моля въведи модел с минимум {MODEL_MIN_LENGTH} символа"

    MIN_WEIGHT_VALUE = 80
    MAX_WEIGHT_VALUE = 500
    MIN_WEIGHT_ERROR_MSG = f"Не съществува толкова лека макара.Въведи минимум {MIN_WEIGHT_VALUE}гр."
    MAX_WEIGHT_ERROR_MSG = f"Не съществува толкова тежка макара.Въведи максимум до {MAX_WEIGHT_VALUE}гр."

    MAX_BEARINGS = 15
    MAX_BEARINGS_ERROR_MSG = f"Макарата не може да има повече от {MAX_BEARINGS} лагера"

    MIN_PRICE_VALUE = 20
    MAX_PRICE_VALUE = 2500
    MIN_PRICE_VALUE_ERROR_MSG = f"Няма такава макара която струва по-малко от {MIN_PRICE_VALUE} лв."
    MAX_PRICE_VALUE_ERROR_MSG = f"Няма такава макара която струва повече от {MAX_PRICE_VALUE} лв."

    size = models.CharField(
        blank=False,
        null=False,
        choices=SIZE_CHOICES,
        verbose_name="Размер",
    )

    gear_ratio = models.CharField(
        blank=False,
        null=False,
        verbose_name="Пред.число",
        choices=GEAR_RATIO_CHOICES,
    )

    model = models.CharField(
        blank=False,
        null=False,
        max_length=MODEL_MAX_LENGTH,
        verbose_name="Модел",
        validators=(
            MinLengthValidator(MODEL_MIN_LENGTH,
                               message=MODEL_ERROR_MSG
                               ),
        ),
    )

    weight = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="Тегло (гр.)",
        validators=(
            MinValueValidator(MIN_WEIGHT_VALUE,
                              message=MIN_WEIGHT_ERROR_MSG
                              ),
            MaxValueValidator(MAX_WEIGHT_VALUE,
                              message=MAX_WEIGHT_ERROR_MSG
                              ),
        ),
    )

    bearings = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="Лагери",
        validators=(
            MaxValueValidator(MAX_BEARINGS,
                              message=MAX_BEARINGS_ERROR_MSG
                              ),
        ),
    )

    price = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="Цена",
        validators=(
            MinValueValidator(MIN_PRICE_VALUE,
                              message=MIN_PRICE_VALUE_ERROR_MSG
                              ),
            MaxValueValidator(MAX_PRICE_VALUE,
                              message=MAX_PRICE_VALUE_ERROR_MSG
                              ),
        ),
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
