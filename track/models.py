from django.contrib.auth.models import User
from django.db import models


class Activity(models.Model):
    name = models.CharField(max_length=255)
    frequency = models.CharField(max_length=50)
    duration = models.PositiveIntegerField()

    class Meta:
        unique_together = ('name', 'frequency', 'duration')

    def __str__(self):
        return f"{self.name} ({self.frequency} - {self.duration}s)"


class ActivityPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    activities = models.ManyToManyField(Activity, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.clean()
        super(ActivityPlan, self).save(*args, **kwargs)


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activity_plan = models.ForeignKey(ActivityPlan, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Settings"


class DailyActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    date = models.DateField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'date', 'activity')

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.activity.name} (Completed: {self.is_completed})"
