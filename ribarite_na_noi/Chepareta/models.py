from django.contrib.auth.models import User
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator,
                                    )
from django.db import models


class Chepare(models.Model):

    TYPE_CHOICES = (
        ('', "Избери тип"),
        ("За сафрид", "За сафрид"),
        ("За чернокоп", "За чернокоп"),
        ("За карагьоз", "За карагьоз"),
        ("За паламуд", "За паламуд"),
        ("Друг", "Друг"),
    )

    HOOK_COUNT_CHOICES = (
        ("", "Брой куки"),
        ("10", "10"),
        ("12", "12"),
        ("14", "14"),
        ("16", "16"),
        ("18", "18"),
        ("20", "20"),
        ("Друг", "Друг"),
    )

    HOOK_NUMBER_CHOICES = (
        ("", "Номер кука"),
        ("12", "12"),
        ("11", "11"),
        ("10", "10"),
        ("9", "9"),
        ("8", "8"),
        ("7", "7"),
        ("6", "6"),
        ("5", "5"),
        ("4", "4"),
        ("3", "3"),
        ("2", "2"),
        ("1", "1"),
        ("Друг", "Друг"),
    )

    COLOR_CHOICES = (
        ("", "Цвят"),
        ("Черга", "Черга"),
        ("Зелено", "Зелено"),
        ("Жълто", "Жълто"),
        ("Синьо", "Синьо"),
        ("Червено", "Червено"),
        ("Тиква", "Тиква"),
        ("Друг", "Друг"),
    )

    MAIN_LINE_THICKNESS_MIN_VALUE = 0.20
    MAIN_LINE_THICKNESS_MAX_VALUE = 0.60

    MAIN_LINE_THICKNESS_MIN_VALUE_ERROR_MSG = f"Основната линия не може да бъде по-тънка от {MAIN_LINE_THICKNESS_MIN_VALUE}"
    MAIN_LINE_THICKNESS_MAX_VALUE_ERROR_MSG = f"Основната линия не може да бъде по-дебела от {MAIN_LINE_THICKNESS_MAX_VALUE}"

    SEMI_MAIN_LINE_THICKNESS_MIN_VALUE = 0.16
    SEMI_MAIN_LINE_THICKNESS_MIN_VALUE_ERROR_MSG = f"Бидема не може да бъде по-тънък от {SEMI_MAIN_LINE_THICKNESS_MIN_VALUE}"
    SEMI_MAIN_LINE_THICKNESS_MAX_VALUE_ERROR_MSG = "Бидема не може да бъде по-дебел от основната линия"

    MIN_PRICE_VALUE = 4
    MIN_PRICE_VALUE_ERROR_MSG = f"Няма толкова евтино чепаре с цена под {MIN_PRICE_VALUE} лв."

    MAX_PRICE_VALUE = 20
    MAX_PRICE_VALUE_ERROR_MSG = f"Няма толкова скъпо чепаре с цена над {MAX_PRICE_VALUE} лв."

    type = models.CharField(
        blank=False,
        null=False,
        choices=TYPE_CHOICES,
        verbose_name="Тип",
    )

    number_of_hooks = models.CharField(
        blank=False,
        null=False,
        choices=HOOK_COUNT_CHOICES,
        verbose_name="Брой куки",
    )

    hook_number = models.CharField(
        blank=False,
        null=False,
        choices=HOOK_NUMBER_CHOICES,
        verbose_name="Номер кука",
    )

    main_line_thickness = models.FloatField(
        blank=False,
        null=False,
        validators=(
            MinValueValidator(MAIN_LINE_THICKNESS_MIN_VALUE,
                              message=MAIN_LINE_THICKNESS_MIN_VALUE_ERROR_MSG
                              ),
            MaxValueValidator(MAIN_LINE_THICKNESS_MAX_VALUE,
                              message=MAIN_LINE_THICKNESS_MAX_VALUE_ERROR_MSG
                              ),
        ),
        verbose_name="Майка",
    )

    semi_main_line_thickness = models.FloatField(
        blank=False,
        null=False,
        validators=(
            MinValueValidator(SEMI_MAIN_LINE_THICKNESS_MIN_VALUE,
                              message=SEMI_MAIN_LINE_THICKNESS_MIN_VALUE_ERROR_MSG
                              ),
        ),
        verbose_name="Бидем",
    )

    color = models.CharField(
        blank=False,
        null=False,
        choices=COLOR_CHOICES,
        verbose_name="Цвят",
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
