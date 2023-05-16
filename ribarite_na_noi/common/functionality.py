def generate_widgets(model, field_data: dict, start_field=0, last_field=-1, *exclude_fields) -> dict:
    result = {}

    for field in model._meta.get_fields()[start_field:last_field]:
        if field.name in exclude_fields:
            continue

        if field_data[field.name].get("choices", False):
            result[field.name] = field_data[field.name]["form"](
                choices=field_data[field.name]['choices'],
                attrs={
                    "class": 'form-control',
                }
            )
            continue

        result[field.name] = field_data[field.name]["form"](
            attrs={
                'class': 'form-control',
                'placeholder': field_data[field.name]['placeholder'],
            },
        )

    return result


def generate_labels(model, start_field=1, last_field=-1, **use_label):
    result = {}

    for field in model._meta.get_fields()[start_field:last_field]:
        if use_label.get(field.name):
            result[field.name] = use_label[field.name]
            continue

        result[field.name] = ""

    return result
