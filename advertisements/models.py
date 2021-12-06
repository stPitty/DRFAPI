from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_advertisement'
    )
    created_at = models.DateTimeField(

        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    favorite = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorite_advertisements'
    )
    is_draft = models.BooleanField(
        default=False
    )
