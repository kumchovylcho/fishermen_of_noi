from django import forms

from ribarite_na_noi.Rods.models import Rod
from ribarite_na_noi.common.functionality import (generate_widgets,
                                                  generate_labels,
                                                  )


class CreateRodForm(forms.ModelForm):

    class Meta:
        model = Rod
        fields = "__all__"
        exclude = ("created_by", "created_on", "updated_on")

        labels = generate_labels(model,
                                 1,
                                 -3,
                                 )

        field_data = {
                'rod_type': {"form": forms.Select, "choices": model.ROD_TYPE_CHOICES},
                'length': {"form": forms.NumberInput, "placeholder": 'Дължина (Пример: 3.80)'},
                'guides': {"form": forms.NumberInput, 'placeholder': 'Брой Водачи'},
                'rod_name': {"form": forms.TextInput, 'placeholder': 'Име на въдицата'},
                'action': {"form": forms.Select, "choices": model.ROD_ACTION_CHOICES},
                'color': {"form": forms.TextInput, 'placeholder': 'Цвят'},
                'price': {"form": forms.TextInput, 'placeholder': 'Цена ЛЕВА'},
                'image': {"form": forms.TextInput, 'placeholder': 'Снимка URL (по избор)'},
                }

        widgets = generate_widgets(model,
                                   field_data,
                                   1,
                                   -3,
                                   )


class SortRodsForm(forms.Form):
    sort_categories = (
        ('length', 'Дължина (възходящ)'),
        ('-length', 'Дължина (низходящ)'),
        ('action', 'Акция (възходящ)'),
        ('-action', 'Акция (низходящ)'),
        ('price', 'Цена (възходящ)'),
        ('-price', 'Цена (низходящ)'),
    )

    sort_by = forms.ChoiceField(
        choices=sort_categories,
        label="Сортирай по",
        required=False,
    )


class FilterRodsForm(forms.Form):
    filter_choices = (
        ("", "Избери тип"),
        ("Мач", "Мач"),
        ("Телемач", "Телемач"),
        ("Телескоп", "Телескоп"),
        ("Спининг", "Спининг"),
        ("", "Избери акция"),
        ("1-5", "1-5"),
        ("1-8", "1-8"),
        ("5-12", "5-12"),
        ("10-27", "10-27"),
        ("20-40", "20-40"),
        ("10-50", "10-50"),
        ("40-80", "40-80"),
    )

    filter_by = forms.ChoiceField(
        choices=filter_choices,
        label="Филтрирай по",
        required=False,
    )