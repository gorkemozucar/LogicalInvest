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
    plot_rsi, rsi_accuracy, rsi_signal = plt.plot_rsi(df)
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

    context = {'title': 'Bollinger Bands (BBANDS)',
               'plot': plot_bb,

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
    plot_rsi, rsi_accuracy, rsi_signal = plt.plot_rsi(df)

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

    context = {'title': 'Relative Strength Index (RSI)',
               'plot': plot_rsi,

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

    context = {'title': 'Supertrend',
               'plot': plot_supertrend,

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

    context = {'title': 'Moving Average Convergence/Divergence (MACD)',
               'plot': plot_macd,

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

    context = {'title': 'Williams %R',
               'plot': plot_williams_r,

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

    context = {'title': 'Simple Moving Averages (SMA)',
               'plot': plot_sma,

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

    context = {'title': 'Stochastic Oscillator',
               'plot': plot_stoch,

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

    context = {'title': 'Commodity Channel Index (CCI)',
               'plot': plot_cci,

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

    context = {'title': 'Average Directional Index (ADX)',
               'plot': plot_adx,

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

    context = {'title': 'Aroon Indicator',
               'plot': plot_aroon,

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

    context = {'title': 'Keltner Channel',
               'plot': plot_kc,

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

    context = {'title': 'True Strength Index (TSI)',
               'plot': plot_tsi,

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

    context = {'title': 'Awesome Oscillator',
               'plot': plot_ao,

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

    context = {'title': 'Coppock Curve',
               'plot': plot_coppock,

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

    context = {'title': 'Know Sure Thing',
               'plot': plot_kst,

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
