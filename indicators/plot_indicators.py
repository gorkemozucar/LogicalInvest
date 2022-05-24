import plotly.graph_objects as go
from plotly.subplots import make_subplots
# from .strategies import *
from .strategies import *
# import indicators.strategies as strategy
from binance.client import Client

from ta.trend import MACD, SMAIndicator, CCIIndicator, ADXIndicator, AroonIndicator, KSTIndicator
from ta.momentum import RSIIndicator, WilliamsRIndicator, StochasticOscillator, TSIIndicator, AwesomeOscillatorIndicator
from ta.volatility import BollingerBands, KeltnerChannel

import pandas_ta
# import indicators.config
from matplotlib.animation import FuncAnimation
from plotly.offline import plot
# from indicators.real_time_data import df
import pandas as pd
from datetime import datetime, timedelta, tzinfo

API_KEY = 'yourbinanceapikey'
API_SECRET = 'yourbinanceapisecret'

# API_KEY = 'jgd9xxpVqENptW4Ggk2y4IlKqkfU3FD7wSLFWjXlcix2thxRnLsJhAo38AwTdYJv'
# API_SECRET = 'LKLHyXmU81wsIt42tWrxpL39bJd86GcJcT25McExZxwIG7kbZFjUOXApdIQHgcJy'

def gather_data(interval, start_n_hours_ago):
    client = Client(API_KEY, API_SECRET)
    # client = Client(indicators.config.API_KEY, indicators.config.API_SECRET, tld='us')

    # symbol = 'BTC-USD'
    # df = yf.Ticker(symbol).history(start='2022-03-14', interval="5m")
    # df = yf.Ticker(symbol).history(start='2022-03-25', interval="5m").tz_convert(tz='Turkey')

    # interval = requests.get("interval")
    # get_interval = request.GET['interval']

    # if "interval" in request.GET:
    #     interval = request.GET["interval"]
    # else:

    candlesticks = client.get_historical_klines(symbol="BTCUSDT", interval=interval, start_str=str(datetime.now()-timedelta(hours=start_n_hours_ago)))
    # candlesticks = client.get_historical_klines(symbol="BTCUSDT", interval=interval, start_str='4 May, 2022')
    # candlesticks = client.get_historical_klines("BTCUSDT", interval, "30 Mar, 2022", limit=500)
    # candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, "9 Mar, 2022", "12 Mar, 2022")
    # print(pd.DataFrame(candlesticks))

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            # "time": data[0] / 1000,  # open time
            "time": datetime.utcfromtimestamp(data[0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # open time
            # "time": datetime.fromtimestamp(data[0] / 1000, tz=tzinfo.tzname("Turkey")).strftime('%Y-%m-%d %H:%M:%S'),  # open time
            # "time": datetime.fromtimestamp(data[0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # open time
            "open": int(float(data[1])),
            "high": int(float(data[2])),
            "low": int(float(data[3])),
            "close": int(float(data[4])),
            "volume": int(float(data[5])),
            "close time": data[6] / 1000,
            "quote asset volume": data[7],
            "number of trades": data[8],
            "taker buy base asset volume": data[9],
            "taker buy quote asset volume": data[10],
            "ignore": data[11],
        }

        # open_time = [int(entry[0]) for entry in candlesticks]
        # open = [float(entry[1]) for entry in candlesticks]
        # high = [float(entry[2]) for entry in candlesticks]
        # low = [float(entry[3]) for entry in candlesticks]
        # close = [float(entry[4]) for entry in candlesticks]
        #
        processed_candlesticks.append(candlestick)

    df = pd.DataFrame(processed_candlesticks)

    # df.set_index('time', inplace=True)
    # df.index = pd.to_datetime(df.index, unit='ms', format='%Y-%m-%d %H:%M:%S')
    return df





def plot_candlestick(df):
    # CANDLESTICK
    # make a grid to display 2 graph
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.22)  # you can add ", row_heights=[0.5,0.1]" and "row_width=[0.25, 0.75]"
    # add chart title
    fig.update_layout(title="BTCUSDT")
    # add candlestick chart for price data to 1st row
    fig.add_trace(go.Candlestick(x=df["time"],
                                 open=df['open'],
                                 high=df['high'],
                                 low=df['low'],
                                 close=df['close'],
                                 name='OHLC',
                                 # increasing_line_color='orange',
                                 # decreasing_line_color='black',
                                 # showlegend=False  #hiding legends(legend is the colors and traces written in the top right)
                                 ), row=1, col=1)
    # removing rangeslider
    # fig.update_layout(xaxis_rangeslider_visible=False)

    # hide weekends
    # fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])

    # # removing all empty dates
    # # build complete timeline from start date to end date
    # dt_all = pd.date_range(start=df.index[0], end=df.index[-1])
    # # retrieve the dates that ARE in the original dataset
    # dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]
    # # define dates with missing values
    # dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
    # hide dates with no values
    # fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

    # do these all in one update method
    # update layout by changing the plot size, hiding legends(legend is the colors and traces written in the top right)
    # & rangeslider, and removing gaps between dates
    # fig.update_layout(height=900, width=1200,
    #                   showlegend=False,
    #                   xaxis_rangeslider_visible=False,
    #                   xaxis_rangebreaks=[dict(values=dt_breaks)])

    # colors = ['green' if row['Open'] - row['Close'] >= 0
    #           else 'red' for index, row in df.iterrows()]
    # plot volume trace on 2nd row
    fig.add_trace(go.Bar(x=df["time"],
                         y=df['volume'],
                         # marker_color=colors,
                         name='Volume',
                         ), row=2, col=1)
    # update layout by changing the width and height of the complete chart, also make the theme dark
    fig.update_layout(height=600, width=1100,
                      # template="plotly_dark",
                      )
    # fig.update_xaxes(showgrid=False)
    fig.update_yaxes(title_text="Price", row=1, col=1)  # showgrid=False,
    fig.update_yaxes(title_text="Volume", row=2, col=1)  # showgrid=False,
    # fig.update_layout(xaxis=go.layout.XAxis(tickangle=90))
    # fig.update_xaxes(tickangle=90)
    # fig.update_xaxes(showgrid=False, row=1, col=1)
    # fig.update_traces()
    # # removing white space
    # fig.update_layout(margin=go.layout.Margin(
    #     l=20,  # left margin
    #     r=20,  # right margin
    #     b=20,  # bottom margin
    #     t=20  # top margin
    # ))

    # ## Customize font, colors, hide range slider
    # layout = go.Layout(
    #     plot_bgcolor='#efefef',
    #     # Font Families
    #     font_family='Monospace',
    #     font_color='#000000',
    #     font_size=20,
    #     xaxis=dict(
    #         rangeslider=dict(
    #             visible=False
    #         )
    #     )
    # )
    # fig.update_layout(layout)
    return fig.to_html()


def plot_bbands(df):
    # BBANDS
    bbands = BollingerBands(close=df['close'],
                            window=20,
                            window_dev=2)

    # Calculate buy sell signals
    df['bollinger_hbands'] = bbands.bollinger_hband()
    df['bollinger_mavg'] = bbands.bollinger_mavg()
    df['bollinger_lbands'] = bbands.bollinger_lband()
    buy_price, buy_signal, sell_price, sell_signal, bb_signal, buy_price_x, sell_price_x = implement_bb_strategy(
        df['close'], df['bollinger_lbands'], df['bollinger_hbands'])

    print('buy', buy_signal, 'sell', sell_signal)
    print('Buy', buy_price)
    print('Sell', sell_price)

    # Plot BBANDS trace
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Candlestick(x=df['time'],
                                 open=df['open'],
                                 high=df['high'],
                                 low=df['low'],
                                 close=df['close'],
                                 name='OHLC',
                                 # increasing_line_color='orange',
                                 # decreasing_line_color='black',
                                 # showlegend=False  #hiding legends(legend is the colors and traces written in the top right)
                                 # opacity=0.8
                                 ), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['bollinger_hbands'],
                             line=dict(color='blue', width=1),
                             name='Bollinger High Band',
                             # hoverlabel=dict(color='red')
                             ))
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['bollinger_mavg'],
                             line=dict(color='#9494b8', width=1),
                             name='Bollinger Moving Average',
                             ))
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['bollinger_lbands'],
                             line=dict(color='blue', width=1),
                             name='Bollinger Low Band',
                             ))

    # hide dates with no values
    # fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

    # place buy and sell orders on the indicator
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][buy_price_x],
                             y=buy_price,
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green',
                             # hoverinfo=['text + x + y'],
                             # hovertext='Buy',
                             hovertemplate="Buy Signal<br>%{x}, %{y}<extra></extra>",
                             name='Buy Signal',
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][sell_price_x],
                             y=sell_price,
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red',
                             name='Sell Signal',
                             ))

    # fig.update_xaxes(rangeselector = dict(
    #     buttons = list([
    #         dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
    #         dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
    #         dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
    #         dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
    #         dict(step = 'all')])))
    # layout = go.Layout(paper_bgcolor='rgba(255,255,2555,0.5)', plot_bgcolor='rgba(250,250,250,0.8)', autosize=True)
    # fig.update_xaxes(showgrid=False)
    fig.update_yaxes(title_text="BBANDS", row=1, col=1)  # color='pink' # showgrid=False,
    fig.update_layout(height=600, width=1100, title='BBANDS',
                      # template="plotly_dark",
                      # legend=dict(orientation="h",
                      #             yanchor="top",
                      #             y=0.99,
                      #             xanchor="left",
                      #             x=0.01,
                      #             bgcolor="LightSteelBlue",
                      #             bordercolor="Black",
                      #             borderwidth=2
                      #             )
                      )

    # # Add upper/lower bounds
    # fig.update_yaxes(range=[-10, 110])
    # fig.add_hline(y=0, col=1, row=1, line_color="#9494b8", line_width=2)
    # fig.add_hline(y=100, col=1, row=1, line_color="#9494b8", line_width=2)

    # removing rangeslider
    # fig.update_layout(xaxis_rangeslider_visible=False)

    # fig.update_layout(xaxis=go.layout.XAxis(tickangle=90))
    # fig.update_xaxes(tickangle=90)
    # fig.update_xaxes(showgrid=False, row=1, col=1)
    # fig.update_traces()
    # # removing white space
    # fig.update_layout(margin=go.layout.Margin(
    #     l=20,  # left margin
    #     r=20,  # right margin
    #     b=20,  # bottom margin
    #     t=20  # top margin
    # ))

    # ## Customize font, colors, hide range slider
    # layout = go.Layout(
    #     plot_bgcolor='#efefef',
    #     # Font Families
    #     font_family='Monospace',
    #     font_color='#000000',
    #     font_size=20,
    #     xaxis=dict(
    #         rangeslider=dict(
    #             visible=False
    #         )
    #     )
    # )
    # fig.update_layout(layout)


    accuracy = calculate_accuracy(buy_price_x, buy_price, sell_price_x, sell_price)

    signal = get_signal(df, buy_price_x, sell_price_x)

    return fig.to_html(), accuracy, signal, df['bollinger_hbands'], df['bollinger_mavg'], df['bollinger_lbands'], buy_price, sell_price, buy_price_x, sell_price_x


def plot_rsi(df):
    # RSI
    rsi = RSIIndicator(close=df['close'],
                window=14)

    # Calculate buy sell signals
    df['rsi'] = rsi.rsi()
    buy_price, buy_signal, sell_price, sell_signal, rsi_signal, rsi_buy_x, rsi_buy_y, rsi_sell_x, rsi_sell_y = implement_rsi_strategy(df['close'], df['rsi'])
    print('buy', buy_signal, 'sell', sell_signal)
    # buy_signal = 0
    # sell_signal = 0
    # if df['rsi']<30:
    #     buy_signal += 1
    # print(df)

    # Plot RSI trace
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Scatter(x=df['time'],
                             y=rsi.rsi(),
                             line=dict(color='#ff9900', width=2)
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][rsi_buy_x],
                             y=rsi_buy_y,
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green'
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][rsi_sell_x],
                             y=rsi_sell_y,
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red'
                             ))

    # Add upper/lower bounds
    fig.update_yaxes(range=[-10, 110])
    fig.add_hline(y=0, col=1, row=1, line_color="#9494b8", line_width=2)
    fig.add_hline(y=100, col=1, row=1, line_color="#9494b8", line_width=2)

    # Add overbought/oversold
    fig.add_hline(y=30, col=1, row=1, line_color='#336699', line_width=2, line_dash='dash')
    fig.add_hline(y=70, col=1, row=1, line_color='#336699', line_width=2, line_dash='dash')


    fig.update_yaxes(title_text="RSI", row=1, col=1)
    fig.update_layout(xaxis_rangeslider_visible=True)
    fig.update_layout(height=600, width=1100)
    # ax1 = plt.subplot2grid((10, 1), (0, 0), rowspan=4, colspan=1)
    # ax1.plot(df.index, buy_price, marker='^', markersize=10, color='green', label='BUY SIGNAL')
    # ax1.plot(df.index, sell_price, marker='v', markersize=10, color='r', label='SELL SIGNAL')

    accuracy = calculate_accuracy(rsi_buy_x, buy_price, rsi_sell_x, sell_price)

    signal = get_signal(df, rsi_buy_x, rsi_sell_x)

    return fig.to_html(), accuracy, signal


def plot_supertrend(df):
    # Supertrend
    supertrend = pandas_ta.supertrend(high=df['high'],
                                      low=df['low'],
                                      close=df['close'],
                                      length=7,
                                      multiplier=3.0)
    # help(pandas_ta.supertrend())

    # sonucu denemek için
    # x = pandas_ta.bbands(close=df['Close'])
    # print(x['BBL_5_2.0'])
    # print(x['BBM_5_2.0'])
    # print(x['BBU_5_2.0'])

    # print(supertrend)

    # Calculate buy sell signals
    df['supertrend'] = supertrend['SUPERT_7_3.0']
    buy_price, buy_signal, sell_price, sell_signal, st_signal, buy_price_x, sell_price_x = implement_st_strategy(df['close'], df['supertrend'])
    print('buy', buy_signal, 'sell', sell_signal)

    # Plot Supertrend trace
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    # colors = ['green' if val >= 0
    #           else 'red' for val in macd.macd_diff()]
    fig.add_trace(go.Candlestick(x=df['time'],
                                 open=df['open'],
                                 high=df['high'],
                                 low=df['low'],
                                 close=df['close']), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['time'],
                             y=supertrend['SUPERT_7_3.0'],
                             line=dict(color='red', width=1),
                             # fill='tonextx', #['none', 'tozeroy', 'tozerox', 'tonexty', 'tonextx','toself', 'tonext']
                             # fillcolor='rgba(100, 255, 150, 0.35)',
                             ))
    fig.add_trace(go.Scatter(x=df['time'],
                             y=supertrend['SUPERTl_7_3.0'],
                             line=dict(color='green', width=1),
                             # fill='tonexty', #['none', 'tozeroy', 'tozerox', 'tonexty', 'tonextx','toself', 'tonext']
                             # fillcolor='rgba(255, 100, 150, 0.35)',
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][buy_price_x],
                             y=buy_price,
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green'
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][sell_price_x],
                             y=sell_price,
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red'
                             ))

    fig.update_yaxes(title_text="Supertrend", row=1, col=1)
    fig.update_yaxes(range=[min(df['low'])-500, max(df['high'])+500])
    fig.update_layout(height=600, width=1100)

    accuracy = calculate_accuracy(buy_price_x, buy_price, sell_price_x, sell_price)

    signal = get_signal(df, buy_price_x, sell_price_x)

    return fig.to_html(), accuracy, signal


def plot_macd(df):
    # MACD
    macd = MACD(close=df['close'],
                window_slow=26,
                window_fast=12,
                window_sign=9)

    # Calculate buy sell signals
    a = {'macd': macd.macd(), 'signal': macd.macd_signal(), 'diff': macd.macd_diff()}
    x = pd.DataFrame(a)
    # print(x)
    # x.tail()
    buy_price, buy_signal, sell_price, sell_signal, macd_signal, macd_buy_x, macd_buy_y, macd_sell_x, macd_sell_y = implement_macd_strategy(df['close'], x)
    print('buy', buy_signal, 'sell', sell_signal)

    # Plot MACD trace
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    colors = ['green' if val >= 0
              else 'red' for val in macd.macd_diff()]
    fig.add_trace(go.Bar(x=df['time'],
                         y=macd.macd_diff(),
                         marker_color=colors
                         ))
    fig.add_trace(go.Scatter(x=df['time'],
                             y=macd.macd(),
                             line=dict(color='black', width=2)
                             ))
    fig.add_trace(go.Scatter(x=df['time'],
                             y=macd.macd_signal(),
                             line=dict(color='blue', width=1)
                             ))
    # x = []
    # for price in buy_price:
    #     x.append(price.index)
    # y = []
    # for points in x:
    #     y.append(points.macd.macd())
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][macd_buy_x],
                             y=macd_buy_y,
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green'
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][macd_sell_x],
                             y=macd_sell_y,
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red'
                             ))


    fig.update_yaxes(title_text="MACD", row=1, col=1)
    fig.update_layout(height=600, width=1100)

    accuracy = calculate_accuracy(macd_buy_x, buy_price, macd_sell_x, sell_price)

    signal = get_signal(df, macd_buy_x, macd_sell_x)

    return fig.to_html(), accuracy, signal


def plot_williams_r_percentage(df):
    # Williams %R
    williams_r = WilliamsRIndicator(high=df['high'],
                                    low=df['low'],
                                    close=df['close'],
                                    lbp=14)

    # Calculate buy sell signals
    df['williams_r'] = williams_r.williams_r()
    buy_price, buy_signal, sell_price, sell_signal, williams_r_signal, williams_r_buy_x, williams_r_buy_y, williams_r_sell_x, williams_r_sell_y = implement_wr_strategy(df['close'], df['williams_r'])
    print('buy', buy_signal, 'sell', sell_signal)

    # Plot Williams %R trace
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Scatter(x=df['time'],
                             y=williams_r.williams_r(),
                             line=dict(color='black', width=2)
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][williams_r_buy_x],
                             y=williams_r_buy_y,
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green'
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][williams_r_sell_x],
                             y=williams_r_sell_y,
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red'
                             ))

    # Add upper/lower bounds
    # fig.update_yaxes(range=[-110, 10])
    fig.add_hline(y=0, col=1, row=1, line_color="#9494b8", line_width=2)
    fig.add_hline(y=-100, col=1, row=1, line_color="#9494b8", line_width=2)

    # Add overbought/oversold
    fig.add_hline(y=-20, col=1, row=1, line_color='#336699', line_width=2, line_dash='dash')
    fig.add_hline(y=-50, col=1, row=1, line_color='#336699', line_width=2, line_dash='dot')
    fig.add_hline(y=-80, col=1, row=1, line_color='#336699', line_width=2, line_dash='dash')

    fig.update_yaxes(title_text="Williams %R", row=1, col=1)
    fig.update_layout(height=600, width=1100)

    accuracy = calculate_accuracy(williams_r_buy_x, buy_price, williams_r_sell_x, sell_price)

    signal = get_signal(df, williams_r_buy_x, williams_r_sell_x)

    return fig.to_html(), accuracy, signal


def plot_sma(df):
    # SMA
    # df['sma_20'][0] = SMAIndicator(close=df['Close'],
    #             window=20)
    # df['sma_50'][0] = SMAIndicator(close=df['Close'],
    #             window=50)

    # window/period için 20-50 yerine 30-100 kullanan da var
    df['sma_20'] = pandas_ta.sma(df['close'], 20)
    df['sma_50'] = pandas_ta.sma(df['close'], 50)

    # Calculate buy sell signals
    buy_price, buy_signal, sell_price, sell_signal, signal, buy_price_x, sell_price_x = implement_sma_strategy(df['close'], df['sma_20'], df['sma_50'])

    # buy_price, buy_signal, sell_price, sell_signal, bb_signal, buy_price_x, sell_price_x = strategy.implement_bb_strategy(df['Close'], df['bollinger_lbands'], df['bollinger_hbands'])

    print('buy', buy_signal, 'sell', sell_signal)
    print('Buy', buy_price)
    print('Sell', sell_price)

    # Plot SMA trace
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Candlestick(x=df['time'],
                                 open=df['open'],
                                 high=df['high'],
                                 low=df['low'],
                                 close=df['close'],
                                 name='OHLC',
                                 opacity=0.8), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['sma_20'],
                             line=dict(color='orange', width=1),
                             name='SMA_20',
                             # hoverlabel=dict(color=)
                             ))
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['sma_50'],
                             line=dict(color='blue', width=1),
                             name='SMA_50',
                             ))

    # place buy and sell orders on the indicator
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][buy_price_x],
                             y=buy_price,
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green',
                             # hoverinfo=['text + x + y'],
                             # hovertext='Buy',
                             hovertemplate="Buy Signal<br>%{x}, %{y}<extra></extra>",
                             name='Buy Signal',
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][sell_price_x],
                             y=sell_price,
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red',
                             name='Sell Signal',
                             ))

    fig.update_yaxes(title_text="SMA", row=1, col=1) # color='pink'
    fig.update_layout(height=600, width=1100,
                      # legend=dict(orientation="h",
                      #             yanchor="top",
                      #             y=0.99,
                      #             xanchor="left",
                      #             x=0.01,
                      #             bgcolor="LightSteelBlue",
                      #             bordercolor="Black",
                      #             borderwidth=2
                      #             )
                      )

    accuracy = calculate_accuracy(buy_price_x, buy_price, sell_price_x, sell_price)

    signal = get_signal(df, buy_price_x, sell_price_x)

    return fig.to_html(), accuracy, signal


def plot_stochastic(df):
    # stochastic
    stoch = StochasticOscillator(high=df['high'],
                                 close=df['close'],
                                 low=df['low'],
                                 window=14,
                                 smooth_window=3)
    # print(stoch.stoch_signal())
    # print(stochastic_d)

    # stochastic_k, stochastic_d = talib.STOCH(high=df['High'],
    #                                          close=df['Close'],
    #                                          low=df['Low'])

    stochas = pandas_ta.stoch(high=df['high'],
                    close=df['close'],
                    low=df['low'])
    df['stoch_k'] = stochas['STOCHk_14_3_3']
    df['stoch_d'] = stochas['STOCHd_14_3_3']

    # Calculate buy sell signals
    buy_price, buy_signal, sell_price, sell_signal, stoch_signal, buy_price_x, sell_price_x  = implement_stochastic_strategy(df['close'], df['stoch_k'], df['stoch_d'])

    # buy_price, buy_signal, sell_price, sell_signal, bb_signal, buy_price_x, sell_price_x = strategy.implement_bb_strategy(df['Close'], df['bollinger_lbands'], df['bollinger_hbands'])

    print('buy', buy_signal, 'sell', sell_signal)
    print('Buy', buy_price)
    print('Sell', sell_price)

    # Plot stochastics trace on 4th row
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['stoch_k'],
                             line=dict(color='black', width=1)
                             ))
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['stoch_d'],
                             line=dict(color='blue', width=1)
                             ))


    # place buy and sell orders on the indicator
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][buy_price_x],
                             y=df['stoch_k'][buy_price_x],
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green',
                             # hoverinfo=['text + x + y'],
                             # hovertext='Buy',
                             hovertemplate="Buy Signal<br>%{x}, %{y}<extra></extra>",
                             name='Buy Signal',
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][sell_price_x],
                             y=df['stoch_k'][sell_price_x],
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red',
                             name='Sell Signal',
                             ))

    fig.update_yaxes(title_text="Stochastic Oscillator", row=1, col=1) # color='pink'
    fig.update_layout(height=600, width=1100,
                      # legend=dict(orientation="h",
                      #             yanchor="top",
                      #             y=0.99,
                      #             xanchor="left",
                      #             x=0.01,
                      #             bgcolor="LightSteelBlue",
                      #             bordercolor="Black",
                      #             borderwidth=2
                      #             )
                      )

    accuracy = calculate_accuracy(buy_price_x, buy_price, sell_price_x, sell_price)

    signal = get_signal(df, buy_price_x, sell_price_x)

    return fig.to_html(), accuracy, signal


def plot_cci(df):
    # CCI
    cci = CCIIndicator(high=df['high'],
                       low=df['low'],
                       close=df['close'],
                       window=20)

    df['cci'] = cci.cci()

    # Calculate buy sell signals
    buy_price, buy_signal, sell_price, sell_signal, cci_signal, buy_price_x, sell_price_x = implement_cci_strategy(df['close'], df['cci'])

    # buy_price, buy_signal, sell_price, sell_signal, bb_signal, buy_price_x, sell_price_x = strategy.implement_bb_strategy(df['Close'], df['bollinger_lbands'], df['bollinger_hbands'])

    print('buy', buy_signal, 'sell', sell_signal)
    print('Buy', buy_price)
    print('Sell', sell_price)

    # Plot SMA trace
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['cci'],
                             line=dict(color='orange', width=1),
                             name='CCI',
                             # hoverlabel=dict(color=)
                             ))

    # place buy and sell orders on the indicator
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][buy_price_x],
                             y=df['cci'][buy_price_x],
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green',
                             # hoverinfo=['text + x + y'],
                             # hovertext='Buy',
                             hovertemplate="Buy Signal<br>%{x}, %{y}<extra></extra>",
                             name='Buy Signal',
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][sell_price_x],
                             y=df['cci'][sell_price_x],
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red',
                             name='Sell Signal',
                             ))

    fig.update_yaxes(title_text="CCI", row=1, col=1) # color='pink'
    fig.update_layout(height=600, width=1100,
                      # legend=dict(orientation="h",
                      #             yanchor="top",
                      #             y=0.99,
                      #             xanchor="left",
                      #             x=0.01,
                      #             bgcolor="LightSteelBlue",
                      #             bordercolor="Black",
                      #             borderwidth=2
                      #             )
                      )

    accuracy = calculate_accuracy(buy_price_x, buy_price, sell_price_x, sell_price)

    signal = get_signal(df, buy_price_x, sell_price_x)

    return fig.to_html(), accuracy, signal


def plot_adx(df):
    # ADX
    adx = ADXIndicator(high=df['high'],
                       low=df['low'],
                       close=df['close'],
                       window=14)

    df['adx'] = adx.adx()
    df['adx_pos'] = adx.adx_pos()
    df['adx_neg'] = adx.adx_neg()

    # Calculate buy sell signals
    buy_price, buy_signal, sell_price, sell_signal, adx_signal, buy_price_x, sell_price_x = implement_adx_strategy(df['close'], df['adx_pos'], df['adx_neg'], df['adx'])

    print('buy', buy_signal, 'sell', sell_signal)
    print('Buy', buy_price)
    print('Sell', sell_price)

    # Plot ADX trace
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['adx'],
                             line=dict(color='blue', width=1),
                             name='ADX',
                             # hoverlabel=dict(color=)
                             ))
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['adx_pos'],
                             line=dict(color='green', width=1),
                             opacity=0.7,
                             name='ADX_POS',
                             ))
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['adx_neg'],
                             line=dict(color='red', width=1),
                             opacity=0.7,
                             name='ADX_NEG',
                             ))

    # place buy and sell orders on the indicator
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][buy_price_x],
                             y=df['adx_pos'][buy_price_x],
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green',
                             # hoverinfo=['text + x + y'],
                             # hovertext='Buy',
                             hovertemplate="Buy Signal<br>%{x}, %{y}<extra></extra>",
                             name='Buy Signal',
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][sell_price_x],
                             y=df['adx_neg'][sell_price_x],
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red',
                             name='Sell Signal',
                             ))

    fig.update_yaxes(title_text="ADX", row=1, col=1) # color='pink'
    fig.update_layout(height=600, width=1100,
                      # legend=dict(orientation="h",
                      #             yanchor="top",
                      #             y=0.99,
                      #             xanchor="left",
                      #             x=0.01,
                      #             bgcolor="LightSteelBlue",
                      #             bordercolor="Black",
                      #             borderwidth=2
                      #             )
                      )

    accuracy = calculate_accuracy(buy_price_x, buy_price, sell_price_x, sell_price)

    signal = get_signal(df, buy_price_x, sell_price_x)

    return fig.to_html(), accuracy, signal


def plot_aroon(df):
    # Aroon
    aroon = AroonIndicator(close=df['close'],
                           window=25)

    df['aroon_up'] = aroon.aroon_up()
    df['aroon_down'] = aroon.aroon_down()

    # Calculate buy sell signals
    buy_price, buy_signal, sell_price, sell_signal, aroon_signal, buy_price_x, sell_price_x = implement_aroon_strategy(
        df['close'], df['aroon_up'], df['aroon_down'])


    print('buy', buy_signal, 'sell', sell_signal)
    print('Buy', buy_price)
    print('Sell', sell_price)

    # Plot Aroon trace
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['aroon_up'],
                             line=dict(color='green', width=1),
                             name='Aroon Up',
                             # hoverlabel=dict(color=)
                             ))
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['aroon_down'],
                             line=dict(color='red', width=1),
                             name='Aroon Down',
                             ))

    # place buy and sell orders on the indicator
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][buy_price_x],
                             y=df['aroon_up'][buy_price_x],
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green',
                             # hoverinfo=['text + x + y'],
                             # hovertext='Buy',
                             hovertemplate="Buy Signal<br>%{x}, %{y}<extra></extra>",
                             name='Buy Signal',
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][sell_price_x],
                             y=df['aroon_down'][sell_price_x],
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red',
                             name='Sell Signal',
                             ))

    fig.update_yaxes(title_text="Aroon", row=1, col=1)  # color='pink'
    fig.update_layout(height=600, width=1100,
                      # legend=dict(orientation="h",
                      #             yanchor="top",
                      #             y=0.99,
                      #             xanchor="left",
                      #             x=0.01,
                      #             bgcolor="LightSteelBlue",
                      #             bordercolor="Black",
                      #             borderwidth=2
                      #             )
                      )

    accuracy = calculate_accuracy(buy_price_x, buy_price, sell_price_x, sell_price)

    signal = get_signal(df, buy_price_x, sell_price_x)

    return fig.to_html(), accuracy, signal


def plot_kc(df):
    # KC
    kc = KeltnerChannel(high=df['high'],
                        low=df['low'],
                        close=df['close'],
                        window=20)

    df['kc_high'] = kc.keltner_channel_hband()
    df['kc_low'] = kc.keltner_channel_lband()
    df['kc_middle'] = kc.keltner_channel_mband()

    # Calculate buy sell signals
    buy_price, buy_signal, sell_price, sell_signal, kc_signal, buy_price_x, sell_price_x  = implement_kc_strategy(df['close'], df['kc_high'], df['kc_low'])


    print('buy', buy_signal, 'sell', sell_signal)
    print('Buy', buy_price)
    print('Sell', sell_price)

    # Plot KC trace
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Candlestick(x=df['time'],
                                 open=df['open'],
                                 high=df['high'],
                                 low=df['low'],
                                 close=df['close'],
                                 name='OHLC',
                                 opacity=0.8), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['kc_high'],
                             line=dict(color='grey', width=1),
                             name='KC Upper',
                             # hoverlabel=dict(color=)
                             ))
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['kc_middle'],
                             line=dict(color='orange', width=1),
                             name='KC Middle',
                             ))
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['kc_low'],
                             line=dict(color='grey', width=1),
                             name='KC Lower',
                             ))

    # place buy and sell orders on the indicator
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][buy_price_x],
                             y=buy_price,
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green',
                             # hoverinfo=['text + x + y'],
                             # hovertext='Buy',
                             hovertemplate="Buy Signal<br>%{x}, %{y}<extra></extra>",
                             name='Buy Signal',
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][sell_price_x],
                             y=sell_price,
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red',
                             name='Sell Signal',
                             ))

    fig.update_yaxes(title_text="KC", row=1, col=1)  # color='pink'
    fig.update_layout(height=600, width=1100,
                      # legend=dict(orientation="h",
                      #             yanchor="top",
                      #             y=0.99,
                      #             xanchor="left",
                      #             x=0.01,
                      #             bgcolor="LightSteelBlue",
                      #             bordercolor="Black",
                      #             borderwidth=2
                      #             )
                      )

    accuracy = calculate_accuracy(buy_price_x, buy_price, sell_price_x, sell_price)

    signal = get_signal(df, buy_price_x, sell_price_x)

    return fig.to_html(), accuracy, signal


def plot_tsi(df):
    # TSI
    tsi = pandas_ta.tsi(close=df['close'])

    df['tsi'] = tsi['TSI_13_25_13']
    df['tsi_signal'] = tsi['TSIs_13_25_13']

    # Calculate buy sell signals
    buy_price, buy_signal, sell_price, sell_signal, tsi_signal, buy_price_x, sell_price_x = implement_tsi_strategy(df['close'], df['tsi'], df['tsi_signal'])

    print('buy', buy_signal, 'sell', sell_signal)
    print('Buy', buy_price)
    print('Sell', sell_price)

    # Plot TSI trace
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['tsi'],
                             line=dict(color='red', width=1),
                             name='TSI Line',
                             # hoverlabel=dict(color=)
                             ))
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['tsi_signal'],
                             line=dict(color='orange', width=1),
                             name='Signal Line',
                             ))

    # place buy and sell orders on the indicator
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][buy_price_x],
                             y=df['tsi'][buy_price_x],
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green',
                             # hoverinfo=['text + x + y'],
                             # hovertext='Buy',
                             hovertemplate="Buy Signal<br>%{x}, %{y}<extra></extra>",
                             name='Buy Signal',
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][sell_price_x],
                             y=df['tsi'][sell_price_x],
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red',
                             name='Sell Signal',
                             ))

    fig.update_yaxes(title_text="TSI", row=1, col=1)  # color='pink'
    fig.update_layout(height=600, width=1100,
                      # legend=dict(orientation="h",
                      #             yanchor="top",
                      #             y=0.99,
                      #             xanchor="left",
                      #             x=0.01,
                      #             bgcolor="LightSteelBlue",
                      #             bordercolor="Black",
                      #             borderwidth=2
                      #             )
                      )

    accuracy = calculate_accuracy(buy_price_x, buy_price, sell_price_x, sell_price)

    signal = get_signal(df, buy_price_x, sell_price_x)

    return fig.to_html(), accuracy, signal


def plot_ao(df):
    # AO
    ao = AwesomeOscillatorIndicator(high=df['high'],
                                    low=df['low'],
                                    window1=5,
                                    window2=34)

    df['ao'] = ao.awesome_oscillator()

    # Calculate buy sell signals
    buy_price, buy_signal, sell_price, sell_signal, ao_signal, buy_price_x, sell_price_x = implement_ao_crossover(df['close'], df['ao'])


    print('buy', buy_signal, 'sell', sell_signal)
    print('Buy', buy_price)
    print('Sell', sell_price)

    # Plot AO trace
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Bar(x=df['time'],
                         y=df['ao'],
                         # marker_color=,
                         # line=dict(color='red', width=1),
                         name='AO',
                         # hoverlabel=dict(color=)
                         ))


    # place buy and sell orders on the indicator
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][buy_price_x],
                             y=df['ao'][buy_price_x],
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green',
                             # hoverinfo=['text + x + y'],
                             # hovertext='Buy',
                             hovertemplate="Buy Signal<br>%{x}, %{y}<extra></extra>",
                             name='Buy Signal',
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][sell_price_x],
                             y=df['ao'][sell_price_x],
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red',
                             name='Sell Signal',
                             ))

    fig.update_yaxes(title_text="AO", row=1, col=1)  # color='pink'
    fig.update_layout(height=600, width=1100,
                      # legend=dict(orientation="h",
                      #             yanchor="top",
                      #             y=0.99,
                      #             xanchor="left",
                      #             x=0.01,
                      #             bgcolor="LightSteelBlue",
                      #             bordercolor="Black",
                      #             borderwidth=2
                      #             )
                      )

    accuracy = calculate_accuracy(buy_price_x, buy_price, sell_price_x, sell_price)

    signal = get_signal(df, buy_price_x, sell_price_x)

    return fig.to_html(), accuracy, signal


def plot_coppock(df):
    # Coppock Curve
    df['coppock'] = pandas_ta.coppock(close=df['close'])

    # Calculate buy sell signals
    buy_price, buy_signal, sell_price, sell_signal, cc_signal, buy_price_x, sell_price_x = implement_cc_strategy(df['close'], df['coppock'])

    print('buy', buy_signal, 'sell', sell_signal)
    print('Buy', buy_price)
    print('Sell', sell_price)

    # Plot CC trace
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Bar(x=df['time'],
                             y=df['coppock'],
                             # line=dict(color='red', width=1),
                             name='Coppock Curve',
                             # hoverlabel=dict(color=)
                             ))

    # place buy and sell orders on the indicator
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][buy_price_x],
                             y=df['coppock'][buy_price_x],
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green',
                             # hoverinfo=['text + x + y'],
                             # hovertext='Buy',
                             hovertemplate="Buy Signal<br>%{x}, %{y}<extra></extra>",
                             name='Buy Signal',
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][sell_price_x],
                             y=df['coppock'][sell_price_x],
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red',
                             name='Sell Signal',
                             ))

    fig.update_yaxes(title_text="Coppock", row=1, col=1)  # color='pink'
    fig.update_layout(height=600, width=1100,
                      # legend=dict(orientation="h",
                      #             yanchor="top",
                      #             y=0.99,
                      #             xanchor="left",
                      #             x=0.01,
                      #             bgcolor="LightSteelBlue",
                      #             bordercolor="Black",
                      #             borderwidth=2
                      #             )
                      )

    accuracy = calculate_accuracy(buy_price_x, buy_price, sell_price_x, sell_price)

    signal = get_signal(df, buy_price_x, sell_price_x)

    return fig.to_html(), accuracy, signal


def plot_kst(df):
    # KST
    kst = KSTIndicator(close=df['close'])

    df['kst'] = kst.kst()
    df['kst_signal'] = kst.kst_sig()

    # Calculate buy sell signals
    buy_price, buy_signal, sell_price, sell_signal, kst_signal, buy_price_x, sell_price_x = implement_kst_strategy(df['close'], df['kst'], df['kst_signal'])

    print('buy', buy_signal, 'sell', sell_signal)
    print('Buy', buy_price)
    print('Sell', sell_price)

    # Plot KST trace
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['kst'],
                             line=dict(color='purple', width=1),
                             name='KST',
                             # hoverlabel=dict(color=)
                             ))
    fig.add_trace(go.Scatter(x=df['time'],
                             y=df['kst_signal'],
                             line=dict(color='orange', width=1),
                             name='KST Signal',
                             ))

    # place buy and sell orders on the indicator
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][buy_price_x],
                             y=df['kst'][buy_price_x],
                             marker_symbol='triangle-up',
                             # s=200,
                             marker_size=15,
                             marker_color='green',
                             # hoverinfo=['text + x + y'],
                             # hovertext='Buy',
                             hovertemplate="Buy Signal<br>%{x}, %{y}<extra></extra>",
                             name='Buy Signal',
                             ))
    fig.add_trace(go.Scatter(mode="markers",
                             x=df['time'][sell_price_x],
                             y=df['kst'][sell_price_x],
                             marker_symbol='triangle-down',
                             # s=200,
                             marker_size=15,
                             marker_color='red',
                             name='Sell Signal',
                             ))

    fig.update_yaxes(title_text="KST", row=1, col=1)  # color='pink'
    fig.update_layout(height=600, width=1100,
                      # legend=dict(orientation="h",
                      #             yanchor="top",
                      #             y=0.99,
                      #             xanchor="left",
                      #             x=0.01,
                      #             bgcolor="LightSteelBlue",
                      #             bordercolor="Black",
                      #             borderwidth=2
                      #             )
                      )

    accuracy = calculate_accuracy(buy_price_x, buy_price, sell_price_x, sell_price)

    signal = get_signal(df, buy_price_x, sell_price_x)

    return fig.to_html(), accuracy, signal
