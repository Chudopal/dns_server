import socket


HOST = '127.0.0.1'
PORT = 53
DNS_HOST = '8.8.8.8'
DNS_PORT = 53


class DNSQueryParser():
    def __init__(self, dns_message):
        self._message = dns_message

    @property
    def message(self):
        return message

    @property
    def response(self):
        self,_build_response()

    def _build_response(self):
        """Generate answer for dns query
        """
        # Transaction ID
        TransactionID = self._get_transaction_id()

    def _get_transaction_id(self) -> list:
        """Returned id of dns message

        Returns:
            list: 2 bytes for transaction id
        """
        return self._message[:2]
    



def send_authority(message):
    server_address = (DNS_HOST, DNS_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message, server_address)
        data, _ = sock.recvfrom(4096)
    finally:
        sock.close()
    return data


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

while(True):
    data, addr = sock.recvfrom(512)
    print(data)
    dns_response = send_authority(message=data)
    sock.sendto(dns_response, addr)


