from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Task


# Create your views here.
def task_delete(request, task_id):
	task = get_object_or_404(Task, id=task_id)

	if request.method == 'DELETE':
		task.delete()
		# clear the modal container after deletion
		return HttpResponse(
			'<script>document.getElementById("modal-container").innerHTML=""</script>'
		)

	# GET request — show confirmation modal
	return render(request, 'tasks/task_delete_confirm.html', {'task': task})
