"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.boards import views as board_views
from apps.cards import views as card_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', board_views.board, name='board'), 
    path('cards/create/', card_views.card_create, name='card-create'),
    path('cards/<int:card_id>/', card_views.card_detail, name='card-detail'),
    path('cards/<int:card_id>/assign/', card_views.card_assign, name='card-assign'),
    path('cards/<int:card_id>/unassign/', card_views.card_unassign, name='card-unassign'),
    path('cards/<int:card_id>/delete/', card_views.card_delete, name='card-delete'),
]
    #path('', include('apps.boards.urls')),
    #path('', include('apps.cards.urls')),
    # path('boards/', include('apps.boards.urls')),
    #path('users/', include('apps.users.urls')),
    #path('cards/', include('apps.cards.urls')),


