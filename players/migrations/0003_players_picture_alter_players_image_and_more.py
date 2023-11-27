# Generated by Django 4.1.4 on 2023-11-07 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_alter_players_firstname_alter_players_gradyear_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='players',
            name='picture',
            field=models.ImageField(default='default.jpg', upload_to='profile_images'),
        ),
        migrations.AlterField(
            model_name='players',
            name='image',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='players',
            name='slug',
            field=models.SlugField(blank=True, default=''),
        ),
    ]
