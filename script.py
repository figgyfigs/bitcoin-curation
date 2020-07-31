# twitter api bot for blocks
import keys
import tweepy
import requests


#Authentication for twitter API
auth = tweepy.OAuthHandler(keys.API_KEY, keys.API_SECRET_KEY)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


class Tweet:

    def __init__(self, info):
        self.height = info['height']
        self.hash = info['id']
        self.timestamp = info['timestamp']
        self.transactions = info['tx_count']
        self.size = info['size']

    def compose_tweet(self):
        tweet = "Block: {}\n# of transactions: {}".format(str(self.height), str(self.transactions))
        return tweet


    def send_tweet(self):
        tweet = self.compose_tweet()
        api.update_status(tweet)


def get_tip_hash():
    response = requests.get('https://blockstream.info/api/blocks/tip/hash')
    response = response.text
    return response

#Returns information about a block.
def block_info():
    block = get_tip_hash()
    response = requests.get('https://blockstream.info/api/block/' + block)
    info = response.json()
    temp = Tweet(info)
    return temp


#if ERROR MESSAGE is duplicate we can do something with try?
def main():
    temp = block_info()
    temp.compose_tweet()
    temp.send_tweet()


main()