from neo4j import GraphDatabase
from neo4j import __version__ as neo4j_version

class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response

    # @staticmethod  
    def executeUpdate(self, tx, query):
        tx.run(query)
    
    def update(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            session.write_transaction(self.executeUpdate, query)
        except Exception as e:
            print("Update failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response
    

if __name__ == '__main__':
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="1234")
    # print(neo4j_version)

    query_string = '''
        MATCH (c:Customer)
        RETURN DISTINCT c.Country
        ORDER BY c.Country
    '''
    print(conn.query(query_string))