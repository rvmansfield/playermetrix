# Generated by Django 4.1.4 on 2023-04-09 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0013_players_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='BLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('details', models.TextField(blank=True, default=None)),
            ],
            options={
                'verbose_name_plural': 'Blog',
            },
        ),
    ]
