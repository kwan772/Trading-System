import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbConnection:
    def __init__(self):
        self.engine = None
        self.session = None

    def connect(self):
        # Define the base class
        self.engine = create_engine(f'mysql+pymysql://root:{os.getenv("DB_PASSWORD")}@localhost/quant_trading')

        # Create a session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
