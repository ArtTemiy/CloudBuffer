# Generated by Django 3.2.9 on 2022-03-25 13:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('Files', '0004_auto_20220325_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_path',
            field=models.CharField(default='', max_length=1024),
            preserve_default=False,
        ),
    ]
