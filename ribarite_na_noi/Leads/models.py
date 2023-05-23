from django.contrib.auth.models import User
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator,
                                    )
from django.db import models


class Lead(models.Model):

    LEAD_CHOICES = (
        ("", "Избери форма"),
        ("Капка", "Капка"),
        ("Круша", "Круша"),
        ("Молив", "Молив"),
    )

    GRAM_CHOICES = (
        ("", "Избери грамаж"),
        ("10", "10"),
        ("20", "20"),
        ("25", "25"),
        ("30", "30"),
        ("35", "35"),
        ("40", "40"),
        ("45", "45"),
        ("50", "50"),
        ("55", "55"),
        ("60", "60"),
        ("65", "65"),
        ("70", "70"),
        ("Друг", "Друг"),
    )

    MIN_PRICE_VALUE = 0.10
    MIN_PRICE_VALUE_ERROR_MSG = f"Няма толкова евтино олово с цена под {MIN_PRICE_VALUE} лв."
    MAX_PRICE_VALUE = 2.00
    MAX_PRICE_VALUE_ERROR_MSG = f"Няма толкова скъпо олово с цена над {MAX_PRICE_VALUE} лв."

    lead_type = models.CharField(
        null=False,
        blank=False,
        choices=LEAD_CHOICES,
        verbose_name="Форма",
    )

    grams = models.CharField(
        null=False,
        blank=False,
        choices=GRAM_CHOICES,
        verbose_name="Грамаж",
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

