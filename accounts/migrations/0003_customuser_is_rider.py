# Generated by Django 2.2.14 on 2020-07-17 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200715_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_rider',
            field=models.BooleanField(default=False),
        ),
    ]