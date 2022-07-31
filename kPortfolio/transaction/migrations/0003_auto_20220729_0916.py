# Generated by Django 3.2.13 on 2022-07-29 07:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_transaction_notes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='total_cost',
            new_name='amount',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='notes',
        ),
        migrations.AddField(
            model_name='transaction',
            name='cost',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.datetime.today, null=True, verbose_name='Transaction date'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('1', 'buy'), ('2', 'sell')], default='buy', max_length=5, verbose_name='Transaction type'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
