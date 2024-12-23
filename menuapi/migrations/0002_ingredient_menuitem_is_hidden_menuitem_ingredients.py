# Generated by Django 5.1.2 on 2024-10-16 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menuapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='menuitem',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='ingredients',
            field=models.ManyToManyField(related_name='menu_items', to='menuapi.ingredient'),
        ),
    ]
