# Generated by Django 2.2.10 on 2020-02-05 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='desc',
            field=models.CharField(default='', max_length=100),
        ),
    ]