class DNSMessage():
    
    def __init__(self):
        self._header: dict = dict()
        self._question: dict = dict()
        self._answer: dict = dict()
        self._authority: dict = dict()
        self._additional: dict = dict()

    @property
    def header(self):
        return self._header

    @property
    def question(self):
        return self._question

    @property
    def answer(self):
        return self._answer

    @property
    def authority(self):
        return self._authority

    @property
    def additional(self):
        return self._additional

