# Generated by Django 5.0.6 on 2024-05-29 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraperscript', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='oscarfilms',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]