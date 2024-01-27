# This is a script to analyze then absorb data from tg. There are two scenarios for this:
# 1. Scrap all data on a given channel for later analysis to find a keyword (i.e. chat about a 0day)
# 2. Scrap only keywords related to the issue at hand (i.e. only search for dialogue on '0day' 'vuln' 'exploit')
# Frankly, I think it's best to just suck up all data (1) over a period of time, then run the analysis (~1 week), save relevant data ,and wipe the rest to add more. 
# Store any relevant containers on the cloud.



# using python-telegram-bot and pandas
from telegram.ext import Updater
import pandas as pd
import logging
from datetime import datetime

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# telegram bot authorization token
TOKEN = 'paste tg token' #tg token here

# initialize list to store the scraped message
scraped_messsages = []

# message handler call back function (When the Telegram bot receives a message,
# the Telegram API triggers the callback function associated with that event.
# the MessageHandler is responsible for listening for messages that match certain
# filters (like text messages that are not commands), and when it detects a match, it calls the search_messages function.)

def search_messages(update, context):
    message_text = update.message.text.lower()
    if any(keyword in message_text for keyword in ['critical','vuln','0day','zero day','exploit']):
        
        # collect relevant data
        author = update.message.from_user.username
        message =  update.message.text
        date = update.message.date

        # append data to list of scrapped msgs
        scraped_messsages.append({
            'author': author,
            'message': message,
            'date': date
        })

# main function to start the bot
def main():
    updater = Updater(TOKEN, used_context=True)
    dp = updater.dispatcher

    # register msg handler
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), search_messages))

# start the bot
    updater.start_polling()
    updater.idle()

# when the bot is stopped, save the scraped msgs to a csv file
    pd.DataFrame(scraped_messsages).to_csv('scraped_messages.csv', index=False)

if __name__ == '__main__':
    main()     

        
