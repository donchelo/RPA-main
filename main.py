import schedule
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from mail_reader.main import MailReader
from assistant.main import Assistant
from json_parser.main import JsonParser
from rpa.main import RPA
import logging

load_dotenv()
logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')

def run_task():
    logging.info('Starting sequence')
    print('Starting sequence')

    # #Mail Reader
    #mail_reader = MailReader()
    #mail_reader.download_pdfs()
    #time.sleep(10)  # Wait for pdfs to download

    # #Assistant
    # assistant = Assistant()
    # assistant.loop_clients_and_call_assistant()
    # time.sleep(10)  # Wait for assistant to finish

    # #Json Parser
    # json_parser = JsonParser()
    # json_parser.call_json_parser()
    # time.sleep(10)  # Wait for json parser to finish

    # #RPA
    rpa = RPA()
    max_retries = 3
    for i in range(max_retries):
        if rpa.open_sap():
            rpa.run()
            rpa.close_sap()
            break
        else:
            print(f"Failed to open SAP. Retrying... ({i+1}/{max_retries})")
            time.sleep(10)

    logging.info('Finished sequence, waiting for next run in 10 minutes')
    print('Finished sequence, waiting for next run in 10 minutes')

run_task()  # Run once at startup, outside of the loop
schedule.every(10).minutes.do(run_task)

while True:
    schedule.run_pending()
    time.sleep(5)  # Check for pending tasks every second
    print('.', end='')
    time.sleep(5)  # Check for pending tasks every second
    print('*', end='')
