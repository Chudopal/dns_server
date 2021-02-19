class DNSQuestion():
    """ DNS question collect query to dns server """
    
    _question_types_in_hex: dict = {
        "A": 0x01,      # IP-address
        "NS": 0x02,     # DNS-server
        "CNAME": 0x03,  # canonic name. www,example.com
    }

    _question_classes_in_hex: dict = {
        "IN": 0x0001,
    }

    def __init__(self):
        self._question_name: str = None #name of resource
        self._question_type: str = None #["A", "NS", "CNAME"]
        self._question_class: str = None #as usual IN (0x0001)

    @property
    def guestion_type_hex(self):
        return self._question_types_in_hex[self._question_type]

    @property
    def question_class_hex(self):
        return self._question_classes_in_hex[self._question_class]

    @property
    def question_name(self):
        return self._question_name