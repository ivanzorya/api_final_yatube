# Generated by Django 3.1.1 on 2020-09-08 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20200908_2021'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique',
        ),
    ]
