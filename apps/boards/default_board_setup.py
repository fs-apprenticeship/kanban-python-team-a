from apps.boards.models import Board, Column
from apps.cards.models import Card

def default_board_setup():

    # create default board (if nonexistent)
    board, _ = Board.objects.get_or_create(title="Default Board")

    # create default columns
    columns = {}
    for idx, title in enumerate(["To Do", "In Progress", "Done"]):
        column, _ = Column.objects.get_or_create(
            board=board,
            title=title,
            defaults={"position": idx}
        )
        columns[title] = column

    # add demo task cards
    demo_cards = [
        ("Set up project repo", "Initialize GitHub repo and virtual environment", "To Do"),
        ("Implement card create", "Add create card functionality", "In Progress"),
        ("Write tests", "Add unit tests for cards", "Done")
    ]

    for title, desc, col_title in demo_cards:
        col = columns[col_title]
        Card.objects.get_or_create(
            title=title,
            description=desc,
            column=col
        )

    print("Default board with columns and demo cards is ready.")