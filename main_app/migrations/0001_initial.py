# Generated by Django 3.1.3 on 2021-02-05 00:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('author', models.CharField(blank=True, max_length=500, null=True)),
                ('desc', models.TextField(blank=True, max_length=10000, null=True)),
                ('isbn', models.CharField(blank=True, max_length=15, null=True)),
                ('image', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club_name', models.CharField(max_length=100)),
                ('invite', models.CharField(default='0PSMEU', max_length=6)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votes', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.book')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.club')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('meeting_link', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('chapters', models.CharField(default='All', max_length=100)),
                ('book', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.book')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.club')),
            ],
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disc_type', models.CharField(choices=[('comment', 'Comment'), ('quesiton', 'Discussion Question'), ('quote', 'Quote')], max_length=100)),
                ('comment', models.TextField(max_length=10000)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.meeting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.club'),
        ),
    ]
