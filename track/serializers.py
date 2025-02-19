from rest_framework import serializers

from track.models import Activity, DailyActivity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name', 'frequency', 'duration']


class DailyActivitySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = DailyActivity
        fields = ['id', 'date', 'activity', 'is_completed']
