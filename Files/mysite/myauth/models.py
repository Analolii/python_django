from django.contrib.auth.models import User
from django.db import models


def avatar_directory_path(instance: "Profile", filename: str) -> str:
    return 'avatar/avatar_{pk}/avatars/{filename}'.format(
        pk=instance.user.pk,
        filename=filename
    )


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['profile'] = self.request.user.profile
    return context


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_directory_path)

