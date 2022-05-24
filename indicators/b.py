import pandas as pd
import requests
import websockets
import pandas_ta as ta


def MACD_Strategy(df, risk):
    MACD_Buy=[]
    MACD_Sell=[]
    position=False

    for i in range(0, len(df)):
        if df['MACD_12_26_9'][i] > df['MACDs_12_26_9'][i] :
            MACD_Sell.append(np.nan)
            if position ==False:
                MACD_Buy.append(df['Adj Close'][i])
                position=True
            else:
                MACD_Buy.append(np.nan)
        elif df['MACD_12_26_9'][i] < df['MACDs_12_26_9'][i] :
            MACD_Buy.append(np.nan)
            if position == True:
                MACD_Sell.append(df['Adj Close'][i])
                position=False
            else:
                MACD_Sell.append(np.nan)
        elif position == True and df['Adj Close'][i] < MACD_Buy[-1] * (1 - risk):
            MACD_Sell.append(df["Adj Close"][i])
            MACD_Buy.append(np.nan)
            position = False
        elif position == True and df['Adj Close'][i] < df['Adj Close'][i - 1] * (1 - risk):
            MACD_Sell.append(df["Adj Close"][i])
            MACD_Buy.append(np.nan)
            position = False
        else:
            MACD_Buy.append(np.nan)
            MACD_Sell.append(np.nan)

    data['MACD_Buy_Signal_price'] = MACD_Buy
    data['MACD_Sell_Signal_price'] = MACD_Sell

MACD_strategy = MACD_Strategy(data, 0.025)

def MACD_color(data):
    MACD_color = []
    for i in range(0, len(data)):
        if data['MACDh_12_26_9'][i] > data['MACDh_12_26_9'][i - 1]:
            MACD_color.append(True)
        else:
            MACD_color.append(False)
    return MACD_color

data['positive'] = MACD_color(data)





def Stoch(close,high,low):    
    slowk, slowd = ta.STOCH(high, low, close)
    stochSell = ((slowk < slowd) & (slowk.shift(1) > slowd.shift(1))) & (slowd > 80)
    stochBuy = ((slowk > slowd) & (slowk.shift(1) < slowd.shift(1))) & (slowd < 20)
    return stochSell,stochBuy, slowk,slowd





# SUPERTREND
son_kapanis = close_array[-1]
onceki_kapanis = close_array[-2]

son_supertrend_deger = supertrend[-1]
onceki_supertrend_deger = supertrend[-2]

# renk yeşile dönüyor, trend yükselişe geçti
if son_kapanis > son_supertrend_deger and onceki_kapanis < onceki_supertrend_deger:
	print('al sinyali')

# renk kırmızıya dönüyor, trend düşüşe geçti
if son_kapanis < son_supertrend_deger and onceki_kapanis > onceki_supertrend_deger:
        print('sat sinyali')







# Calculate Start and End time for our historical data request window
def startEnd(interval):
    end = datetime.now()
    start = {
      'minute': lambda end: end - relativedelta(days=5),
      'hour': lambda end: end - relativedelta(months=2),
      'daily': lambda end: end - relativedelta(years=2),
      'weekly': lambda end: end - relativedelta(years=5),
      'monthly': lambda end: end - relativedelta(years=10),
    }[interval](end)
    return start.strftime("%Y-%m-%dT%H:%M:%S"),end.strftime("%Y-%m-%dT%H:%M:%S")

myStart, myEnd = startEnd(myInterval)  # myInterval = '5m' or '1day'








def on_message(ws, message):
    candlesticks = json.loads(message)
    # print(candlesticks['k']['t'])
    processed_data = []
    candlestick = {
        "time": datetime.utcfromtimestamp(candlesticks['k']['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # open time
        # "time": datetime.fromtimestamp(data[0] / 1000, tz=tzinfo.tzname("Turkey")).strftime('%Y-%m-%d %H:%M:%S'),  # open time
        # "time": datetime.fromtimestamp(data[0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # open time
        "Open": int(float(candlesticks['k']['o'])),
        "High": int(float(candlesticks['k']['h'])),
        "Low": int(float(candlesticks['k']['l'])),
        "Close": int(float(candlesticks['k']['c'])),
        "Volume": int(float(candlesticks['k']['v'])),
        "close time": candlesticks['k']['T'] / 1000,
        "quote asset volume": candlesticks['k']['q'],
        "number of trades": candlesticks['k']['n'],
        "taker buy base asset volume": candlesticks['k']['V'],
        "taker buy quote asset volume": candlesticks['k']['Q'],
        "ignore": candlesticks['k']['B'],
    }

    # open_time = [int(entry[0]) for entry in candlesticks]
    # open = [float(entry[1]) for entry in candlesticks]
    # high = [float(entry[2]) for entry in candlesticks]
    # low = [float(entry[3]) for entry in candlesticks]
    # close = [float(entry[4]) for entry in candlesticks]
    #
    processed_data.append(candlestick)
    # print(processed_data)
    df = pd.DataFrame(processed_data)
    return df


def on_error(ws, error):
    print(error)


def on_close(close_msg):
    print(close_msg)


async def streamKline(symbol, interval):
    socket = f'wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}'
    async with websockets.connect(socket) as client:
        while True:
            candlesticks = json.loads(await client.recv())
            processed_data = []
            candlestick = {
                "time": datetime.utcfromtimestamp(candlesticks['k']['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # open time
                # "time": datetime.fromtimestamp(data[0] / 1000, tz=tzinfo.tzname("Turkey")).strftime('%Y-%m-%d %H:%M:%S'),  # open time
                # "time": datetime.fromtimestamp(data[0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # open time
                "Open": int(float(candlesticks['k']['o'])),
                "High": int(float(candlesticks['k']['h'])),
                "Low": int(float(candlesticks['k']['l'])),
                "Close": int(float(candlesticks['k']['c'])),
                "Volume": int(float(candlesticks['k']['v'])),
                "close time": candlesticks['k']['T'] / 1000,
                "quote asset volume": candlesticks['k']['q'],
                "number of trades": candlesticks['k']['n'],
                "taker buy base asset volume": candlesticks['k']['V'],
                "taker buy quote asset volume": candlesticks['k']['Q'],
                "ignore": candlesticks['k']['B'],
            }

            # open_time = [int(entry[0]) for entry in candlesticks]
            # open = [float(entry[1]) for entry in candlesticks]
            # high = [float(entry[2]) for entry in candlesticks]
            # low = [float(entry[3]) for entry in candlesticks]
            # close = [float(entry[4]) for entry in candlesticks]
            #
            processed_data.append(candlestick)
            # print(processed_data)
            data = pd.DataFrame(processed_data)
            df.append(data)
            time.sleep(1)

        # print(candlesticks)
    # ws = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_close=on_close)
    # ws.run_forever()








def update_graph():
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.22)  # you can add ", row_heights=[0.5,0.1]" and "row_width=[0.25, 0.75]"
    # add chart title
    fig.update_layout(title="BTCUSDT")
    # add candlestick chart for price data to 1st row
    fig.add_trace(go.Candlestick(x=df['time'],
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 # increasing_line_color='orange',
                                 # decreasing_line_color='black',
                                 # showlegend=False  #hiding legends(legend is the colors and traces written in the top right)
                                 ), row=1, col=1)

    fig.canvas.draw()
    time.sleep(1)
    # plt.pause(0.1)


async def main():
    url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
    async with websockets.connect(url) as client:
        while True:
            data = json.loads(await client.recv())['k']

            event_time = datetime.utcfromtimestamp(data['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # open time

            if(data["x"]):
                # print(event_time, data['c'])
                df["time"].append(event_time)
                df["Open"].append(int(float(data['o'])))
                df["High"].append(int(float(data['h'])))
                df["Low"].append(int(float(data['l'])))
                df["Close"].append(int(float(data['c'])))
                df["Volume"].append(int(float(data['v'])))

            # update_graph()
            print(df)








def live_data():
    first = True
    data = gather_data(Client.KLINE_INTERVAL_5MINUTE, 12)
    while True:
        if (datetime.now().second % 10 == 0) or first:
            # refresh data
            first = False
            data = gather_data(Client.KLINE_INTERVAL_5MINUTE, 12)
            time.sleep(1)
        return data
df = live_data()









def on_message(ws, message):
    # global df
    candlesticks = json.loads(message)
    # print(candlesticks['k']['t'])
    processed_data = []
    candlestick = {
        "time": datetime.utcfromtimestamp(candlesticks['k']['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # open time
        # "time": datetime.fromtimestamp(data[0] / 1000, tz=tzinfo.tzname("Turkey")).strftime('%Y-%m-%d %H:%M:%S'),  # open time
        # "time": datetime.fromtimestamp(data[0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # open time
        "Open": int(float(candlesticks['k']['o'])),
        "High": int(float(candlesticks['k']['h'])),
        "Low": int(float(candlesticks['k']['l'])),
        "Close": int(float(candlesticks['k']['c'])),
        "Volume": int(float(candlesticks['k']['v'])),
        "close time": candlesticks['k']['T'] / 1000,
        "quote asset volume": candlesticks['k']['q'],
        "number of trades": candlesticks['k']['n'],
        "taker buy base asset volume": candlesticks['k']['V'],
        "taker buy quote asset volume": candlesticks['k']['Q'],
        "ignore": candlesticks['k']['B'],
    }

    # open_time = [int(entry[0]) for entry in candlesticks]
    # open = [float(entry[1]) for entry in candlesticks]
    # high = [float(entry[2]) for entry in candlesticks]
    # low = [float(entry[3]) for entry in candlesticks]
    # close = [float(entry[4]) for entry in candlesticks]
    #
    processed_data.append(candlestick)
    # print(processed_data)
    data = pd.DataFrame(processed_data)
    df.append(data)



def on_error(ws, error):
    print(error)


def on_close(close_msg):
    print(close_msg)


def streamKline(symbol, interval):
    socket = f'wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}'
    ws = websocket.WebSocketApp(socket, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()
    # ws.create_dispatcher(10)
    # time.sleep(100)




# loop = asyncio.get_event_loop()
# loop.run_until_complete(streamKline('btcusdt', '1m'))
#
# frames = [gather_data(Client.KLINE_INTERVAL_1MINUTE, 12), streamKline('btcusdt', '1m')]
# df = pd.concat(frames)
# print(streamKline('btcusdt', '1m'))

# y = on_message(message=streamKline('btcusdt', '1m'))
# print(y)
# y = streamKline('btcusdt', '1m')
# print(y)


def get_data():
    # x = streamKline('btcusdt', '1m')
    # data = gather_data(Client.KLINE_INTERVAL_1MINUTE, 12)
    frames = [gather_data(Client.KLINE_INTERVAL_1MINUTE, 12), streamKline('btcusdt', '1m')]
    # data.append(x)
    data = pd.concat(frames)
    time.sleep(100)
    return data

# df = get_data()

# t = threading.Thread(target=streamKline('btcusdt', '1m'))
# t.start()

def take_data():
    payload = {
        'symbol': 'BTCUSD',
        'interval': '1m',
        'limit': 200,
    }

    url = 'https://api.binance.us/api/v3/klines'
    r = requests.get(url, params=payload)
    r = r.json()

    processed_candlesticks = []
    unix_time =[]
    for data in r:
        unix_time.append(data[:][0])
        candlestick = {
            # "time": datetime.utcfromtimestamp(data[:][0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # open time
            # "time": data[:][0],  # open time
            # "time": datetime.fromtimestamp(data[0] / 1000, tz=tzinfo.tzname("Turkey")).strftime('%Y-%m-%d %H:%M:%S'),  # open time
            # "time": datetime.fromtimestamp(data[0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # open time
            "Open": int(float(data[:][1])),
            "High": int(float(data[:][2])),
            "Low": int(float(data[:][3])),
            "Close": int(float(data[:][4])),
            "Volume": int(float(data[:][5])),
            "close time": data[:][6] / 1000,
            "quote asset volume": data[:][7],
            "number of trades": data[:][8],
            "taker buy base asset volume": data[:][9],
            "taker buy quote asset volume": data[:][10],
            "ignore": data[:][11],
        }

        # open_time = [int(entry[0]) for entry in candlesticks]
        # open = [float(entry[1]) for entry in candlesticks]
        # high = [float(entry[2]) for entry in candlesticks]
        # low = [float(entry[3]) for entry in candlesticks]
        # close = [float(entry[4]) for entry in candlesticks]
        #
        processed_candlesticks.append(candlestick)


    # df = pd.DataFrame(processed_candlesticks)

    new_time = []
    for n in unix_time:
        new_time.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(n/1000)))
    # df.index = df["time"]
    df = pd.DataFrame(processed_candlesticks, index=new_time)
    ts_df = df.reindex(index=df.index[::-1])
    return ts_df


# df = candles('BTCUSD')




import time
import requests
import pandas as pd

payload = {
        'symbol': 'BTCUSD',
        'interval': '1m',
        'limit': 200,
    }

    url = 'https://api.binance.us/api/v3/klines'
    r = requests.get(url, params=payload)
    r = r.json()

    processed_candlesticks = []
    unix_time = []
    for data in r:
        unix_time.append(data[:][0])
        candlestick = {
            # "time": datetime.utcfromtimestamp(data[:][0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # open time
            # "time": data[:][0],  # open time
            # "time": datetime.fromtimestamp(data[0] / 1000, tz=tzinfo.tzname("Turkey")).strftime('%Y-%m-%d %H:%M:%S'),  # open time
            # "time": datetime.fromtimestamp(data[0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # open time
            "Open": int(float(data[:][1])),
            "High": int(float(data[:][2])),
            "Low": int(float(data[:][3])),
            "Close": int(float(data[:][4])),
            "Volume": int(float(data[:][5])),
            "close time": data[:][6] / 1000,
            "quote asset volume": data[:][7],
            "number of trades": data[:][8],
            "taker buy base asset volume": data[:][9],
            "taker buy quote asset volume": data[:][10],
            "ignore": data[:][11],
        }

        processed_candlesticks.append(candlestick)

    new_time = []
    for n in unix_time:
        new_time.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(n / 1000)))
    # df.index = df["time"]
    df = pd.DataFrame(processed_candlesticks, index=new_time)




# Convert date to timestamp and make index
data.index = data["Date"].apply(lambda x: pd.Timestamp(x))
data.drop("Date", axis=1, inplace=True)


# Get today's date as UTC timestamp
today = datetime.today().strftime("%d/%m/%Y")
today = datetime.strptime(today + " +0000", "%d/%m/%Y %z")
to = int(today.timestamp())
# Get date ten years ago as UTC timestamp
ten_yr_ago = today-relativedelta(years=10)
fro = int(ten_yr_ago.timestamp())
