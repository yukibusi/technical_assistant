# Generated by Django 5.0.6 on 2024-06-21 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant_app', '0002_group_groupitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
