# Generated by Django 2.0.5 on 2018-05-28 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20180528_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/%Y/%m/%d/', verbose_name='Фотография товара'),
        ),
    ]
