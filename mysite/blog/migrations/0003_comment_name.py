# Generated by Django 3.1.4 on 2020-12-26 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(default='anonumus', max_length=30),
        ),
    ]
