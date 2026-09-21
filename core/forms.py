from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ваше имя',
            'required': 'required',
            'minlength': '2',
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '+7 (___) ___-__-__',
            'required': 'required',
            'pattern': r'[\d\s\+\-\(\)]{10,}',
            'title': 'Введите корректный номер телефона (минимум 10 цифр)',
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email (необязательно)',
        })
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Комментарий (необязательно)',
            'rows': 3,
        })
    )

    # Чекбокс согласия на обработку ПД
    consent = forms.BooleanField(
        required=True,
        label='Я согласен(а) на обработку персональных данных',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox',
            'id': 'consent-checkbox',
        }),
        error_messages={
            'required': 'Необходимо согласие на обработку персональных данных',
        }
    )

    # Honeypot от ботов
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput())