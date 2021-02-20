# Generated by Django 3.1.2 on 2021-02-20 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Price')),
                ('start_date', models.DateTimeField(verbose_name='Start Date')),
                ('end_date', models.DateTimeField(verbose_name='End date')),
                ('barcode', models.PositiveSmallIntegerField(unique=True, verbose_name='Barcode')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'tickets',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tickets_app.ticket', verbose_name='Ticket')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
    ]