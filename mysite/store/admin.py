from django.contrib import admin
from .models import Category, Customer, Product, Order, TelegramUser

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)


# Telegram User identify
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'first_name', 'last_name', 'created_at', 'last_login_at')
    search_fields = ('telegram_id', 'username', 'first_name', 'last_name')
    ordering = ('-last_login_at',)
