# Generated by Django 3.2 on 2023-09-23 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0014_auto_20230922_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.CharField(blank=True, default='', max_length=256, null=True, verbose_name='Описание'),
        ),
    ]
