from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import ContactRequest
from .utils import send_vk_message, send_email_notification
from django.conf import settings


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

            # VK
            vk_text = (
                f"🔔 Новая заявка\n\n"
                f"👤 Имя: {contact_obj.name}\n"
                f"📞 Телефон: {contact_obj.phone}\n"
                f"📧 Email: {contact_obj.email or 'не указан'}\n"
                f"💬 Сообщение: {contact_obj.message or 'нет'}"
            )
            send_vk_message(vk_text)

            messages.success(request, 'Спасибо! Заявка отправлена. Мы свяжемся с вами.')
            return redirect('core:contact')

    return render(request, 'core/contact.html', {'form': form})


def privacy_policy(request):
    """Политика обработки персональных данных"""
    context = {
        'operator_name': settings.OPERATOR_FULL_NAME,
        #'operator_inn': settings.OPERATOR_INN,
        'operator_email': settings.OPERATOR_EMAIL,
        'site_url': settings.SITE_URL,
    }
    return render(request, 'core/privacy.html', context)


def consent(request):
    """Согласие на обработку персональных данных"""
    context = {
        'operator_name': settings.OPERATOR_FULL_NAME,
        #'operator_inn': settings.OPERATOR_INN,
        'operator_email': settings.OPERATOR_EMAIL,
        'site_url': settings.SITE_URL,
    }
    return render(request, 'core/consent.html', context)


def kids_view(request):
    """Страница M2Bilingual Kids (заглушка)"""
    return render(request, 'core/kids.html')
