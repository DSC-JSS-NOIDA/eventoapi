# Generated by Django 2.1.2 on 2018-10-17 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20181017_0339'),
    ]

    operations = [
        migrations.AddField(
            model_name='society',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
