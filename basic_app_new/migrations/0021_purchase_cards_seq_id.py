# Generated by Django 3.1.4 on 2021-07-04 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app_new', '0020_auto_20210627_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_cards',
            name='seq_id',
            field=models.IntegerField(default=0),
        ),
    ]