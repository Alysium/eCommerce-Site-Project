# Generated by Django 2.0.5 on 2018-07-21 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20180720_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='storelocation',
            name='streetName',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='storelocation',
            name='streetNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
