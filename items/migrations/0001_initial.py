# Generated by Django 2.2.14 on 2020-07-11 06:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('photo', django_resized.forms.ResizedImageField(crop=None, force_format='PNG', keep_meta=True, quality=0, size=[600, 600], upload_to='items')),
                ('expected_price', models.IntegerField(default=0)),
                ('expected_store', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('delivered', models.BooleanField(default=False)),
                ('closed', models.BooleanField(default=False)),
                ('closed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
