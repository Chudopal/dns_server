class DNSQuestion():

    _question_types_in_hex: dict = {
        "A": 0x01,
        "NS": 0x02,
        "CNAME": 0x03,       
    }

    _question_classes_in_hex: dict = {
        "IN": 0x0001,
    }

    def __init__(self):
        self._question_name: str = None #name of resource
        self._question_type: str = None #["A", "NS", "CNAME"]
        self._question_class: str = None #as usual IN (0x0001)
