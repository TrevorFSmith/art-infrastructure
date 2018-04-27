#!/usr/bin/python
"""Classes which are useful when controlling projectors using the PJLink protocol.
    Information on the PJLink protocol can be found here: http://pjlink.jbmia.or.jp/english/
"""

import sys, time
sys.path.insert(0, '../')
from pjlink import PJLinkProtocol, PJLinkController
from mocks import MockPJLinkProjector


USAGE_MESSAGE = 'usage: pjlink [projector|name|on|off|mute|unmute|mute-status] <host> <password>'


def main():
    try:
        action = sys.argv[1]
    except IndexError:
        print USAGE_MESSAGE
        return
    if action == 'name':
        controller = PJLinkController(host=sys.argv[2], password=sys.argv[3])
        print controller.query_name()
    elif action == 'off':
        controller = PJLinkController(host=sys.argv[2], password=sys.argv[3])
        controller.power_off()
    elif action == 'on':
        controller = PJLinkController(host=sys.argv[2], password=sys.argv[3])
        controller.power_on()
    elif action == 'status':
        controller = PJLinkController(host=sys.argv[2], password=sys.argv[3])
        print controller.query_power()
    elif action == 'mute':
        controller = PJLinkController(host=sys.argv[2], password=sys.argv[3])
        print controller.set_mute(PJLinkProtocol.VIDEO_MUTE_ON)
    elif action == 'unmute':
        controller = PJLinkController(host=sys.argv[2], password=sys.argv[3])
        print controller.set_mute(PJLinkProtocol.VIDEO_MUTE_OFF)
    elif action == 'mute-status':
        controller = PJLinkController(host=sys.argv[2], password=sys.argv[3])
        print "(audio is muted, video is muted): (%s, %s)"  % controller.query_mute()
    elif action == 'projector':
        projector = MockPJLinkProjector()
        projector.port = 4352
        projector.start()
        seconds_to_wait = 5
        while projector.running == False and seconds_to_wait > 0:
            time.sleep(1)
            seconds_to_wait -= 1
        if not projector.running:
            print 'Could not start the projector'
            return
        print 'Projector running: %s:%s' % (projector.server.getsockname()[0], projector.server.getsockname()[1])
        while True: time.sleep(100)
    else:
        print USAGE_MESSAGE
        return


if __name__ == "__main__":
    main()
