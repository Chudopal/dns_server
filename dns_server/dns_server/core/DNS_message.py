class DNSMessage():
    """Entity for dns message
    """
    def __init__(self, dns_message):
        self._message: bytearray = dns_message
        self._responce: bytearray = None

    def _build_response(self):
        """Generate answer for dns query
        """
        # Transaction ID
        transaction_id = self._get_transaction_id()

    def _get_transaction_id(self) -> list:
        """Returned id of dns message

        Returns:
            list: 2 bytes for transaction id
        """
        return self._message[:2]

    @property
    def message(self) -> bytearray:
        return self._message

    @property
    def response(self):
        self._build_response()
