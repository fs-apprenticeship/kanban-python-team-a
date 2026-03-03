from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Card
from apps.users.models import User
from apps.boards.models import Column 

# Create - create a task card
# GET: show create form
# POST: create card and refresh column display.
def card_create(request):

    # getting the column id where card should go
    # from col id GET when user clicks "add card" or submitted form POST when user clicks "save"
    column_id = request.GET.get('column_id') or request.POST.get('column_id')
    column = get_object_or_404(Column, id=column_id)                   #

    # POST - user submitted form
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        # requires title for creation
        if title:
            Card.objects.create(
                title=title,
                description=description,
                column=column,
            )

        # return updated html
        return render(request, 'partials/column_cards.html', {
            'column': column,
            'is_done': column.title.lower() == 'done',
        })


    # GET — return the create form for user to enter
    return render(request, 'partials/card_create_form.html', {
        'column': column,
    })

# Detail View - Retrieves specific card by ID and return modal view displaying its details & all users for assignment purposes
def card_detail(request, card_id):
    # retrieve card from db with id
    card = get_object_or_404(Card, id=card_id)

    # get all users
    users = User.objects.all()

    # return template for card detail modal
    #    - passes specific card obj
    #    - list of all users
    return render(request, 'cards/card_detail_modal.html', {
            'card': card, 
            'users': users,
        })

# Edit - edit task card information
def card_edit(request, card_id):
    # retrieve card from db with id
    card = get_object_or_404(Card, id=card_id)

    # get all users
    users = User.objects.all()

    # render edit modal w/ card & user data
    return render(request, 'cards/card_edit_modal.html', {
        'card': card,
        'users': users,
    })

# Delete - remove task card from db
def card_delete(request, card_id):
    # retrieve card from db with id
    card = get_object_or_404(Card, id=card_id)

    # if method == DELETE, remove card from db
    if request.method == 'DELETE':
        card.delete()
        # clear modal container after deletion
        # return small JS response to clear modal after deletion
        return HttpResponse(
            '<script>'
            'document.getElementById("modal-container").innerHTML="";'
            'var el = document.getElementById("card-%s"); if(el) el.remove();'
            '</script>' % card_id
        )
    
    # GET request — show confirmation modal
    return render(request, 'cards/card_delete_confirm.html', {'card': card})

# Assign - assign a user to a task card
def card_assign(request, card_id):
    # retrieve card from db with id
    card = get_object_or_404(Card, id=card_id)

    # only process assignment if POST request (form submission)
    if request.method == 'POST':
        # get user's id from submitted form
        user_id = request.POST.get('user_id')
        # if id provided, retrieve user
        if user_id:
            user = get_object_or_404(User, id=user_id)
            card.assignees.add(user)
            card.save()

    # re-render card detail modal after changes
    return render(request, 'cards/card_detail_modal.html', {
        'card': card,
        'users': User.objects.all(),
        })

# Unassign - remove user from task card assignment
def card_unassign(request, card_id):
    # retrieve card from db with id
    card = get_object_or_404(Card, id=card_id)

    # only process unassignment if POST request
    if request.method == 'POST':
        # get user's id from submitted form
        user_id = request.POST.get('user_id')
        # if id provided, retrieve user
        if user_id:
            user = get_object_or_404(User, id=user_id)
            card.assignees.remove(user)
            card.save()

    # re-render card detail modal after changes
    return render(request, 'cards/card_detail_modal.html', {
        'card': card,
        'users': User.objects.all(),
    })
