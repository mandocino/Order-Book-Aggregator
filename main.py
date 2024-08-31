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
    order_books_list = []

    try:
        print("Starting the Arbitrage Bot.")
        while True:
            try:
                for symbol in symbols:
                    for exchange in exchanges_list:
                        print(symbol + " | " + exchange.get_name() + " | " +  # get prices
                              str(get_price(exchange.get_accessHandler(), symbol)))

                for i in range(len(exchanges_list)):
                    if (len(exchanges_list) > 1):
                        for k in range(i + 1, len(exchanges_list)):
                            priceDifference = get_price(exchanges_list[k].get_accessHandler(
                            ), symbol) - get_price(exchanges_list[i].get_accessHandler(), symbol)
                            if (priceDifference < 0):
                                print("Can make " + str("{:.2f}".format(abs(priceDifference))) + "$" + " from buying on " +
                                      exchanges_list[k].get_name() + " and selling to " + exchanges_list[i].get_name())  # find differences
                            elif (priceDifference > 0):
                                print("Can make " + str("{:.2f}".format(priceDifference)) + "$" + " from buying on " +
                                      exchanges_list[i].get_name() + " and selling to " + exchanges_list[k].get_name())
                    else:
                        print("Error! Only 1 exchange inputted.")

                for i in range(len(exchanges_list)):
                    order_books_list.append((exchanges_list[i].get_name(), get_orderbook(  # get order books
                        exchanges_list[i].get_accessHandler(), symbol)))

                theOrderBook = myOrderBook()
                theOrderBook.aggregate_order_books(order_books_list)
                theOrderBook.display_order_book_stacked()
                order_books_list = []

            except Exception as e:
                print(f"An error occurred: {str(e)}")
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nInterrupt received. Closing the bot.")


if __name__ == '__main__':
    main()
