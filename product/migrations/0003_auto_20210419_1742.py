# Generated by Django 3.1.5 on 2021-04-19 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210309_1853'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='category',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Active Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='extension',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Extension'),
        ),
        migrations.AddField(
            model_name='product',
            name='file',
            field=models.FileField(null=True, upload_to='mockup-file/%d/%m/%Y/', verbose_name='MockUp File'),
        ),
        migrations.AddField(
            model_name='product',
            name='resolution',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Resolution'),
        ),
    ]
