import os
import re
import json
import tweepy
import urllib
import logging

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
    # "created_at":"Fri Aug 19 12:01:31 +0000 2022",
    tweet_datetime = re.search(r"\w{3}\s(\w{3})\s(\d{1,2})\s(\d{1,2})\:(\d{1,2}):.*", tweet_info_json['created_at'])
    tweet_month = tweet_datetime.group(1)
    tweet_day = tweet_datetime.group(2).zfill(2)
    tweet_hour = tweet_datetime.group(3).zfill(2)
    tweet_min = tweet_datetime.group(4)

    tweet_parseddate = f"{tweet_day}-{tweet_month}_{tweet_hour}{tweet_min}" #19-Aug_1701

    tweet_media_url = tweet_info_json['extended_entities']['media'][0]['media_url']+":large"

    logging.info(f"Retrieved tweet {target_url}, \n \t published at {tweet_parseddate} with media url {tweet_media_url}")

    image_filename = f"{tweet_parseddate}_{ACCOUNT_NAME}.jpg" #19-Aug-_1701_asoftbird.jpg

    dl_image = urllib.request.urlretrieve(tweet_media_url, filename=OUTPUT_DIR+image_filename)
    logging.info(f"Saved image as {image_filename} in {OUTPUT_DIR}.")