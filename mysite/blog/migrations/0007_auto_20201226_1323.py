# Generated by Django 3.1.4 on 2020-12-26 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20201226_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(default='anonumus', max_length=30),
        ),
    ]
