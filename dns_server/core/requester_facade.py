from abc import ABC, abstractmethod


class RequesterFacade(ABC):

    @abstractmethod
    def get_record(self, name: str) -> tuple:
        ...

    @abstractmethod
    def add_record(self,
                   name: str,
                   record_type: str,
                   time_to_live: int,
                   record: str):
        ...

    @abstractmethod
    def update_record(self,
                      name: str,
                      type: str,
                      time_to_live: int,
                      record: str):
        ...            