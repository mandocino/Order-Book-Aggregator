import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import defaultdict


class Data:
    def __init__(self, price, quantity, name):
        self.price = float(price)
        self.quantity = float(quantity)
        self.name = name


class myOrderBook:
    def __init__(self):
        self.bids = defaultdict(float)
        self.asks = defaultdict(float)

    def add_bid(self, price, quantity, name):
        self.bids[(price, name)] += quantity

    def add_ask(self, price, quantity, name):
        self.asks[(price, name)] += quantity

    def display_order_book_stacked(self):
        bids_data = {
            'Price': [price for price, name in self.bids.keys()],
            'Quantity': [quantity for quantity in self.bids.values()],
            'Name': [name for _, name in self.bids.keys()]
        }

        asks_data = {
            'Price': [price for price, name in self.asks.keys()],
            'Quantity': [quantity for quantity in self.asks.values()],
            'Name': [name for _, name in self.asks.keys()]
        }

        bids_df = pd.DataFrame(data=bids_data)
        asks_df = pd.DataFrame(data=asks_data)

        bids_df = bids_df.groupby(['Price', 'Name'])[
            'Quantity'].sum().reset_index()
        asks_df = asks_df.groupby(['Price', 'Name'])[
            'Quantity'].sum().reset_index()

        df = pd.concat([bids_df, asks_df], ignore_index=True)
        df = df.groupby(['Price', 'Name'])['Quantity'].sum().reset_index()

        sns.set(style="whitegrid")

        name_palette = {"Alice": "tab:blue", "Bob": "tab:orange",
                        "Charlie": "tab:green", "David": "tab:red"}

        plt.figure(figsize=(10, 6))

        sns.barplot(x='Price', y='Quantity', hue='Name', data=df, ci=None,
                    palette=name_palette, hue_order=['Alice', 'Bob', 'Charlie', 'David'])

        plt.xlabel('Price (USD)')
        plt.ylabel('Quantity (BTC)')
        plt.title('Order Book')
        plt.legend(title='Name', loc='upper right')

        plt.xticks(rotation=45)

        plt.show()

order_book = myOrderBook()
order_book.add_bid(10000, 0.5, 'Alice')
order_book.add_bid(10000, 0.5, 'Bob')

order_book.add_bid(9900, 0.8, 'Alice')
order_book.add_bid(10000, 1.2, 'Bob')
order_book.add_ask(10100, 0.3, 'Charlie')
order_book.add_ask(10300, 0.9, 'David')

order_book.display_order_book_stacked()
