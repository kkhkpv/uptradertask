from django.contrib import admin
from .models import MenuModel, MenuItem


@admin.register(MenuItem, MenuModel)
class DefaultAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}
