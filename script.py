# twitter api bot for blocks
import keys
import tweepy
import requests

class Tweet:

    def __init__(self, info, auth):
        self.height = info['height']
        self.hash = info['id']
        self.timestamp = info['timestamp']
        self.transactions = info['tx_count']
        self.size = info['size']
        self.auth = auth

    def compose_tweet(self):
        tweet = "Block: {}\nHash: {}\n# of transactions: {}\nTimeStamp: {}\nSize(KB): {}".format(self.height, self.hash, self.transactions, self.timestamp, self.size)
        return tweet


    def send_tweet(self):
        tweet = self.compose_tweet()
        self.auth.update_status(tweet)
        #print(tweet)


#Authentication for twitter API
def authenticate():
    auth = tweepy.OAuthHandler(keys.API_KEY, keys.API_SECRET_KEY)
    auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

def get_tip_hash():
    response = requests.get('https://blockstream.info/api/blocks/tip/hash')
    response = response.text
    return response

#Returns information about a block.
def block_info():
    block = get_tip_hash()
    response = requests.get('https://blockstream.info/api/block/' + block)
    info = response.json()
    #temp = Tweet(info)
    return info

obj = Tweet(block_info(), authenticate())


#if ERROR MESSAGE is duplicate we can do something with try?
def main():
    #temp = block_info()
    obj.compose_tweet()
    obj.send_tweet()


main()