# Generated by Django 5.1.2 on 2024-11-16 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed'), ('Accepted', 'Accepted')], default='New', max_length=10),
        ),
    ]
