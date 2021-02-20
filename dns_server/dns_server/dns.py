import socket


HOST = '127.0.0.1'
PORT = 53

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

while(True):
    data, addr = sock.recvfrom(512)
    print(data)
    dns_response = b"Hello World"
    sock.sendto(dns_response, addr)


