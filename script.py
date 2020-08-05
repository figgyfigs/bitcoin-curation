# twitter api bot for blocks
import keys
import tweepy
import requests

class Tweet:

    def __init__(self, info, auth):
        self.height = info['height']
        self.hash = info['id']
        self.transactions = info[# twitter api bot for blocks
import keys
import tweepy
import requests

class Tweet:

    def __init__(self, info, auth):
        self.height = info['height']
        self.hash = info['id']
        self.transactions = info['tx_count']
        self.auth = auth

    def compose_tweet(self):
        tweet = "Block: {}\n# of transactions: {}".format(self.height, self.transactions,)
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
    print(info)
    #return info

def coinbase_txid():
    response = requests.get('https://blockstream.info/api/block/' + get_tip_hash() + '/txid/0')
    txid = response.text
    return txid
#Calculates and returns the total fees in a specific block
#First: Look up the coinbase txid
#Second: Using the txid look up the tx info
#Calculate fee per block (vout - 6.25)
def fees_per_block(txid):
    response = requests.get('https://blockstream.info/api/tx/' + txid)
    response = response.json()
    print(response)


#block_info()
txid = coinbase_txid()
fees_per_block(txid)



#obj = Tweet(block_info(), authenticate())


#if ERROR MESSAGE is duplicate we can do something with try?
def main():
    #temp = block_info()
    obj.compose_tweet()
    obj.send_tweet()


#main()
'tx_count']
        self.auth = auth

    def compose_tweet(self):
        tweet = "Block: {}\n# of transactions: {}".format(self.height, self.transactions,)
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
    print(info)
    #return info

def coinbase_txid():
    response = requests.get('https://blockstream.info/api/block/' + get_tip_hash() + '/txid/0')
    txid = response.text
    return txid
#Calculates and returns the total fees in a specific block
#First: Look up the coinbase txid
#Second: Using the txid look up the tx info
#Calculate fee per block (vout - 6.25)
def fees_per_block(txid):
    response = requests.get('https://blockstream.info/api/tx/' + txid)
    response = response.json()
    print(response)


#block_info()
txid = coinbase_txid()
fees_per_block(txid)



#obj = Tweet(block_info(), authenticate())


#if ERROR MESSAGE is duplicate we can do something with try?
def main():
    #temp = block_info()
    obj.compose_tweet()
    obj.send_tweet()


#main()
