import os
import sys
import time
import signal
import logging

from django.core.management.base import BaseCommand, CommandError

from scheduler.models import Scheduler

from lighting.tasks import ProjectorEventTask
from iboot.tasks import IBootEventTask


SCHEDULED_TASKS = [
                   ProjectorEventTask(),
                   IBootEventTask(),
                  ]

SCHEDULED_PATH_PID = '/tmp/artserver_scheduler.pid'


class Command(BaseCommand):

    help = "Runs the scheduler."

    def handle(self, *labels, **options):
        print 'Running the scheduler'
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename='/tmp/scheduler-art-server.txt', filemode = 'w')
        write_proc(SCHEDULED_PATH_PID)

        scheduler = Scheduler()
        for task in SCHEDULED_TASKS:
            scheduler.add_task(task)
        scheduler.start_all_tasks()

        try:
            while True: time.sleep(10000000)
        except KeyboardInterrupt:
            scheduler.stop_all_tasks()
            os._exit(0)
        print 'Exited'


def write_proc(lockfile_path):
    if os.access(lockfile_path, os.F_OK):
        pidfile = open(lockfile_path, "r")
        pidfile.seek(0)
        old_pd = pidfile.readline()
        if os.path.exists("/proc/%s" % old_pd): # this only works on OSes with /proc/ (e.g. linux)
            print "You already have an instance of the program running"
            print "It is running as process %s," % old_pd
            return False
        else:
            os.remove(lockfile_path)

    pidfile = open(lockfile_path, "w")
    pidfile.write("%s" % os.getpid())
    pidfile.close
    return True