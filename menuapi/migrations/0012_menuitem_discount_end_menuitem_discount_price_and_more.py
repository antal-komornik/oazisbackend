# Generated by Django 5.1.2 on 2024-12-05 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menuapi', '0011_alter_menuitem_category_alter_menuitem_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='discount_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='discount_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]