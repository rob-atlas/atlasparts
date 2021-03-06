# Generated by Django 3.0 on 2020-06-12 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnleashedShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=50, null=True)),
                ('street', models.CharField(max_length=50, null=True)),
                ('town', models.CharField(max_length=50, null=True)),
                ('state', models.CharField(max_length=50, null=True)),
                ('postcode', models.CharField(max_length=8, null=True)),
                ('country', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnleashedVenueAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=50, null=True)),
                ('street', models.CharField(max_length=50, null=True)),
                ('town', models.CharField(max_length=50, null=True)),
                ('state', models.CharField(max_length=50, null=True)),
                ('postcode', models.CharField(max_length=8, null=True)),
                ('country', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='unleashedsalesorder',
            name='customer_reference',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='unleashedsalesorder',
            name='delivery_name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
