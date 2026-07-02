import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from main.models import PlayerProfile, PlayerMetric, Event

User = get_user_model()

# Maps CSV column names to PlayerMetric.metricType choices
METRIC_MAP = {
    'Height':    'height',
    'Weight':    'weight',
    'IF Velo':   'ifvelo',
    'OF Velo':   'ofvelo',
    'C Velo':    'catchvelo',
    'Pop Time':  'poptime',
    'Exit Velo': 'exitvelo',
    '60 Yard':   'sixtyyard',
    'FB':        'fbvelo',
    'Change':    'changeup',
    'Curve /Sl': 'slider',
}


class Command(BaseCommand):
    help = 'Import player profiles and metrics from an event results CSV (guilford.csv format)'

    def add_arguments(self, parser):
        parser.add_argument('--file', required=True, type=str, help='Path to the CSV file')
        parser.add_argument('--user', type=str, help='Username to assign imported profiles to (default: first superuser)')
        parser.add_argument('--event', type=int, help='Event ID to link all imported metrics to (optional)')

    def handle(self, *args, **options):
        file_path = options['file']
        if not os.path.isabs(file_path):
            file_path = os.path.join(settings.BASE_DIR, file_path)

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        user = self._resolve_user(options.get('user'))
        if not user:
            return

        event = None
        if options.get('event'):
            try:
                event = Event.objects.get(pk=options['event'])
                self.stdout.write(f'Linking metrics to event: {event}')
            except Event.DoesNotExist:
                self.stderr.write(self.style.ERROR(f'Event ID {options["event"]} not found'))
                return

        profiles_created = profiles_skipped = metrics_created = metrics_skipped = errors = 0

        with open(file_path, newline='', encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                first = (row.get('First') or row.get('First Name') or '').strip()
                last = (row.get('Name') or row.get('Last Name') or '').strip()

                if not first and not last:
                    continue

                grad_year = self._parse_int(row.get('Grad Year') or row.get('Team'))
                player_age = self._age_from_grad_year(grad_year)

                # --- Profile ---
                profile, created = PlayerProfile.objects.get_or_create(
                    firstName=first,
                    lastName=last,
                    graduation_year=grad_year,
                    defaults={
                        'user': user,
                        'team': row.get('Team', '').strip() or None,
                        'graduation_year': grad_year,
                    }
                )
                if created:
                    profiles_created += 1
                else:
                    profiles_skipped += 1

                # --- Metrics ---
                for csv_col, metric_type in METRIC_MAP.items():
                    value = self._parse_decimal(row.get(csv_col))
                    if value is None:
                        continue

                    # Skip if this exact measurement already exists for this player+type+event
                    if PlayerMetric.objects.filter(
                        profile=profile,
                        metricType=metric_type,
                        metric=value,
                        event=event,
                    ).exists():
                        metrics_skipped += 1
                        continue

                    try:
                        PlayerMetric.objects.create(
                            profile=profile,
                            metricType=metric_type,
                            metric=value,
                            playerAge=player_age,
                            gradClass=grad_year or 2026,
                            event=event,
                            capturedBy='Player Metrix',
                        )
                        metrics_created += 1
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f'  Error saving {metric_type} for {first} {last}: {e}'))
                        errors += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nDone.\n'
            f'  Profiles:  {profiles_created} created, {profiles_skipped} already existed\n'
            f'  Metrics:   {metrics_created} created, {metrics_skipped} skipped, {errors} errors'
        ))

    def _resolve_user(self, username):
        if username:
            try:
                return User.objects.get(username=username)
            except User.DoesNotExist:
                self.stderr.write(self.style.ERROR(f'User "{username}" not found'))
                return None
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            self.stderr.write(self.style.ERROR('No superuser found. Use --user <username> to specify one.'))
        return user

    def _age_from_grad_year(self, grad_year):
        if not grad_year:
            return 16
        from datetime import date
        age = 18 - (grad_year - date.today().year)
        return max(12, min(20, age))

    def _parse_int(self, value):
        if not value or str(value).strip() == '':
            return None
        try:
            return int(float(str(value).strip()))
        except (ValueError, TypeError):
            return None

    def _parse_decimal(self, value):
        if value is None:
            return None
        s = str(value).strip()
        if s in ('', '0', '0.0', '0.00'):
            return None
        try:
            v = float(s)
            return v if v > 0 else None
        except (ValueError, TypeError):
            return None
