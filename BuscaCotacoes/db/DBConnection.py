from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBConnection:
    conn = None
    engine = None
    session = None

    def createConnection(self, strconn):
        self.engine = create_engine(strconn, isolation_level="READ UNCOMMITTED")
        self.conn = self.engine.connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def connectionCreated(self):
        if self.engine is None:
            return False
        else:
            return True

    def disposeConnection(self):
        self.session.close()
        self.conn.close()

    def __repr__(self):
        return f'DBConnection'
