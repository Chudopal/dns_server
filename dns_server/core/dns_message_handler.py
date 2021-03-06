import socket
from datetime import datetime
from dns_server.core.dns_message import DNSMessage
from dns_server.core.requester_facade import RequesterFacade
from configuration import (
    DNS_HOST,
    DNS_PORT,
)


class DNSMessageHandler():

    def __init__(self,
                 requester: RequesterFacade,
                 data_record: bytes):
        self._requester: RequesterFacade = requester
        self._data_record: bytes = data_record
        self._dns_message = DNSMessage()
        self._dns_cursor = 0
        self._create_message()

    @property
    def dns_message(self):
        return self._dns_message

    def _create_message(self) -> DNSMessage:
        """Configure basic dns message
        """
        self._dns_message = DNSMessage()
        domain = self._get_question_domain()
        self._dns_message.name = domain[0]
        self._dns_message.type = int.from_bytes(domain[1], 'big')
        db_data = self._requester.get_record(
            self._dns_message
        )
        if db_data:
            self._dns_message.added_time = db_data[0][4]
            self._dns_message.time_to_live = db_data[0][2]
            self._dns_message.record = db_data[0][3]
            self.is_record_in_db = True
        else:
            self._is_record_in_db = False

    @property
    def response(self):
        dns_response: bytes = None
        if self._is_record_in_db and self._verify_time():
            dns_response = self._build_response()
            self._update()
        else:
            dns_response = self._make_authority_request()
            print(dns_response)
            self._data_record = dns_response
            self._parse_message()
            self._save()
        return dns_response

    def _parse_message(self):
        self._dns_message.record = ".".join(
            [str(record) for record in self._data_record[-4:]]
        )
        print(
            self._data_record
        )
        print(self._dns_message.record)

    def _build_response(self):
        transaction_id = self._dns_message[:2]
        flags = self._get_flags()
        q_count = b'\x00\x01'
        answer_account = len(self._get_recs()[0]).to_bytes(
            2, byteorder='big')

    def _verify_time(self):
        time_now = int(
            datetime.timestamp(
                datetime.now()
            )
        )
        deleted_time = self._dns_message.time_to_live \
            + self._dns_message.added_time
        if deleted_time <= time_now:
            return False
        else:
            return True

    def _make_authority_request(self):
        server_address = (DNS_HOST, DNS_PORT)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.sendto(self._data_record, server_address)
            data, _ = sock.recvfrom(512)
        finally:
            sock.close()
        return data

    def _get_question_domain(self):
        data = self._data_record[12:]
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
        return (".".join(domain_parts), question_type)

    def _get_flags(self):
        flags = self._dns_message[2:4]
        byte1 = bytes(flags[:1])
        QR = '1'
        OPCODE = ''
        for bit in range(1, 5):
            OPCODE += str(ord(byte1) & (1 << bit))
        AA = '1'
        TC = '0'
        RD = '0'
        # Byte 2
        RA = '0'
        Z = '000'
        RCODE = '0000'
        return int(QR+OPCODE+AA+TC+RD, 2).to_bytes(1, byteorder='big')\
            + int(RA+Z+RCODE, 2).to_bytes(1, byteorder='big')

    def _get_recs(self):
        domain, _ = self._get_question_domain()
        record = self._requester.get_record(self.dns_message.name)
        return (record[0], record[1], domain)

    def _save(self):
        self._requester.update_record(
            name=self._dns_message.name,
            type=self._dns_message.type,
            time_to_live=self._dns_message.time_to_live,
            record=self._dns_message.record
        )

    def _update(self):
        self._requester.add_record(
            name=self._dns_message.name,
            type=self._dns_message.type,
            time_to_live=self._dns_message.time_to_live,
            record=self._dns_message.record
        )
