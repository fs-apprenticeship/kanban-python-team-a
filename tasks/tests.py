from django.test import TestCase
from .models import Task

# basic model behavior
class TaskModelTest(TestCase):

    def test_create(self):
        """Checks if Task was successfully created with appropriate fields"""
        task = Task.objects.create(
            title="Test Task",
            description="This is a test.",
        )

        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.status, Task.Status.NOT_STARTED)
        self.assertEqual(task.description, "This is a test.")
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)

    
    def test_del(self):
        """Checks if Task was successflly deleted"""
        task = Task.objects.create(title="Task to delete")
        task_id = task.id
        task.delete()
        self.assertFalse(Task.objects.filter(id=task_id).exists())