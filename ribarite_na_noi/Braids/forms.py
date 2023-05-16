from django import forms

from ribarite_na_noi.Braids.models import Braid
from ribarite_na_noi.common.functionality import (generate_labels,
                                                  generate_widgets,
                                                  )


class CreateBraidForm(forms.ModelForm):

    class Meta:
        model = Braid
        fields = "__all__"
        exclude = ("created_by", "created_on", "updated_on")

        labels = generate_labels(model,
                                 1,
                                 -3,
                                 is_colored="Шарено ли е ?",
                                 )

        field_data = {
            'name': {"form": forms.TextInput, 'placeholder': 'Име на влакното'},
            'thickness': {"form": forms.Select, "choices": model.THICKNESS_CHOICES},
            'strength': {"form": forms.Select, "choices": model.STRENGTH_CHOICES},
            'length': {"form": forms.Select, "choices": model.LENGTH_CHOICES},
            'is_colored': {"form": forms.BooleanField, 'placeholder': 'Шарено ли е ?'},
            'price': {"form": forms.NumberInput, 'placeholder': 'Цена ЛЕВА'},
            'image': {"form": forms.TextInput, 'placeholder': 'Снимка URL (по избор)'},
        }

        widgets = generate_widgets(model,
                                   field_data,
                                   1,
                                   -3,
                                   "is_colored",
                                   )


class SortBraidsForm(forms.Form):
    sort_categories = (
        ('-price', 'Цена (низходяща)'),
        ('price', 'Цена (възходяща)'),
        ('-thickness', 'Дебелина (низходяща)'),
        ('thickness', 'Дебелина (възходяща)'),
        ('-strength', 'Издръжливост (низходяща)'),
        ('strength', 'Издръжливост (възходяща)'),
        ('-length', 'Дължина (м) (низходящи)'),
        ('length', 'Дължина (м) (възходящи)'),
    )

    sort_by = forms.ChoiceField(
        choices=sort_categories,
        label="Сортирай по",
        required=False,
    )


class FilterBraidsForm(forms.Form):
    filter_choices = (
        ('', 'Избери дебелина'),
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
        ('', 'Избери здравина'),
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
        ('', 'Избери дължина'),
        ('150', '150м.'),
        ('200', '200м.'),
        ('250', '250м.'),
        ('300', '300м.'),
        ('500', '500м.'),
    )

    filter_by = forms.ChoiceField(
        choices=filter_choices,
        label="Филтрирай по",
        required=False,
    )
