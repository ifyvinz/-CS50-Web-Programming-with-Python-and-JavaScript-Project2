# Generated by Django 3.1.6 on 2022-04-09 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20220330_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='auctions/static/auctions/images'),
        ),
    ]