from django import forms

from ribarite_na_noi.Leads.models import Lead
from ribarite_na_noi.common.functionality import (generate_labels,
                                                  generate_widgets,
                                                  )


class CreateLeadForm(forms.ModelForm):

    class Meta:
        model = Lead
        fields = "__all__"
        exclude = ("created_by", "created_on", "updated_on")

        labels = generate_labels(model,
                                 1,
                                 -3,
                                 )

        field_data = {
            'lead_type': {"form": forms.Select, "choices": model.LEAD_CHOICES},
            'grams': {"form": forms.Select, "choices": model.GRAM_CHOICES},
            'price': {"form": forms.NumberInput, 'placeholder': 'Цена ЛЕВА'},
            'image': {"form": forms.TextInput, 'placeholder': 'Снимка URL (по избор)'},
        }

        widgets = generate_widgets(model,
                                   field_data,
                                   1,
                                   -3,
                                   )


class SortLeadsForm(forms.Form):
    sort_categories = (
        ('-price', 'Цена (низходяща)'),
        ('price', 'Цена (възходяща)'),
        ('-lead_type', 'форма (ЯЮ)'),
        ('lead_type', 'форма (АБВ)'),
        ('-grams', 'Грамаж (низходящ)'),
        ('grams', 'Грамаж (възходящ)'),
    )

    sort_by = forms.ChoiceField(
        choices=sort_categories,
        label="Сортирай по",
        required=False,
    )


class FilterLeadsForm(forms.Form):
    filter_choices = (
        ("", "Избери форма"),
        ("Капка", "Капка"),
        ("Круша", "Круша"),
        ("Молив", "Молив"),
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

    filter_by = forms.ChoiceField(
        choices=filter_choices,
        label="Филтрирай по",
        required=False,
    )