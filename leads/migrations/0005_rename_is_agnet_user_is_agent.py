# Generated by Django 4.0.2 on 2022-07-08 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0004_alter_lead_agent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_agnet',
            new_name='is_agent',
        ),
    ]
