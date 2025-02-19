from datetime import date

from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
)
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from track.helpers import (
    ActivityToggleThrottle,
    create_daily_activities_if_missing,
    fetch_existing_daily_activities,
    parse_date,
)
from track.models import DailyActivity
from track.serializers import DailyActivitySerializer


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="date",
            description="Date for fetching activities (format: YYYY-MM-DD)",
            required=True,
            type=OpenApiTypes.DATE,
            location=OpenApiParameter.QUERY,
        )
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_daily_activity(request):
    user = request.user
    requested_date = parse_date(request)
    today = date.today()

    if requested_date is None:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    daily_activities = fetch_existing_daily_activities(user, requested_date)
    if requested_date < today:
        serializer = DailyActivitySerializer(daily_activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    daily_activities = create_daily_activities_if_missing(user, requested_date)

    serializer = DailyActivitySerializer(daily_activities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([ActivityToggleThrottle])
def toggle_activity_completion(request, pk):
    user = request.user

    # Fetch the daily activity for the user; return 404 if not found
    daily_activity = get_object_or_404(DailyActivity, id=pk, user=user)

    with transaction.atomic():
        daily_activity.is_completed = not daily_activity.is_completed
        daily_activity.save(update_fields=["is_completed"])

    return Response(
        {"message": "Activity updated", "is_completed": daily_activity.is_completed},
        status=status.HTTP_200_OK,
    )
