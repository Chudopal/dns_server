import socket
from dns_server.core.dns_message_handler import DNSMessageHandler
from dns_server.infrastructure.db.db_requester import DBRequester


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

            requester = DBRequester()
            dns_message_handler = DNSMessageHandler(requester ,data)
            print(dns_message_handler.dns_message.name)
            print(dns_message_handler.dns_message.type)
            response = dns_message_handler.response
            self._socket.sendto(response, addr)

    def _send_authority(self, message):
        server_address = (self._dns_host, self._dns_port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(message, server_address)
            data, _ = sock.recvfrom(512)
        finally:
            sock.close()
        return data
