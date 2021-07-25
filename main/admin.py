from django.contrib import admin
from .models import User, AddItem

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number']


@admin.register(AddItem)
class ItemAdmin(admin.ModelAdmin):
    pass