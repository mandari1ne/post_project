from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Subscription

class SubscriptionInline(admin.TabularInline):
    model = Subscription
    fk_name = "subscriber"
    extra = 1

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('icon', 'level',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('icon', 'level',)}),
    )
    inlines = [SubscriptionInline]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscription)
