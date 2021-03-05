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
            self._save()
        else:
            dns_response = self._make_authority_request()
            self._data_record = dns_response
            self._create_message()
            self._update()
        return dns_response

    def _build_response(self):
        pass

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
