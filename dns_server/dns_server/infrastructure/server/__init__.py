#import sys
#import socket
#import binascii
#
#
#def send_udp_message(message, address, port):
#    """send_udp_message sends a message to UDP server
#
#    message should be a hexadecimal encoded string
#    """
#    message = message.replace(" ", "").replace("\n", "")
#    server_address = (address, port)
#
#    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    try:
#        sock.sendto(binascii.unhexlify(message), server_address)
#        data, _ = sock.recvfrom(4096)
#    finally:
#        sock.close()
#    return binascii.hexlify(data).decode("utf-8")
#
#
#def format_hex(hex):
#    """format_hex returns a pretty version of a hex string"""
#    octets = [hex[i:i+2] for i in range(0, len(hex), 2)]
#    pairs = [" ".join(octets[i:i+2]) for i in range(0, len(octets), 2)]
#    return "\n".join(pairs)
#
#
#message = """
#   AAAA01000001000000000000076578616d706c6503636f6d0000010001
# """
#
#response = send_udp_message(message, "8.8.8.8", 53)
#print(format_hex(response)) 
#
#
#class Server():
#    def __init__(
#        self, 
#        host: int, 
#        port: str,
#        authority_host: int,
#        authority_port: str,
#    ):
#        self._host = host
#        self._port = port
#        self._authority_host = authority_host
#        self._authority_port = authority_port
#
#    def run(self):
#
#        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
#        server_socket.bind((self._host,self._port))
#        try:
#            while 1:
#                data, addr = server_socket.recvfrom(1024)
#
#                #HERE WILL BE LOGIC
#
#                #p=DNSQuery(data)
#                #server_socket.sendto(p.respuesta(ip), addr)
#        except KeyboardInterrupt:   
#            server_socket.close()
#
#    def send_udp_message(message, address, port):
#        """send_udp_message sends a message to UDP server
#
#        message should be a hexadecimal encoded string
#        """
#        message = message.replace(" ", "").replace("\n", "")
#        server_address = (address, port)
#
#        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#        try:
#            sock.sendto(binascii.unhexlify(message), server_address)
#            data, _ = sock.recvfrom(4096)
#        finally:
#            sock.close()
#        return binascii.hexlify(data).decode("utf-8")
#
#
#




# python3
import socket
import sys
import time
import threading
import binascii
#from configuration import (
#    AUTHORITY_SERVER_HOST,
#    AUTHORITY_SERVER_PORT,
#    HOST,
#    PORT,
#)


AUTHORITY_SERVER_HOST = "8.8.8.8"
AUTHORITY_SERVER_PORT = 53
HOST = "127.0.0.1"
PORT = 53211


class Server():

    def run_server(self, port=53210):
        serv_sock = self.create_serv_sock(port)
        cid = 0
        while True:
            client_sock = self.accept_client_conn(serv_sock, cid)
            t = threading.Thread(target=self.serve_client,
                                 args=(client_sock, cid))
            t.start()  # Запуск нового потока
            cid += 1

    def serve_client(self, client_sock, cid):
        # Реализация совпадает с версией из синхронной обработки.
        request = self.read_request(client_sock)
        if request is None:
            print(f'Client #{cid} unexpectedly disconnected')
        else:
            response = self.handle_request(request)
            self.write_response(client_sock, response, cid)

    def create_serv_sock(self, serv_port):
        serv_sock = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM,
                                    proto=0)
        serv_sock.bind((HOST, serv_port))
        serv_sock.listen()
        return serv_sock

    def accept_client_conn(self, serv_sock, cid):
        client_sock, client_addr = serv_sock.accept()
        print(f'Client #{cid} connected '
              f'{client_addr[0]}:{client_addr[1]}')
        return client_sock

    def read_request(self, client_sock, delimiter=b'!'):
        request = bytearray()
        try:
            #while True:
            #    chunk = client_sock.recv(4096)
            #    if not chunk:
            #        # Клиент преждевременно отключился.
            #        return None
            #
            #    request += chunk
            #    print(request)
            #    if delimiter in request:
            #        return request

            request = client_sock.recv(4096)
            if not request:
                # Клиент преждевременно отключился.
                return None
            print(request)
            return request

        except ConnectionResetError:
            # Соединение было неожиданно разорвано.
            return None
        except:
            raise

    def handle_request(self, request):
        #time.sleep(5)
        #return request[::-1]
        return self.send_udp_message(request)

    def write_response(self, client_sock, response, cid):
        client_sock.sendall(response)
        client_sock.close()
        print(f'Client #{cid} has been served')

    def send_udp_message(self, message):
        """send_udp_message sends a message to UDP server

        message should be a hexadecimal encoded string
        """
        #message = message.replace(" ", "").replace("\n", "")
        server_address = (AUTHORITY_SERVER_HOST, AUTHORITY_SERVER_PORT)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(message, server_address)
            data, _ = sock.recvfrom(4096)
        finally:
            sock.close()
        print(binascii.hexlify(data).decode("utf-8"))
        print(data)
        return data

    def format_hex(self, hex):
        """format_hex returns a pretty version of a hex string"""
        octets = [hex[i:i+2] for i in range(0, len(hex), 2)]
        pairs = [" ".join(octets[i:i+2]) for i in range(0, len(octets), 2)]
        return "\n".join(pairs)

    def create_records(self, messsage):
        pass

    def save(self):
        pass


if __name__ == '__main__':
    server = Server()
    try:
        server.run_server(PORT)
    except Exception as e:
        server.run_server()