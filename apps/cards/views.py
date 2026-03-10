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

    # load anything the template might need (users for assignment list)
    users = User.objects.all()

    # POST indicates form submission to update the card
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        status = request.POST.get('status')

        # require at least a title to avoid blanking out
        if title:
            card.title = title
            card.description = description
            if status in dict(Card.Status.choices):
                card.status = status

                # if we know how to map this status to a column title, try to relocate
                status_map = {
                    Card.Status.NOT_STARTED: 'To Do',
                    Card.Status.IN_PROGRESS: 'In Progress',
                    Card.Status.COMPLETE: 'Done',
                    Card.Status.OVERDUE: 'To Do',
                }
                target_title = status_map.get(status)
                if target_title:
                    try:
                        new_col = card.column.board.columns.get(title=target_title)
                        card.column = new_col
                    except Exception:
                        pass
            card.save()

        # after saving, re‑render the detail view so user sees changes
        # include script to update the card title (and done status class) in the board
        # and move the card element into the appropriate column container
        target_col_id = card.column.id
        script = (
            "var el = document.querySelector('#card-%s');" % card.id +
            "if(el){" +
            " el.querySelector('.card-title').textContent = %r;" % card.title +
            " var sourceParent = el.parentNode;" +
            " var target = document.querySelector('#column-cards-%s');" % target_col_id +
            " if(target && el.parentNode !== target){" +
            "  target.querySelectorAll('div').forEach(function(d){ if(d.id === '' && d.textContent.includes('No tasks yet')){ d.remove(); }});" +
            "  target.appendChild(el);" +
            "  if(sourceParent && sourceParent.querySelectorAll('[id^=\"card-\"]').length === 0){" +
            "    var emptyMsg = document.createElement('div');" +
            "    emptyMsg.style.color = '#aaa';" +
            "    emptyMsg.style.fontSize = '0.85rem';" +
            "    emptyMsg.style.padding = '0.5rem';" +
            "    emptyMsg.textContent = 'No tasks yet';" +
            "    sourceParent.appendChild(emptyMsg);" +
            "  }" +
            " }" +
            " if(%r === 'complete'){ el.classList.add('card-done'); }" % card.status +
            " else { el.classList.remove('card-done'); }" +
            "}"
        )
        return render(request, 'cards/card_detail_modal.html', {
            'card': card,
            'users': users,
            'extra_script': script,
        })

    # GET request — render the edit form modal
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
        col_id = card.column.id
        card.delete()
        # After deletion, check if column has any remaining cards
        remaining_cards = Card.objects.filter(column_id=col_id).count()
        
        script = (
            'document.getElementById("modal-container").innerHTML="";' +
            'var el = document.getElementById("card-%s"); if(el) el.remove();' % card_id
        )
        
        # if column is now empty, add the "No tasks yet" message
        if remaining_cards == 0:
            script += (
                'var colContainer = document.querySelector("#column-cards-%s");' % col_id +
                'if(colContainer){' +
                '  var emptyMsg = document.createElement("div");' +
                '  emptyMsg.style.color = "#aaa";' +
                '  emptyMsg.style.fontSize = "0.85rem";' +
                '  emptyMsg.style.padding = "0.5rem";' +
                '  emptyMsg.textContent = "No tasks yet";' +
                '  colContainer.appendChild(emptyMsg);' +
                '}'
            )
        
        return HttpResponse(
            '<script>%s</script>' % script
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
