import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from style import *

def make_plot(ticker, dates, data, title, legend):
    if len(dates) > len(data):
        print("Error: dates are not of the same length as the data. Unable to make plot.")
        return 1
    dates_fl = []
    for date in dates:
        dates_fl.append(date.timestamp())
    data_np = np.array(data)
    dates_np = np.array(dates_fl)
    coeffs = np.polyfit(dates_np, data_np, 1)
    poly_eqn = np.poly1d(coeffs)
    y_hat = poly_eqn(dates_np)
    
    if (max(abs(data_np)) > 1e9):
        formatter = FuncFormatter(billions)
    elif (max(abs(data_np)) > 1e6):
        formatter = FuncFormatter(millions)
    elif (max(abs(data_np)) > 1e3):
        formatter = FuncFormatter(thousands)
    else:
        formatter = FuncFormatter(percentage)
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(formatter)
    ax.set_title(title + ' - ' + str(ticker))
    ax.plot(dates, data_np, "--")
    ax.plot(dates,y_hat)
    ax.grid(b=None, which='both', axis='both', color='#2b2b2b', linestyle=(0, (1, 2)), linewidth=0.5)
    ax.legend(['Data from Ycharts','Linear fit'])
    plt.xlabel('Date',fontsize=11)
    plt.ylabel(legend, fontsize=11)