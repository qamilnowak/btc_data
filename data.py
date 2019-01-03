from coinmarketcap import Market
from datetime import datetime
from decimal import Decimal
from blockchain import statistics
import pandas as pd
import requests
coinmarketcap = Market()
cnmc_stats = coinmarketcap.stats(convert='USD')
cnmc_ticker = coinmarketcap.ticker(start=0, limit=1, convert='USD')
# CoinMarketCap DATA
last_updated = datetime.fromtimestamp(int(cnmc_ticker['data']['1']['last_updated'])).strftime('%Y-%m-%d %H:%M:%S')
btc_price_cmc = cnmc_ticker['data']['1']['quotes']['USD']['price']
btc_volume_24h_cmc = cnmc_ticker['data']['1']['quotes']['USD']['volume_24h']
btc_market_cap = cnmc_ticker['data']['1']['quotes']['USD']['market_cap']
btc_percent_change_1h = cnmc_ticker['data']['1']['quotes']['USD']['percent_change_1h']
btc_percent_change_24h = cnmc_ticker['data']['1']['quotes']['USD']['percent_change_24h']
btc_percent_change_7d = cnmc_ticker['data']['1']['quotes']['USD']['percent_change_7d']
supply_percentage = Decimal(cnmc_ticker['data']['1']['total_supply'] / cnmc_ticker['data']['1']['max_supply'])
btc_dominance = cnmc_stats['data']['bitcoin_percentage_of_market_cap']
total_market_cap = cnmc_stats['data']['quotes']['USD']['total_market_cap']

# Crypto Whale MARKET INFRO - Twitter
# Blockchain Data
stats = statistics.get()
btc_trade_volume = stats.trade_volume_btc
btc_volume_24h_blockchain = stats.trade_volume_usd
btc_hash_rate = stats.hash_rate


def api_response_decoded(url):
	"""Function to obtain data from api"""
	return requests.get(url).content.decode("utf-8")


# Blockchain Data from API
transaction_count_24h = api_response_decoded('https://blockchain.info/q/24hrtransactioncount')
btc_difficulty = api_response_decoded('https://blockchain.info/q/getdifficulty')
# To Do convert to more practical value than satoshi
btc_sent_24h = api_response_decoded('https://blockchain.info/q/24hrbtcsent')

# https://api.blockchain.info/charts/estimated-transaction-volume?format=json
# https://api.blockchain.info/charts/transaction-fees?format=json
# https://www.blockchain.com/pl/charts/estimated-transaction-volume

parameter_list = [
	btc_price_cmc, btc_percent_change_1h, btc_percent_change_24h,
	btc_percent_change_7d, btc_volume_24h_cmc, supply_percentage,
	btc_dominance, total_market_cap, btc_trade_volume,
	btc_volume_24h_blockchain, btc_hash_rate, transaction_count_24h,
	btc_difficulty, btc_sent_24h
]
columns_list = [
	'btc_price', '%1h', '%24h',
	'%7d', 'volume_24h', 'supply_percentage',
	'btc_dominance', 'total_market_cap', 'btc_trade_volume',
	'btc_volume_24h_blockchain', 'btc_hash_rate',
	'transaction_count_24h', 'btc_difficulty', 'btc_sent_24h'
]
new_row = {last_updated: parameter_list}
df = pd.DataFrame.from_dict(new_row, orient='index', columns=columns_list).rename_axis('date', axis='columns')
print(df)
df.to_csv(path_or_buf='save.csv', sep=';', index_label='date')
