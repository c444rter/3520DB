from neo4j import GraphDatabase

class Neo4JConnector:
	def __init__(self, uri, user, password):
		self.driver = GraphDatabase.driver(uri, auth=(user, password))
	
	def close(self):
		self.driver.close()

	def print_greeting(self, message):
		with self.driver
