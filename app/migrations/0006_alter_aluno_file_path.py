# Generated by Django 3.2.9 on 2021-12-09 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20211207_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='file_path',
            field=models.CharField(default='default.png', max_length=255),
        ),
    ]
