from datetime import date, datetime

from django.db import transaction
from rest_framework.throttling import UserRateThrottle

from track.models import (
    Activity,
    DailyActivity,
    UserSettings,
)


class ActivityToggleThrottle(UserRateThrottle):
    rate = "5/min"  # Limit to 5 requests per minute


def parse_date(request):
    """Extracts and validates the date from request parameters."""
    requested_date = request.query_params.get('date', None)

    if requested_date:
        try:
            parsed_date = datetime.strptime(requested_date, "%Y-%m-%d").date()
        except ValueError:
            return None  # Invalid format
    else:
        parsed_date = date.today()  # Default to today

    return parsed_date


def fetch_existing_daily_activities(user, requested_date):
    """Retrieve daily activities for the user based on date."""
    return DailyActivity.objects.filter(user=user, date=requested_date)


def create_daily_activities_if_missing(user, requested_date):
    """Create daily activities for the user based on ActivityPlan, if missing."""
    user_settings = UserSettings.objects.filter(user=user).select_related('activity_plan').first()

    if not user_settings or not user_settings.activity_plan:
        return []

    activity_plan = user_settings.activity_plan
    planned_activities = set(Activity.objects.filter(activityplan=activity_plan))

    existing_daily_activities = DailyActivity.objects.filter(user=user, date=requested_date).select_related('activity')
    existing_activities = {da.activity: da for da in existing_daily_activities}

    new_daily_activities = []
    for activity in planned_activities:
        if activity in existing_activities:
            # Keep the existing activity
            continue

        new_daily_activities.append(
            DailyActivity(user=user, activity=activity, date=requested_date)
        )
    
    # activities that should be removed (not in plan)
    activities_to_remove = [da for da in existing_daily_activities if da.activity not in planned_activities]

    with transaction.atomic():
        # Delete outdated activities
        if activities_to_remove:
            DailyActivity.objects.filter(id__in=[da.id for da in activities_to_remove]).delete()

        # Create missing activities
        if new_daily_activities:
            DailyActivity.objects.bulk_create(new_daily_activities)

    return fetch_existing_daily_activities(user, requested_date)
