# Generated by Django 3.1.3 on 2021-02-05 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20210205_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='invite',
            field=models.CharField(default='IJS47L', max_length=6),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='meeting_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
