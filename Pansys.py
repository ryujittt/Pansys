import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout,QHBoxLayout,QCheckBox, QWidget, QPushButton,QLabel,QLineEdit


from datetime import datetime
import numpy as np
import ccxt
import mplfinance as mpf
import pandas as pd
import random

import matplotlib.pyplot as plt

        
        


class Pansys(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Pansys')
#         self.setGeometry(100, 100, 800, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)



        
        
        self.Box = QVBoxLayout()
        self.Box_2 = QHBoxLayout()
        self.layout.addLayout(self.Box)
        self.layout.addLayout(self.Box_2)
        


        #         self.start = False
        self.label_symbol = QLabel()
        self.label_symbol.setText('Symbol')
        self.Box.addWidget(self.label_symbol)
        
        # Add QComboBox for symbol
        self.symbol_edit = QLineEdit(self)
        self.symbol_edit.setText('ETH/USDT')  # Set default value
        self.Box.addWidget(self.symbol_edit)
        


        self.label_timeframe = QLabel()
        self.label_timeframe.setText('Timeframe')
        self.Box.addWidget(self.label_timeframe)
        
        # Add QComboBox for timeframe
        self.timeframe_edit = QLineEdit(self)
        self.timeframe_edit.setText('5m')
        self.Box.addWidget(self.timeframe_edit)

        
        


 

        
        
        self.label_short = QLabel()
        self.label_short.setText('Short')
        self.Box.addWidget(self.label_short)
        
        self.short_edit = QLineEdit(self)
        self.short_edit.setText('75')
        self.Box.addWidget(self.short_edit)
        
        self.label_long = QLabel()
        self.label_long.setText('Long')
        self.Box.addWidget(self.label_long)
        
        self.long_edit = QLineEdit(self)
        self.long_edit.setText('100')
        self.Box.addWidget(self.long_edit)
        
        
        self.label_sample = QLabel()
        self.label_sample.setText('Sample')
        self.Box.addWidget(self.label_sample)
        
        self.sample_edit = QLineEdit(self)
        self.sample_edit.setText('75')
        self.Box.addWidget(self.sample_edit)
        
        self.historic = QCheckBox("HISTORIC", self)
        self.ema = QCheckBox("EMA", self)
        self.Box_2.addWidget(self.historic)
        self.Box_2.addWidget(self.ema)
        
        
        # Create a QPushButton
        self.go_button = QPushButton('Start', self)

        # Connect the button to a function (slot)
        self.go_button.clicked.connect(self.update_program)


        self.Box.addWidget(self.go_button)

        

        
        




        



 
    def update_program(self):
#         try:
            
        df,ohlcv = self.fetch_data()
        self.RealTime_Executing(df,ohlcv)
#         except:
#             self.Price.setText('Error')
    def fetch_data(self):
        exchange = ccxt.binance()

        degree = 2  # You can adjust the degree based on your data
        
        random_day = random.randint(1, 25)
        random_month = random.randint(1, 11)
        
        start_date = datetime(2023, random_month, random_day,5,0)  # Replace with your desired start date
        exchange = ccxt.binance()
        since = exchange.parse8601(str(start_date))

        self.short = int(self.short_edit.text())
        self.long = int(self.long_edit.text())
        self.sample = int(self.sample_edit.text())

        self.symbol = self.symbol_edit.text()
        self.timeframe = self.timeframe_edit.text()
        self.limit = self.sample + self.long

        
        
        if self.historic.isChecked():
            ohlcv = exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=self.limit , since = since)
        else:
            ohlcv = exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=self.limit)
            



        ohlcv_arrays = np.array(ohlcv).T
        timestamp_array = ohlcv_arrays[0]
        open_array = ohlcv_arrays[1]
        high_array = ohlcv_arrays[2]
        low_array = ohlcv_arrays[3]
        close_array = ohlcv_arrays[4] 
        volume_array = ohlcv_arrays[5]
        index_array = np.arange(len(timestamp_array))
        
        self.candle_average = np.mean(abs(ohlcv_arrays[4] - ohlcv_arrays[1] ))/4

        

        df = np.array([index_array, high_array, low_array, close_array, timestamp_array, volume_array, open_array])
        
        return df , ohlcv
        
        
    def RealTime_Executing(self,df,ohlcv):
        
        columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        _data = pd.DataFrame(ohlcv, columns=columns)
        df_data = _data.iloc[-self.sample:].copy()
        
        df_data['blocks'] = df_data['volume']*(abs(df_data['close']-df_data['open'])/(df_data['high']-df_data['low']))

        # Calculate the difference between each element and the first element
        c = df_data['blocks'] - df_data['blocks'].shift(1)

        # Apply the condition: if c is positive, keep the original value, otherwise set to NaN
        df_data['c_positive'] = np.where(c > 0, df_data['blocks'], np.nan)

        df_data['volume'] = df_data['c_positive']

        df_data['timestamp'] = pd.to_datetime(df_data['timestamp'], unit='ms')  # Convert timestamp to datetime

        df_data.set_index('timestamp', inplace=True)

        price = []
        weighted = []
        weighted_short = []

        
        for i in range(self.sample):
            data = self.Weighted_Price(self.long, i, df)
            weighted.append(data[0])
            price.append(data[1])

        for i in range(self.sample):
            data = self.Weighted_Price(self.short, i, df)

            weighted_short.append(data[0])



        self.plot_data(weighted, weighted_short,df_data)

    def Weighted_Price(self, _backtime, _index, _df):


        df = _df[:, self.limit-_backtime-self.sample+_index+1:self.limit-self.sample+_index+1]

        
    

        close_price = df[3]



        Y = close_price
        X = np.arange(len(close_price))
        W = df[5]
        W_normalized = W / sum(W)
        weighted_average = sum(W_normalized * Y)
        coefficients = np.polyfit(X, Y - weighted_average, 2)
        adjusted_curve = np.polyval(coefficients, X[-1]) + weighted_average
        return adjusted_curve, close_price[-1]


    def plot_data(self,weighted, weighted_short,df_data):
        x = np.arange(len(weighted))

        
        
#         sessions = [13, 16, 21]
        sessions = [7, 13, 16, 21]
        color = 'r'
        date = []
        
        # Plot vertical lines for each session
        for session in sessions:
            # Filter the DataFrame to get data where the hour component matches the session
            stamp  = df_data[df_data.index.hour == session]
            try : 
                date.append(stamp.index[0])
            except:
                pass

        # Plot using mplfinance
        plot_size = (90, 45)
# Create the plot with the given size


        additional_short = mpf.make_addplot(np.array(weighted_short), color='red', width = 0.6)
        additional_long = mpf.make_addplot(np.array(weighted), color='green', width = 0.6)
        
        if self.ema.isChecked() :
            mpf.plot(df_data, type='candle', style='yahoo',ema = (150,15), addplot = [additional_short,additional_long] ,  volume=True, vlines=dict(vlines=date,linewidths=1,colors = color,linestyle='dotted',alpha=0.4),savefig = 'weighted_price_graph.png' )
        else:
            mpf.plot(df_data, type='candle', style='yahoo', addplot = [additional_short,additional_long] ,  volume=True, vlines=dict(vlines=date,linewidths=1,colors = color,linestyle='dotted',alpha=0.4),savefig = 'weighted_price_graph.png' )


        



if __name__ == '__main__':
    app = None
    app = QApplication(sys.argv)
    main_app = Pansys()
    main_app.show() 
    sys.exit(app.exec_())
