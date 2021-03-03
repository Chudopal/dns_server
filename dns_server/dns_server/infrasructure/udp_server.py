import socket
from dns_server.core.dns_message import DNSMessage
from dns_server.core.dns_message_handler import DNSMessageHandler


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

            dns_message = DNSMessage()
            dns_message_handler = DNSMessageHandler(dns_message)
            dns_message_handler.create_message(data)
            # Handle message

            dns_response = self._send_authority(message=data)

            message = DNSMessage(dns_response)

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
