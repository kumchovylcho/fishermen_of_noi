from django import forms

from ribarite_na_noi.Chepareta.models import Chepare
from ribarite_na_noi.common.functionality import (generate_labels,
                                                  generate_widgets,
                                                  )


class CreateChepareForm(forms.ModelForm):

    class Meta:
        model = Chepare
        fields = "__all__"
        exclude = ("created_by", "created_on", "updated_on")

        labels = generate_labels(model,
                                 1,
                                 -3,
                                 )

        field_data = {
            'type': {"form": forms.Select, 'choices': model.TYPE_CHOICES},
            'number_of_hooks': {"form": forms.Select, "choices": model.HOOK_COUNT_CHOICES},
            'hook_number': {"form": forms.Select, "choices": model.HOOK_NUMBER_CHOICES},
            'main_line_thickness': {"form": forms.NumberInput, "placeholder": "Основна линия (0.30)"},
            'semi_main_line_thickness': {"form": forms.NumberInput, 'placeholder': 'Бидем (0.18)'},
            'color': {"form": forms.Select, 'choices': model.COLOR_CHOICES},
            'price': {"form": forms.NumberInput, 'placeholder': "Цена в ЛЕВА"},
            'image': {"form": forms.TextInput, 'placeholder': 'Снимка URL (по избор)'},
        }

        widgets = generate_widgets(model,
                                   field_data,
                                   1,
                                   -3,
                                   )

    def clean_semi_main_line_thickness(self):
        main_line = self.cleaned_data.get('main_line_thickness')
        semi_main_line = self.cleaned_data.get('semi_main_line_thickness')

        if main_line and semi_main_line:
            if semi_main_line >= main_line:
                raise forms.ValidationError(Chepare.SEMI_MAIN_LINE_THICKNESS_MAX_VALUE_ERROR_MSG)

        return semi_main_line


class SortCheparetaForm(forms.Form):
    sort_categories = (
        ('-price', 'Цена (низходяща)'),
        ('price', 'Цена (възходяща)'),
        ('-number_of_hooks', 'Бр.куки (низходящи)'),
        ('number_of_hooks', 'Бр.куки (възходящи)'),
        ('-hook_number', 'Номер кука (низходяща)'),
        ('hook_number', 'Номер кука (възходяща)'),
        ('-main_line_thickness', 'Дебелина майка (низходяща)'),
        ('main_line_thickness', 'Дебелина майка (възходяща)'),
    )

    sort_by = forms.ChoiceField(
        choices=sort_categories,
        label="Сортирай по",
        required=False,
    )


class FilterCheparetaForm(forms.Form):
    filter_choices = (
        ('', "Избери тип"),
        ("За сафрид", "За сафрид"),
        ("За чернокоп", "За чернокоп"),
        ("За карагьоз", "За карагьоз"),
        ("За паламуд", "За паламуд"),
        ("", "Брой куки"),
        ("10", "10"),
        ("12", "12"),
        ("14", "14"),
        ("16", "16"),
        ("18", "18"),
        ("20", "20"),
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
        ("", "Цвят"),
        ("Черга", "Черга"),
        ("Зелено", "Зелено"),
        ("Жълто", "Жълто"),
        ("Синьо", "Синьо"),
        ("Червено", "Червено"),
        ("Тиква", "Тиква"),
    )

    filter_by = forms.ChoiceField(
        choices=filter_choices,
        label="Филтрирай по",
        required=False,
    )
