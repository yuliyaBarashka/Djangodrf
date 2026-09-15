import requests
from django.core.mail import send_mail
from django.conf import settings


def send_telegram_message(text):
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return False
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': settings.TELEGRAM_CHAT_ID, 'text': text, 'parse_mode': 'HTML'}
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram error: {e}")
        return False


def send_email_notification(name, phone, email, message):
    subject = "🔔 Новая заявка с сайта M2Bilingual"
    body = f"""
Новая заявка с сайта M2Bilingual:

👤 Имя: {name}
📞 Телефон: {phone}
📧 Email: {email or 'не указан'}
💬 Сообщение: {message or 'нет'}

---
Отправлено автоматически с m2bilingual.ru
"""
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['zohn12333@gmail.com'],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False