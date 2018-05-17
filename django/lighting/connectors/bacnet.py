#!/usr/bin/python

"""These functions wrap the bacnet command line apps from http://bacnet.sourceforge.net/
In your env. vars. you'll need a BACNET_BIN_DIR with the full path to the directory containing the compiled apps.
Like so (no slash on the end, please):
BACNET_BIN_DIR = '/usr/local/src/bacnet-stack-0.5.3/bin'
You can also set BACNET_EXECUTABLE_EXTENSION via env. variable as well.
"""

USAGE_MESSAGE = 'usage: bacnet_control <read-ao|write-ao> <device id> <property id> [<value>]'

import os, sys, subprocess
sys.path.insert(0, '../')

from ai.bacnet import BacnetControl


def main():
    try:
        action = sys.argv[1]
        device_id = sys.argv[2]
        property_id = sys.argv[3]
    except IndexError:
        print USAGE_MESSAGE
        return

    control = BacnetControl(os.environ['BACNET_BIN_DIR'])
    if action == 'read-ao':
        print control.read_analog_output(device_id, property_id)
    elif action == 'write-ao':
        try:
            value = sys.argv[4]
        except IndexError:
            print USAGE_MESSAGE
            return
        print control.write_analog_output_int(device_id, property_id, value)
    else:
        print USAGE_MESSAGE
        return

if __name__ == '__main__':
    main()
