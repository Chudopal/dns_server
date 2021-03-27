from datetime import datetime
from dns_server.infrastructure.db.db_connector import DBConnector
from dns_server.core.requester_facade import RequesterFacade

class DBRequester(RequesterFacade):

    def __init__(self):
        self._connector = DBConnector().connector
        self._cursor = self._connector.cursor()
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS dns_record(
                name VARCHAR(50),
                record_type INTEGER,
                time_to_live INTEGER,
                record VARCHAR(20),
                time INTEGER
            );
            """
        )

    def get_record(self, name: str):
        try:
            self._cursor.execute(
                f"""SELECT * FROM dns_record
                WHERE name='{name}';
                """
            )
        except Exception as exp:
            print(Exception)
        return self._cursor.fetchall()

    def add_record(self,
                   name: str,
                   type: str,
                   time_to_live: int,
                   record: str):
        try:
            self._cursor.execute(
                f""" INSERT INTO dns_record(name, record_type, time_to_live, record, time)
                VALUES ('{name}', {type}, {time_to_live}, '{record}', {self._get_time()});
                """
            )
        except Exception as exp:
            print(exp)

    def update_record(self,
                      name: str,
                      type: str,
                      time_to_live: int,
                      record: str):
        try:
            self._cursor.execute(
                f"""UPDATE dns_record SET
                type={type},
                time_to_live={time_to_live},
                record='{record}',
                time={self._get_time()}
                WHERE dns_record.name='{name}';
                """
            )
        except Exception as exp:
            print(exp)

    @staticmethod
    def _get_time():
        return int(
            datetime.timestamp(
                datetime.now()
            )
        )
    