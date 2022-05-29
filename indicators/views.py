from django.shortcuts import render, redirect

#most dependencies and imports made in functions.py to avoid clutter
from .functions import *
from binance.client import Client
from datetime import datetime, timedelta
from plotly.subplots import make_subplots
from . import plot_indicators as plt
from django.http import JsonResponse
# import indicators.config
import math

# Create your views here.

# def homeView(request):
#
#
#     api_key = 'YX9741BHQFXIYA0B'
#
#     stock = 'PLTR'
#
#     api_key = 'YX9741BHQFXIYA0B'
#     period= 60
#
#     ts = TimeSeries(key=api_key, output_format='pandas',)
#     data_ts, meta_data_ts = ts.get_intraday(stock, interval='1min', outputsize='compact')
#
#     ti = TechIndicators(key=api_key, output_format='pandas')
#     data_ti, meta_data_ti  = ti.get_rsi(stock, interval='1min', time_period=period, series_type='close')
#
#     ts_df = data_ts
#     ti_df = data_ti
#
#     #Fundamentals
#     payload = {'function': 'OVERVIEW', 'symbol': 'PLTR', 'apikey': 'YX9741BHQFXIYA0B'}
#     r = requests.get('https://www.alphavantage.co/query', params=payload)
#     r = r.json()
#
#
#     #plotly graph
#     def candlestick():
#         figure = go.Figure(
#             data = [
#                     go.Candlestick(
#                       x = ts_df.index,
#                       high = ts_df['2. high'],
#                       low = ts_df['3. low'],
#                       open = ts_df['1. open'],
#                       close = ts_df['4. close'],
#                     )
#                   ]
#         )
#
#         candlestick_div = plot(figure, output_type='div')
#         return candlestick_div
#
#
#     sector = r['Sector']
#     marketcap = r['MarketCapitalization']
#     peratio = r['PERatio']
#     yearhigh = r['52WeekHigh']
#     yearlow = r['52WeekLow']
#     eps = r['EPS']
#
#
#
#     timeseries = ts_df.to_dict(orient='records')
#
#     closingprice = []
#     for k in timeseries:
#       closingprice.append(k['4. close'])
#
#     lowprice = []
#     for k in timeseries:
#       closingprice.append(k['3. low'])
#
#     highprice = []
#     for k in timeseries:
#       closingprice.append(k['2. high'])
#
#     openprice = []
#     for k in timeseries:
#       closingprice.append(k['1. open'])
#
#     pricedata = {
#         'close': [closingprice],
#         'open': [openprice],
#         'high': [highprice],
#         'low': [lowprice],
#     }
#
#     #miscellaneous stuff
#     day = datetime.now()
#     day = day.strftime("%A")
#
#     def human_format(num):
#         magnitude = 0
#         while abs(num) >= 1000:
#             magnitude += 1
#             num /= 1000.0
#         # add more suffixes if you need them
#         return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
#
#     marketcap = int(marketcap)
#     marketcap = human_format(marketcap)
#
#     closingprice = closingprice[0:15]
#
#
#     context = {
#         'sector': sector,
#         'marketcap': marketcap,
#         'peratio': peratio,
#         'yearhigh': yearhigh,
#         'yearlow': yearlow,
#         'eps': eps,
#         'closingprice': closingprice,
#         'openprice': openprice,
#         'highprice': highprice,
#         'lowprice': lowprice,
#         'pricedata': pricedata,
#         'timeseries': timeseries,
#         'stock': stock,
#         'day': day,
#         'candlestick': candlestick(),
#     }
#
#     return render(request, 'indicators/index.html', context)



def homeView(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        return redirect('crypto/')

    context={

    }
    return render(request, 'indicators/index.html', context)



def cryptoView(request):

    if request.method == 'POST':
        # symbol = request.POST.get('symbol')
        # symbol = symbol.upper()
        symbol = 'BTCUSD'
        interval = request.POST.get('interval')
    else:
        symbol = 'BTCUSD'
        interval = '1m'

    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)



    #get a fricken df
    ts_df = candles(symbol, interval)
    #PlotlyGraph
    def candlestick():
        figure = go.Figure(
            data = [
                    go.Candlestick(
                      x = ts_df['time'],
                      high = ts_df['high'],
                      low = ts_df['low'],
                      open = ts_df['open'],
                      close = ts_df['close'],
                    )
                  ]
        )

        candlestick_div = plot(figure, output_type='div')
        return candlestick_div
    #endPlotlyGraph
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")


    context={
    'moredata': moredata,
    'eth': eth,
    'btc': btc,
    'ltc': ltc,
    'percentchange': percentchange,
    'buyers': buyers,
    'sellers': sellers,
    'data': data,
    'candlestick': candlestick(),
    }
    return render(request, 'indicators/crypto.html', context)


def candlestick(request):
    API_KEY = 'yourbinanceapikey'
    API_SECRET = 'yourbinanceapisecret'

    client = Client(API_KEY, API_SECRET)

    if request.method == 'POST':
        interval = request.POST.get('interval')
        print(interval)
        start_time = int(request.POST.get('starting_time'))
    else:
        interval = client.KLINE_INTERVAL_1MINUTE
        start_time = 48

    global df
    df = plt.gather_data(interval, start_time)
    # request.session['df'] = df

    plot_candlestick = plt.plot_candlestick(df)

    indicator_data = [('Bollinger Bands (BBANDS)', 0.5),
                      ('Relative Strength Index (RSI)', 0.3),
                      ('Stochastic RSI', 0.5),
                      ('Supertrend', 0.4),
                      ('Moving Average Convergence/Divergence (MACD)', 0.6),
                      ('The Ichimoku Cloud', 0.7),
                      ('Williams %R', 0.8),
                      ('Exponential Moving Average (EMA)', 0.9)]
    indicator_data.sort(key=lambda a: a[1], reverse=True)
    links = ('http://127.0.0.1:8000/',
             'http://127.0.0.1:8000/macd',
             'http://127.0.0.1:8000/',
             'http://127.0.0.1:8000/macd',
             'http://127.0.0.1:8000/')

    plot_bb, bb_accuracy, bb_signal, bb_hband, bb_mavg, bb_lband, buy_price, sell_price, buy_price_x, sell_price_x = plt.plot_bbands(df)
    plot_rsi, rsi_accuracy, rsi_signal, rsi, rsi_buy_x, rsi_sell_x = plt.plot_rsi(df)
    plot_supertrend, supertrend_accuracy, supertrend_signal = plt.plot_supertrend(df)
    plot_macd, macd_accuracy, macd_signal = plt.plot_macd(df)
    plot_williams_r, williams_r_accuracy, williams_r_signal = plt.plot_williams_r_percentage(df)
    plot_sma, sma_accuracy, sma_signal = plt.plot_sma(df)
    plot_stoch, stoch_accuracy, stoch_signal = plt.plot_stochastic(df)
    plot_cci, cci_accuracy, cci_signal = plt.plot_cci(df)
    plot_adx, adx_accuracy, adx_signal = plt.plot_adx(df)
    plot_aroon, aroon_accuracy, aroon_signal = plt.plot_aroon(df)
    plot_kc, kc_accuracy, kc_signal = plt.plot_kc(df)
    plot_tsi, tsi_accuracy, tsi_signal = plt.plot_tsi(df)
    plot_ao, ao_accuracy, ao_signal = plt.plot_ao(df)
    plot_coppock, coppock_accuracy, coppock_signal = plt.plot_coppock(df)
    plot_kst, kst_accuracy, kst_signal = plt.plot_kst(df)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")


    context = {
        'moredata': moredata,
        'eth': eth,
        'btc': btc,
        'ltc': ltc,
        'percentchange': percentchange,
        'buyers': buyers,
        'sellers': sellers,
        'data': data,
        'candle_data': history(interval, start_time),

            'title': 'BTCUSDT Candlestick Chart',
               'plot': plot_candlestick,
               'indicators': indicator_data,
               'links': links,

               'bbands': 'Bollinger Bands (BBANDS)',
               'bb_accuracy': bb_accuracy,
               'bb_signal': bb_signal,

               'rsi': 'Relative Strength Index (RSI)',
               'rsi_accuracy': rsi_accuracy,
               'rsi_signal': rsi_signal,

               'supertrend': 'Supertrend',
               'supertrend_accuracy': supertrend_accuracy,
               'supertrend_signal': supertrend_signal,

               'macd': 'Moving Average Convergence/Divergence (MACD)',
               'macd_accuracy': macd_accuracy,
               'macd_signal': macd_signal,

               'williams_r_percentage': 'Williams %R',
               'williams_r_accuracy': williams_r_accuracy,
               'williams_r_signal': williams_r_signal,

               'sma': 'Simple Moving Average (SMA)',
               'sma_accuracy': sma_accuracy,
               'sma_signal': sma_signal,

               'stochastic': 'Stochastic Oscillator',
               'stoch_accuracy': stoch_accuracy,
               'stoch_signal': stoch_signal,

               'cci': 'Commodity Channel Index (CCI)',
               'cci_accuracy': cci_accuracy,
               'cci_signal': cci_signal,

               'adx': 'Average Directional Index (ADX)',
               'adx_accuracy': adx_accuracy,
               'adx_signal': adx_signal,

               'aroon': 'Aroon Indicator',
               'aroon_accuracy': aroon_accuracy,
               'aroon_signal': aroon_signal,

               'kc': 'Keltner Channel',
               'kc_accuracy': kc_accuracy,
               'kc_signal': kc_signal,

               'tsi': 'True Strength Index',
               'tsi_accuracy': tsi_accuracy,
               'tsi_signal': tsi_signal,

               'ao': 'Awesome Oscillator',
               'ao_accuracy': ao_accuracy,
               'ao_signal': ao_signal,

               'coppock': 'Coppock Curve',
               'coppock_accuracy': coppock_accuracy,
               'coppock_signal': coppock_signal,

               'kst': 'Know Sure Thing (KST)',
               'kst_accuracy': kst_accuracy,
               'kst_signal': kst_signal,
               }

    return render(request, 'indicators/crypto.html', context)


def bbands(request):
    API_KEY = 'yourbinanceapikey'
    API_SECRET = 'yourbinanceapisecret'

    client = Client(API_KEY, API_SECRET)

    if request.method == 'POST':
        interval = request.POST.get('interval')
        print(interval)
        start_time = int(request.POST.get('starting_time'))
    else:
        interval = client.KLINE_INTERVAL_1MINUTE
        start_time = 48




    # df = request.session.get('df')
    plot_bb, bb_accuracy, bb_signal, bb_hband, bb_mavg, bb_lband, buy_price, sell_price, buy_price_x, sell_price_x = plt.plot_bbands(df)

    time = df["time"].tolist()
    hband_list = bb_hband.tolist()
    new_hband_list = [x for x in hband_list if math.isnan(x) == False]

    mavg_list = bb_mavg.tolist()
    new_mavg_list = [x for x in mavg_list if math.isnan(x) == False]

    lband_list = bb_lband.tolist()
    new_lband_list = [x for x in lband_list if math.isnan(x) == False]

    # animate = FuncAnimation(fig=plot_bb, func=, frames=1000)
    # print(animate)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'To understand Bollinger Bands, it is essential to know what Simple Moving Average (SMA) is. Simple Moving Average is the average price of a stock given a specified period of time. Bollinger Bands are trend lines plotted above and below the SMA of the given stock at a specific standard deviation level. To understand Bollinger Bands better, have a look at the above chart that represents the Bollinger Bands of the BTCUSD stock calculated with SMA 20.'
    info2 = 'Bollinger Bands are great to observe the volatility of a given stock over a period of time. The volatility of a stock is observed to be lower when the space or distance between the upper and lower band is less. Similarly, when the space or distance between the upper and lower band is more, the stock has a higher level of volatility.'

    context = {'title': 'Bollinger Bands (BBANDS)',
               'plot': plot_bb,
               'info': info,
               'info2': info2,

               'candle_data': history(interval, start_time),

               'time': time,
               'hband': new_hband_list,
               'mavg': new_mavg_list,
               'lband': new_lband_list,
               'buy_price': buy_price,
               'sell_price': sell_price,
               'buy_price_x': buy_price_x,
               'sell_price_x': sell_price_x,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def rsi(request):
    API_KEY = 'yourbinanceapikey'
    API_SECRET = 'yourbinanceapisecret'

    client = Client(API_KEY, API_SECRET)

    if request.method == 'POST':
        interval = request.POST.get('interval')
        print(interval)
        start_time = int(request.POST.get('starting_time'))
    else:
        interval = client.KLINE_INTERVAL_1MINUTE
        start_time = 48



    plot_rsi, rsi_accuracy, rsi_signal, rsi_plot, rsi_buy_x, rsi_sell_x = plt.plot_rsi(df)

    time = df["time"].tolist()

    rsi_list = rsi_plot.tolist()
    new_rsi_list = [x for x in rsi_list if math.isnan(x) == False]



    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'Founded and developed by J. Welles Wilder in 1978, the Relative Strength Index shortly known as RSI is a momentum oscillator that is used by traders to identify whether the market is in the state of overbought or oversold. Being an oscillator, the values of RSI bound between 0 to 100. The traditional way to evaluate a market state using the Relative Strength Index is that an RSI reading of 70 or above reveals a state of overbought, and similarly, an RSI reading of 30 or below represents the market is in the state of oversold. The standard setting of RSI is 14 as the lookback period. RSI might sound more similar to Stochastic Oscillator in terms of value interpretation but the way it\'s being calculated is quite different.'
    info2 = ''

    context = {'title': 'Relative Strength Index (RSI)',
               'plot': plot_rsi,
               'info': info,
               # 'info2': info2,

               'candle_data': history(interval, start_time),

               'time': time,
               'rsi': new_rsi_list,
               'buy_price_x': rsi_buy_x,
               'sell_price_x': rsi_sell_x,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def supertrend(request):
    plot_supertrend, supertrend_accuracy, supertrend_signal = plt.plot_supertrend(df)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'Supertrend is a trend-following indicator and this can be observed in the chart that the indicator directly reveals the current trend of the market more accurately. To understand the SuperTrend indicator, it is essential to know what the Average True Range (ATR) is as it is involved in the calculation of the SuperTrend indicator.'
    info2 = 'The Average True Range is a technical indicator that measures how much an asset moves on an average. It is a lagging indicator meaning that it takes into account the historical data of an asset to measure the current value but it’s not capable of predicting the future data points. This is not considered as a drawback while using ATR as it’s one of the indicators to track the volatility of a market more accurately. Along with being a lagging indicator, ATR is also a non-directional indicator meaning that the movement of ATR is inversely proportional to the actual movement of the market. While using ATR as an indicator for trading purposes, traders must ensure that they are cautious than ever as the indicator is very lagging.'
    info3 = 'As the name suggests, the SuperTrend indicator tracks the direction of a trending market. This indicator is well-known for its precision in spotting efficient buy and sell signals for trades. The line of the SuperTrend indicator turns green if the readings of the indicator are below the closing price and turns red if it’s above the closing price. Traders use the color changes or trend changes observed in the SuperTrend indicator line to mark buy and sell signals for their trades. To be more elaborate, traders go long (buy the stock) if the indicator’s line crosses from above to below the closing price line, and similarly, they go short (sell the stock) if the indicator’s line crosses from below to above the closing price line. This SuperTrend strategy is called the crossover strategy.'

    context = {'title': 'Supertrend',
               'plot': plot_supertrend,
               'info': info,
               'info2': info2,
               'info3': info3,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def macd(request):
    plot_macd, macd_accuracy, macd_signal = plt.plot_macd(df)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'To understand MACD, it is essential to know what Exponential Moving Average (EMA) means. EMA is a type of Moving Average (MA) that automatically allocates greater weighting (importance) to the most recent data point and lesser weighting to data points in the distant past.'
    info2 = 'MACD is a trend-following leading indicator that is calculated by subtracting two Exponential Moving Averages (one with longer and the other shorter periods). There are three notable components in a MACD indicator: MACD line, signal line and histogram.'
    info3 = 'MACD Line: This line is the difference between two given Exponential Moving Averages. To calculate the MACD line, one EMA with a longer period known as slow length and another EMA with a shorter period known as fast length is calculated. The most popular length of the fast and slow is 12, 26 respectively. The final MACD line values can be arrived at by subtracting the slow length EMA from the fast length EMA.'
    info4 = 'Signal Line: This line is the Exponential Moving Average of the MACD line itself for a given period of time. The most popular period to calculate the Signal line is 9. As we are averaging out the MACD line itself, the Signal line will be smoother than the MACD line.'
    info5 = 'Histogram: As the name suggests, it is a histogram purposely plotted to reveal the difference between the MACD line and the Signal line. It is a great component to be used to identify trends.'

    context = {'title': 'Moving Average Convergence/Divergence (MACD)',
               'plot': plot_macd,
               'info': info,
               'info2': info2,
               'info3': info3,
               'info4': info4,
               'info5': info5,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def williams_r_percentage(request):
    plot_williams_r, williams_r_accuracy, williams_r_signal = plt.plot_williams_r_percentage(df)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'Founded by Larry Williams, the Williams %R is a momentum indicator whose values oscillate between 0 to -100. This indicator is most similar to the Stochastic Oscillator but differs in its calculation. Traders use this indicator to spot potential entry and exit points for trades by constructing two levels of overbought and oversold. The traditional threshold for overbought and oversold levels are 20 and 80 respectively but there aren\'t any prohibitions in taking other values too.'
    info2 = 'The underlying idea of this indicator is that the stock will keep reaching new highs when it is a strong uptrend and similarly, the stock will reach new lows when it follows a sturdy downtrend.'

    context = {'title': 'Williams %R',
               'plot': plot_williams_r,
               'info': info,
               'info2': info2,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def sma(request):
    plot_sma, sma_accuracy, sma_signal = plt.plot_sma(df)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'Simple Moving Average (SMA) is the average price of a specified period of time. It is a technical indicator and widely used in creating trading strategies. Usually, two SMAs are calculated to build a trading strategy, one with a short period of time and the other with longer than the first one.'

    context = {'title': 'Simple Moving Averages (SMA)',
               'plot': plot_sma,
               'info': info,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def stochastic(request):
    plot_stoch, stoch_accuracy, stoch_signal = plt.plot_stochastic(df)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'Stochastic Oscillator is a momentum-based leading indicator that is widely used to identify whether the market is in the state of overbought or oversold.'
    info2 = 'The values of the Stochastic Oscillator always lie between 0 to 100 due to its normalization function. The general overbought and oversold levels are considered as 80 and 20 respectively but it could vary from one person to another. The Stochastic Oscillator comprises two main components: %K line and %D line.'
    info3 = '%K Line: This line is the most important and core component of the Stochastic Oscillator indicator. It is also known as the Fast Stochastic indicator. The sole purpose of this line is to express the current state of the market (overbought or oversold).'
    info4 = '%D Line: Also known as the Slow Stochastic Indicator, is the moving average of the %K line for a specified period. It is also known as the smooth version of the %K line as the line graph of the %D line will look smoother than the %K line. The standard setting of the %D line is 3 as the number of periods.'

    context = {'title': 'Stochastic Oscillator',
               'plot': plot_stoch,
               'info': info,
               'info2': info2,
               'info3': info3,
               'info4': info4,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def cci(request):
    plot_cci, cci_accuracy, cci_signal = plt.plot_cci(df)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'The CCI is a leading indicator that measures the difference between the current price and the historical average price over a specified period of time, i.e. when the value of CCI reveals extreme positive readings, then it is considered that the current price is well above the historical average. Likewise, when the value of CCI reveals extreme negative readings, then it is considered that the current price is below the historical average. It can be used to trade in any form of market let it be equity or forex. The most general setting of CCI is 20 as the specified number of period.'
    info2 = 'This indicator is unique from the rest of the leading indicators as many of the leading ones have values bound between 0 to 100 but CCI can reach extreme values acting as an unbounded oscillator. Since CCI has indefinite values, traders determine the overbought and oversold levels for individual assets by looking for extreme points of CCI where the price is reversed. This way of determining overbought and oversold levels is called a Reversal Strategy.'

    context = {'title': 'Commodity Channel Index (CCI)',
               'plot': plot_cci,
               'info': info,
               'info2': info2,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def adx(request):
    plot_adx, adx_accuracy, adx_signal = plt.plot_adx(df)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'To understand ADX, it is essential to know what the Average True Range (ATR) is as it is involved in the calculation of the Average Directional Index (ADX).'
    info2 = 'The Average True Range is a technical indicator that measures how much an asset moves on an average. It is a lagging indicator meaning that it takes into account the historical data of an asset to measure the current value but it’s not capable of predicting the future data points. This is not considered as a drawback while using ATR as it’s one of the indicators to track the volatility of a market more accurately. Along with being a lagging indicator, ATR is also a non-directional indicator meaning that the movement of ATR is inversely proportional to the actual movement of the market. While using ATR as an indicator for trading purposes, traders must ensure that they are cautious than ever as the indicator is very lagging.'
    info3 = 'ADX is a technical indicator that is widely used in measuring the strength of the market trend. Now, the ADX doesn’t measure the direction of the trend, whether it’s bullish or bearish, but just represents how strong the trend is. So, to identify the direction of the trend, ADX is combined with a Positive Directional Index (+ DI) and a Negative Directional Index (- DI). As the name suggests, the + DI measures the bullish or positive trend of the market, similarly, the - DI measures the bearish or negative trend of the market. The values of all the components are bound between 0 to 100, hence acting as an oscillator. The traditional setting of ADX is 14 as the lookback period. To calculate the values of ADX with 14 as the lookback period, first, the Positive (+ DM) and Negative Directional Movement (- DM) is determined.'

    context = {'title': 'Average Directional Index (ADX)',
               'plot': plot_adx,
               'info': info,
               'info2': info2,
               'info3': info3,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def aroon(request):
    plot_aroon, aroon_accuracy, aroon_signal = plt.plot_aroon(df)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'Founded by Tushar Chande in 1995, the Aroon indicator is a momentum oscillator that is specifically designed to track a market’s trend or market volatility and how strong the trend is. This indicator is widely used by traders to identify a new trend in the market and make potential entry and exit points accordingly. Being an oscillator, the values of the Aroon indicator bound between 0 to 100.'
    info2 = 'The Aroon indicator is composed of two components: The Aroon up line and the Aroon down line. The Aroon up line measures the strength of the uptrend in a market and similarly, the Aroon down line measures the strength of the downtrend in a market. The traditional setting for the Aroon indicator is either 14 for short-term or 25 for long-term as the lookback period.'
    info3 = 'The main concept of the Aroon indicator is that the market tends to attain more new highs during a strong uptrend, and similarly, the market is bound to reach more new lows during a sturdy downtrend.'

    context = {'title': 'Aroon Indicator',
               'plot': plot_aroon,
               'info': info,
               'info2': info2,
               'info3': info3,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def kc(request):
    plot_kc, kc_accuracy, kc_signal = plt.plot_kc(df)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'To understand Keltner Channel, it is essential to know what the Average True Range (ATR) is since it is involved in the calculation of the Keltner Channel.'
    info2 = 'Founded by Wilder Wiles (creator of the most popular indicator, the RSI), the Average True Range is a technical indicator that measures how much an asset moves on an average. It is a lagging indicator meaning that it takes into account the historical data of an asset to measure the current value but it’s not capable of predicting the future data points. This is not considered as a drawback while using ATR as it’s one of the indicators to track the volatility of a market more accurately. Along with being a lagging indicator, ATR is also a non-directional indicator meaning that the movement of ATR is inversely proportional to the actual movement of the market. While using ATR as an indicator for trading purposes, traders must ensure that they are cautious than ever as the indicator is very lagging.'
    info3 = 'Founded by Chester Keltner, the Keltner Channel is a technical indicator that is often used by traders to identify volatility and the direction of the market. The Keltner Channel is composed of three components: The upper band, the lower band, and the middle line.'
    info4 = 'The middle line of the Keltner Channel is the 20-day Exponential Moving Average of the closing price of the stock. The upper band is calculated by first adding the 20-day Exponential Moving Average of the closing price of the stock by the multiplier (two) and then, multiplied by the 10-day ATR. The lower band calculation is almost similar to that of the upper band but instead of adding, we will be subtracting the 20-day EMA by the multiplier.'
    info5 = 'The Keltner Channel can be used in an extensive number of ways but the most popular usages are identifying the market volatility and direction. The volatility of the market can be determined by the space that exists between the upper and lower band. If the space between the bands is wider, then the market is said to be volatile or showing greater price movements. On the other hand, the market is considered to be in a state of non-volatile or consolidating if the space between the bands is narrow. The other popular usage is identifying the market direction. The market direction can be determined by following the direction of the middle line as well as the upper and lower band.'
    info6 = 'While seeing the chart of the Keltner Channel, it might resemble the Bollinger Bands. The only difference between these two indicators is the way each of them is being calculated. The Bollinger Bands use standard deviation for its calculation, whereas, the Keltner Channel utilizes ATR to calculate its readings.'

    context = {'title': 'Keltner Channel',
               'plot': plot_kc,
               'info': info,
               'info2': info2,
               'info3': info3,
               'info4': info4,
               'info5': info5,
               'info6': info6,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def tsi(request):
    plot_tsi, tsi_accuracy, tsi_signal = plt.plot_tsi(df)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'The True Strength Index (TSI) is a momentum oscillator that is primarily used by traders to determine whether a market is an upward or a downward momentum and trade along with it. It is also used to identify the current state of the market, overbought or oversold but, this is not the indicator’s main forte. The True Strength Index is composed of two components: TSI line and signal line.'
    info2 = 'TSI Line: The first component is the TSI line itself which is calculated by first determining the actual price change (current closing price minus the previous closing price) and the absolute price change (absolute values of the actual price change) and then multiplied by 100.'
    info3 = 'Signal line: The next component is the Signal line component which is an Exponential Moving Average of the TSI for a specified number of periods (falls within 7 to 12 periods).'
    info4 = 'TSI is primarily used to spot the momentum of the market and this can be seen clearly in the chart where the readings of the TSI above the positive territory (greater than zero) directly reveals that the market is in upward momentum and below the negative territory reveals a downward momentum in the market.'
    info5 = 'TSI can also be used to determine whether the market is in the state of overbought or oversold. Usually, indicators like RSI have a standard threshold of overbought and oversold levels which is 70 and 30 respectively, and these thresholds are applicable to any tradable asset. Whereas, the levels of overbought and oversold vary from one asset to another while using the True Strength Index, and in our case, we could consider -10 as the oversold level and 10 as the overbought level.'

    context = {'title': 'True Strength Index (TSI)',
               'plot': plot_tsi,
               'info': info,
               'info2': info2,
               'info3': info3,
               'info4': info4,
               'info5': info5,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def ao(request):
    plot_ao, ao_accuracy, ao_signal = plt.plot_ao(df)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'To understand Awesome Oscillator, it is essential to have some knowledge of the Simple Moving Average (SMA). SMA is the average price of a specified period of time.'
    info2 = 'Awesome Oscillator (AO) is a leading technical indicator used to identify a market’s trend or to measure a market’s momentum. The Awesome Oscillator is plotted in the form of a histogram which reveals a green bar when the current bar is higher than the previous bar, similarly, a red bar is revealed when the current bar is lower than the previous bar. Being an oscillator, the values of the Awesome Oscillator fluctuates above and below the zero line.'

    context = {'title': 'Awesome Oscillator',
               'plot': plot_ao,
               'info': info,
               'info2': info2,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def coppock(request):
    plot_coppock, coppock_accuracy, coppock_signal = plt.plot_coppock(df)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'Coppock curve is specifically dedicated to long-term trading purposes. To understand Coppock Curve it is essential to have some knowledge of the Rate Of Change (ROC) and the Weighted Moving Average (WMA).'
    info2 = 'The Rate Of Change indicator is a momentum indicator that is used by traders as an instrument to determine the percentage change in price from the current closing price and the price of a specified number of periods ago. Unlike other momentum indicators like the RSI and CCI, the Rate Of Change indicator is an unbounded oscillator whose values does not bound between certain limits.'
    info3 = 'Next is the WMA. One thing that bothered traders while using Simple Moving Average is that the indicator assigned equal weights to all data points present in a series. Here is where the Weighted Moving Average comes into play. To solve this problem, the WMA assigns greater weight (or greater importance) to the latest or the recent data point and lesser weight to the data points in the past. To determine the WMA for a given series, each value is multiplied by certain weights that are predetermined and the results are summed up.'
    info4 = 'Founded by Edwin Coppock, the Coppock Curve is a long-term momentum indicator that is often used by traders or investors to identify uptrends and downtrends in a market. This indicator is majorly applied on market indices like the S&P 500 to determine buy and sell signals.'
    info5 = 'From the above chart, it can be observed that whenever the readings of the Coppock Curve are above zero, the histogram is plotted in green color, and similarly, whenever the readings are below zero or negative, the histogram turns to red color. Now, using the histogram, we could easily spot the current trend of the market. If the histogram is plotted in green color, it represents that the market is in an uptrend, and if the histogram is plotted in red color, the market is observed to be in a downtrend. The Coppock Curve can also be used to detect ranging and trending markets but it’s not its main forte.'

    context = {'title': 'Coppock Curve',
               'plot': plot_coppock,
               'info': info,
               'info2': info2,
               'info3': info3,
               'info4': info4,
               'info5': info5,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def kst(request):
    plot_kst, kst_accuracy, kst_signal = plt.plot_kst(df)

    symbol = 'BTCUSD'
    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    percentchange = pricedata['priceChangePercent']
    buyers = pricedata['askQty']
    sellers = pricedata['bidQty']

    eth = pricechange(symbol='ETHUSD')
    btc = pricechange(symbol="BTCUSD")
    ltc = pricechange(symbol="LTCUSD")

    info = 'To understand KST indicator, it is essential to know what the Rate Of Change indicator. The Rate Of Change indicator is a momentum indicator that is used by traders as an instrument to determine the percentage change in price from the current closing price and the price of a specified number of periods ago. Unlike other momentum indicators like the RSI and CCI, the Rate Of Change indicator is an unbounded oscillator whose values does not bound between certain limits.'
    info2 = 'If the readings of the ROC indicator are observed to be above the zero line, then the market is considered to reveal a sturdy upward momentum, and similarly, if the values are below the zero line, the market is considered to reveal a strong downward momentum. This is one way of using the ROC indicator and other usages include generating potential buy and sell signals, identifying the market state (overbought or oversold), and detecting divergences.'
    info3 = 'The Know Sure Thing indicator is an unbounded momentum oscillator that is widely used by traders to understand the readings of the ROC indicator feasibly. The KST indicator is based on four different timeframes of smoothed ROC and combines the collective data into one oscillator. The Know Sure Thing indicator is composed of two components: KST line and signal line.'
    info4 = 'KST line: The first component is the KST line itself. To calculate the readings of the KST line, four ROCs with 10, 15, 20, 30 as the ’n’ values respectively determined.'
    info5 = 'Signal line: Now, the second component of the Know Sure Thing indicator is the Signal line component. This component is the smoothed version of the KST line.'

    context = {'title': 'Know Sure Thing',
               'plot': plot_kst,
               'info': info,
               'info2': info2,
               'info3': info3,
               'info4': info4,
               'info5': info5,

               'moredata': moredata,
               'eth': eth,
               'btc': btc,
               'ltc': ltc,
               'percentchange': percentchange,
               'buyers': buyers,
               'sellers': sellers,
               'data': data,
               }
    return render(request, 'indicators/bbands.html', context)


def history(interval, start_n_hours_ago):
    API_KEY = 'jgd9xxpVqENptW4Ggk2y4IlKqkfU3FD7wSLFWjXlcix2thxRnLsJhAo38AwTdYJv'
    API_SECRET = 'LKLHyXmU81wsIt42tWrxpL39bJd86GcJcT25McExZxwIG7kbZFjUOXApdIQHgcJy'

    client = Client(API_KEY, API_SECRET)
    candlesticks = client.get_historical_klines(symbol="BTCUSDT", interval=interval,
                                                start_str=str(datetime.now() - timedelta(hours=start_n_hours_ago)))

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,  # open time
            # "time": datetime.fromtimestamp(data[0] / 1000, tz=tzinfo.tzname("Turkey")).strftime('%Y-%m-%d %H:%M:%S'),  # open time
            # "time": datetime.fromtimestamp(data[0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),  # open time
            "open": int(float(data[1])),
            "high": int(float(data[2])),
            "low": int(float(data[3])),
            "close": int(float(data[4])),
            # "volume": int(float(data[5])),
            # "close time": data[6] / 1000,
            # "quote asset volume": data[7],
            # "number of trades": data[8],
            # "taker buy base asset volume": data[9],
            # "taker buy quote asset volume": data[10],
            # "ignore": data[11],
        }
        processed_candlesticks.append(candlestick)

        # open_time = [int(entry[0]) for entry in candlesticks]
        # open = [float(entry[1]) for entry in candlesticks]
        # high = [float(entry[2]) for entry in candlesticks]
        # low = [float(entry[3]) for entry in candlesticks]
        # close = [float(entry[4]) for entry in candlesticks]
        #
    response = JsonResponse(processed_candlesticks, safe=False, headers={
        'Access-Control-Allow-Origin': 'http://127.0.0.1:8000',
    })
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # response.headers.setdefault(response.headers.keys(), 'Access-Control-Allow-Origin', '*')
    # context = {'candle_data': response,
    #            }
    response_1 = json.loads(response.content)
    return response_1
    # return render(request, 'indicators/crypto.html', context)
