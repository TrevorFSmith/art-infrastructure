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
    def __init__(self, loopdelay=5, initdelay=0):
        Task.__init__(self, self.do_it, loopdelay, initdelay)

    def do_it(self):
        for creston in Creston.objects.all():
            control = CrestonControl(creston.host, creston.port)
            try:
                status = control.send_command("Update")
            except CrestonSocketException:
                status= None
            if status:
                creston.status = True
            else:
                creston.status = False
            creston.save()


class ProjectorStatusTask(Task):
    def __init__(self, loopdelay=5, initdelay=0):
        Task.__init__(self, self.do_it, loopdelay, initdelay)

    def do_it(self):
        for projector in Projector.objects.all():
            controller = PJLinkController(projector.pjlink_host, projector.pjlink_port, projector.pjlink_password)
            try:
                status = controller.query_power()
            except PJLinkSocketException:
                status = None
            if status:
                projector.status = True
            else:
                projector.status = False
            projector.save()