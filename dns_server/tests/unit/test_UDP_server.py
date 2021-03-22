import unittest
from dns_server.infrasructure.UDP_server import UDPServer
#from configuration import (
#    HOST,
#    PORT,
#    DNS_HOST,
#    DNS_PORT,
#)

class TestUDPServer(unittest.TestCase):

    def setUp(self) -> None:
        self.server = UDPServer()
        return super().setUp()

    def test_run(self):
        a+b
        #self.server.run()
        self.assertFalse(True)