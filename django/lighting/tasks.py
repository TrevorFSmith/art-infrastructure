from scheduler.models import Task
from models import *
from lighting.creston import CrestonControl, SocketException as CrestonSocketException

class ProjectorEventTask(Task):
    """The task which runs scheduled events for the projector."""
    def __init__(self, loopdelay=60, initdelay=1):
        Task.__init__(self, self.do_it, loopdelay, initdelay)

    def do_it(self):
        for event in ProjectorEvent.objects.all():
            if event.due_for_execution(): event.execute()


class LightingStatusTask(Task):
    def __init__(self, loopdelay=5, initdelay=1):
        Task.__init__(self, self.do_it, loopdelay, initdelay)

    def do_it(self):
        status_list = []
        for creston in Creston.objects.all():
            control = CrestonControl(creston.host, creston.port, 1)
            try:
                control_info = control.send_command("Update")
            except CrestonSocketException:
                control_info = None
            if control_info:
                creston.status = True
                creston.save()
                status_list.append(True)
            else:
                creston.status = False
                creston.save()
                status_list.append(False)
        print status_list