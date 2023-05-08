from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Friend(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_friends', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friend_friends', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('from_user', 'to_user')
    
    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super().save(*args, **kwargs)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.email} -> {self.to_user.email} ({self.created_at})"



