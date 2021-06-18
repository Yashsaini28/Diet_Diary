# Generated by Django 3.1.7 on 2021-05-19 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app_new', '0003_auto_20210519_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase_det_new',
            name='ss_code',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporary_new',
            name='ss_code',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporary_purchase_new',
            name='ss_code',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction_det_new',
            name='ss_code',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unsaved_new',
            name='ss_code',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unsaved_purchase_new',
            name='ss_code',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
