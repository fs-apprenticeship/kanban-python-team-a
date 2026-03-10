from django.test import TestCase
from django.urls import reverse
from .models import Board, Column
from apps.users.models import User


# Create your tests here.

class BoardModelTest(TestCase):
    def test_board_creation(self):
        board = Board.objects.create(
            title="Sprint Board",
            description="Test Description"
        )
        self.assertEqual(board.title, "Sprint Board")
        self.assertEqual(board.description, "Test Description")
        self.assertEqual(str(board), "Sprint Board")


class ColumnModelTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(title="Test Board")

    def test_column_creation(self):
        column = Column.objects.create(
            board=self.board,
            title="To Do",
            position=1
        )
        self.assertEqual(column.board, self.board)
        self.assertEqual(column.title, "To Do")
        self.assertEqual(str(column), "Test Board - To Do")

    def test_column_ordering(self):
        col1 = Column.objects.create(board=self.board, title="B", position=2)
        col2 = Column.objects.create(board=self.board, title="A", position=1)

        columns = list(self.board.columns.all())
        self.assertEqual(columns[0], col2)
        self.assertEqual(columns[1], col1)


class BoardViewTest(TestCase):

    def test_no_board_renders_no_board_template(self):
        response = self.client.get(reverse("board"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "boards/no_board.html")

    def test_board_renders_detail_template(self):
        board = Board.objects.create(title="Main Board")

        Column.objects.create(board=board, title="To Do", position=1)
        Column.objects.create(board=board, title="In Progress", position=2)
        Column.objects.create(board=board, title="Done", position=3)

        User.objects.create(username="testuser")

        response = self.client.get(reverse("board"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "boards/board_detail.html")
        self.assertContains(response, "Main Board")
        self.assertContains(response, "TO DO")
        self.assertContains(response, "IN PROGRESS")
        self.assertContains(response, "DONE")