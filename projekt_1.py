#%matplotlib inline                      #handling jupyter error
import pandas
from projekt_1_handlers import emaCompute
import matplotlib.pyplot as plt
import numpy as np
wig20_input = pandas.read_csv('wig20_d.csv')            #Data, Otwarcie, Najnizszy, Najwyzszy,  Zamkniecie, Wolumen
                                                        # 0  ,     1   ,    2     ,      3    ,    4     ,    5     
c_size = len(wig20_input.columns)       #columns size
i_size = wig20_input.size // c_size     #input size(rows)

np_csv = wig20_input.to_numpy()         #numpy conversion
values = np_csv[:,4]                    #values to compute

macd_val = []
prices_df = pandas.DataFrame(values)
day12 = prices_df.ewm(span=12).mean()
day26 = prices_df.ewm(span=26).mean()
for i in range(26,i_size,1):            #computing macd values from 26 to the end, because we need 27 values in case to compute ema26
    ema_12 = day12.iloc[i,0]
    ema_26 = day26.iloc[i,0]
    macd_val.append(ema_12 - ema_26)

signal_val = []                         #computing macd signal values from 9 to the end, because we need 19 values in case to compute ema9
signal_df = pandas.DataFrame(macd_val)
day9 = signal_df.ewm(span=9).mean()
for i in range(9, len(macd_val),1):
    ema_9 = day9.iloc[i,0]
    signal_val.append(ema_9)

x_axis = np.arange(0,len(signal_val))
x_limit = [len(signal_val)- 100, len(signal_val)-1]         #limitations to plots
y_limit = [-200,200]

plt.plot(x_axis, macd_val[9:],'b', label="MACD")            #plotting MACD and MACD-signal on each other
plt.plot(x_axis, signal_val,'r', label="MACD-signal")       #red - MACD-signal, blue - MACD
plt.title("MACD, MACD-signal")
plt.xlabel("Indeks próbki")
plt.ylabel("Wskaźnik")
plt.legend(loc="upper left")
axes = plt.gca()
axes.set_xlim(x_limit)
axes.set_ylim(y_limit)
plt.show()

plt.plot(x_axis, values[35:])                               #plotting values in case to check the usage of the MACD
plt.title("Values")
axes = plt.gca()
axes.set_xlim(x_limit)
plt.show()