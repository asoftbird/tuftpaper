import os
import sys
import json
import tweepy
import urllib
import logging

from pathlib import PosixPath, WindowsPath
from dotenv import load_dotenv

# config
# TODO: pull this from exec arguments instead of json
with open("config.json") as cfgfile:
    CFG = json.load(cfgfile)

load_dotenv()

LOGFILE=CFG["log-file"]
ACCOUNT_NAME=CFG["account-name"]
OUTPUT_DIR=CFG["output-dir"]
TZMOD=int(CFG['timezone-modifier'])

CONS_KEY=os.getenv('TWT_CONSUMER_APIKEY')
CONS_SEC=os.getenv('TWT_CONSUMER_APISECRET')
AUTH_ACC=os.getenv('TWT_AUTH_ACCESSTOKEN')
AUTH_SEC=os.getenv('TWT_AUTH_SECRET')
BEARER=os.getenv('TWT_BEARER')

logging.basicConfig(filename=LOGFILE, 
    encoding='utf-8', 
    level=logging.INFO, 
    format='%(asctime)s %(message)s',
    datefmt='[%a %d-%m-%y %H:%M:%S]'
    )

# init
base_posix_path = PosixPath

if sys.platform.startswith("linux"):
    pass
elif sys.platform.startswith("win32"):
    PosixPath = WindowsPath

# references
auth = tweepy.OAuthHandler(CONS_KEY, CONS_SEC)
auth.set_access_token(AUTH_ACC, AUTH_SEC)
twapi = tweepy.API(auth, wait_on_rate_limit=True)
client = tweepy.Client(BEARER)

try:
    twapi.verify_credentials()
    print("Authentication OK")
except Exception as e:
    logging.error(f"Error during authentication: {e}")


# get user ID, latest tweet, tweet info from account name
user = twapi.get_user(screen_name=ACCOUNT_NAME)
user_id = user.id_str

logging.info(f"Configured for @{ACCOUNT_NAME} with ID {user_id}.")

response = client.get_users_tweets(user_id, max_results=5)

target_id = response.data[0].id
target_url = f"https://twitter.com/{ACCOUNT_NAME}/status/{target_id}"

tweet_object = twapi.lookup_statuses([target_id], include_entities=False, trim_user=True)
tweet_info_json = tweet_object[0]._json

# check for placeholder image from bot
if "4325.000" in tweet_info_json['text']:
    logging.info("Bot posted an error image, skipping")
else:
    tweet_time = tweet_info_json['created_at'][4:-14] # 'Aug 19 15:01'
    tweet_time_date = tweet_time[:-6] # 'Aug 19'
    tweet_time_h = tweet_time[7:-3] # '15'
    tweet_time_min = tweet_time[10:] # '01'
    tweet_time = f"{tweet_time_date} {int(tweet_time_h)+TZMOD}:{tweet_time_min}" # 'Aug 19 17:01'

    tweet_time_date_safe = f"{tweet_time[:-9]}{tweet_time[4:-6]}" # 'Aug19'
    tweet_time_safe = f"{tweet_time_date_safe}_{int(tweet_time_h)+TZMOD}{tweet_time_min}" # 'Aug19_1701'

    tweet_media_url = tweet_info_json['extended_entities']['media'][0]['media_url']+":large"

    logging.info(f"Retrieved tweet {target_url}, \n \t published at {tweet_time} with media url {tweet_media_url}")

    image_filename = f"{ACCOUNT_NAME}_{tweet_time_safe}.jpg"

    dl_image = urllib.request.urlretrieve(tweet_media_url, filename=OUTPUT_DIR+image_filename)
    logging.info(f"Saved image as {image_filename} in {OUTPUT_DIR}.")