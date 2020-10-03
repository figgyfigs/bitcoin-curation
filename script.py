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
        #self.previous_blockhash = info['previousblockhash']

    def compose_tweet(self):
        tweet = "Block: {}\n# of transactions: {}\nFees paid: {} BTC\n\nNext Block: {} sat/vB\n1 Hour: {} sat/vB\n3 Hours: {} sat/vB\n1 Day: {} sat/vB\n\n" \
                    "Mempool Data:\nMempool Transactions: {}\nMempool Fees: {} BTC\n#Bitcoin".format(self.height, self.transactions,
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


def get_block_hash(block):
    response = requests.get('https://blockstream.info/api/block-height/' + str(block))
    block_hash = response.text
    print(block_hash)
    return block_hash


#using this function to begin the program. Getting the initial block.
def get_tip_hash():
    response = requests.get('https://blockstream.info/api/blocks/tip/hash')
    tip_hash = response.text
    return tip_hash


def block_info(hash):
    #block_hash = get_block_hash(block)
    #block = get_tip_hash()
    response = requests.get('https://blockstream.info/api/block/' + hash)
    info = response.json()
    #print(info)
    return info


def coinbase_txid(hash):
    #tip_hash = get_tip_hash()
    response = requests.get('https://blockstream.info/api/block/' + hash + '/txid/0')
    txid = response.text
    return txid

#Calculates and returns the total fees in a specific block
#Look up the coinbase txid
#Using the txid look up the tx info
#Calculate fee per block (vout - 625000000)
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



def format_reward(fees):

    fees = str(fees)
    #Check if fees are greater than or equal to 10btc
    if len(fees) == 10:
        first_str = fees[0:2]
        second_str = fees[2:]
        final_str = first_str + '.' + second_str
        return float(final_str)
    elif len(fees) == 9:
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


#This function returns the height once the program runs for the first time. This will help to keep track of what needs to come next.
def start(hash):

    #hash = get_block_hash(x)
    txid = coinbase_txid(hash)
    tweet = Tweet(block_info(hash), authenticate(), fees_per_block(txid), fee_estimates(), get_mempool())
    tweet.compose_tweet()
    tweet.send_tweet()
    return tweet.height



def main():

    initial_block = get_tip_hash()
    #print(initial_block)
    block = start(initial_block)
    block += 1

    while True:
        print("Sleeping for 5 mins.")
        time.sleep(300)

        check_hash = get_block_hash(block)
        if check_hash is not 'Block not found':
            txid = coinbase_txid(check_hash)
            tweet = Tweet(block_info(check_hash), authenticate(), fees_per_block(txid), fee_estimates(), get_mempool())
            tweet.compose_tweet()
            tweet.send_tweet()
            block += 1
            print("block is " + str(block))
        else:
            break



main()

