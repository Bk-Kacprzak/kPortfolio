# Generated by Django 3.2.13 on 2022-06-10 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_rename_username_user_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='first_name',
        ),
    ]
