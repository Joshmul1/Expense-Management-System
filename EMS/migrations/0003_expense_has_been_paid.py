# Generated by Django 2.2.7 on 2020-03-17 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS', '0002_expense_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='has_been_paid',
            field=models.BooleanField(default=False),
        ),
    ]
