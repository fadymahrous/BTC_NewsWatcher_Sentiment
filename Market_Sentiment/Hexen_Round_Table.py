
from Market_Sentiment.Get_Latest_Headlines_Forexlive import GetLatestHeadlinesForexlive
from Market_Sentiment.LLM_Judging import LLMJudging
from typing import List
import json
from time import sleep

break_for_throttling_in_seconds=30

class HexenRoundTable:
    def __init__(self,hexen_name_list:List=None,discuss_over_last_n_minutes:int=None):
        if hexen_name_list is None or discuss_over_last_n_minutes is None:
            raise ValueError(f'please provide part of the model names from amazon bedrock to look for it in list, and the last n minutes to check news at these minutes')
        self.hexen_name_list=hexen_name_list
        self.discuss_over_last_n_minutes=discuss_over_last_n_minutes
        self.judging=LLMJudging()
    
    def start_discussion(self)->List:
        read_news=GetLatestHeadlinesForexlive()
        news_list=read_news.get_recent_articles(self.discuss_over_last_n_minutes)

        if news_list:
            for headline in news_list:
                headline_and_detail=f"Headline-{headline['title']} Details-{headline['details']}"
                ##Iteriting over each Hexe
                opinions={}
                for hexe in self.hexen_name_list:
                    opinions[hexe]=self.judging.send_message(hexe,headline_and_detail)
                sleep(break_for_throttling_in_seconds)
                headline['hexenmeinung']=json.dumps(opinions)
        return news_list


        
