from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_add_playerprofile_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playerprofile',
            old_name='slug',
            new_name='player_id',
        ),
    ]
