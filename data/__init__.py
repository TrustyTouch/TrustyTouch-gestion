import psycopg2

class db:
    conn = None
    conn_auth = None
    @staticmethod
    def getconn():
        if db.conn is None:
            db.conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="postgres",
                host="host.docker.internal",
                port="5432"
            )
        return db.conn
    @staticmethod
    def getconn_auth():
        if db.conn_auth is None:
            db.conn_auth = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="postgres",
                host="host.docker.internal",
                port="5433"
            )
        return db.conn_auth