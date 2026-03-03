from django.db import models
from django.conf import settings
from apps.boards.models import Column

# represents task card that's within a Board Column
# tracks title, description, status, column placement, and assigned users.
class Card(models.Model):

    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Not Started'
        IN_PROGRESS = 'in_progress', 'In Progress'
        OVERDUE = 'overdue', 'Overdue'
        COMPLETE= 'complete', "Complete"
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_STARTED
    )

    column = models.ForeignKey(
        Column,
        on_delete=models.CASCADE,
        related_name='cards'
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='assigned_cards'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title

