#!/usr/bin/python

"""This sets the values of the projector dimming control panel via the network"""

import sys
sys.path.insert(0, '../')
from creston import CrestonControl
import socket
import traceback


def main(control):
    while True:
        sys.stdout.write('COMMAND >> ')
        line = raw_input()
        if line == None: break
        line = line.strip()
        if len(line) == 0: continue
        if line == '\i':
            print control.query_status()
        else:
            response = control.send_command(line)
            if response: print response


def print_help():
    print 'python creston_control.py <host>'
    print 'Raw control commands can be entered.'
    print '\i queries the status'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_help()
        sys.exit(2)
    control = None
    try:
        control = CrestonControl(sys.argv[1])
        if not control.can_connect(): raise(Exception('Could not connect to %s' % sys.argv[1]))
        main(control)
    except EOFError:
        pass
    except KeyboardInterrupt:
        pass
    if control: control.close()
    print

# Copyright 2011 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
