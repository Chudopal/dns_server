class DNSHeader():

    def __init__(self):
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