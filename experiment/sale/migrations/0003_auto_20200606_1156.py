# Generated by Django 3.0 on 2020-06-06 01:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0002_unleashedlineitem_unleashedsalesorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unleashedsalesorder',
            name='reqd_date',
        ),
        migrations.AddField(
            model_name='unleashedsalesorder',
            name='install_date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='unleashedsalesorder',
            name='jurisdiction',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='unleashedsalesorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]
