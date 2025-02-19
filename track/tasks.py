import logging

from celery import shared_task
from django.db import transaction
from django.utils.timezone import now

from track.helpers import (
    create_daily_activities_if_missing,
    fetch_existing_daily_activities,
)
from track.models import User

logger = logging.getLogger(__name__)


@shared_task
def generate_daily_activities():
    """
    Runs at 12:00 AM daily.
    Creates DailyActivity instances for each active user with an assigned ActivityPlan.
    """
    today = now().date()
    active_users = User.objects.filter(is_active=True)

    with transaction.atomic():
        for user in active_users:
            try:
                daily_activities = fetch_existing_daily_activities(user, today)
                if not daily_activities:
                    logger.info(f"Processing user {user.id} for daily activities on {today}")
                    created_activities = create_daily_activities_if_missing(user, today)
                    logger.info(f"Created {len(created_activities)} DailyActivity entries for user {user.id}")
            except Exception as e:
                logger.error(f"Failed to create DailyActivity for user {user.id} ({user.username}): {e}")
