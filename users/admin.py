from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User, Payment


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email', 'first_name', 'last_name',
        'is_teacher', 'is_student', 'is_staff', 'is_active',
    )
    list_filter = (
        'is_teacher', 'is_student', 'is_staff',
        'is_active', 'is_superuser', 'groups',
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'city')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'phone', 'city', 'avatar', 'bio')
        }),
        ('Роли', {
            'fields': ('is_teacher', 'is_student', 'is_staff', 'is_active', 'is_superuser')
        }),
        ('Права', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        ('Даты', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_teacher', 'is_student'),
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'amount', 'payment_method',
        'status', 'payment_date',
    )
    list_filter = ('status', 'payment_method')
    search_fields = ('user__email',)
    readonly_fields = ('payment_date', 'stripe_session_id', 'stripe_payment_url')
    date_hierarchy = 'payment_date'
