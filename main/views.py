from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.contrib import messages
from decimal import Decimal
from .forms import PlayerMetricForm, CaptureForm, PlayerProfileForm
from .models import PlayerMetric, MetricsHistory, MetricsRange, Event
import json
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

# Create your views here.

def index(request):

    return render(request, 'main/index.html')


def players(request):
    from .models import PlayerProfile
    search = request.GET.get('search', '').strip()
    qs = PlayerProfile.objects.all().order_by('lastName', 'firstName')
    if search:
        qs = qs.filter(Q(firstName__icontains=search) | Q(lastName__icontains=search))
    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'main/players.html', {
        'page_obj': page_obj,
        'search': search,
        'total': qs.count(),
    })

def contact(request):
    return render(request, 'main/contact.html')


def calculate_percentile(min_val, max_val, current_val):
    if max_val == min_val:
        raise ValueError("max and min cannot be the same")
    
    # Clamp current_val between min and max to avoid weird % outside 0–100
    current_val = max(min_val, min(current_val, max_val))
    
    percentile = (current_val - min_val) / (max_val - min_val) * 100
    return int(percentile)



def results(request, metric_id):
    try:
        player_metric = PlayerMetric.objects.get(id=metric_id)

        print('hello world')
        print(player_metric.playerAge)
        
        # Get comparison data from MetricsRange for the same metric type and age
        comparison_data = []
        
        # Get the player's age for comparison
        playerAge = int(player_metric.playerAge)
        
        # Try to get the metrics range for this metric type and graduation class
        try:
            metrics_range = MetricsRange.objects.get(
                metricType=player_metric.metricType,
                playerAge=playerAge
            )
            
            comparison_data = {
                'min_value': metrics_range.Min,
                'max_value': metrics_range.Max,
                'average': metrics_range.Avg,
                'current_value': player_metric.metric,
                'metric_type_display': player_metric.get_metricType_display(),
                'metric_type': player_metric.metricType,
                'playerAge': player_metric.playerAge,
                'player_age': player_metric.playerAge,
                'has_data': True,
                'percentile': calculate_percentile(metrics_range.Min, metrics_range.Max, player_metric.metric),
                
            }

            print(comparison_data)
            
        except MetricsRange.DoesNotExist:
            # No range data for this metric type and graduation class
            comparison_data = {
                'no_data': True,
                'playerAge': playerAge,
                'player_age': playerAge,
                'metric_type_display': player_metric.get_metricType_display()
            }
        
        return render(request, 'main/results.html', {
            'player_metric': player_metric,
            'comparison_data': comparison_data
        })
    except PlayerMetric.DoesNotExist:
        return redirect('evaluate')

def metrics_history(request):
    # Get search parameters
    search_query = request.GET.get('search', '')
    player_id = request.GET.get('player_id', '')
    event_id = request.GET.get('event_id', '')
    
    # Start with all records
    metrics_list = MetricsHistory.objects.all()
    
    # Apply filters
    if search_query:
        metrics_list = metrics_list.filter(
            Q(player_id__icontains=search_query) |
            Q(event_id__icontains=search_query) |
            Q(gradYear__icontains=search_query)
        )
    
    if player_id:
        metrics_list = metrics_list.filter(player_id=player_id)
    
    if event_id:
        metrics_list = metrics_list.filter(event_id=event_id)
    
    # Pagination
    paginator = Paginator(metrics_list, 25)  # Show 25 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'player_id': player_id,
        'event_id': event_id,
        'total_records': metrics_list.count(),
    }
    
    return render(request, 'main/metrics_history.html', context)


@login_required
def add(request, player_id):
    """View for capturing multiple metrics at once - requires login"""
    from .models import PlayerProfile
    profile = get_object_or_404(PlayerProfile, player_id=player_id, user=request.user)
    if request.method == 'POST':
        form = CaptureForm(request.POST)
        if form.is_valid():
            date_captured = form.cleaned_data.get('dateCaptured')
            captured_by = form.cleaned_data.get('capturedBy')
            notes = form.cleaned_data.get('notes')

            saved_count = 0
            for field_name, value in form.cleaned_data.items():
                if field_name.startswith('metric_') and value is not None:
                    metric_type = field_name.replace('metric_', '')
                    try:
                        PlayerMetric.objects.create(
                            metricType=metric_type,
                            metric=value,
                            playerAge=form.cleaned_data.get('playerAge'),
                            profile=profile,
                            dateCaptured=date_captured,
                            capturedBy=captured_by,
                            notes=notes
                        )
                        saved_count += 1
                    except Exception as e:
                        messages.error(request, f'Error saving {metric_type}: {str(e)}')

            if saved_count > 0:
                messages.success(request, f'Successfully saved {saved_count} metric(s)!')
                return redirect('profile_detail', player_id=profile.player_id)
            else:
                messages.warning(request, 'No metrics were saved. Please fill in at least one metric.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CaptureForm()

    return render(request, 'main/add.html', {'form': form, 'profile': profile})


@login_required
def profile_list(request):
    from .models import PlayerProfile
    profiles = PlayerProfile.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'main/profile_list.html', {'profiles': profiles})


def profile_detail(request, player_id):
    """View for displaying a specific player profile - publicly accessible"""
    from .models import PlayerProfile
    player_profile = get_object_or_404(PlayerProfile, player_id=player_id)
    profile_user = player_profile.user
    
    # Get all metrics for this profile, ordered by date for charts
    user_metrics = PlayerMetric.objects.filter(profile=player_profile).order_by('dateCaptured')

    # Get latest metrics for each type (ordered by date descending)
    latest_metrics_query = PlayerMetric.objects.filter(profile=player_profile).order_by('-dateCaptured', '-created_at')
    latest_metrics = {}
    for metric in latest_metrics_query:
        if metric.metricType not in latest_metrics:
            latest_metrics[metric.metricType] = metric
    
    # Initialize metric data containers
    metrics_data = {
        'sixtyyard': {'dates': [], 'values': [], 'labels': [], 'display': '60 Yard Dash',        'unit': 'seconds', 'reverse': True},
        'fbvelo':    {'dates': [], 'values': [], 'labels': [], 'display': 'Fastball Velocity',    'unit': 'mph',     'reverse': False},
        'exitvelo':  {'dates': [], 'values': [], 'labels': [], 'display': 'Exit Velocity',        'unit': 'mph',     'reverse': False},
        'ofvelo':    {'dates': [], 'values': [], 'labels': [], 'display': 'Outfield Velocity',    'unit': 'mph',     'reverse': False},
        'ifvelo':    {'dates': [], 'values': [], 'labels': [], 'display': 'Infield Velocity',     'unit': 'mph',     'reverse': False},
        'catchvelo': {'dates': [], 'values': [], 'labels': [], 'display': 'Catcher Velocity',     'unit': 'mph',     'reverse': False},
        'poptime':   {'dates': [], 'values': [], 'labels': [], 'display': 'Pop Time',             'unit': 'seconds', 'reverse': True},
        'changeup':  {'dates': [], 'values': [], 'labels': [], 'display': 'Changeup',             'unit': 'mph',     'reverse': False},
        'curve':     {'dates': [], 'values': [], 'labels': [], 'display': 'Curveball',            'unit': 'mph',     'reverse': False},
        'slider':    {'dates': [], 'values': [], 'labels': [], 'display': 'Slider',               'unit': 'mph',     'reverse': False},
        'height':    {'dates': [], 'values': [], 'labels': [], 'display': 'Height',               'unit': 'inches',  'reverse': False},
        'weight':    {'dates': [], 'values': [], 'labels': [], 'display': 'Weight',               'unit': 'lbs',     'reverse': False},
    }
    
    # Organize metrics by type
    for metric in user_metrics:
        if metric.metricType in metrics_data:
            date_str = metric.dateCaptured.strftime('%Y-%m-%d') if metric.dateCaptured else 'N/A'
            # Get capturedBy display value
            captured_by_display = metric.get_capturedBy_display() if metric.capturedBy else 'N/A'
            # Create label as array for multi-line display in Chart.js
            label = [date_str, captured_by_display]
            metrics_data[metric.metricType]['dates'].append(date_str)
            metrics_data[metric.metricType]['values'].append(float(metric.metric))
            metrics_data[metric.metricType]['labels'].append(label)
    
    # Calculate percentile for latest metric of each type
    for metric_type, metric in latest_metrics.items():
        player_age = int(metric.playerAge)
        try:
            metrics_range = MetricsRange.objects.get(
                metricType=metric_type,
                playerAge=player_age
            )
            percentile = calculate_percentile(metrics_range.Min, metrics_range.Max, metric.metric)
            metrics_data[metric_type]['latest_value'] = float(metric.metric)
            metrics_data[metric_type]['date_captured'] = metric.dateCaptured.strftime('%m/%d/%Y') if metric.dateCaptured else 'N/A'
            metrics_data[metric_type]['percentile'] = percentile
            metrics_data[metric_type]['has_percentile'] = True
            metrics_data[metric_type]['player_age'] = player_age
        except MetricsRange.DoesNotExist:
            metrics_data[metric_type]['latest_value'] = float(metric.metric)
            metrics_data[metric_type]['date_captured'] = metric.dateCaptured.strftime('%Y-%m-%d') if metric.dateCaptured else 'N/A'
            metrics_data[metric_type]['has_percentile'] = False
            metrics_data[metric_type]['player_age'] = player_age
    
    # Check if viewing own profile
    is_own_profile = request.user.is_authenticated and request.user == profile_user
    
    # Prepare context with JSON data for each metric
    context = {
        'user': profile_user,
        'profile': player_profile,
        'total_metrics': user_metrics.count(),
        'is_own_profile': is_own_profile,
        'metrics_data': {
            metric_type: {
                'dates': json.dumps(data['dates']),
                'values': json.dumps(data['values']),
                'labels': json.dumps(data['labels']),
                'display': data['display'],
                'unit': data['unit'],
                'reverse': data['reverse'],
                'has_data': len(data['dates']) > 0,
                'latest_value': data.get('latest_value'),
                'date_captured': data.get('date_captured'),
                'percentile': data.get('percentile'),
                'has_percentile': data.get('has_percentile', False),
                'player_age': data.get('player_age'),
                'metric_type': metric_type,
            }
            for metric_type, data in metrics_data.items()
        }
    }
    
    return render(request, 'main/profile.html', context)

def evaluate(request):
    if request.method == 'POST':
        form = PlayerMetricForm(request.POST)
        if form.is_valid():
            player_metric = form.save()
            return redirect('results', metric_id=player_metric.id)
        else:
            # Form has errors, will be displayed in template
            pass
    else:
        form = PlayerMetricForm()
    
    return render(request, 'main/evaluate.html', {'form': form})

@login_required
def edit_profile(request, profile_id):
    from .models import PlayerProfile
    profile = get_object_or_404(PlayerProfile, pk=profile_id, user=request.user)
    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Profile updated successfully!')
                logger.info(f"Profile updated successfully for user: {request.user.username}")
                return redirect('profile_detail', player_id=profile.player_id)
            except Exception as e:
                logger.error(f"Error uploading profile for user {request.user.username}: {str(e)}", exc_info=True)
                if 'S3' in str(type(e).__name__) or 'ClientError' in str(type(e).__name__):
                    messages.error(request, 'Failed to upload image to storage. Please check file size and format. If the problem persists, contact support.')
                    logger.error(f"S3 ClientError for user {request.user.username}: {str(e)}")
                elif 'IOError' in str(type(e).__name__) or 'OSError' in str(type(e).__name__):
                    messages.error(request, 'File system error occurred. Please try again.')
                    logger.error(f"File system error for user {request.user.username}: {str(e)}")
                else:
                    messages.error(request, 'An error occurred while updating your profile. Please try again.')
                    logger.error(f"Unexpected error for user {request.user.username}: {str(e)}")
        else:
            messages.error(request, 'Please correct the errors below.')
            logger.warning(f"Form validation failed for user {request.user.username}: {form.errors}")
    else:
        form = PlayerProfileForm(instance=profile)

    return render(request, 'main/edit_profile.html', {'form': form, 'profile': profile})


@login_required
def profile_create(request):
    from .models import PlayerProfile
    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('profile_detail', player_id=profile.player_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PlayerProfileForm()
    return render(request, 'main/edit_profile.html', {'form': form, 'profile': None})


@login_required
@require_POST
def profile_delete(request, profile_id):
    from .models import PlayerProfile
    profile = get_object_or_404(PlayerProfile, pk=profile_id, user=request.user)
    profile.delete()
    messages.success(request, 'Profile deleted.')
    return redirect('profile_list')


@login_required
def playerevaluation(request):
    """View for comparing all user stats to averages - requires login"""
    user = request.user
    
    # Get all metrics across all profiles belonging to this user
    user_metrics = PlayerMetric.objects.filter(profile__user=user).order_by('-dateCaptured', '-created_at')
    
    # Get the latest metric for each metric type
    latest_metrics = {}
    for metric in user_metrics:
        if metric.metricType not in latest_metrics:
            latest_metrics[metric.metricType] = metric
    
    # Prepare comparison data for each metric type
    evaluation_data = []
    
    for metric_type, metric in latest_metrics.items():
        grad_class = int(metric.gradClass)
        
        # Try to get the metrics range for this metric type and graduation class
        try:
            metrics_range = MetricsRange.objects.get(
                metricType=metric_type,
                gradClass=grad_class
            )
            
            percentile = calculate_percentile(metrics_range.Min, metrics_range.Max, metric.metric)
            
            evaluation_data.append({
                'metric_type': metric_type,
                'metric_type_display': metric.get_metricType_display(),
                'current_value': metric.metric,
                'min_value': metrics_range.Min,
                'max_value': metrics_range.Max,
                'average': metrics_range.Avg,
                'grad_class': grad_class,
                'percentile': percentile,
                'has_data': True,
                'date_captured': metric.dateCaptured,
            })
            
        except MetricsRange.DoesNotExist:
            # No range data for this metric type and graduation class
            evaluation_data.append({
                'metric_type': metric_type,
                'metric_type_display': metric.get_metricType_display(),
                'current_value': metric.metric,
                'grad_class': grad_class,
                'has_data': False,
                'date_captured': metric.dateCaptured,
            })
    
    # Sort by metric type for consistent display
    evaluation_data.sort(key=lambda x: x['metric_type'])
    
    context = {
        'user': user,
        'evaluation_data': evaluation_data,
        'total_metrics': len(evaluation_data),
    }
    
    return render(request, 'main/playerevaluation.html', context)


def events(request):
    events = Event.objects.filter(active=True).order_by('-date')
    return render(request, 'main/events.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    metrics = event.metrics.select_related('profile').order_by('profile__lastName', 'profile__firstName')

    # Preferred column order matching METRIC_TYPE_CHOICES
    metric_order = ['sixtyyard', 'fbvelo', 'exitvelo', 'ofvelo', 'ifvelo', 'catchvelo',
                    'poptime', 'changeup', 'curve', 'slider', 'height', 'weight']
    metric_labels = {
        'sixtyyard': '60 Yard', 'fbvelo': 'FB Velo', 'exitvelo': 'Exit Velo',
        'ofvelo': 'OF Velo', 'ifvelo': 'IF Velo', 'catchvelo': 'C Velo',
        'poptime': 'Pop Time', 'changeup': 'Changeup', 'curve': 'Curve',
        'slider': 'Slider', 'height': 'Height', 'weight': 'Weight',
    }

    # Collect which metric types actually appear in this event's data
    present_types = set(metrics.values_list('metricType', flat=True))
    columns = [mt for mt in metric_order if mt in present_types]

    # Build one row per player with values pre-ordered to match columns
    players_map = {}
    for m in metrics:
        key = m.profile_id
        if key not in players_map:
            players_map[key] = {'profile': m.profile, 'values': {}}
        players_map[key]['values'][m.metricType] = m.metric

    player_rows = [
        {
            'profile': p['profile'],
            'row_values': [p['values'].get(col) for col in columns],
        }
        for p in players_map.values()
    ]

    column_labels = [metric_labels[col] for col in columns]

    return render(request, 'main/event_detail.html', {
        'event': event,
        'player_rows': player_rows,
        'column_labels': column_labels,
    })
