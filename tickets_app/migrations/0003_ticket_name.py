# Generated by Django 3.1.2 on 2021-02-20 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets_app', '0002_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='name',
            field=models.CharField(default='1', max_length=100, verbose_name='Name'),
        ),
    ]
