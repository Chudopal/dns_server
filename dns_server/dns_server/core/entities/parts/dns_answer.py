class DNSAnswer():

    _types_in_hex: dict = {
        "A": 0x01,      # IP-address
        "NS": 0x02,     # DNS-server
        "CNAME": 0x03,  # canonic name. www,example.com
    }

    def __init__(self):
        self._domain_name: str = None
        self._type: str = None
        self._time_to_live: int = None
        self._length_of_data: int = 4 # 4 for IPv4, 6 for IPv6
        self._resource_data: str = None # IP of resouce

    @property
    def guestion_type_hex(self):
        return self._types_in_hex[self._type]

    @property
    def domain_name(self):
        return self._domain_name

    @property
    def TTL(self):
        return self._time_to_live

    @property
    def length_of_data(self):
        return self._length_of_data

    @property
    def resource_data(self):
        return self._resource_data