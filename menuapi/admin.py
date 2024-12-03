from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, MenuItem, DailyMenu, Ingredient

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(DailyMenu)
admin.site.register(Ingredient)