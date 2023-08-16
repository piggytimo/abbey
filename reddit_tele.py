from __future__ import unicode_literals

import telegram
import praw
import logging
import html
import sys
import os
import json

from time import sleep
from datetime import datetime

credentials = {}

credentials["token"] = os.environ.get('TOKEN')
credentials["subreddit"] = os.environ.get('SUB')
credentials["channel"] = os.environ.get('CHANNEL')

log = logging.getLogger('doggo')
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

if credentials["token"] == "": 
    raise RuntimeError('Bot token not found 🙁! Put bot token🔐 in credentials.json!')
if credentials["subreddit"] == "":
    raise RuntimeError('Subreddit name not found 🙁! Enter the subreddit name📃 in credentials.json!')
if credentials["channel"] == "":
    raise RuntimeError('Telegram Channel name not found 🙁! Enter the channel name📰 in credentials.json!')

token = credentials["token"]
channel = credentials["channel"]
sub = "dogpictures"
start_time = datetime.utcnow().timestamp()

def prev_submissions():
    try:
        with open('prev_submissions.id', 'r') as f:
            return f.read().strip()
    except:
        return None

def write_submissions(sub_id):
    try:
        with open('prev_submissions.id', 'w') as f:
            f.write(sub_id)
    except:
        log.expection("Error writing sub ID!")

post = False
last_sub_id = prev_submissions()

if not last_sub_id:
    log.info("Latest submission not found, starting all submissions!")
    post = True
else:
    log.info("Last posted submission is {}".format(last_sub_id))

r = praw.Reddit(user_agent="Dank Doggo by Harsha :D", 
                client_id=os.environ.get('CLIENT_ID'),
                client_secret=os.environ.get('CLIENT_SECRET'),
                username=os.environ.get('RUSERNAME'),
                password=os.environ.get('RPASS'))
r.read_only = True
subreddit = r.subreddit(sub)

bot = telegram.Bot(token=token)
# for submission in subreddit.stream.submissions():
#     print(submission.url)

while True:
    try:
        for submission in subreddit.hot():
            try:
                link = "https://redd.it/{id}".format(id=submission.id)
                if not post and submission.created_utc < start_time:
                    log.info("Skipping {} --- latest submission not found!".format(submission.id))
                    if submission.id == last_sub_id:
                        post = True
                    continue
                image = html.escape(submission.url or '')
                title = html.escape(submission.title or '')
                user = html.escape(submission.author.name or '')

                template = "{title}\n{link}\nby {user}"
                message = template.format(title=title, link=link, user=user)

                log.info("Posting {}".format(link))
                bot.sendPhoto(chat_id=channel, photo=submission.url, caption=message)
                # bot.sendMessage(chat_id=channel, parse_mode=telegram.ParseMode.HTML, text=message)
                write_submissions(submission.id)
                sleep(300)
            except Exception as e:
                log.exception("Error parsing {}".format(link))
    except Exception as e:
        log.exception("Error fetching new submissions, restarting in 10 secs")
        sleep(10)






# import praw
# from telegram import Bot
# from telegram.ext import Updater
# import time
# import asyncio

# # Reddit API credentials
# reddit = praw.Reddit(
#     client_id='ahp6H2_Oku5pt6x6S-mGjQ',
#     client_secret='e6WWJqxTJlo7EpGjUDfIJT7Bwj4UAw',
#     user_agent='AbbeyRedditTelegram/1.0 by u/DentistLongjumping70'
# )

# # Telegram bot credentials
# bot_token = '6010686801:AAHsUQZMS4pyMVsVDNxNrWuq8TvCKb9uZhE'
# bot = Bot(token=bot_token)
# updater = Updater(bot=bot, update_queue = asyncio.Queue(maxsize=10)) #, use_context=True)
# # dispatcher = updater.dispatcher

# # Reddit subreddit and Telegram chat
# subreddit_name = 'conversation'  # Change this to the subreddit you're interested in
# chat_id = '@piggytimo'  # Use @usernames or IDs, find your chat ID using the get_chat_id function

# # async def some_function():
# #     chat_id = '123456789'  # Replace with the actual chat ID
# #     message = 'Hello, world!'
    
# #     await bot.send_message(chat_id=chat_id, text=message)

# # # Assuming you're within an async context (inside an async function or coroutine)
# # await some_function()


# def get_chat_id(update, context):
#     print(update.message.chat_id)

# # def main():
# #     subreddit = reddit.subreddit(subreddit_name)
# #     while True:
# #         for submission in subreddit.new(limit=5):
# #             message = f"New post in r/{subreddit_name}\n\n{submission.title}\n{submission.url}"
# #             bot.send_message(chat_id=chat_id, text=message)
# #             time.sleep(5)  # To avoid sending messages too quickly

# # if __name__ == '__main__':
# #     main()

# async def send_reddit_post(submission):
#     message = f"New post in r/{subreddit_name}\n\n{submission.title}\n{submission.url}"
#     await bot.send_message(chat_id='@piggytimo', text=message)

# async def main():
#     subreddit = reddit.subreddit(subreddit_name)
#     while True:
#         for submission in subreddit.new(limit=5):
#             await send_reddit_post(submission)
#             await asyncio.sleep(5)  # To avoid sending messages too quickly

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.create_task(main())
#     loop.run_forever()


