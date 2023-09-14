# Generated by Django 3.2 on 2023-09-14 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_comment_review'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'default_related_name': 'comments', 'ordering': ['pub_date']},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='created',
            new_name='pub_date',
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.CharField(max_length=2048, verbose_name='Текст отзыва'),
        ),
    ]