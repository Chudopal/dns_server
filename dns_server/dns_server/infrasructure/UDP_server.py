#from configuration import DNS_HOST, HOST
#HOST = '127.0.0.1'
#PORT = 53
#DNS_HOST = '8.8.8.8'
#DNS_PORT = 53

#from dns_server.core.DNS_message import DNSMessage
#import socket
#import sys
#import os
#
#PACKAGE_PARENT = '..'
#SCRIPT_DIR = os.path.dirname(os.path.realpath(
#    os.path.join(os.getcwd(), os.path.expanduser(__file__))))
#sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import socket


class DNSMessage():
    """Entity for dns message
    """

    def __init__(self, dns_message):
        self._message: bytearray = dns_message
        self._responce: bytearray = None

    def _build_response(self):
        """Generate answer for dns query
        """
        # Transaction ID
        transaction_id = self._get_transaction_id()

    def _get_transaction_id(self) -> list:
        """Returned id of dns message

        Returns:
            list: 2 bytes for transaction id
        """
        return self._message[:2]

    @property
    def message(self) -> bytearray:
        return self._message

    @property
    def response(self):
        self._build_response()




class UDPServer():
    """ UDP server for receiving and sending 
    messages to DNS authority server
    """
    def __init__(self,
                 host: str = '127.0.0.1',
                 port: int = 53,
                 dns_host: str = '8.8.8.8',
                 dns_port: int = 53):
        self._host: str = host
        self._port: int = port
        self._dns_host: str = dns_host
        self._dns_port: int = dns_port

    def run(self):
        """Initialize and run server execution
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(
            (
                self._host,
                self._port,
            )
        )
        self._run_server()

    def _run_server(self):
        while(True):
            data, addr = self._socket.recvfrom(512)

            print(data)

            dns_response = self._send_authority(message=data)

            self._socket.sendto(dns_response, addr)

    def _send_authority(self, message):
        server_address = (self._dns_host, self._dns_port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(message, server_address)
            data, _ = sock.recvfrom(512)
        finally:
            sock.close()
        return data



if __name__ == "__main__":
    server = UDPServer('127.0.0.1', 53)
    server.run()
