import requests
from django.core.mail import send_mail
from django.conf import settings


def send_vk_message(text):
    """Отправка сообщения в VK от имени сообщества"""
    if not settings.VK_GROUP_TOKEN or not settings.VK_ADMIN_ID:
        print("VK: токен или admin_id не заданы")
        return False

    url = 'https://api.vk.com/method/messages.send'
    params = {
        'user_id': settings.VK_ADMIN_ID,
        'message': text,
        'random_id': 0,
        'access_token': settings.VK_GROUP_TOKEN,
        'v': '5.131',
    }

    try:
        response = requests.post(url, data=params, timeout=10)
        data = response.json()
        if 'error' in data:
            print(f"VK API error: {data['error']}")
            return False
        print(f"VK: сообщение отправлено, response: {data}")
        return True
    except Exception as e:
        print(f"VK error: {e}")
        return False


def send_email_notification(name, phone, email, message):
    """Отправка email"""
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
            recipient_list=['zohn12333@gmail.com' , 'ut122235@gmail.com'],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False