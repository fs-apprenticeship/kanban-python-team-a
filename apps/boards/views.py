from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Column

# Create your views here.
def board_list(request):
    board = Board.objects.first()
    if board:
        return redirect('board-detail', board_id=board.id)
    return render(request, 'boards/board_list.html', {'boards': []})

def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    columns = board.columns.prefetch_related('cards__assignees').all()
    return render(request, 'boards/board_detail.html', {
        'board': board,
        'columns': columns,
    })