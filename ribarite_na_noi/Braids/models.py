from django.contrib.auth.models import User
from django.core.validators import (MinLengthValidator,
                                    MinValueValidator,
                                    MaxValueValidator,
                                    )
from django.db import models


class Braid(models.Model):
    NAME_MAX_LENGTH = 15
    NAME_MIN_LENGTH = 3
    NAME_MIN_LENGTH_ERROR_MSG = f"Името на влакното не може да бъде под {NAME_MIN_LENGTH} символа"

    THICKNESS_CHOICES = (
        ('', "Дебелина"),
        ('#0.2', '#0.2'),
        ('#0.3', '#0.3'),
        ('#0.4', '#0.4'),
        ('#0.5', '#0.5'),
        ('#0.6', '#0.6'),
        ('#0.8', '#0.8'),
        ('#1', '#1'),
        ('#1.2', '#1.2'),
        ('#1.5', '#1.5'),
        ('#2', '#2'),
        ('Друг', 'Друг'),
    )

    STRENGTH_CHOICES = (
        ('', 'Издръжливост (кг)'),
        ('2.5кг', '2.5кг'),
        ('3кг', '3кг'),
        ('3.3кг', '3.3кг'),
        ('3.8кг', '3.8кг'),
        ('4.2кг', '4.2кг'),
        ('5.4кг', '5.4кг'),
        ('6кг', '6кг'),
        ('6.8кг', '6.8кг'),
        ('8кг', '8кг'),
        ('10кг', '10кг'),
        ('Друг', 'Друг'),
    )

    LENGTH_CHOICES = (
        ('', 'Дължина (м)'),
        ('150', '150м.'),
        ('200', '200м.'),
        ('250', '250м.'),
        ('300', '300м.'),
        ('500', '500м.'),
    )

    IS_COLORED_CHOICES = (
            ('', 'Избери'),
            (False, "Не"),
            (True, "Да"),
        )

    MIN_PRICE_VALUE = 10
    MIN_PRICE_VALUE_ERROR_MSG = f"Няма толкова евтино влакно с цена под {MIN_PRICE_VALUE} лв."

    MAX_PRICE_VALUE = 300
    MAX_PRICE_VALUE_ERROR_MSG = f"Няма толкова скъпо влакно с цена над {MAX_PRICE_VALUE} лв."

    name = models.CharField(
        blank=False,
        null=False,
        max_length=NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(NAME_MIN_LENGTH, message=NAME_MIN_LENGTH_ERROR_MSG),
        ),
        verbose_name="Име на влакно",
    )

    thickness = models.CharField(
        blank=False,
        null=False,
        choices=THICKNESS_CHOICES,
        verbose_name="Дебелина",
    )

    strength = models.CharField(
        blank=False,
        null=False,
        choices=STRENGTH_CHOICES,
        verbose_name="Издръжливост",
    )

    length = models.CharField(
        blank=False,
        null=False,
        choices=LENGTH_CHOICES,
        verbose_name="Дължина (м)",
    )

    is_colored = models.BooleanField(
        blank=False,
        null=False,
        verbose_name="Шарено ли е ?",
        choices=IS_COLORED_CHOICES,
    )

    price = models.FloatField(
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