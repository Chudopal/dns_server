import socket


class UDPServer():
    def __init__(self, host, port):
        self._host: str = host 
        self._port: int = port

    def run(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(
            (
                self._host,
                self._port,
            )
        )

    def _run_server(self):
        while(True):
            data, addr = self._socket.recvfrom(512)
            
            print(data)
            
            #dns_response = send_authority(message=data)
            
            #sock.sendto(dns_response, addr)
