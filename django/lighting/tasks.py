
from scheduler import Task

class ProjectorEventTask(Task):
	"""The task which runs scheduled events for the projector."""
	def __init__(self, loopdelay=60, initdelay=1):
		Task.__init__(self, self.do_it, loopdelay, initdelay)

	def do_it(self):
		from models import ProjectorEvent
		for event in ProjectorEvent.objects.all():
			if event.due_for_execution(): event.execute()
