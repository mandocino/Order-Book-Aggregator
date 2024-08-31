import matplotlib.pyplot as plt
import pandas as pd
import Data as Data
from collections import defaultdict
from DataPacket import dataPacket
import plotly.graph_objects as go

class myOrderBook:
    def __init__(self):
        self.bids = defaultdict(list)
        self.asks = defaultdict(list)

    def add_bid(self, price, quantity, name):
        self.bids[price].append(dataPacket(quantity, name))

    def add_ask(self, price, quantity, name):
        self.asks[price].append(dataPacket(quantity, name))

    def display_order_book(self):
        max_bids = max(self.bids.values(), default=0)
        max_asks = max(self.asks.values(), default=0)

        print("Order Book:")
        print("Bids:")
        for price in sorted(self.bids.keys(), reverse=True):
            quantity = self.bids[price]
            bar_length = int(50 * quantity / max_bids)
            print(f"{price:10.2f} | {'█' * bar_length} ({quantity:.3f})")

        print("\nAsks:")
        for price in sorted(self.asks.keys()):
            quantity = self.asks[price]
            bar_length = int(50 * quantity / max_asks)
            print(f"{price:10.2f} | {'█' * bar_length} ({quantity:.3f})")

    def display_order_book_stacked_matlib(self):

        bids_list = []
        for price, packets in self.bids.items():
            for packet in packets:
                bids_list.append((price, packet.quantity, packet.name))

        bids_df = pd.DataFrame(bids_list, columns=[
            'price', 'quantity', 'name'])
        bids_df['type'] = 'bid'

        asks_list = []
        for price, packets in self.asks.items():
            for packet in packets:
                asks_list.append((price, packet.quantity, packet.name))

        asks_df = pd.DataFrame(asks_list, columns=[
            'price', 'quantity', 'name'])
        asks_df['type'] = 'ask'

        df = pd.concat([bids_df, asks_df], ignore_index=True)
        df = df.dropna()
        plt.figure(figsize=(10, 6))

        colors = {
            'bid': 'blue',
            'ask': 'red',
        }

        df['color'] = df['type'].map(colors)

        legend_exchanges = set()

        for idx, row in df.iterrows():
            # Check if the exchange is already in the legend
            if row['name'] not in legend_exchanges:
                # Add the exchange to the legend_exchanges set
                legend_exchanges.add(row['name'])
            # Plot the data with the appropriate color and label
                plt.barh(row['price'], row['quantity'],
                         color=row['color'], label=row['name'])
            else:
                # For exchanges that are already in the legend, just plot the data without the label
                plt.barh(row['price'], row['quantity'], color=row['color'])

        # Add labels and title
        plt.xlabel('Quantity')
        plt.ylabel('Price')

        # Add a legend
        plt.legend(title='Exchange', loc='upper right')

        # Show the plot

    def display_order_book_stacked(self):
        bids_list = []
        for price, packets in self.bids.items():
            for packet in packets:
                bids_list.append((price, packet.quantity, packet.name))

        bids_df = pd.DataFrame(bids_list, columns=[
                               'price', 'quantity', 'name'])
        bids_df['type'] = 'bid'

        asks_list = []
        for price, packets in self.asks.items():
            for packet in packets:
                asks_list.append((price, packet.quantity, packet.name))

        asks_df = pd.DataFrame(asks_list, columns=[
                               'price', 'quantity', 'name'])
        asks_df['type'] = 'ask'

        df = pd.concat([bids_df, asks_df], ignore_index=True)
        df = df.dropna()

        colorsOrders = {
            'bid': 'blue',
            'ask': 'red',
        }

        colorsExchanges = {
            'kraken': 'blue',
            'binance': 'gold',
            'kucoin': 'green',
            'duplicateExchange': 'silver',
        }

    # Map the colors to the 'type' column in the DataFrame
        df['color'] = df['type'].map(colorsOrders)
        df['color'] = df['name'].map(colorsExchanges)

    # Create a hover text for the bars, showing the exchange name and quantity
        hover_text = df.apply(
            lambda row: f"{row['name']} | Quantity: {row['quantity']}", axis=1)

    # Plot the interactive bar chart using plotly
        fig = go.Figure()

        max_price = df['price'].max()
        min_price = df['price'].min()
        max_price = max_price + 10
        min_price = min_price - 10

        fig.update_yaxes(range=[min_price, max_price])
        # print("asks")
        # for exchange in df.loc[df['type'] == 'ask', 'name']:
        #    print(exchange + " : " + colorsExchanges[exchange])

    # Add bid bars
        fig.add_trace(go.Bar(
            y=df.loc[df['type'] == 'bid', 'price'],
            x=df.loc[df['type'] == 'bid', 'quantity'],
            text=hover_text[df['type'] == 'bid'],
            width=0.5,
            orientation='h',
            marker=dict(
                color='blue',
                line=dict(
                    color=[colorsExchanges[exchange]
                           for exchange in df.loc[df['type'] == 'ask', 'name']],
                    width=2)),
            name='Bid'
        ))

    # Add ask bars
        fig.add_trace(go.Bar(
            y=df.loc[df['type'] == 'ask', 'price'],
            x=df.loc[df['type'] == 'ask', 'quantity'],
            text=hover_text[df['type'] == 'ask'],
            width=0.5,
            orientation='h',
            marker=dict(
                color='red',
                line=dict(
                    color=[colorsExchanges[exchange]
                           for exchange in df.loc[df['type'] == 'ask', 'name']],
                    width=2)),
            name='Ask'
        ))

    # Customize the layout and add labels
        fig.update_layout(
            xaxis_title='Quantity',
            yaxis_title='Price',
            legend_title='Exchange',
            yaxis_tickformat='.2f',
            hovermode='closest',  # Show closest data point when hovering
            title='Order Book Stacked',
            template='plotly_white',
            bargap=0.1,  # Adjust the gap between individual bars within a group
            bargroupgap=0.1,  # Adjust the gap between different groups of bars
            paper_bgcolor='white'
        )
        plot_json = fig.to_json()
        return plot_json

    def aggregate_order_books(self, order_books_list):
        all_bids = []
        all_asks = []

        for n in range(len(order_books_list)):
            for bid in order_books_list[n][1]['bids']:
                if len(bid) == 3:
                    price, quantity, _ = bid
                    # bidData = Data()
                    all_bids.append((price, quantity, order_books_list[n][0]))
                else:
                    price, quantity = bid
                    all_bids.append((price, quantity, order_books_list[n][0]))

            for ask in order_books_list[n][1]['asks']:
                if len(ask) == 3:
                    price, quantity, _ = ask
                    all_asks.append((price, quantity, order_books_list[n][0]))
                else:
                    price, quantity = ask
                    all_asks.append((price, quantity, order_books_list[n][0]))

        all_bids.sort(key=lambda x: x[0])
        all_asks.sort(key=lambda x: x[0])

        for bid in all_bids[:250]:
            self.add_bid(bid[0], bid[1], bid[2])

        for ask in all_asks[:250]:
            self.add_ask(ask[0], ask[1], ask[2])

        return self
