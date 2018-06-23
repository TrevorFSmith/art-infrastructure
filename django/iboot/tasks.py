# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
from scheduler.models import Task
from iboot.models import IBootEvent, IBootDevice
from iboot.iboot_control import IBootControl, SocketException
from django.conf import settings


class IBootEventTask(Task):
    """The task which runs scheduled events."""
    def __init__(self, loopdelay=60, initdelay=1):
        Task.__init__(self, self.do_it, loopdelay, initdelay)

    def do_it(self):
        for event in IBootEvent.objects.all():
            if event.due_for_execution(): event.execute()

class IBootStatusTask(Task):
    def __init__(self, loopdelay=5, initdelay=1):
        Task.__init__(self, self.do_it, loopdelay, initdelay)

    def do_it(self):
        status_list = []
        for iboot in IBootDevice.objects.all():
            control = IBootControl(settings.IBOOT_POWER_PASSWORD, iboot.host, iboot.port, 1)
            try:
                control_status = control.query_iboot_state()
            except SocketException:
                control_status = None
            if control_status:
                iboot.status = True
                iboot.save()
                status_list.append(True)
            else:
                iboot.status = False
                iboot.save()
                status_list.append(False)
        print status_list
