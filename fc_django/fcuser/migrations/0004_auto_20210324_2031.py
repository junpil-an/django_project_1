# Generated by Django 3.1.7 on 2021-03-24 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcuser', '0003_auto_20210320_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fcuser',
            name='level',
            field=models.CharField(choices=[('user', 'user'), ('admin', 'admin')], max_length=8, verbose_name='등급'),
        ),
        migrations.AlterField(
            model_name='fcuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='비밀번호'),
        ),
    ]