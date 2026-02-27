from django.urls import path
from . import views

urlpatterns = [
    path('cards/<int:card_id>/', views.card_detail, name='card-detail'),
    path('cards/<int:card_id>/edit/', views.card_edit, name='card-edit'),
    path('cards/<int:card_id>/update/', views.card_update, name='card-update'),
    path('cards/<int:card_id>/delete/', views.card_delete, name='card-delete'),
    path('cards/<int:card_id>/assign/', views.card_assign, name='card-assign'),
    path('cards/<int:card_id>/unassign/', views.card_unassign, name='card-unassign'),
]