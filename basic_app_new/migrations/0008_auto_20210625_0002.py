# Generated by Django 3.1.7 on 2021-06-24 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app_new', '0007_food_diary_new_seq_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food_diary_new',
            name='seq_id',
            field=models.CharField(max_length=200),
        ),
    ]
