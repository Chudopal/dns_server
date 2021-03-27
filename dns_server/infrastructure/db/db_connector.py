import psycopg2
import os


def singleton(cls):
	instances = {}

	def getinstance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return getinstance


@singleton
class DBConnector():

	_connector = None

	@property
	def connector(self):
		if not self._connector:
			#self._connector = psycopg2.connect(
			#	dbname=os.environ.get("DBNAME"),
			#	user=os.environ.get("USER"),
			#	password=os.environ.get("PASSWORD")
			#)
			self._connector = psycopg2.connect(
            	dbname='dns',
            	user='admin',
            	password='admin'
            )
			self._connector.autocommit = True
			
		return self._connector

