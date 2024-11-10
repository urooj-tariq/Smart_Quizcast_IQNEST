from django.db import models
from django.contrib.auth.models import User

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links rating to a specific user
    value = models.IntegerField()  # Stores the rating value (e.g., from 1 to 5)
    created_at = models.DateTimeField(auto_now_add=True)  # Stores the time the rating was created


class MentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    expertise = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"