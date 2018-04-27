"""This sets the values of the projector dimming control panel via the network"""
import socket
import traceback


class CrestonControl(object):
    """The Crestron controller class.
    NOTE: This is not thread safe so use a controller in each thread."""
    def __init__(self, host, port=1313, timeout=15):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None

    def can_connect(self): return self.ping() == 'Pong'

    def ping(self): return self.send_command('Ping')

    def raise_high(self): return self.send_command('HighLvlUp')
    def lower_high(self): return self.send_command('HighLvlDown')

    def raise_low(self): return self.send_command('DimLvlUp')
    def lower_low(self): return self.send_command('DimLvlDown')

    def query_status(self):
        """
        Returns a map of status values like so:
        {'High': '55000', 'Current': '62965', 'Wake': '5:00 AM', 'Low': '62965', 'Lamp1': '2-1468', 'Sleep': '1:00 AM', 'Lamp2': '2-1469'}
        """
        lines = self.send_command('Update', lines=9)
        results = {}
        for line in lines:
            key, val = line.split('-', 1)
            results[key] = val
        return results


    def toggle_dim(self):
        """Returns True if enabled, False if disabled, and None if there is an error"""
        result = self.send_command('EnableDim')
        if result == None: return None
        return result == 'DimEnabled'

    def close(self):
        if self.sock:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.sock = None

    def format_command(self, command): return '%s%s' % (command, '\r\n')

    def send_command(self, command, lines=1):
        """
        Sends a command to the device.
        If lines == 1: it returns a string
        if lines > 1: it returns an array of strings
        Returns None if it can't control the device.
        """

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        try:
            self.sock.connect((self.host, self.port))
            welcome = self.sock.recv(1024)
            msg = self.format_command(command)
            self.sock.send(msg)
            results = []

            for i in range(lines):
                value = self.sock.recv(2048)
                if len(value.strip()) == 0: continue
                results.append(value.strip())

            if len(results) == 0:
                self.close()
                return None

            self.close()
            if lines == 1: return results[0]
            return results
        except:
            traceback.print_exc()
        self.close()
        return None
