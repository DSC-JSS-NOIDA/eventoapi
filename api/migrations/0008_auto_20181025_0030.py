# Generated by Django 2.1.2 on 2018-10-24 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20181025_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('0', 'Regular'), ('1', 'Admin')], default='0', max_length=1),
        ),
    ]
