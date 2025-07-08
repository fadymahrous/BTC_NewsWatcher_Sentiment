from sqlalchemy import create_engine,URL,text,MetaData,Table
from typing import List
from configparser import ConfigParser
from os import path

class DatabaseEngine:
    def __init__(self):
        #Initiate DB Configuration
        config=ConfigParser()
        config.read(path.join('config','config.ini'))
        db_configuration=config['Database_Configuration']
        """Better to be fetched from config file using config parser"""
        url_object = URL.create(
            "postgresql+psycopg2",
            database=db_configuration.get('name'),
            username=db_configuration.get('user'),
            password=db_configuration.get('password'),
            host=db_configuration.get('host'),
        )
        self.engine = create_engine(url_object)
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT CURRENT_TIMESTAMP;"))
        except Exception as e:
            raise e

    def get_engine(self):
        return self.engine

    def load_to_database(self,data:List):
        if not data:
            raise ValueError(" the list passed is empty")
        metadata = MetaData()

        # Reflect the existing table
        forex_headlines = Table("trade_augur_news_healines", metadata, autoload_with=self.engine)

        with self.engine.begin() as conn:
            conn.execute(forex_headlines.insert(), data)

        print("Data inserted successfully.")