# Generated by Django 5.0.3 on 2024-04-06 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackendWork', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favorite',
            field=models.ManyToManyField(blank=True, null=True, to='BackendWork.product'),
        ),
    ]
