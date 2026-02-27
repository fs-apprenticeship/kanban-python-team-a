from django.contrib import admin
from .models import Card, Comment, Label

# Register your models here.
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['title', 'column', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'column']
    search_fields = ['title', 'description']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['card', 'author', 'created_at']

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'board']