# Generated by Django 4.0.4 on 2022-05-29 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listofcountries',
            old_name='descriptions',
            new_name='description',
        ),
    ]
