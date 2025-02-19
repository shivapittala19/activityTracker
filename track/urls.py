from django.urls import path

from track.views import (
    fetch_daily_activity,
    toggle_activity_completion,
)

urlpatterns = [
    path('user_progress/', fetch_daily_activity, name='user_progress'),
    path('toggle_activity/<int:pk>/', toggle_activity_completion, name='toggle_activity'),
]
