from django.test import TestCase, Client
from django.urls import reverse
from apps.boards.models import Board, Column
from .models import Card
from apps.users.models import User

class CardTests(TestCase):

    # SETUP - testing setup
    def setUp(self):
        # create a default test board and columns
        self.board = Board.objects.create(title="Test Board")
        self.column = Column.objects.create(
            board=self.board,
            title="To Do",
            position=0
        )
        self.client = Client()


    # TEST CREATE - task card is created successfully with appropriate info
    def test_create_card(self):
        """Test: Add a card to a column"""
        url = reverse('card-create')  

        # POST to card_create view
        response = self.client.post(url, {  # adjust URL if you have a route for creation
            'title': 'Test Card',
            'description': 'This is a test',
            'column_id': self.column.id
        })

        self.assertIn(response.status_code, [200, 302])

        # check card exists in DB
        card = Card.objects.filter(
            title='Test Card',
            column=self.column
        ).first()

        self.assertIsNotNone(card)                               # verify creation (not none)
        self.assertEqual(card.description, 'This is a test')     # description must match


    # TEST INVALID CREATION - task card not created when required fields empty
    def test_create_card_invalid(self):
        """Test: Card is not created when required data is missing"""
        url = reverse('card-create')

        response = self.client.post(url, {
            'title': '',  # invalid (assuming title required)
            'column_id': self.column.id
        })
        self.assertEqual(Card.objects.count(), 0)                # card should not be created/present


    # TEST DELETE - task card is deleted successfully
    def test_delete_card_sucess(self):
        """Test: Delete a card"""
        # create a card first
        card = Card.objects.create(
            title='Delete Me',
            column=self.column
        )
        url = reverse('card-delete', args=[card.id])
        response = self.client.delete(f'/cards/{card.id}/delete/')    # simulate DELETE request
        self.assertFalse(Card.objects.filter(id=card.id).exists())    # card should no longer exist

    # TEST DELETE INVALID - no task card found, delete attempted
    def test_delete_card_not_found(self):
        """Test: Deleting non-existent card returns 404"""
        url = reverse('card-delete', args=[999])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)    # task card is not found, should return code 404