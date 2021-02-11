import pymongo


class DBManager():

    @classmethod
    def get_db(cls):
        ...

    @classmethod
    def create_db(cls):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mydatabase"]