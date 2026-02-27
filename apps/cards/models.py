from django.db import models
from django.conf import settings
from apps.boards.models import Column

# Create your models here.
class Card(models.Model):

    class Status(models.TextChoices):
        TODO = 'todo', 'To Do'
        IN_PROGRESS = 'in_progress', 'In Progress'
       # IN_REVIEW = 'in_review', 'In Review'
        DONE = 'done', 'Done'
    #id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO
    )
    #created_by = models.ForeignKey(
    #    settings.AUTH_USER_MODEL,
     #   on_delete=models.SET_NULL,
      #  null=True,
    #    blank=True,
    #    related_name='created_cards'
    #)
    #assignees = models.ManyToManyField(
    #    settings.AUTH_USER_MODEL,
    #    blank=True,
    #    related_name='assigned_cards'
    #)
    
 
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
   # position = models.PositiveIntegerField(default=0)
   # due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title

#class Comment(models.Model):
#    card = models.ForeignKey(
#        Card,
#        on_delete=models.CASCADE,
#        related_name='comments'
#    )
#    author = models.ForeignKey(
#        settings.AUTH_USER_MODEL,
#        on_delete=models.SET_NULL,
#        null=True,
#        blank=True,
#        related_name='comments'
#    )
#    content = models.TextField()
#    created_at = models.DateTimeField(auto_now_add=True)
#    updated_at = models.DateTimeField(auto_now=True)
#    class Meta:
#        ordering = ['created_at']

#    def __str__(self):
#        return f"Comment by {self.author} on {self.card}"

#class Label(models.Model):
 #   name = models.CharField(max_length=50)
 #   color = models.CharField(max_length=7)  # hex color e.g. #FF5733
 #   board = models.ForeignKey(
 #       'boards.Board',
 #       on_delete=models.CASCADE,
 #       related_name='labels'
  #  )
  #  def __str__(self):
  #      return self.name