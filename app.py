from flask import Flask, render_template, request, redirect, url_for, session
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
import os
import ccxt
import time
from Exchange import myExchange
from OrderBook import myOrderBook


def read_file_and_create_objects(file_path):
    exchanges = []
    with open(file_path, 'r') as file:
        for line in file:
            name, key, privateKey = line.strip().split('|')
            if (name.lower() == "kraken"):
                accessHandler = ccxt.kraken(
                    {'apiKey': key, 'secret': privateKey})
            elif (name.lower() == "binance"):
                accessHandler = ccxt.binance(
                    {'apiKey': key, 'secret': privateKey})
            elif (name.lower() == "kucoin"):
                accessHandler = ccxt.kucoin(
                    {'apiKey': key, 'secret': privateKey})
            elif (name.lower() == "coinbase"):
                accessHandler = ccxt.coinbase(
                    {'apiKey': key, 'secret': privateKey})
            exchange = myExchange(name, key, privateKey, accessHandler)
            exchanges.append(exchange)
    return exchanges


def get_price(exchange, symbol):
    ticker = exchange.fetch_ticker(symbol)
    return ticker['last']


def get_orderbook(exchange, symbol):
    ticker = exchange.fetch_order_book(symbol)
    return ticker


def main():
    symbols = ['BTC/USDT']
    file_path = 'exchanges.txt'
    exchanges_list = read_file_and_create_objects(file_path)  # get exchanges

    try:
        print("Connecting to Exchanges and Getting Prices")
        try:
            order_books_list = []
            for symbol in symbols:
                for exchange in exchanges_list:
                    print(symbol + " | " + exchange.get_name() + " | " +
                          str(get_price(exchange.get_accessHandler(), symbol)))
            for i in range(len(exchanges_list)):
                order_books_list.append((exchanges_list[i].get_name(), get_orderbook(
                    exchanges_list[i].get_accessHandler(), symbol)))
            theOrderBook = myOrderBook()
            theOrderBook.aggregate_order_books(order_books_list)
            response = theOrderBook.display_order_book_stacked()
            return response
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nInterrupt received. Closing the bot.")


app = Flask(__name__)
#app.secret_key = os.urandom(24)
#connectionString = 'mongodb+srv://mendohman:Z56Yqb9WdU9mSzUx@cluster0.ozb0hll.mongodb.net/?retryWrites=true&w=majority'
#client = MongoClient(connectionString, server_api=ServerApi('1'))
#try:
    #client.admin.command('ping')
   # print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
 #   print(e)
#
symbols = ['BTC/USDT']
file_path = 'exchanges.txt'
order_books_list = []
theOrderBook = myOrderBook()
exchanges_list = read_file_and_create_objects(file_path)
print("Connecting to Exchanges and Getting Prices")
try:
    for symbol in symbols:
        for exchange in exchanges_list:
            print(symbol + " | " + exchange.get_name() + " | " +  # get prices
                  str(get_price(exchange.get_accessHandler(), symbol)))
    for i in range(len(exchanges_list)):
        order_books_list.append((exchanges_list[i].get_name(), get_orderbook(  # get order books
            exchanges_list[i].get_accessHandler(), symbol)))

except Exception as e:
    print(f"An error occurred: {str(e)}")
    time.sleep(5)

#db = client.test
#collection = db.testcol
#logged_in = False


@app.route('/')
def displayHome():
    return render_template('homepage.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/search/<query>')
def search(query):
    theOrderBook.aggregate_order_books(order_books_list)
    plot_json = theOrderBook.display_order_book_stacked()
    return render_template('index.html', plot_json=plot_json, query=query)


if __name__ == '__main__':
    app.run(debug=True)
