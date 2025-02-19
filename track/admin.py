from django.contrib import admin

from track.models import (
    Activity,
    ActivityPlan,
    DailyActivity,
    UserSettings,
)


@admin.register(ActivityPlan)
class ActivityPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    filter_horizontal = ('activities',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'frequency', 'duration']
    search_fields = ['name']


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_plan']
    search_fields = ['user__username']


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'activity', 'is_completed']
    list_filter = ['date', 'user']
    search_fields = ['user__username', 'activity__name']
