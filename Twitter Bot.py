import time
import tweepy
import requests
from fuzzywuzzy import fuzz
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

api_key = ""
api_secret = ""
bearer_token = r""
access_token = ""
access_token_secret = ""

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

last_replied_id = None

def get_mentioned_tweets():
    global last_replied_id
    my_headers = {'Authorization' : 'Bearer AAAAAAAAAAAAAAAAAAAAABySnwEAAAAAzFQ%2Bh04AKHpS%2F7YcJzRBQqNqVBk%3DBFJ3lXqY13TvmVPXwWKTc8YGkISNfK4tjcAz7SiS3uHzwgLKKo'}
    url = 'https://api.twitter.com/2/users/1664004857374601216/mentions'
    if last_replied_id:
        url += f'?since_id={last_replied_id}'
    response = requests.get(url, headers=my_headers)
    if response.status_code == 200:
        responseObj = response.json()
        if 'data' in responseObj:
            tweets = responseObj['data']
            new_tweets = []
            for tweet in tweets:
                if tweet['id'] != last_replied_id:
                    new_tweets.append(tweet)
            if tweets:
                last_replied_id = tweets[0]['id']
            return new_tweets
        else:
            print("Error: No data key in response.")
    else:
        print(f"Error: Status code {response.status_code} returned from API.")

if __name__ == "__main__":
    while True:
        new_mentions = get_mentioned_tweets()
        if new_mentions:
            print("New mentioned tweets:")
            for tweet in new_mentions:
                if '@chartthisbart' in tweet['text']:
                    content = tweet['text'].split('@chartthisbart', 1)[1].strip()
                    tweet_id = tweet['id']
                    print("Tweet ID:", tweet_id)
                    print("Content:", content)

                    available_coins = cg.get_coins_list()

                    best_match = None
                    best_match_ratio = 0

                    for coin in available_coins:
                        coin_name = coin['id']
                        match_ratio = fuzz.ratio(content.lower(), coin_name.lower())
                        if match_ratio > best_match_ratio:
                            best_match = coin
                            best_match_ratio = match_ratio

                    if best_match:
                        coin_data = cg.get_coin_by_id(id=best_match['id'])
                        market_data = coin_data['market_data']
                        name = coin_data['name']
                        symbol = coin_data['symbol']
                        current_price = market_data['current_price']
                        market_cap = market_data['market_cap']
                        total_volume = market_data['total_volume']

                        print(f"Closest Match: {name} (ID: {best_match['id']})")
                        print(f"Symbol: {symbol}")
                        print(f"Current Price: {current_price['usd']} USD")
                        print(f"Market Cap: {market_cap['usd']} USD")
                        print(f"Total Volume: {total_volume['usd']} USD")

                    else:
                        print("No matching coin found.")

        else:
            print("No new mentioned tweets found.")
        time.sleep(30)
