from db_connector import DBConnector


class BDRequestor():

    def __init__(self):
        self._connector = DBConnector().connector
        self._cursor = self._connector.cursor()

    def get_record(self, name: str):
        try:
            self._cursor.execute(
                f"""SELECT * FROM dns_records 
                WHERE name={name};
                """
            )
        except Exception as exp:
            print(Exception)
        return self._cursor.fetchall()

    def add_record(self,
                   name: str,
                   record_type: str,
                   time_to_live: int,
                   record: str):
        try:
            self._cursor.execute(
                f""" INSERT INTO dns_records(name, record_type, time_to_live, record)
                VALUES ({name}, {record_type}, {time_to_live}, {record});
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
                f"""UPDATE dns_records SET
                type={type},
                time_to_live={time_to_live},
                record={record}
                WHERE name={name};
                """
            )
        except Exception as exp:
            print(exp)
