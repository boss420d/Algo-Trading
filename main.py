
###########################################################################################################
'''
Description
This is the code for the trading bot.
You should execute this code on  an open market day @9:15AM.
This bot places order based on conditions acquired from the indicators RSI and EMA
Python code is used to create the condition and selenium is used to place the order from the browser to get a web interface feel.
Steps to execute and pre-requisites are mentioned in the readme file in the repo.'''
###########################################################################################################
print("Author: Gautam Singh")
print("Credits: [Gautam Singh]")
print("Email: 420boss.d@gmail.com")
##################################################

from nsepy import get_history
from datetime import date, datetime
import os
from tradingview_ta import TA_Handler, Interval, Exchange
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

os.system("figlet -c Python Trading Bot ")
Today = date.today()
y = Today.strftime("%Y")
m = Today.strftime("%m")
d = Today.strftime("%d")
# d = "30"


#last order
last_order="sell"
sold_before = False
bought_before = False
current_price = 0
take_profit = 0.0
take_loss = 0.0


#load chrome driver 
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.maximize_window()
driver.get("https://in.tradingview.com/")
time.sleep(60)

##############################################################################################################
#initiating tradingview handler to get the recomendation for sonata software for 15 min interval
symbol = input("Enter the stock")
ssw = TA_Handler(
    symbol="SONATSOFTW",
    screener="india",
    exchange="NSE",
    interval=Interval.INTERVAL_5_MINUTES
)
#############################################################################################################
def countdown(t):

    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1


while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if(current_time >= "09:25:00" and current_time < "15:00:00"):

        rec = ssw.get_analysis()
        RSI = rec.indicators["RSI"]
        # MACD = rec.indicators["MACD.macd"]
        EMA = rec.moving_averages["COMPUTE"]["EMA10"]
        print("RSI:", RSI, "EMA:", EMA)


        if ( RSI >= 30 and RSI <= 70 and EMA == "BUY" ):
            if (last_order=="sell"):
                print("Buying 5 stock of SONATSOFTW")
                last_order="buy"
                print(last_order)
                print(sold_before)
                #buy 1 stock
                driver.find_element(By.XPATH,"//div[8]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]").click()
                driver.find_element(By.XPATH,"//div[1]/div[1]/div[6]/button[1]/div[1]/span[2]").click()
                current_price = driver.find_element(By.XPATH,"//div[2]/div[8]/div[1]/div/div/div[1]/div[2]/div/div[2]/div[2]/div").text
                print(current_price)
                take_profit = float(current_price) + 8
                take_loss = float(current_price) - 5
                while True:
                    print("Time left till next call - ")
                    countdown(int(5))
                    rec = ssw.get_analysis()
                    RSI = rec.indicators["RSI"]
                    # MACD = rec.indicators["MACD.macd"]
                    EMA = rec.moving_averages["COMPUTE"]["EMA10"]
                    print("RSI:", RSI, "EMA:", EMA)
                    current_price = driver.find_element(By.XPATH,"//div[2]/div[8]/div[1]/div/div/div[1]/div[2]/div/div[2]/div[2]/div").text
                    if((RSI >= 30 and EMA == "SELL") or (float(current_price) >= take_profit) or (float(current_price) <= take_loss)):
                        #sell the stock
                        print("Selling The Stock")
                        last_order="sell"
                        print(last_order)
                        #sell stock
                        driver.find_element(By.XPATH,"//body[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]").click()
                        time.sleep(2)
                        driver.find_element(By.XPATH,"//button[1]/div[1]/span[2]").click            ()
                        break
                    else:
                        print("no adjustment required")
            else:
                print("last order not sold")
        elif( RSI >= 50 and EMA == "SELL" ):
            if ( last_order == "sell"):
                print("Selling Stock")
                driver.find_element(By.XPATH,"//body[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]").click()
                time.sleep(2)
                driver.find_element(By.XPATH,"//button[1]/div[1]/span[2]").click            ()
                current_price = driver.find_element(By.XPATH,"//div[2]/div[8]/div[1]/div/div/div[1]/div[2]/div/div[2]/div[2]/div").text
                print(current_price)
                take_profit = float(current_price) - 8
                take_loss = float(current_price) + 5
                while True:
                    print("Time left till next call - ")
                    countdown(int(5))
                    rec = ssw.get_analysis()
                    RSI = rec.indicators["RSI"]
                    # MACD = rec.indicators["MACD.macd"]
                    EMA = rec.moving_averages["COMPUTE"]["EMA10"]
                    print("RSI:", RSI, "EMA:", EMA)
                    current_price = driver.find_element(By.XPATH,"//div[2]/div[8]/div[1]/div/div/div[1]/div[2]/div/div[2]/div[2]/div").text
                    if((RSI <= 30 and EMA == "BUY") or ( float(current_price) <= take_profit) or (float(current_price) >= take_loss)):
                        #buy the stock
                        print("Buying the stock")
                        driver.find_element(By.XPATH,"//div[8]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]").click()
                        driver.find_element(By.XPATH,"//div[1]/div[1]/div[6]/button[1]/div[1]/span[2]").click()
                        break
                    else:
                        print("no adjustment required")

        else:
            print("condition not favourable..waiting")
          
    elif(current_time >= "15:00:00"):
        print("Time to close for the day")
        # #fetch open profit
        open_profit = driver.find_element(By.XPATH,"//div[4]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]").text
       # print(open_profit)
        # P = "1000"
        print("Calculating profit :",open_profit)
        break
    else:
        if(current_time >= "09:15:00" and current_time < "09:25:00"):
            print("Analysing market","\n\n")
        elif(current_time < "9:15:00"):
            print("Waiting for market to open")
        else:
            print("No action required")
        
    
# Use "Ctrl + C" for exiting this code.
# Use vs code for trading.
# This code is made for Trading View only connect your brocker with trading view for executing order.
# This is code run when marker will open, use in nse stock also change it.
# Thank you for using this code.
    


