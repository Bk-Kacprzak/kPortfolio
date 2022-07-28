from django import forms


def style_form(fields, attrs):
    input_type = 'text'
    for field in fields.items():
        if "password" in field[0]:
            input_type = 'password'
        else:
            input_type = 'text'
        attrs['type'] = input_type
        field[1].widget = forms.TextInput(attrs=attrs)
