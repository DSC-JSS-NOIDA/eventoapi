# Generated by Django 2.1.2 on 2018-10-27 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20181027_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='registration_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
