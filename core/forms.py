from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ваше имя'}))
    phone = forms.CharField(max_length=20, required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+7 (___) ___-__-__'}))
    email = forms.EmailField(required=False,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email (необязательно)'}))
    message = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Комментарий (необязательно)', 'rows': 3}))
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput())