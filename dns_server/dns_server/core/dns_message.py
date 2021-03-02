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
        # type
        # time_to_live
        # record
        flags = self._get_flags()
        print(flags)

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

    def _get_flags(self):
        """Parse flags from incoming message 
        and create new for answer"""
        flags = self._message[2:4]
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

    @property
    def message(self) -> bytearray:
        return self._message

    @property
    def response(self):
        self._build_response()
