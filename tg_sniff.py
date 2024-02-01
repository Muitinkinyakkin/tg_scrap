# This is a script to scrap data from tg on a given channel for later analysis to find specific keywords (i.e. chat about insider threats)




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
TOKEN = 'paste tg token' 

# initialize list to store the scraped message
scraped_messsages = []

# message handler call back function (When the Telegram bot receives a message,
# the Telegram API triggers the callback function associated with that event.
# the MessageHandler is responsible for listening for messages that match certain
# filters (like text messages that are not commands), and when it detects a match, it calls the search_messages function.)

def search_messages(update, context):
    message_text = update.message.text.lower()
    if any(keyword in message_text for keyword in ['insider','I know someone','teller']):
        
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

        
