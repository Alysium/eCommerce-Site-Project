# Generated by Django 2.0.5 on 2018-07-21 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_store_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storelocation',
            name='streetName',
        ),
        migrations.RemoveField(
            model_name='storelocation',
            name='streetNumber',
        ),
        migrations.AddField(
            model_name='storelocation',
            name='address',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='storelocation',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='storelocation',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
