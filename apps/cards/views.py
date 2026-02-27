from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Card
from apps.users.models import User
from apps.boards.models import Column 

# Create your views here.
def card_create(request):
    column_id = request.GET.get('column_id') or request.POST.get('column_id')
    column = get_object_or_404(Column, id=column_id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if title:
            Card.objects.create(
                title=title,
                description=description,
                column=column,
            )

        # Return updated card list for this column
        return render(request, 'partials/column_cards.html', {
            'column': column,
            'is_done': column.title.lower() == 'done',
        })

    # GET — return the create form
    return render(request, 'partials/card_create_form.html', {
        'column': column,
    })

def card_detail(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    users = User.objects.all()
    return render(request, 'cards/card_detail_modal.html', {
            'card': card, 
            'users': users,
        })


def card_edit(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    users = User.objects.all()
    return render(request, 'cards/card_edit_modal.html', {
        'card': card,
        'users': users,
    })
def card_update(request, card_id):
    card = get_object_or_404(Card, id=card_id)

    if request.method == 'POST':
        card.title = request.POST.get('title', card.title)
        card.description = request.POST.get('description', card.description)
        card.status = request.POST.get('status', card.status)

        # Handle assignees — getlist because multiple can be selected
        assignee_ids = request.POST.getlist('assignees')
        card.assignees.set(assignee_ids)

        card.save()

    return render(request, 'cards/card_detail_modal.html', {
        'card': card,
        'users': User.objects.all(),
        })

def card_delete(request, card_id):
    card = get_object_or_404(Card, id=card_id)

    if request.method == 'DELETE':
        card.delete()
        # Clear the modal container after deletion
        return HttpResponse(
            '<script>document.getElementById("modal-container").innerHTML=""</script>'
        )

    # GET request — show confirmation modal
    return render(request, 'cards/card_delete_confirm.html', {'card': card})

def card_assign(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            user = get_object_or_404(User, id=user_id)
            card.assignees.add(user)
            card.save()
    return render(request, 'cards/card_detail_modal.html', {
        'card': card,
        'users': User.objects.all(),
        })

def card_unassign(request, card_id):
    card = get_object_or_404(Card, id=card_id)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            user = get_object_or_404(User, id=user_id)
            card.assignees.remove(user)
            card.save()

    return render(request, 'cards/card_detail_modal.html', {
        'card': card,
        'users': User.objects.all(),
    })
