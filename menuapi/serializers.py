from rest_framework import serializers, viewsets
from .models import Category, MenuItem, DailyMenu, Ingredient, PizzaPricing
from django.forms.models import model_to_dict



class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'order']


# class MenuItemSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     category_id = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all(), write_only=True)
#     ingredients = IngredientSerializer(many=True, read_only=True)
#     ingredient_ids = serializers.PrimaryKeyRelatedField(
#         queryset=Ingredient.objects.all(), write_only=True, many=True, required=False, default=list)
#     is_on_discount = serializers.BooleanField(read_only=True)
#     current_price = serializers.DecimalField(
#         max_digits=6, decimal_places=2, read_only=True)
#     image = serializers.ImageField(required=False)

#     class Meta:
#         model = MenuItem
#         fields = ['id', 'name', 'description', 'price', 'category', 'category_id',
#                   'ingredients', 'ingredient_ids', 'discount_price', 'discount_start',
#                   'discount_end', 'is_on_discount', 'current_price', 'is_hidden', 'image']

#     def create(self, validated_data):
#         category_id = validated_data.pop('category_id')
#         ingredient_ids = validated_data.pop('ingredient_ids', [])
#         validated_data['category'] = category_id
#         menu_item = MenuItem.objects.create(**validated_data)
#         menu_item.ingredients.set(ingredient_ids)
#         return menu_item

#     def update(self, instance, validated_data):
#         category_id = validated_data.pop('category_id', None)
#         ingredient_ids = validated_data.pop('ingredient_ids', None)
#         if category_id:
#             instance.category = category_id
#         if ingredient_ids is not None:
#             instance.ingredients.set(ingredient_ids)
#         return super().update(instance, validated_data)


class PizzaPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaPricing
        fields = ['price_32', 'price_40', 'price_60']


class MenuItemSerializer(serializers.ModelSerializer):
    pizza_pricing = PizzaPricingSerializer(read_only=True)
    price = serializers.FloatField()  # Decimal helyett float

    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'description', 'price', 'category',
            'ingredients', 'is_pizza', 'pizza_pricing'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_pizza:
            data['prices'] = {
                # "price_32": str(instance.pizza_pricing.price_32),
                # "price_40": str(instance.pizza_pricing.price_40),
                # "price_60": str(instance.pizza_pricing.price_60)
                32: instance.pizza_pricing.price_32,
                40: instance.pizza_pricing.price_40,
                60: instance.pizza_pricing.price_60

            }
            data.pop('price')  # Eltávolítjuk az alap árat pizzáknál
        return data

# class MenuItemSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     category_id = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all(), write_only=True)
#     ingredients = IngredientSerializer(many=True, read_only=True)
#     ingredient_ids = serializers.PrimaryKeyRelatedField(
#         queryset=Ingredient.objects.all(), write_only=True, many=True, required=False, default=list)
#     is_on_discount = serializers.BooleanField(read_only=True)
#     current_price = serializers.DecimalField(
#         max_digits=6, decimal_places=2, read_only=True)
#     image = serializers.ImageField(required=False)
#     url = serializers.HyperlinkedIdentityField(
#         view_name='menuitem-detail',
#         lookup_field='slug'
#     )

#     class Meta:
#         model = MenuItem
#         fields = ['id', 'url', 'name', 'slug', 'description', 'price', 'category', 'category_id',
#                   'ingredients', 'ingredient_ids', 'discount_price', 'discount_start',
#                   'discount_end', 'is_on_discount', 'current_price', 'is_hidden', 'image']


# class DailyMenuSerializer(serializers.ModelSerializer):
#     soup = MenuItemSerializer(read_only=True)
#     main_course1 = MenuItemSerializer(read_only=True)
#     main_course2 = MenuItemSerializer(read_only=True)
#     soup_id = serializers.PrimaryKeyRelatedField(
#         queryset=MenuItem.objects.all(), write_only=True)
#     main_course1_id = serializers.PrimaryKeyRelatedField(
#         queryset=MenuItem.objects.all(), write_only=True)
#     main_course2_id = serializers.PrimaryKeyRelatedField(
#         queryset=MenuItem.objects.all(), write_only=True)

#     class Meta:
#         model = DailyMenu
#         fields = ['id', 'date', 'soup', 'main_course1', 'main_course2',
#                   'soup_id', 'main_course1_id', 'main_course2_id']

#     def create(self, validated_data):
#         soup_id = validated_data.pop('soup_id')
#         main_course1_id = validated_data.pop('main_course1_id')
#         main_course2_id = validated_data.pop('main_course2_id')
#         validated_data['soup'] = soup_id
#         validated_data['main_course1'] = main_course1_id
#         validated_data['main_course2'] = main_course2_id
#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         for field in ['soup', 'main_course1', 'main_course2']:
#             field_id = validated_data.pop(f'{field}_id', None)
#             if field_id:
#                 setattr(instance, field, field_id)
#         return super().update(instance, validated_data)


class DailyMenuSerializer(serializers.ModelSerializer):
    soup = MenuItemSerializer(read_only=True)
    main_course1 = MenuItemSerializer(read_only=True)
    main_course2 = MenuItemSerializer(read_only=True)
    soup_name = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), write_only=True)
    main_course1_name = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), write_only=True)
    main_course2_name = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), write_only=True)

    class Meta:
        model = DailyMenu
        fields = ['id', 'date', 'soup', 'main_course1', 'main_course2',
                  'soup_name', 'main_course1_name', 'main_course2_name']

    def to_representation(self, instance):
        # Az eredeti objektum szerializĂˇlĂˇsa
        data = super().to_representation(instance)

        # ĂtalakĂ­tĂˇs tĂ¶mbbĂ©
        menu_items = []
        if data['soup']:
            menu_items.append({**data['soup'], 'type': 'soup'})
        if data['main_course1']:
            menu_items.append({**data['main_course1'], 'type': 'main_course1'})
        if data['main_course2']:
            menu_items.append({**data['main_course2'], 'type': 'main_course2'})

        # Visszaadjuk a kĂ­vĂˇnt formĂˇtumban
        return {
            'id': data['id'],
            'date': data['date'],
            'menu_items': menu_items
        }

    def create(self, validated_data):
        soup_name = validated_data.pop('soup_name')
        main_course1_name = validated_data.pop('main_course1_name')
        main_course2_name = validated_data.pop('main_course2_name')
        validated_data['soup'] = soup_name
        validated_data['main_course1'] = main_course1_name
        validated_data['main_course2'] = main_course2_name
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for field in ['soup', 'main_course1', 'main_course2']:
            field_id = validated_data.pop(f'{field}_name', None)
            if field_id:
                setattr(instance, field, field_id)
        return super().update(instance, validated_data)

# class DailyMenuSerializer(serializers.ModelSerializer):
#     soup = MenuItemSerializer(read_only=True)
#     main_course1 = MenuItemSerializer(read_only=True)
#     main_course2 = MenuItemSerializer(read_only=True)
#     soup_id = serializers.PrimaryKeyRelatedField(
#         queryset=MenuItem.objects.all(), write_only=True)
#     main_course1_id = serializers.PrimaryKeyRelatedField(
#         queryset=MenuItem.objects.all(), write_only=True)
#     main_course2_id = serializers.PrimaryKeyRelatedField(
#         queryset=MenuItem.objects.all(), write_only=True)

#     class Meta:
#         model = DailyMenu
#         fields = ['id', 'date', 'soup', 'main_course1', 'main_course2',
#                   'soup_id', 'main_course1_id', 'main_course2_id']

#     def to_representation(self, instance):
#         # Az eredeti objektum szerializálása
#         data = super().to_representation(instance)

#         # Átalakítás tömbbé
#         menu_items = []
#         if data['soup']:
#             menu_items.append({**data['soup'], 'type': 'soup'})
#         if data['main_course1']:
#             menu_items.append({**data['main_course1'], 'type': 'main_course1'})
#         if data['main_course2']:
#             menu_items.append({**data['main_course2'], 'type': 'main_course2'})

#         # Visszaadjuk a kívánt formátumban
#         return {
#             'id': data['id'],
#             'date': data['date'],
#             'menu_items': menu_items
#         }

#     def create(self, validated_data):
#         soup_id = validated_data.pop('soup_id')
#         main_course1_id = validated_data.pop('main_course1_id')
#         main_course2_id = validated_data.pop('main_course2_id')
#         validated_data['soup'] = soup_id
#         validated_data['main_course1'] = main_course1_id
#         validated_data['main_course2'] = main_course2_id
#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         for field in ['soup', 'main_course1', 'main_course2']:
#             field_id = validated_data.pop(f'{field}_id', None)
#             if field_id:
#                 setattr(instance, field, field_id)
#         return super().update(instance, validated_data)
