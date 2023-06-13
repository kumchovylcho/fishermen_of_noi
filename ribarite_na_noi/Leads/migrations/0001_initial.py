# Generated by Django 4.2 on 2023-06-13 23:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lead_type', models.CharField(choices=[('', 'Избери форма'), ('Капка', 'Капка'), ('Круша', 'Круша'), ('Молив', 'Молив')], verbose_name='Форма')),
                ('grams', models.CharField(choices=[('', 'Избери грамаж'), ('10', '10'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'), ('40', '40'), ('45', '45'), ('50', '50'), ('55', '55'), ('60', '60'), ('65', '65'), ('70', '70'), ('Друг', 'Друг')], verbose_name='Грамаж')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0.1, message='Няма толкова евтино олово с цена под 0.1 лв.'), django.core.validators.MaxValueValidator(2.0, message='Няма толкова скъпо олово с цена над 2.0 лв.')], verbose_name='Цена')),
                ('image', models.URLField(blank=True, null=True, verbose_name='Снимка URL')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
