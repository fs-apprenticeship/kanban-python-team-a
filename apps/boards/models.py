from django.db import models
from django.conf import settings


# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
  
    def __str__(self):
        return self.title
    

    
class Column(models.Model):
    board = models.ForeignKey(
        Board, 
        on_delete=models.CASCADE,
        related_name='columns'
    )
    title = models.CharField(max_length=100)
    position = models.PositiveBigIntegerField(default=0)
   

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"{self.board.title} - {self.title}"