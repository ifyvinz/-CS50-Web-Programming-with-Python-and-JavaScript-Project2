# Generated by Django 3.1.6 on 2022-05-15 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20220424_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='title',
            field=models.CharField(default='Title', max_length=100),
        ),
    ]
