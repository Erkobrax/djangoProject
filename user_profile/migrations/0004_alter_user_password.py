# Generated by Django 3.2.9 on 2022-01-01 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_auto_20220101_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=25, verbose_name='password1'),
        ),
    ]
