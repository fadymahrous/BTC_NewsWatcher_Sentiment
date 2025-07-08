import time
from Market_Sentiment.Hexen_Round_Table import HexenRoundTable
from Market_Sentiment.Database_Engine import DatabaseEngine

hexen_models = ['llama3-2', 'pixtral-large', 'sonnet-4']
cycle_every_in_min=20
def main():
    save_discussion = DatabaseEngine()  # Reuse this if safe
    while True:
        print("Starting new discussion cycle...")
        round_table = HexenRoundTable(hexen_models, cycle_every_in_min)
        result = round_table.start_discussion()
        if result:
            save_discussion.load_to_database(result)

        print("Cycle complete. Sleeping for 20 minutes...")
        time.sleep(cycle_every_in_min * 60)

if __name__ == '__main__':
    main()
