from django.contrib import admin
from .models import Category

class CategorAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategorAdmin)