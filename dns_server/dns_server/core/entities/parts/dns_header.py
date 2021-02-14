class DNSHeader():

    def __init__(self):

        # metadata
        self._message_type: bool = True # 1 - qury, 0 - response
        self._operation_code: int = 0 # 0 - standart query, 1 - invers query, 2 - server's status query
        self._authoritative_answer = False #True if is from db, not from auth. server
        self._truncated = False # the message is truncated
        self._recursion_desired = True # if False - return addres of another DNS server, else - return required IP
        self._recursion_available = True # if it true - if server can be resursed
        self._return_code = 0 # 0 - ok, 3 - name mistake. 

        # about body
        self._question_count: int = None
        self._answer_count: int = None
        self._authority_count: int = None
        self._additional_count: int = None

    @property
    def question_count(self):
        return self._question_count

    @property
    def answer_count(self):
        return self._answer_count

    @property
    def authority_count(self):
        return self._authority_count

    @property
    def additional_count(self):
        return self._additional_count