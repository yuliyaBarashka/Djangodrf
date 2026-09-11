import stripe
from django.conf import settings
from django.db import transaction
from users.models import Payment
from lms.models import Course

# Настройка Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course):
    """
    Создание продукта в Stripe

    Args:
        course: объект Course

    Returns:
        dict: данные созданного продукта
    """
    try:
        product = stripe.Product.create(
            name=course.name,
            description=course.description or f"Курс: {course.name}",
        )
        return {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'created': product.created,
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка создания продукта в Stripe: {str(e)}")


def create_stripe_price(course, amount):
    """
    Создание цены в Stripe

    Args:
        course: объект Course
        amount: сумма в рублях (будет конвертирована в копейки)

    Returns:
        dict: данные созданной цены
    """
    try:
        # Конвертируем рубли в копейки
        amount_in_cents = int(amount * 100)

        price = stripe.Price.create(
            product=course.stripe_product_id,  # Используем сохраненный ID продукта
            unit_amount=amount_in_cents,
            currency='rub',
        )
        return {
            'id': price.id,
            'product': price.product,
            'unit_amount': price.unit_amount,
            'currency': price.currency,
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка создания цены в Stripe: {str(e)}")


def create_checkout_session(price_id, success_url, cancel_url):
    """
    Создание сессии для оплаты в Stripe

    Args:
        price_id: ID цены в Stripe
        success_url: URL для успешной оплаты
        cancel_url: URL для отмены оплаты

    Returns:
        dict: данные созданной сессии
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return {
            'id': session.id,
            'url': session.url,
            'payment_status': session.payment_status,
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка создания сессии в Stripe: {str(e)}")


def create_payment_with_stripe(user, course, amount, success_url, cancel_url):
    """
    Создание платежа с интеграцией Stripe

    Args:
        user: объект User
        course: объект Course
        amount: сумма платежа
        success_url: URL для успешной оплаты
        cancel_url: URL для отмены оплаты

    Returns:
        dict: данные платежа с ссылкой на оплату
    """
    with transaction.atomic():
        # 1. Создаем продукт в Stripe (если еще не создан)
        if not course.stripe_product_id:
            product_data = create_stripe_product(course)
            course.stripe_product_id = product_data['id']
            course.save()

        # 2. Создаем цену в Stripe
        price_data = create_stripe_price(course, amount)

        # 3. Создаем сессию для оплаты
        session_data = create_checkout_session(
            price_data['id'],
            success_url,
            cancel_url
        )

        # 4. Сохраняем платеж в БД
        payment = Payment.objects.create(
            user=user,
            course=course,
            amount=amount,
            payment_method='card',  # Stripe использует карты
            stripe_session_id=session_data['id'],
            stripe_payment_url=session_data['url'],
            stripe_price_id=price_data['id'],
            stripe_product_id=course.stripe_product_id,
            status='pending'
        )

        return {
            'payment_id': payment.id,
            'amount': payment.amount,
            'payment_url': session_data['url'],
            'session_id': session_data['id'],
            'status': 'pending',
        }


def retrieve_stripe_session(session_id):
    """
    Получение данных о сессии из Stripe

    Args:
        session_id: ID сессии в Stripe

    Returns:
        dict: данные сессии
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            'id': session.id,
            'payment_status': session.payment_status,
            'customer_details': session.customer_details,
            'amount_total': session.amount_total,
            'currency': session.currency,
            'status': session.status,
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Ошибка получения данных сессии из Stripe: {str(e)}")
    