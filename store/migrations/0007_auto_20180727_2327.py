# Generated by Django 2.0.5 on 2018-07-28 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20180727_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='sLogo',
            field=models.ImageField(blank=True, upload_to='storeLogos'),
        ),
    ]
