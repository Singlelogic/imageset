# Generated by Django 3.1 on 2020-08-05 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageproc', '0003_auto_20200804_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]