# Generated by Django 3.1.7 on 2021-06-24 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app_new', '0013_food_diary_new_seq_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food_diary_new',
            name='seq_id',
            field=models.IntegerField(default=0),
        ),
    ]
