# Generated by Django 2.0.5 on 2018-07-29 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20180729_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storelocation',
            name='phoneNum',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
