

from django.dispatch import receiver
from menuapi.models import MenuItem, PizzaPricing


@receiver(post_save, sender=MenuItem)
def ensure_pizza_pricing(sender, instance, created, **kwargs):
    """
    Biztosítja, hogy minden pizza típusú MenuItem-hez legyen PizzaPricing
    """
    if instance.is_pizza:
        PizzaPricing.objects.get_or_create(menu_item=instance)
