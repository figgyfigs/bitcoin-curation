# twitter api bot for blocks
import keys
import tweepy
import requests

BLOCK_REWARD = 625000000

#Class Tweet
class Tweet:

    def __init__(self, info, auth, fees):
        self.height = info['height']
        self.hash = info['id']
        self.transactions = info['tx_count']
        self.fees = fees
        self.auth = auth

    def compose_tweet(self):
        tweet = "Block: {}\n# of transactions: {}\nFees paid(sats): {}\n#Bitcoin".format(self.height, self.transactions, format_reward(self.fees))
        return tweet

    def send_tweet(self):
        tweet = self.compose_tweet()
        self.auth.update_status(tweet)

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
    return info

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
    tx_info = response.json()
    total_reward = tx_info['vout'][0]['value']
    #return total_reward - BLOCK_REWARD
    return 192344321


#Need to add cases that check when the fees is less than a bitcoin(million sats)
def format_reward(fees):

    fees  = str(fees)

    if len(fees) == 9:
        first_str = fees[0:1]
        second_str = fees[1:]
        final_str = first_str + '.' + second_str
        return final_str



def main():

    txid = coinbase_txid()
    obj = Tweet(block_info(), authenticate(), fees_per_block(txid))
    obj.compose_tweet()
    obj.send_tweet()


main()
