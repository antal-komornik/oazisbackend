from rest_framework import viewsets, filters, generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, MenuItem, DailyMenu, Ingredient
from .serializers import CategorySerializer, MenuItemSerializer, DailyMenuSerializer, IngredientSerializer
from rest_framework.decorators import api_view
from django.db.models import Prefetch
from collections import OrderedDict

# @api_view(['GET'])
# def get_formatted_menu(request):
#     # Optimalizált lekérdezés az N+1 probléma elkerülésére
#     menu_items = MenuItem.objects.select_related('category').prefetch_related(
#         'ingredients'
#     ).filter(is_hidden=False)

#     # Formázott menü létrehozása
#     formatted_menu = {}

#     # Menüelemek feldolgozása és kategóriákba rendezése
#     for item in menu_items:
#         category_name = item.category.name if item.category else 'Egyéb'

#         # Ha ez az első elem ebben a kategóriában, hozzuk létre a listát
#         if category_name not in formatted_menu:
#             formatted_menu[category_name] = []

#         # Összetevők listájának létrehozása
#         ingredients_list = [
#             ingredient.name for ingredient in item.ingredients.all()]

#         # Menüelem formázása
#         formatted_item = {
#             'id': item.id,
#             'name': item.name,
#             'price': float(item.current_price),
#             'image': request.build_absolute_uri(item.image.url) if item.image else '/images/kv.jpg',
#             'description': item.description,
#             'ingredients': ingredients_list
#         }

#         formatted_menu[category_name].append(formatted_item)

#     # Üres kategóriák lekérése és hozzáadása
#     empty_categories = Category.objects.exclude(
#         name__in=formatted_menu.keys()
#     )

#     # Üres kategóriák hozzáadása üres listákkal
#     for category in empty_categories:
#         formatted_menu[category.name] = []

#     return Response(formatted_menu)


@api_view(['GET'])
def get_formatted_menu(request):
    # Kategóriák lekérése sorrendben
    categories = Category.objects.all().order_by('order')

    # Optimalizált lekérdezés az N+1 probléma elkerülésére
    menu_items = MenuItem.objects.select_related('category').prefetch_related(
        'ingredients'
    ).filter(is_hidden=False)

    # Formázott menü létrehozása OrderedDict használatával
    formatted_menu = OrderedDict()

    # Először hozzuk létre az összes kategóriát (üres listákkal)
    for category in categories:
        formatted_menu[category.name] = []

    # Menüelemek feldolgozása és kategóriákba rendezése
    for item in menu_items:
        category_name = item.category.name if item.category else 'Egyéb'

        # Összetevők listájának létrehozása
        ingredients_list = [
            ingredient.name for ingredient in item.ingredients.all()]

        discount_price = item.discount_price
        discount_start = item.discount_start
        discount_end = item.discount_end
        slug = item.slug
        # Menüelem formázása
        formatted_item = {
            'id': item.id,
            'name': item.name,
            'price': float(item.current_price),
            'image': request.build_absolute_uri(item.image.url) if item.image else '/images/kv.jpg',
            'description': item.description or '',
            'ingredients': ingredients_list,
            'discount_price': discount_price,
            'discount_start': discount_start,
            'discount_end': discount_end,
            'slug': slug,
        }

        # Ha valami miatt a kategória még nem létezik (nem kellene előfordulnia)
        if category_name not in formatted_menu:
            formatted_menu[category_name] = []

        formatted_menu[category_name].append(formatted_item)

    # Az 'Egyéb' kategória mindig legyen utoljára, ha létezik
    if 'Egyéb' in formatted_menu:
        other_items = formatted_menu.pop('Egyéb')
        formatted_menu['Egyéb'] = other_items

    return Response(formatted_menu)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


# class MenuItemViewSet(viewsets.ModelViewSet):
#     serializer_class = MenuItemSerializer
#     parser_classes = (MultiPartParser, FormParser)

#     def get_queryset(self):
#         queryset = MenuItem.objects.all()
#         show_hidden = self.request.query_params.get(
#             'show_hidden', 'false').lower() == 'true'

#         if not show_hidden:
#             queryset = queryset.filter(is_hidden=False)

#         return queryset

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             self.perform_create(serializer)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(
#             instance, data=request.data, partial=partial)

#         if serializer.is_valid():
#             self.perform_update(serializer)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'slug'  # Ez teszi lehetővé a slug alapú keresést

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        show_hidden = self.request.query_params.get(
            'show_hidden', 'false').lower() == 'true'

        if not show_hidden:
            queryset = queryset.filter(is_hidden=False)

        return queryset
# class DailyMenuViewSet(viewsets.ModelViewSet):
#     queryset = DailyMenu.objects.all()
#     serializer_class = DailyMenuSerializer


class DailyMenuViewSet(viewsets.ModelViewSet):
    queryset = DailyMenu.objects.all()
    serializer_class = DailyMenuSerializer

    def list(self, request, *args, **kwargs):
        # Ha speciális formázásra van szükség a lista végpontnál
        response = super().list(request, *args, **kwargs)
        return response

    def retrieve(self, request, *args, **kwargs):
        # Ha speciális formázásra van szükség az egyedi lekérésnél
        response = super().retrieve(request, *args, **kwargs)
        return response
# Új nézetek a keresésekhez


class MenuItemSearchView(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'ingredients__name']

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        show_hidden = self.request.query_params.get(
            'show_hidden', 'false').lower() == 'true'

        if not show_hidden:
            queryset = queryset.filter(is_hidden=False)

        return queryset


class MenuItemCategoryFilterView(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        show_hidden = self.request.query_params.get(
            'show_hidden', 'false').lower() == 'true'

        if not show_hidden:
            queryset = queryset.filter(is_hidden=False)

        return queryset
