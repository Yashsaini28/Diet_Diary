# Generated by Django 3.1.7 on 2021-06-24 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app_new', '0018_remove_purchase_cards_calorie_saturated_fats'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_cards',
            name='calorie_saturated_fats',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
