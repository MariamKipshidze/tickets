# Generated by Django 3.1.2 on 2021-02-20 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets_app', '0003_ticket_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tk_order', to='tickets_app.ticket', verbose_name='Ticket'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
    ]