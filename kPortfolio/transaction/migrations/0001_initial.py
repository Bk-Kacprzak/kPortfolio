# Generated by Django 3.2.13 on 2022-07-28 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('asset', '0001_initial'),
        ('portfolio', '0003_alter_portfolio_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.FloatField(verbose_name='Price')),
                ('total_cost', models.PositiveIntegerField(blank=True, null=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='asset.asset')),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.portfolio')),
            ],
            options={
                'verbose_name': 'Portfolio',
                'verbose_name_plural': 'Portfolios',
            },
        ),
    ]