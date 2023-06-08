from django import forms

from ribarite_na_noi.Reels.models import Reel
from ribarite_na_noi.common.functionality import (generate_widgets,
                                                  generate_labels,
                                                  )


class CreateReelForm(forms.ModelForm):

    class Meta:
        model = Reel
        fields = "__all__"
        exclude = ("created_by", "created_on", "updated_on")

        labels = generate_labels(model,
                                 1,
                                 -3,
                                 )

        field_data = {
            'size': {"form": forms.Select, "choices": model.SIZE_CHOICES},
            'gear_ratio': {"form": forms.Select, "choices": model.GEAR_RATIO_CHOICES},
            'model': {"form": forms.TextInput, 'placeholder': 'Модел на макарата'},
            'weight': {"form": forms.NumberInput, 'placeholder': 'Тегло (гр.)'},
            'bearings': {"form": forms.NumberInput, 'placeholder': 'Лагери (броя)'},
            'price': {"form": forms.NumberInput, 'placeholder': 'Цена ЛЕВА'},
            'image': {"form": forms.TextInput, 'placeholder': 'Снимка URL (по избор)'},
        }

        widgets = generate_widgets(model,
                                   field_data,
                                   1,
                                   -3,
                                   )


class SortReelsForm(forms.Form):
    sort_categories = (
        ('-price', 'Цена (низходяща)'),
        ('price', 'Цена (възходяща)'),
        ('size', 'Размер (възходящ)'),
        ('-size', 'Размер (низходящ)'),
        ('gear_ratio', 'Пред.число (възходящ)'),
        ('-gear_ratio', 'Пред.число (низходящ)'),
    )

    sort_by = forms.ChoiceField(
        choices=sort_categories,
        label="Сортирай по",
        required=False,
    )


class FilterReelsForm(forms.Form):
    filter_choices = (
        ('', 'Избери размер'),
        ("1000", "1000"),
        ("2000", "2000"),
        ("3000", "3000"),
        ("4000", "4000"),
        ("5000", "5000"),
        ("6000", "6000"),
        ("7000", "7000"),
        ("8000", "8000"),
        ('', 'Пред.число'),
        ("4.2:1", "4.2:1"),
        ("4.9:1", "4.9:1"),
        ("5:1", "5:1"),
        ("5.2:1", "5.2:1"),
        ("5.3:1", "5.3:1"),
        ("5.4:1", "5.4:1"),
        ("5.7:1", "5.7:1"),
        ("6.1:1", "6.1:1"),
        ("6.2:1", "6.2:1"),
        ("6.5:1", "6.5:1"),
    )

    filter_by = forms.ChoiceField(
        choices=filter_choices,
        label="Филтрирай по",
        required=False,
    )