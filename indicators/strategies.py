
def calculate_accuracy(buy_price_x, buy_price, sell_price_x, sell_price):
    # calculate accuracy
    # Al emri vermiş- Bir sonraki emir ne olursa olsun(Al-Sat) al emri verdikten sonraki emire gelene kadar fiyat artmışşsa doğru al emrinden sonraki emire gelene kadar azalmışsa yanlış
    # Sat emri vermiş-Bir sonraki emir ne olursa olsu n(Al-Sat) sat emri verdikten sonraki emire gelene kadar fiyat azalmışsa doğru sat emrinden sonraki emire gelene kadar artmışsa yanlış
    accurate_guess = 0
    price_dict = dict(zip(buy_price_x, buy_price))
    price_dict.update(dict(zip(sell_price_x, sell_price)))
    print(price_dict)
    price_dict = dict(sorted(price_dict.items(), key=lambda x: x[0], reverse=False))
    print(price_dict)
    for i in range(len(price_dict) - 1):
        if list(price_dict.values())[i] in buy_price and list(price_dict.values())[i] < list(price_dict.values())[
            i + 1]:
            accurate_guess += 1
        elif list(price_dict.values())[i] in sell_price and list(price_dict.values())[i] > list(price_dict.values())[
            i + 1]:
            accurate_guess += 1

    if (len(price_dict) - 1 > 0):
        accuracy = accurate_guess / (len(price_dict) - 1)
        f_accuracy = "{:.2f}".format(accuracy)
        return f_accuracy
    else:
        print("There is not enough trading order to calculate the accuracy of the indicator"
              " for the given time interval and starting time!")
        return 0


def get_signal(df, buy_price_x, sell_price_x):
    signal = 'Do Nothing'  # or we can say 'Keep' as the default signal
    if len(buy_price_x) > 0 and len(sell_price_x) > 0:
        if buy_price_x[-1] == df.shape[0] - 1:
            signal = 'Buy'
        elif sell_price_x[-1] == df.shape[0] - 1:
            signal = 'Sell'
    return signal


def implement_bb_strategy(data, lower_bb, upper_bb):
    buy_price = []
    sell_price = []
    bb_signal = []

    buy_price_x = []
    sell_price_x = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    for i in range(1, len(data)):
        if data[i - 1] > lower_bb[i - 1] and data[i] < lower_bb[i]:
            if signal != 1:
                buy_price_x.append(i)
                buy_price.append(data[i])
                # sell_price.append(np.nan)
                signal = 1
                buy_signal += 1
                bb_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                bb_signal.append(0)
        elif data[i - 1] < upper_bb[i - 1] and data[i] > upper_bb[i]:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price_x.append(i)
                sell_price.append(data[i])
                signal = -1
                sell_signal += 1
                bb_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                bb_signal.append(0)
        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            bb_signal.append(0)

    return buy_price, buy_signal, sell_price, sell_signal, bb_signal, buy_price_x, sell_price_x


def implement_rsi_strategy(prices, rsi):
    buy_price = []
    sell_price = []
    rsi_signal = []

    rsi_buy_x = []
    rsi_buy_y = []
    rsi_sell_x = []
    rsi_sell_y = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    for i in range(1, len(rsi)):
        if rsi[i - 1] > 30 and rsi[i] < 30:
            if signal != 1:
                buy_price.append(prices[i])
                # sell_price.append(np.nan)
                rsi_buy_x.append(i)
                rsi_buy_y.append(rsi[i])


                signal = 1
                buy_signal += 1
                rsi_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                rsi_signal.append(0)
        elif rsi[i - 1] < 70 and rsi[i] > 70:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price.append(prices[i])

                rsi_sell_x.append(i)
                rsi_sell_y.append(rsi[i])

                signal = -1
                sell_signal += 1
                rsi_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                rsi_signal.append(0)
        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            rsi_signal.append(0)

    return buy_price, buy_signal, sell_price, sell_signal, rsi_signal, rsi_buy_x, rsi_buy_y, rsi_sell_x, rsi_sell_y


def implement_st_strategy(prices, st):
    buy_price = []
    sell_price = []
    st_signal = []

    buy_price_x = []
    sell_price_x = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    for i in range(1, len(st)):
        if st[i - 1] > prices[i - 1] and st[i] < prices[i]:
            if signal != 1:
                buy_price.append(prices[i])
                # sell_price.append(np.nan)
                buy_price_x.append(i)
                signal = 1
                buy_signal += 1
                st_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                st_signal.append(0)
        elif st[i - 1] < prices[i - 1] and st[i] > prices[i]:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price.append(prices[i])
                sell_price_x.append(i)

                signal = -1
                sell_signal += 1
                st_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                st_signal.append(0)
        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            st_signal.append(0)

    return buy_price, buy_signal, sell_price, sell_signal, st_signal, buy_price_x, sell_price_x


def implement_macd_strategy(prices, data):
    buy_price = []
    sell_price = []
    macd_signal = []

    macd_buy_x = []
    macd_buy_y = []
    macd_sell_x = []
    macd_sell_y = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    for i in range(1, len(data)):
        if data['macd'][i] > data['signal'][i]:
            if signal != 1:
                buy_price.append(prices[i])
                # sell_price.append(np.nan)

                macd_buy_x.append(i)
                macd_buy_y.append(data['signal'][i])

                signal = 1
                buy_signal += 1
                macd_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                macd_signal.append(0)
        elif data['macd'][i] < data['signal'][i]:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price.append(prices[i])

                macd_sell_x.append(i)
                macd_sell_y.append(data['signal'][i])

                signal = -1
                sell_signal += 1
                macd_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                macd_signal.append(0)
        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            macd_signal.append(0)

    return buy_price, buy_signal, sell_price, sell_signal, macd_signal, macd_buy_x, macd_buy_y, macd_sell_x, macd_sell_y


def implement_wr_strategy(prices, wr):
    buy_price = []
    sell_price = []
    wr_signal = []

    williams_r_buy_x = []
    williams_r_buy_y = []
    williams_r_sell_x = []
    williams_r_sell_y = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    for i in range(1, len(wr)):
        if wr[i - 1] > -80 and wr[i] < -80:
            if signal != 1:
                buy_price.append(prices[i])
                # sell_price.append(np.nan)

                williams_r_buy_x.append(i)
                williams_r_buy_y.append(wr[i])

                signal = 1
                buy_signal += 1
                wr_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                wr_signal.append(0)
        elif wr[i - 1] < -20 and wr[i] > -20:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price.append(prices[i])

                williams_r_sell_x.append(i)
                williams_r_sell_y.append(wr[i])

                signal = -1
                sell_signal += 1
                wr_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                wr_signal.append(0)
        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            wr_signal.append(0)

    return buy_price, buy_signal, sell_price, sell_signal, wr_signal, williams_r_buy_x, williams_r_buy_y, williams_r_sell_x, williams_r_sell_y


def implement_sma_strategy(data, short_window, long_window):
    sma1 = short_window
    sma2 = long_window
    buy_price = []
    sell_price = []
    sma_signal = []

    buy_price_x = []
    sell_price_x = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    for i in range(len(data)):
    # for i in range(len(data)-1):
    #     if sma1[i] > sma2[i] and sma1[i+1] < sma2[i+1]:
        if sma1[i] > sma2[i]:
            if signal != 1:
                buy_price.append(data[i])
                # sell_price.append(np.nan)
                buy_price_x.append(i)

                buy_signal += 1

                signal = 1
                sma_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                sma_signal.append(0)
        # elif sma2[i] > sma1[i] and sma2[i+1] < sma1[i+1]:
        elif sma2[i] > sma1[i]:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price.append(data[i])
                sell_price_x.append(i)

                sell_signal += 1

                signal = -1
                sma_signal.append(-1)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                sma_signal.append(0)
        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            sma_signal.append(0)

    return buy_price, buy_signal, sell_price, sell_signal, sma_signal, buy_price_x, sell_price_x
    # return pd.Series([buy_price, buy_signal, sell_price, sell_signal, sma_signal])


def implement_stochastic_strategy(prices, k, d):
    buy_price = []
    sell_price = []
    stoch_signal = []

    buy_price_x = []
    sell_price_x = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    for i in range(len(prices)):
        if k[i] < 20 and d[i] < 20 and k[i] < d[i]:
            if signal != 1:
                buy_price.append(prices[i])
                # sell_price.append(np.nan)
                buy_price_x.append(i)
                buy_signal += 1

                signal = 1
                stoch_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                stoch_signal.append(0)
        elif k[i] > 80 and d[i] > 80 and k[i] > d[i]:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price.append(prices[i])

                sell_price_x.append(i)
                sell_signal += 1

                signal = -1
                stoch_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                stoch_signal.append(0)
        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            stoch_signal.append(0)

    return buy_price, buy_signal, sell_price, sell_signal, stoch_signal, buy_price_x, sell_price_x


def implement_cci_strategy(prices, cci):
    buy_price = []
    sell_price = []
    cci_signal = []

    buy_price_x = []
    sell_price_x = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    lower_band = (-150)
    upper_band = 150

    for i in range(1, len(prices)):
        if cci[i - 1] > lower_band and cci[i] < lower_band:
            if signal != 1:
                buy_price.append(prices[i])
                # sell_price.append(np.nan)

                buy_price_x.append(i)
                buy_signal += 1

                signal = 1
                cci_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                cci_signal.append(0)

        elif cci[i - 1] < upper_band and cci[i] > upper_band:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price.append(prices[i])

                sell_price_x.append(i)
                sell_signal += 1

                signal = -1
                cci_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                cci_signal.append(0)

        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            cci_signal.append(0)

    return buy_price, buy_signal, sell_price, sell_signal, cci_signal, buy_price_x, sell_price_x


def implement_adx_strategy(prices, pdi, ndi, adx):
    buy_price = []
    sell_price = []
    adx_signal = []

    buy_price_x = []
    sell_price_x = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    for i in range(1, len(prices)):
        if adx[i - 1] < 25 and adx[i] > 25 and pdi[i] > ndi[i]:
            if signal != 1:
                buy_price.append(prices[i])
                # sell_price.append(np.nan)

                buy_price_x.append(i)
                buy_signal += 1

                signal = 1
                adx_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                adx_signal.append(0)
        elif adx[i - 1] < 25 and adx[i] > 25 and ndi[i] > pdi[i]:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price.append(prices[i])

                sell_price_x.append(i)
                sell_signal += 1

                signal = -1
                adx_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                adx_signal.append(0)
        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            adx_signal.append(0)

    return buy_price, buy_signal, sell_price, sell_signal, adx_signal, buy_price_x, sell_price_x


def implement_aroon_strategy(prices, up, down):
    buy_price = []
    sell_price = []
    aroon_signal = []

    buy_price_x = []
    sell_price_x = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    for i in range(len(prices)):
        if up[i] >= 70 and down[i] <= 30:
            if signal != 1:
                buy_price.append(prices[i])
                # sell_price.append(np.nan)

                buy_price_x.append(i)
                buy_signal += 1

                signal = 1
                aroon_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                aroon_signal.append(0)
        elif up[i] <= 30 and down[i] >= 70:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price.append(prices[i])

                sell_price_x.append(i)
                sell_signal += 1

                signal = -1
                aroon_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                aroon_signal.append(0)
        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            aroon_signal.append(0)

    return buy_price, buy_signal, sell_price, sell_signal, aroon_signal, buy_price_x, sell_price_x


def implement_kc_strategy(prices, kc_upper, kc_lower):
    buy_price = []
    sell_price = []
    kc_signal = []

    buy_price_x = []
    sell_price_x = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    for i in range(len(prices)-1):
        if prices[i] < kc_lower[i] and prices[i + 1] > prices[i]:
            if signal != 1:
                buy_price.append(prices[i])
                # sell_price.append(np.nan)

                buy_price_x.append(i)
                buy_signal += 1

                signal = 1
                kc_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                kc_signal.append(0)
        elif prices[i] > kc_upper[i] and prices[i + 1] < prices[i]:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price.append(prices[i])

                sell_price_x.append(i)
                sell_signal += 1

                signal = -1
                kc_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                kc_signal.append(0)
        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            kc_signal.append(0)

    return buy_price, buy_signal, sell_price, sell_signal, kc_signal, buy_price_x, sell_price_x


def implement_tsi_strategy(prices, tsi, signal_line):
    buy_price = []
    sell_price = []
    tsi_signal = []

    buy_price_x = []
    sell_price_x = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    for i in range(1, len(prices)):
        if tsi[i - 1] < signal_line[i - 1] and tsi[i] > signal_line[i]:
            if signal != 1:
                buy_price.append(prices[i])
                # sell_price.append(np.nan)

                buy_price_x.append(i)
                buy_signal += 1

                signal = 1
                tsi_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                tsi_signal.append(0)
        elif tsi[i - 1] > signal_line[i - 1] and tsi[i] < signal_line[i]:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price.append(prices[i])

                sell_price_x.append(i)
                sell_signal += 1

                signal = -1
                tsi_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                tsi_signal.append(0)
        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            tsi_signal.append(0)

    return buy_price, buy_signal, sell_price, sell_signal, tsi_signal, buy_price_x, sell_price_x


def implement_ao_crossover(price, ao):
    buy_price = []
    sell_price = []
    ao_signal = []

    buy_price_x = []
    sell_price_x = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    for i in range(1, len(ao)):
        if ao[i] > 0 and ao[i - 1] < 0:
            if signal != 1:
                buy_price.append(price[i])
                # sell_price.append(np.nan)

                buy_price_x.append(i)
                buy_signal += 1

                signal = 1
                ao_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                ao_signal.append(0)
        elif ao[i] < 0 and ao[i - 1] > 0:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price.append(price[i])

                sell_price_x.append(i)
                sell_signal += 1

                signal = -1
                ao_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                ao_signal.append(0)
        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            ao_signal.append(0)
    return buy_price, buy_signal, sell_price, sell_signal, ao_signal, buy_price_x, sell_price_x


def implement_cc_strategy(prices, cc):
    buy_price = []
    sell_price = []
    cc_signal = []

    buy_price_x = []
    sell_price_x = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    for i in range(4, len(prices)):
        if cc[i - 4] < 0 and cc[i - 3] < 0 and cc[i - 2] < 0 and cc[i - 1] < 0 and cc[i] > 0:
            if signal != 1:
                buy_price.append(prices[i])
                # sell_price.append(np.nan)

                buy_price_x.append(i)
                buy_signal += 1

                signal = 1
                cc_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                cc_signal.append(0)
        elif cc[i - 4] > 0 and cc[i - 3] > 0 and cc[i - 2] > 0 and cc[i - 1] > 0 and cc[i] < 0:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price.append(prices[i])

                sell_price_x.append(i)
                sell_signal += 1

                signal = -1
                cc_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                cc_signal.append(0)
        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            cc_signal.append(0)

    return buy_price, buy_signal, sell_price, sell_signal, cc_signal, buy_price_x, sell_price_x


def implement_kst_strategy(prices, kst_line, signal_line):
    buy_price = []
    sell_price = []
    kst_signal = []

    buy_price_x = []
    sell_price_x = []

    buy_signal = 0
    sell_signal = 0

    signal = 0

    for i in range(1, len(kst_line)):

        if kst_line[i - 1] < signal_line[i - 1] and kst_line[i] > signal_line[i]:
            if signal != 1:
                buy_price.append(prices[i])
                # sell_price.append(np.nan)

                buy_price_x.append(i)
                buy_signal += 1

                signal = 1
                kst_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                kst_signal.append(0)

        elif kst_line[i - 1] > signal_line[i - 1] and kst_line[i] < signal_line[i]:
            if signal != -1:
                # buy_price.append(np.nan)
                sell_price.append(prices[i])

                sell_price_x.append(i)
                sell_signal += 1

                signal = -1
                kst_signal.append(signal)
            else:
                # buy_price.append(np.nan)
                # sell_price.append(np.nan)
                kst_signal.append(0)

        else:
            # buy_price.append(np.nan)
            # sell_price.append(np.nan)
            kst_signal.append(0)

    return buy_price, buy_signal, sell_price, sell_signal, kst_signal, buy_price_x, sell_price_x
