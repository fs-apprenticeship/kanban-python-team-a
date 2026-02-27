from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Column
from apps.users.models import User

# Create your views here.
def board(request):
    board = Board.objects.first()
    if not board:
        return render(request, 'boards/no_board.html')

    # Get columns in fixed order by title
    todo = board.columns.filter(title='To Do').first()
    in_progress = board.columns.filter(title='In Progress').first()
    done = board.columns.filter(title='Done').first()

    return render(request, 'boards/board_detail.html', {
        'board': board,
        'columns': [
            {'column': todo, 'label': 'TO DO'},
            {'column': in_progress, 'label': 'IN PROGRESS'},
            {'column': done, 'label': 'DONE'},
        ],
        'users': User.objects.all(),
    })







#def board_list(request):
#    board = Board.objects.first()
#    if board:
#        return redirect('board-detail', board_id=board.id)
#    return render(request, 'boards/board_list.html', {'boards': []})

#def board_detail(request, board_id):
#    board = get_object_or_404(Board, id=board_id)
 #   columns = board.columns.prefetch_related('cards__assignees').all()
 #   return render(request, 'boards/board_detail.html', {
 #       'board': board,
 #       'columns': columns,
 #   })