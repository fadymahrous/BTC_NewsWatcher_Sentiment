from sqlalchemy import create_engine,URL,text,MetaData,Table
from typing import List,Dict,Any
from configparser import ConfigParser
from os import path,makedirs
import json
from datetime import datetime,timezone

class DatabaseEngine:
    def __init__(self):
        #Initiate DB Configuration
        config=ConfigParser()
        config.read(path.join('config','config.ini'))
        db_configuration=config['Database_Configuration']

        #Make Dictionary for failed to load data, to be check later and not to lose them.
        makedirs(path.join('Market_Sentiment','Failed_toload_headlines'),exist_ok=True)
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
                result = connection.execute(text("SELECT 1;"))
        except Exception as e:
            raise RuntimeError(f"couldnt create Engine and connect to the database for more details:{e}") from e
        
        # Reflect the existing table
        self.metadata = MetaData()
        self.forex_headlines = Table("trade_augur_news_healines", self.metadata, autoload_with=self.engine)

    def get_engine(self):
        return self.engine

    def load_to_database(self,data:List[Dict[str,Any]])-> None:
        if not data:
            raise ValueError(" the list passed is empty")
        
        #Create failed to load file
        today_str=datetime.now(timezone.utc).strftime('%Y%m%d')
        fail_to_load_file=path.join('Market_Sentiment','Failed_toload_headlines',f'Failed_load_{today_str}.txt')

        try:
            with self.engine.begin() as conn:
                conn.execute(self.forex_headlines.insert(), data)
        except Exception as e:
            with open(fail_to_load_file,'a') as failure_file:
                list_of_str=[json.dumps(record) for record in data]
                failure_file.write(','.join(list_of_str)+',')
            raise RuntimeError(f'We couldnt load the data correctly so its stored in {str(fail_to_load_file)} for more details {e}') from e

        print("Data inserted successfully.")