# Generated by Django 4.1.4 on 2023-11-05 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
        ('members', '0005_alter_profile_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='player',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='players.players'),
        ),
    ]
