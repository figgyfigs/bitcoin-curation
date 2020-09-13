# twitter api bot for blocks
import keys
import tweepy
import requests
import time

BLOCK_REWARD = 625000000


class Tweet:

    def __init__(self, info, auth, fees, fee_estimates, mempool):
        self.height = info['height']
        self.hash = info['id']
        self.transactions = info['tx_count']
        self.fees = fees
        self.auth = auth
        self.estimates = fee_estimates
        self.mempool_tx = mempool['count']
        self.mempool_fees = mempool['total_fee']
        self.previous_blockhash = info['previousblockhash']


    #def check_block(self):
        #self.height


    def compose_tweet(self):
        tweet = "Block: {}\n# of transactions: {}\nFees paid: {} BTC\n\nNext Block: {} sat/vB\n1 Hour: {} sat/vB\n3 Hours: {} sat/vB\n1 Day: {} sat/vB\n\n" \
                    "Mempool Data:\nMempool Transactions: {}\nMempool Fees: {} BTC".format(self.height, self.transactions,
                        round(format_reward(self.fees), 2), self.estimates[0], self.estimates[1], self.estimates[2], self.estimates[3], self.mempool_tx, round(format_reward(self.mempool_fees), 2))
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

#Returns the height of the last block
def get_height():
    response = requests.get('https://blockstream.info/api/blocks/tip/height')
    height = response.json()
    return height



#TODO: This function well check if there is a new block every 5 minutes.
#       * If no new block is found we return and wait
#       * If new block is found we check if we didn't miss any previous blocks. This
#       check is necessary since blocks are not always found in 10 minutes so we could potentially
#       skip a block.
#       if checks are valid we send out the tweet
def check_block():
    pass

#TODO: A function that calls .../api/block-height/{block number}
# This will receive the hash of a specific block.

#using this function to begin the program and finding the latest hash at tip
def get_tip_hash():
    response = requests.get('https://blockstream.info/api/blocks/tip/hash')
    tip_hash = response.text
    return tip_hash

#TODO: Changing this function to receive a parameter that includes the hash of the block we want to look up
#Returns information about a block.
def block_info():
    block = get_tip_hash()
    response = requests.get('https://blockstream.info/api/block/' + block)
    info = response.json()
    return info


def coinbase_txid():
    tip_hash = get_tip_hash()
    response = requests.get('https://blockstream.info/api/block/' + tip_hash + '/txid/0')
    txid = response.text
    return txid

#Calculates and returns the total fees in a specific block
#Look up the coinbase txid
#Using the txid look up the tx info
#Calculate fee per block (vout - 6.25)


def fees_per_block(txid):
    response = requests.get('https://blockstream.info/api/tx/' + txid)
    tx_info = response.json()
    total_reward = tx_info['vout'][0]['value']
    return total_reward - BLOCK_REWARD


def fee_estimates():
    fees = []
    url = requests.get('https://blockstream.info/api/fee-estimates')
    response = url.json()
    # Next Block confirmation
    fees.append(response['1'])
    # ~1 Hour Confirmation
    fees.append(response['6'])
    # ~3 Hour Confirmation
    fees.append(response['18'])
    # ~1 Day Confirmation
    fees.append(response['144'])
    format_fees = [round(x, 1) for x in fees]
    return format_fees


#TODO: Add test case if fees in mempool are 10 btc or more
def format_reward(fees):

    fees = str(fees)

    if len(fees) == 9:
        first_str = fees[0:1]
        second_str = fees[1:]
        final_str = first_str + '.' + second_str
        return float(final_str)
    elif len(fees) == 8:
        final_str = '.' + fees[0:]
        return float(final_str)
    else:
        final_str = '.0' + fees[0:]
        return float(final_str)


def get_mempool():
    url = requests.get('https://blockstream.info/api/mempool')
    mempool = url.json()
    return mempool


def main():

    #TODO: Blockstream provides a call that gives the hash of a specefic block 
    #      Knowing the initial block number, I know what the next blocks should be
    #      Keep blocks future blocks in a list and see if the program is on the right 
    #       order. If not find what block was skipped and continue.

    block = [0]
    while True:
        txid = coinbase_txid()
        tweet = Tweet(block_info(), authenticate(), fees_per_block(txid), fee_estimates(), get_mempool())
        #block.append(tweet.height)
        prev_hash = tweet.previous_blockhash
        block[0] = tweet.height
        print(block)
        print(prev_hash)
        tweet.compose_tweet()
        tweet.send_tweet()

        while True:
            print("sleeping zzzzzzzzzzzzz.")
            time.sleep(300)
            tip = get_height()
            print("Sending api request.")

            if block[0] < tip:
                break

        else:
            break









main()

