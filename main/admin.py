from django.contrib import admin
from .models import PlayerMetric, MetricsHistory, MetricsRange, PlayerProfile, Event, BlogPost

@admin.register(PlayerMetric)
class PlayerMetricAdmin(admin.ModelAdmin):
    list_display = ('metricType', 'metric', 'event', 'created_at', 'profile')
    list_filter = ('metricType',)
    search_fields = ('metric', 'playerAge', 'profile__firstName', 'profile__lastName', 'profile__player_id')
    date_hierarchy = None
    ordering = ('-created_at',)

@admin.register(MetricsHistory)
class MetricsHistoryAdmin(admin.ModelAdmin):
    list_display = ('player_id', 'event_id', 'event_date', 'height', 'weight', 'exitVelo', 'sixtyyard', 'maxFB')
    list_filter = ('event_date', 'gradYear', 'event_id')
    search_fields = ('player_id', 'event_id')
    date_hierarchy = 'event_date'
    ordering = ('-event_date', 'player_id')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Player Information', {
            'fields': ('player_id', 'height', 'weight', 'gradYear')
        }),
        ('Velocity Metrics', {
            'fields': ('ifVelo', 'ofVelo', 'cVelo', 'exitVelo', 'maxFB')
        }),
        ('Time Metrics', {
            'fields': ('popTime', 'sixtyyard')
        }),
        ('Pitch Velocities', {
            'fields': ('changeUp', 'curve', 'slider')
        }),
        ('Event Information', {
            'fields': ('event_id', 'event_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MetricsRange)
class MetricsRangeAdmin(admin.ModelAdmin):
    list_display = ('metricType', 'Min', 'Max', 'Avg', 'playerAge')
    list_filter = ('metricType', 'playerAge')
    search_fields = ('metricType',)
    ordering = ('metricType', 'playerAge')
    
    fieldsets = (
        ('Metric Information', {
            'fields': ('metricType', 'playerAge')
        }),
        ('Range Values', {
            'fields': ('Min', 'Max', 'Avg')
        }),
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'active')
    list_filter = ('active',)
    search_fields = ('title', 'location')
    ordering = ('date',)
    list_editable = ('active',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'published', 'created_at')
    list_filter = ('published',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('published',)
    date_hierarchy = 'date'
    ordering = ('-date',)
    fields = ('title', 'slug', 'date', 'image', 'post', 'published')

@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'firstName', 'lastName', 'get_positions_display', 'team', 'graduation_year', 'created_at')
    search_fields = ('user__username', 'firstName', 'lastName', 'team', 'positions')
    list_filter = ('graduation_year',)
    readonly_fields = ('created_at', 'updated_at')

    def get_positions_display(self, obj):
        return obj.get_positions_display()
    get_positions_display.short_description = 'Positions'
