from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from menuapi.views import (
    CategoryViewSet, MenuItemViewSet, DailyMenuViewSet, IngredientViewSet,
    MenuItemSearchView, MenuItemCategoryFilterView, get_formatted_menu
)
from menuapi import views

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'menu-items', MenuItemViewSet, basename='menuitem')
router.register(r'daily-menu', DailyMenuViewSet)



urlpatterns = [
    path('api/data/admin/', admin.site.urls),
    path('api/data/', include(router.urls)),
    path('api/data/auth/', include('userauth.urls')),
    path('api/data/auth/api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),
    path('api/data/filter/menu-items/',
         MenuItemSearchView.as_view(), name='menuitem-search'),
    path('api/data/filter/menu-items-by-category/',
         MenuItemCategoryFilterView.as_view(), name='menuitem-category-filter'),
    path('api/data/formatted-menu/', views.get_formatted_menu,
         name='formatted-menu'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
