from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, MenuItem, DailyMenu, Ingredient, PizzaPricing
from django.core.exceptions import ValidationError
from django.forms import ModelForm


class PizzaPricingInline(admin.StackedInline):
    model = PizzaPricing
    can_delete = False
    max_num = 1  # Csak egy PizzaPricing lehet

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(menu_item__category__name="Pizza")

    def has_add_permission(self, request, obj=None):
        # Csak akkor engedélyezzük az új PizzaPricing hozzáadását, ha még nincs
        if obj is None:
            return True
        return not hasattr(obj, 'pizza_pricing')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    inlines = [PizzaPricingInline]
    list_display = ['name', 'category', 'get_price_display']

    def get_price_display(self, obj):
        if obj.is_pizza and hasattr(obj, 'pizza_pricing'):
            pricing = obj.pizza_pricing
            return f"32 cm: {pricing.price_32}Ft, 40 cm: {pricing.price_40}Ft, 60 cm: {pricing.price_60}Ft"
        return f"{obj.price}Ft"
    get_price_display.short_description = 'Ár'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_pizza and not hasattr(obj, 'pizza_pricing'):
            PizzaPricing.objects.create(menu_item=obj)

admin.site.register(Category)
# admin.site.register(MenuItem)
admin.site.register(DailyMenu)
admin.site.register(Ingredient)
