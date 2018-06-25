from scheduler.models import Task
from models import *
from lighting.creston import CrestonControl, SocketException as CrestonSocketException
from lighting.pjlink import PJLinkController, SocketException as PJLinkSocketException

class ProjectorEventTask(Task):
    """The task which runs scheduled events for the projector."""
    def __init__(self, loopdelay=60, initdelay=1):
        Task.__init__(self, self.do_it, loopdelay, initdelay)

    def do_it(self):
        for event in ProjectorEvent.objects.all():
            if event.due_for_execution(): event.execute()


class CrestonStatusTask(Task):
    def __init__(self, loopdelay=5, initdelay=1):
        Task.__init__(self, self.do_it, loopdelay, initdelay)

    def do_it(self):
        status_list = []
        for creston in Creston.objects.all():
            control = CrestonControl(creston.host, creston.port, 1)
            try:
                status = control.send_command("Update")
            except CrestonSocketException:
                status= None
            if status:
                creston.status = True
                creston.save()
                status_list.append(True)
            else:
                creston.status = False
                creston.save()
                status_list.append(False)
        print status_list


class ProjectorStatusTask(Task):
    def __init__(self, loopdelay=5, initdelay=1):
        Task.__init__(self, self.do_it, loopdelay, initdelay)

    def do_it(self):
        status_list = []
        for projector in Projector.objects.all():
            controller = PJLinkController(projector.pjlink_host, projector.pjlink_port, projector.pjlink_password)
            try:
                status = controller.query_power()
            except PJLinkSocketException:
                status = None
            if status:
                projector.status = True
                projector.save()
                status_list.append(True)
            else:
                projector.status = False
                projector.save()
                status_list.append(False)
        print status_list