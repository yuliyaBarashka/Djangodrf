from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import ContactRequest
from .utils import send_telegram_message, send_email_notification


def index(request):
    """Главная страница"""
    return render(request, 'core/index.html')


def contact(request):
    """Страница с формой заявки"""
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Сохраняем в БД
            contact_obj = ContactRequest.objects.create(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data.get('email'),
                message=form.cleaned_data.get('message'),
            )

            # Email
            send_email_notification(
                name=contact_obj.name,
                phone=contact_obj.phone,
                email=contact_obj.email,
                message=contact_obj.message,
            )

            # Telegram
            telegram_text = (
                f"🔔 <b>Новая заявка</b>\n\n"
                f"👤 <b>Имя:</b> {contact_obj.name}\n"
                f"📞 <b>Телефон:</b> {contact_obj.phone}\n"
                f"📧 <b>Email:</b> {contact_obj.email or 'не указан'}\n"
                f"💬 <b>Сообщение:</b> {contact_obj.message or 'нет'}"
            )
            send_telegram_message(telegram_text)

            messages.success(request, 'Спасибо! Заявка отправлена. Мы свяжемся с вами.')
            return redirect('core:contact')

    return render(request, 'core/contact.html', {'form': form})