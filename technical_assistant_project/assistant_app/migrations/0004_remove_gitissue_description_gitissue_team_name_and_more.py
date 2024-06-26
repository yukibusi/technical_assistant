# Generated by Django 5.0.6 on 2024-06-21 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant_app', '0003_alter_group_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gitissue',
            name='description',
        ),
        migrations.AddField(
            model_name='gitissue',
            name='team_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='gitissue',
            name='url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
