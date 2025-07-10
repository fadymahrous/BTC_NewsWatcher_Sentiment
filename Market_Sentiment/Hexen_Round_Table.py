
from Market_Sentiment.Get_Latest_Headlines_Forexlive import GetLatestHeadlinesForexlive
from Market_Sentiment.LLM_Judging import LLMJudging
from typing import List,Dict
import json
from time import sleep

THROTLING_GUARD=30

class HexenRoundTable:
    def __init__(self,hexen_name_list:List=None,discuss_over_last_n_minutes:int=None):
        if hexen_name_list is None or discuss_over_last_n_minutes is None:
            raise ValueError(f'please provide part of the model names from amazon bedrock to look for it in list, and the last n minutes to check news at these minutes')
        self.hexen_name_list=hexen_name_list
        self.discuss_over_last_n_minutes=discuss_over_last_n_minutes
        self.judging=LLMJudging()
    
    def start_discussion(self)->List[Dict]:
        """
        Orchestrates retrieval of recent ForexLive headlines and LLM sentiment evaluation across configured models.
        """
        read_news=GetLatestHeadlinesForexlive()
        news_list=read_news.get_recent_articles(self.discuss_over_last_n_minutes)

        if news_list:
            for headline in news_list:
                headline_and_detail=f"Headline-{headline['title']} Details-{headline['details']}"
                # Iterating over each Hexe
                opinions={}
                for hexe in self.hexen_name_list:
                    try:
                        opinions[hexe]=self.judging.send_message(hexe,headline_and_detail)
                    except Exception as e:
                        raise RuntimeError(f"couldnt send to model {hexe}, for more details check:{e}") from e
                sleep(THROTLING_GUARD)
                headline['hexenmeinung']=json.dumps(opinions)
        return news_list


        
