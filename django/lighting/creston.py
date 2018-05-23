"""This sets the values of the projector dimming control panel via the network"""
import socket
import traceback
from socket import error as socket_error


BUFF = 1024


class SocketException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class CrestonControl(object):
    """The Crestron controller class.
    NOTE: This is not thread safe so use a controller in each thread."""
    def __init__(self, host, port=1313, timeout=15):
        self.host = host
        self.port = port
        self.timeout = timeout


    def can_connect(self):
        return self.ping() == 'Pong'


    def ping(self): 
        return self.send_command('Ping')


    def raise_high(self):
        return self.send_command('HighLvlUp')


    def lower_high(self):
        return self.send_command('HighLvlDown')


    def raise_low(self):
        return self.send_command('DimLvlUp')


    def lower_low(self): 
        return self.send_command('DimLvlDown')


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


    def format_command(self, command): 
        return '%s%s' % (command, '\r\n')


    def send_command(self, command, lines=1):
        """
        Sends a command to the device.
        If lines == 1: it returns a string
        if lines > 1: it returns an array of strings
        Returns None if it can't control the device.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.host, self.port))
            msg = self.format_command(command)
            sock.send(msg)
            results = []

            for i in range(lines):
                value = sock.recv(BUFF)
                if len(value.strip()) == 0:
                    continue
                results.append(value.strip())

            if len(results) == 0:
                sock.close()
                return None

            if lines == 1:
                sock.close()
                return results[0]

            return results
        except socket_error as serr:
            sock.close()
            raise SocketException(serr)