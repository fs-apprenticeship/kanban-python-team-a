from django.db import models

class Task(models.Model):

    # define status options as fixed set
    class Status(models.TextChoices):
        # (DB value, UI label)
        NOT_STARTED = "NOT_STARTED", "Not Started"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        OVERDUE = "OVERDUE", "Overdue"
        COMPLETED = "COMPLETED", "Completed"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # status options defined to set, default = not started 
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_STARTED,
    )

    created_at = models.DateTimeField(auto_now_add=True)     # automatically set when task created
    updated_at = models.DateTimeField(auto_now=True)         # automatically updated when task updated

    def __str__(self):
        return self.title
