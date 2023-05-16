# Generated by Django 4.2 on 2023-05-12 02:37

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
            name='Braid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, validators=[django.core.validators.MinLengthValidator(3, message='Името на влакното не може да бъде под 3 символа')], verbose_name='Име на влакно')),
                ('thickness', models.CharField(choices=[('', 'Дебелина'), ('#0.2', '#0.2'), ('#0.3', '#0.3'), ('#0.4', '#0.4'), ('#0.5', '#0.5'), ('#0.6', '#0.6'), ('#0.8', '#0.8'), ('#1', '#1'), ('#1.2', '#1.2'), ('#1.5', '#1.5'), ('#2', '#2'), ('Друг', 'Друг')], verbose_name='Дебелина')),
                ('strength', models.CharField(choices=[('', 'Издръжливост (кг)'), ('2.5кг', '2.5кг'), ('3кг', '3кг'), ('3.3кг', '3.3кг'), ('3.8кг', '3.8кг'), ('4.2кг', '4.2кг'), ('5.4кг', '5.4кг'), ('6кг', '6кг'), ('6.8кг', '6.8кг'), ('8кг', '8кг'), ('10кг', '10кг'), ('Друг', 'Друг')], verbose_name='Издръжливост')),
                ('length', models.CharField(choices=[('', 'Дължина (м)'), ('150', '150м.'), ('200', '200м.'), ('250', '250м.'), ('300', '300м.'), ('500', '500м.')], verbose_name='Дължина (м)')),
                ('is_colored', models.BooleanField(choices=[('', 'Избери'), (False, 'Не'), (True, 'Да')], verbose_name='Шарено ли е ?')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(10, message='Няма толкова евтино влакно с цена под 10 лв.'), django.core.validators.MaxValueValidator(300, message='Няма толкова скъпо влакно с цена над 300 лв.')], verbose_name='Цена')),
                ('image', models.URLField(blank=True, null=True, verbose_name='Снимка URL')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
