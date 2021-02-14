from abc import ABC, abstractmethod


class AbstractHandler(ABC):

    @abstractmethod
    def get_formated(self):
        ...

    @abstractmethod
    def handle(self):
        ...