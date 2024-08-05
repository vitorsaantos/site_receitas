from django.contrib import admin
from .models import Category, Recipe



class CategorAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeADmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategorAdmin)