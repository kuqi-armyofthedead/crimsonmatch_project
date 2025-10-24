from django.contrib.auth.models import User
from django.db import models

class VampireProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age_of_turning = models.PositiveIntegerField()
    blood_type_preference = models.CharField(max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'),
        ('B-', 'B-'), ('AB+', 'AB+'), ('O+', 'O+'), ('O-', 'O-')
    ])
    favorite_night_activity = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} (Turned at {self.age_of_turning})"

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given')
    liked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('liker', 'liked')

    def __str__(self):
        return f"{self.liker} likes {self.liked}"
