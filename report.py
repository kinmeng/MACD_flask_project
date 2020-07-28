import requests
import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
from datetime import datetime, timedelta, date
import talib
import time
import csv
import math

def get_data(stock_symbols):
    ##online
    pd.set_option('display.max_rows', 40000)
    yf.pdr_override() 
    end_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    start_date = datetime.strftime(datetime.now() - timedelta(days = 200), '%Y-%m-%d')
    df = pdr.get_data_yahoo(stock_symbols, start_date, end_date, threads=True)
    # df.to_pickle('two_stocks.pkl')
    ##offline
    # df = pd.read_pickle('two_stocks.pkl')
    # print(df.columns)
    return df

#deal breaker based on past data and limited future data
def breaker(date, macdhist_df, macd, macd_df, stock_symbol, check):
    #true is what u want
    #false breaks the appending of the date for u
    #check is what u want if u want to check all positive put p
   
    pre_days = (date - timedelta(5)).strftime('%Y-%m-%d')
    pre_days_alt = (date - timedelta(7)).strftime('%Y-%m-%d')
    intersect = (date-timedelta(1)).strftime('%Y-%m-%d')
    x = macd_df.get(key=pre_days)
    y = macd_df.get(key=pre_days_alt)
    # print("type----------------------------------------", type(macd_df[date:pre_days_alt]), macd_df[pre_days:date].max())
    # print(" what is x y ", x,y)
    # print("macd period-------------------------------------------------",macd_df[pre_days:date])
    macdhist_breaker = True
    macd_breaker = True
    breaker = True
    #buy_signal
    if check == 'p':
    
    
        for h in macdhist_df[pre_days:intersect]:
            if math.isnan(h) == True:
                continue
            elif h > 0:
                breaker = False
                # print(date, " broke cuz of positive")
        if x != None:    
            current_macdperiod_min = macd_df[pre_days:date].min()
            # print("min", current_macdperiod_min)
            if (((macd - current_macdperiod_min)/abs(current_macdperiod_min))* 100) < 12:  
                # print((((macd - current_macdperiod_min)/abs(current_macdperiod_min))* 100))
                breaker = False
                # print(date, " broke cuz of macd buy x")
        elif y != None:
            current_macdperiod_min = macd_df[pre_days_alt:date].min()
            # print("min", current_macdperiod_min)
            if (((macd - current_macdperiod_min)/abs(current_macdperiod_min))* 100) < 12:
                # print((((macd - current_macdperiod_min)/abs(current_macdperiod_min))* 100))
                breaker = False
                # print(date, " broke cuz of macd buy y")
        # if macd_breaker == False and macdhist_breaker == False:
        #     breaker = False
        # else:
        #     breaker = True
    #sell_signal
    elif check == 'n':

     
        for h in macdhist_df[pre_days:intersect]:
            if math.isnan(h) == True:
                continue
            elif h < 0:
                breaker = False
                # print(date, " broke cuz of negative")
        if x != None: 
            current_macdperiod_max = macd_df[pre_days:date].max()
            # print("max", current_macdperiod_max)
            if (((macd-current_macdperiod_max)/abs(current_macdperiod_max))* 100) > -12:
                breaker = False
                # print(date, " broke cuz of macd sell x")
                # print((((macd-current_macdperiod_max)/abs(current_macdperiod_max))* 100))
        elif y != None:
            current_macdperiod_max = macd_df[pre_days_alt:date].max()
            # print("max", current_macdperiod_max)
            if (((macd-current_macdperiod_max)/abs(current_macdperiod_max))* 100) > -12:
                breaker = False
                # print(date, " broke cuz of macd sell y")
                # print(((macd-current_macdperiod_max)/abs(current_macdperiod_max))*100)
        # if macd_breaker == False and macdhist_breaker == False:
        #     breaker = False
        # else:
        #     breaker = True

    return breaker

def pastmacdhist(moving_list_macdhist, indicate):
    #indicate is what u want for the past 10 datapts
    #buy signals should all be negative
    #sell signals should all be positive
    # true is what u want
    answer =  True
 
    if indicate == 'p':
        for i in moving_list_macdhist:
            if i < 0:
                answer = False
  
  

    elif indicate == 'n':
        for i in moving_list_macdhist:
            if i > 0:
                answer= False
    
    return answer


def date_intersection(macdsignal_df, macd_df, macdhist_df, date_df, stock_symbol, date_storage):
    
   

    stock_symbol = stock_symbol

    previous_macd = float('nan')
    previous_signal = float('nan')
    previous_macdhist = float('nan')
    
    moving_list_macdhist = []

    for macdsig,macd,macdhist,date in zip(macdsignal_df, macd_df, macdhist_df, date_df):
        # date = date.to_pydatetime()
        # if (datetime.now() - date).days <= 5: 
        # print(macdhist, previous_macdhist, macd, macdsig)
        if (math.isnan(macdsig) == True) or (math.isnan(macd) == True) or (math.isnan(previous_macd)== True) or (math.isnan(previous_signal)==True) or (math.isnan(previous_macdhist)==True):
            pass
        elif (math.isnan(macdsig) == False) and (math.isnan(macd) == False) and (math.isnan(previous_macd)== False) and (math.isnan(previous_signal)==False) and (math.isnan(previous_macdhist) ==False):
            
            if (macdhist> 0 and previous_macdhist<0) or (macdhist<0 and previous_macdhist>0): #intersection occured
                # print(date, " intersection occured ", macdhist, previous_macdhist, pastmacdhist(moving_list_macdhist, indicate='n'), pastmacdhist(moving_list_macdhist, indicate='p'))
                # print(date, macdhist, previous_macdhist, "here", math.isnan(macdsig), "here")
                    #https://www.programiz.com/python-programming/datetime/strftime
            
                # print(macdsig,macd,macdhist,previous_macd, previous_signal, date, pastmacdhist(moving_list_macdhist, indicate='n'), pastmacdhist(moving_list_macdhist, indicate='p'))
                if (previous_macd < previous_signal) and (macd > macdsig):
                    #previous condition if date.date() < datetime.today().date() and ((date.date() + timedelta(5) in macdhist_df) or (date.date() + timedelta(7) in macdhist_df)):
                    # if date.date() < datetime.today().date() and (date.date() + timedelta(3) in macdhist_df):
               
                    if macd < -0.1 and (stock_symbol not in date_storage) and breaker(date, macdhist_df, macd, macd_df, stock_symbol, check='p') == True:
                        # print("accepted as buy")
                        date_storage[stock_symbol] = [(date.strftime('%Y-%m-%d'),'b')]
                    elif macd < -0.1 and (stock_symbol in date_storage) and breaker(date, macdhist_df, macd, macd_df, stock_symbol, check='p') == True:
                        # print("accepted as buy")
                        date_storage[stock_symbol].append((date.strftime('%Y-%m-%d'),'b'))
                    else:
                        # print(breaker(date, macdhist_df, macd, macd_df, stock_symbol, check='p'))
                        # print("pass under buy")
                        pass
      
                
               
                
                elif (previous_macd > previous_signal) and (macd< macdsig):
            
                    # if date.date() < datetime.today().date() and (date.date() + timedelta(3) in macdhist_df):
                        # print('sell signal')
                    if macd > 0.1 and (stock_symbol not in date_storage) and breaker(date, macdhist_df, macd, macd_df, stock_symbol, check='n') == True:
                        date_storage[stock_symbol] = [(date.strftime('%Y-%m-%d'),'s')]
                        # print("accepted as sell")
                    elif macd > 0.1 and (stock_symbol in date_storage) and breaker(date, macdhist_df, macd, macd_df, stock_symbol, check='n') == True:
                        # print("accepted as sell")
                        date_storage[stock_symbol].append((date.strftime('%Y-%m-%d'),'s'))
                    else:
                        pass
           
 
        # if len(moving_list_macdhist) <= 5:
        #     moving_list_macdhist.append(macdhist)
        # else:
        #     moving_list_macdhist.pop(0)
        #     moving_list_macdhist.append(macdhist)


        previous_macd = macd
        previous_signal = macdsig
        previous_macdhist = macdhist
    # print(date_storage)
    return date_storage#outputs the symbol




def williams_r(df,stock_symbol, macdsignal, macd, status, date_reset):
    

    High = df[('High',stock_symbol)]
    Low = df[('Low', stock_symbol)]
    prices = df[('Close', stock_symbol)]
    
    df['willsr'] = talib.WILLR(High, Low, prices,timeperiod= 14)
    pd.set_option('display.max_rows', 40000)


    # print(df['willsr'].head())
    date_reset = date_reset
    for willsr, date, high, low, macdsignal_pt, macd_pt in zip(df['willsr'],date_reset, df[('High',stock_symbol)],df[('Low', stock_symbol)],macdsignal, macd):
        # if willsr == 'NaN':
        #     status.append('no data')
        #     date = date.to_pydatetime()
        #     continue
        # else:
        #     date = date.to_pydatetime()
        
        if willsr > -20:
            # print(date.strftime('%d-%m-%Y'), 'overbought')
            # if (datetime.now() - date).days <= 5:
            
            if stock_symbol not in status:
                status[stock_symbol] = [(date.strftime('%Y-%m-%d'), 'overbought')]
            else:
                status[stock_symbol].append((date.strftime('%Y-%m-%d'), 'overbought'))
        elif willsr < -80:
            # print(date.strftime('%d-%m-%Y'), 'oversold')
            # if (datetime.now() - date).days <= 5:

            if stock_symbol not in status:
                status[stock_symbol] = [(date.strftime('%Y-%m-%d'), 'oversold')]
            else:
                status[stock_symbol].append((date.strftime('%Y-%m-%d'), 'oversold'))
        else:
            continue
    
    return status

def final_tabulation(intersectdict,willsdict, symbol, high_priority, low_priority, no_importance):


    if symbol in intersectdict:
        
        if (symbol in intersectdict) and (symbol in willsdict):
            date_tracker = []
    
            # print("williams%r", willsdict)
            for signals in intersectdict[symbol]:
                current_date = signals[0]   
                current_signal = signals[1]
                before_signal = None
                after_signal = None

                for status in willsdict[symbol]:

                    wills_date = status[0]

                    if datetime.strptime(current_date, '%Y-%m-%d').date() >= (datetime.today()-timedelta(3)).date():
                        # print(current_date, wills_date, abs((datetime.strptime(current_date, '%Y-%m-%d').date() - datetime.strptime(wills_date, '%Y-%m-%d').date()).days)<9)
                        if (datetime.strptime(wills_date, '%Y-%m-%d').date() < datetime.strptime(current_date, '%Y-%m-%d').date()) and (
                            abs((datetime.strptime(current_date, '%Y-%m-%d').date() - datetime.strptime(wills_date, '%Y-%m-%d').date()).days)<9):
                            # print(wills_date, abs((datetime.strptime(current_date, '%Y-%m-%d').date() - datetime.strptime(wills_date, '%Y-%m-%d').date()).days)<9)
                            before_signal = status
                        

                        elif datetime.strptime(wills_date, '%Y-%m-%d').date()  >= datetime.strptime(current_date, '%Y-%m-%d').date() and (
                            abs((datetime.strptime(current_date, '%Y-%m-%d').date()-datetime.strptime(wills_date, '%Y-%m-%d').date()).days)<9):
                                # print(wills_date, abs((datetime.strptime(current_date, '%Y-%m-%d').date() - datetime.strptime(wills_date, '%Y-%m-%d').date()).days)<9)
                                after_signal = status
                        
                        
                        if (type(before_signal) == tuple) or (type(after_signal) == tuple):
                            # print("here")
                            if (type(before_signal) == tuple) and (current_signal == 'b' and before_signal[1] == 'oversold'):
                                # print(symbol, current_date, "i was here")
                    
                                if current_date not in date_tracker:
                                    date_tracker.append(current_date)
                                    
                                    if symbol not in high_priority:
                                
                                        high_priority[symbol] = [(before_signal, current_date)]
                                    else:
                                        high_priority[symbol].append((before_signal, current_date))
                                before_signal = None
                                after_signal = None

                            elif (type(after_signal) == tuple) and (current_signal == 'b' and after_signal[1] == 'oversold'):
                                # print(symbol, current_date, "i was here")
                    
                                if current_date not in date_tracker:
                                    date_tracker.append(current_date)
                                    
                                    if symbol not in high_priority:
                                
                                        high_priority[symbol] = [(after_signal, current_date)]
                                    else:
                                        high_priority[symbol].append((after_signal, current_date))
                                before_signal = None
                                after_signal = None

                            elif (type(before_signal) == tuple) and (current_signal == 's' and before_signal[1] == 'overbought'):
                                # print(symbol, current_date, "i was here", "s")
                    
                                if current_date not in date_tracker:
                                    date_tracker.append(current_date)
                                    if symbol not in high_priority:
                                
                                        high_priority[symbol] = [(before_signal, current_date)]
                                    else:
                                        high_priority[symbol].append((before_signal, current_date))
                                before_signal = None
                                after_signal = None

                            elif (type(after_signal) == tuple) and (current_signal == 's' and after_signal[1] == 'overbought'):
                                # print(symbol, current_date, "i was here", 's')
                    
            
                                if current_date not in date_tracker:
                                    date_tracker.append(current_date)
                                    if symbol not in high_priority:
                                
                                        high_priority[symbol] = [(after_signal, current_date)]
                                    else:
                                        high_priority[symbol].append((after_signal, current_date))
                                before_signal = None
                                after_signal = None
                    
                            else:
                                
                                before_signal = None
                                after_signal = None
                                continue
                    
                
            else:
                low_priority[symbol] = "There was an intersection within last 5 days, but williams%r was normal"

        else:#symbol did not intersect within last 5 days
            if symbol in willsdict: #but the stock was either underbought or oversold
                low_priority[symbol] = willsdict[symbol]
            else: #none of the criteria were fulfilled
                no_importance[symbol] = "none"
            
    # print(high_priority)
    return high_priority, low_priority, no_importance

def process_data(stock_data, stock_symbols):
    df = stock_data
    # df.reset_index(inplace=True)
    # print(df)
    date_storage = {}
    status = {}
    high_priority = {}
    low_priority = {}
    no_importance = {}
    unprocessed = []
  
    for symbol in stock_symbols:
        print(symbol)

        prices = df[('Close', str(symbol))]
        
        if prices.isnull().values.any() == False:
            macd_actual, macdsignal_actual, macdhist_actual  = talib.MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9)
            df[('macdsignal', str(symbol))] = macdsignal_actual
            df[('macd', str(symbol))] = macd_actual
            df[('macdhist', str(symbol))] = macdhist_actual
          
          
            # pd.set_option('display.max_rows', 40000)
            
            #https://stackoverflow.com/questions/40815238/python-pandas-convert-index-to-datetime
            date_reset = pd.to_datetime(df.index)
            # print("date-reset---------------", date_reset)
            # print(df[[('macdsignal', str(symbol)),('macd', str(symbol)), ('macdhist', str(symbol))]])
            # print(type(df[('macdhist', str(symbol))]['2020-02-20':'2020-02-20']))
            # print("filter date-----------------------------------------",df[('macdhist', str(symbol))]['2020-02-20':'2020-02-20'], df.index, df.columns)
            # print(date_reset)
            # print(df['Date'])
          
            intersectdict = date_intersection(df[('macdsignal', str(symbol))], df[('macd', str(symbol))], df[('macdhist', str(symbol))], date_reset, symbol, date_storage)
        
    
            willsdict = williams_r(df, symbol, df[('macdsignal', str(symbol))], df[('macd', str(symbol))], status, date_reset)
    
            # *** in outer function ***
            # store all conditions fulfilled data
            # store intersection data
            # in this function it should only handle data per symbol
            
            high_priority, low_priority, no_importance,  = final_tabulation(intersectdict,willsdict, symbol, high_priority, low_priority, no_importance)
            

        else:
            unprocessed.append(symbol)

    return high_priority, low_priority, no_importance, unprocessed
            


###########for offline testing##################################
# stock_symbols_df = pd.read_csv('./stock_symbols/test_10.csv')
# stock_symbols = stock_symbols_df['Symbol']
# stock_symbols = [str(x).replace('\xa0', '') for x in stock_symbols]
# df = pd.read_pickle('ten.pkl')#tobecommentedout)#tobecommentedout
# high_priority, low_priority, no_importance, unprocessed = process_data(df,stock_symbols)
# print(high_priority, low_priority, no_importance)
###############for offline testing#######################
# stock_symbols = ['AAPL', 'TSLA']
# df = pd.read_pickle('ten.pkl')#tobecommentedout)#tobecommentedout
# df = get_data(stock_symbols)
# high_priority, low_priority, no_importance, unprocessed = process_data(df,stock_symbols)
# print(high_priority, low_priority, no_importance)




#########################onlinetest##############################

# name_stock_file ='nasdaq-2000.csv' #change this
# filename = "report" + '-' + str(date.today()) + '-'+ name_stock_file.split('.')[0] +'.csv'
# stock_symbols_df = pd.read_csv('./stock_symbols/'+ name_stock_file)
# stock_symbols = stock_symbols_df['Symbol']
# stock_name = stock_symbols_df['Name']
# stock_symbols = list(stock_symbols)
# #https://stackoverflow.com/questions/10993612/python-removing-xa0-from-string
# stock_symbols = [str(x).replace('\xa0', '') for x in stock_symbols]
# # stock_symbols = ['DRD', 'HEBT']
# stock_data = get_data(stock_symbols)
# high_priority, low_priority, no_importance, unprocessed = process_data(stock_data,stock_symbols)
# report_results = [high_priority, low_priority, no_importance]

# with open(filename, 'w', newline="") as csv_file:  
#     writer = csv.writer(csv_file)
#     writer.writerow(['Symbol','Name', 'Signal'])
#     for sym, name in zip(stock_symbols, stock_name):
#         for key, value in high_priority.items():
#             if key == sym:
#                 writer.writerow([key, name, value])

# print("report has been generated")

