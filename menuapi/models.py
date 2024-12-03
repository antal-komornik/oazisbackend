from django.db import models
from django.utils import timezone
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


# class Category(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name
class Category(models.Model):
    name = models.CharField(max_length=100)
    # Új mező a sorrend meghatározásához
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']  # Alapértelmezett rendezés az order mező szerint

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class MenuItem(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='menu_items')
#     # ingredients = models.ManyToManyField(Ingredient, related_name='menu_items')
#     ingredients = models.ManyToManyField(Ingredient, related_name='menu_items', blank=True)
#     discount_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
#     discount_start = models.DateTimeField(null=True, blank=True)
#     discount_end = models.DateTimeField(null=True, blank=True)
#     is_hidden = models.BooleanField(default=False)
#     image = models.ImageField(upload_to='menu_items/', null=True, blank=True)


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=0)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='menu_items')
    ingredients = models.ManyToManyField(
        Ingredient, related_name='menu_items', blank=True)
    discount_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    discount_start = models.DateTimeField(null=True, blank=True)
    discount_end = models.DateTimeField(null=True, blank=True)
    is_hidden = models.BooleanField(default=False)
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ha már létezik ilyen slug, akkor számot adunk hozzá
            counter = 1
            original_slug = self.slug
            while MenuItem.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def is_on_discount(self):
        now = timezone.now()
        return (self.discount_price is not None and
                self.discount_start is not None and
                self.discount_end is not None and
                self.discount_start <= now <= self.discount_end)

    @property
    def current_price(self):
        return self.discount_price if self.is_on_discount else self.price


class DailyMenu(models.Model):
    date = models.DateField()
    soup = models.ForeignKey(
        MenuItem, on_delete=models.SET_NULL, null=True, related_name='soup_of_day')
    main_course1 = models.ForeignKey(
        MenuItem, on_delete=models.SET_NULL, null=True, related_name='main_course1_of_day')
    main_course2 = models.ForeignKey(
        MenuItem, on_delete=models.SET_NULL, null=True, related_name='main_course2_of_day')

    def __str__(self):
        return f"Menu for {self.date}"
