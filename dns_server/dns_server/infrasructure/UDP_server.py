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
        self._responce: bytearray = self._build_response()

    def _build_response(self):
        """Generate answer for dns query
        """
        # Transaction ID
        transaction_id = self._get_transaction_id()
        name = self._get_question_domain()[0]
        print(name)
        #type
        #time_to_live
        #record
        #flags = self._get_flags()


    def _get_transaction_id(self) -> list:
        """Returned id of dns message

        Returns:
            list: 2 bytes for transaction id
        """
        return self._message[:2]

    def _get_question_domain(self):
        data = self._message[12:]
        state = 0
        expected_length = 0
        domain_string = ''
        domain_parts = []
        x = 0
        y = 0
        for byte in data:
            if state == 1:
                if byte != 0:
                    domain_string += chr(byte)
                x += 1
                if x == expected_length:
                    domain_parts.append(domain_string)
                    domain_string = ''
                    state = 0
                    x = 0
                if byte == 0:
                    domain_parts.append(domain_string)
                    break
            else:
                state = 1
                expected_length = byte
            y += 1

        question_type = data[y:y+2]
        return (domain_parts, question_type)

    #def _get_flags(self):
    #    binary_flags = self._message[2:4]

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



if __name__ == "__main__":
    server = UDPServer()
    server.run()
