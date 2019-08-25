# Generated by Django 2.0.5 on 2018-06-24 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brandName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='GeneralItemDictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shoeName', models.CharField(max_length=200)),
                ('shoeDescription', models.CharField(max_length=1000)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Brand')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Gender')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additionalName', models.CharField(blank=True, max_length=100, null=True)),
                ('colorway', models.CharField(blank=True, max_length=1000, null=True)),
                ('productDescription', models.CharField(blank=True, max_length=1000, null=True)),
                ('color', models.ManyToManyField(to='products.Color')),
                ('generalItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.GeneralItemDictionary')),
            ],
        ),
        migrations.CreateModel(
            name='ProductPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageName', models.CharField(max_length=200)),
                ('displayImage', models.BooleanField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ShoeStyle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='generalitemdictionary',
            name='style',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ShoeStyle'),
        ),
    ]