# Generated by Django 2.1.2 on 2018-10-24 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20181023_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='society',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Society'),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
