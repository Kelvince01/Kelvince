# Generated by Django 3.1.3 on 2020-11-30 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20201129_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='description',
            field=models.CharField(max_length=400, null=True),
        ),
    ]
