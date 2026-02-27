from django.contrib import admin
from .models import Board, BoardMembership, Column 

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created_at']
    search_fields = ['title']


@admin.register(BoardMembership)
class BoardMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'board', 'role', 'joined_at']


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ['title', 'board', 'position']
    ordering = ['board', 'position']