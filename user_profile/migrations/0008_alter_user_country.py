# Generated by Django 3.2.9 on 2022-01-02 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0007_auto_20220101_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(default='Global', max_length=30, verbose_name='country'),
        ),
    ]
