# Generated by Django 3.1.7 on 2021-03-20 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fcuser',
            name='level',
            field=models.CharField(choices=[('user', 'user'), ('admin', 'admin')], default='hhjg6272@naver.com', max_length=8, verbose_name='등급'),
            preserve_default=False,
        ),
    ]
