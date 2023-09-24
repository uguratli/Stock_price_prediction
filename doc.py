import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import os
from fpdf import FPDF
import pickle
import datetime as dt
from f_basics import *
import warnings
warnings.filterwarnings("ignore")


def Stock_folder(stock_name):
    """ Folder creation function.
    Creates file for given stock name and current period, if it doesnt exists.
    """

    path = os.getcwd()
    directory = f'{stock_name}-{dt.datetime.today().strftime("%b-%Y")}'
    if not os.path.exists(os.path.join(path,directory)):
        os.mkdir(os.path.join(path,directory))
    else:
        print(f'{os.path.join(path,directory)} - File already exists')
    return os.path.join(path,directory)
    
def PDF_out(pdf_name ,folder_dir):
    """ PDF report function.
    """
    report = FPDF()
    report.add_page()
    report.set_font('Arial', size = 25)
    report.set_margins(0, 0, 0)
    report.set_font('Arial', 'B', 14)
    report.cell(w = 40,
                h = 10, 
                txt = dt.datetime.today().strftime("%b-%Y"),
                border = 0,
                ln = 1, 
                align = '',
                fill = False,
                link = '')
    
    i = 1
    j = 0
    k = 0
    X, Y = 5, 30
    for file in os.listdir(folder_dir):
        print(file)
        if file == '.DS_Store':
            pass
        else:
            print(f'Y = {Y}')
            print(f'X = {X}')
            report.image(os.path.join(folder_dir,file),
                        x = X,
                        y = Y,
                        w = 110,
                        h = 110,
                        type = '',
                        link = '')
            X = 5 + 100*(i%2)
            Y += 100*(j%2) 
            i += 1
            j += 1
            k += 1
            if (k%4) == 0:
                report.add_page()
                Y = 30  
    report.output(pdf_name, 'F')
    return print(f'done!{pdf_name}')

def Candlestick(dataframe, stock):
    """ Candlestick plot function.
    Generates candlestick graph for given stock data frame (plotly).
    """
    fig = go.Figure(data = [go.Candlestick( x = dataframe.index,
                                       open = dataframe['Open'],
                                       high = dataframe['High'],
                                       low = dataframe['Low'],
                                       close = dataframe['Close'])])
    fig.update_layout(
        title = stock
    )
    return fig


def format_legend(plot):
    plot_legend = plot.legend(loc='upper left', bbox_to_anchor=(-0.005, 0.95), fontsize=16)
    for text in plot_legend.get_texts():
        text.set_color(color ='grey')

def format_borders(plot):
    plot.spines['top'].set_visible(False)
    plot.spines['left'].set_visible(False)
    plot.spines['left'].set_color("grey")
    plot.spines['bottom'].set_color("grey")

def plot_cross(plot, golden, death):
    for i in golden:
        plot.axvline(x = i, color = 'yellow', label = "Golden Cross")
    for i in death:
        plot.axvline(x = i, color = 'black', label = "Death Cross")  

def plot_sma(plot, dates, close):
    s_mov_avg = {
        'SMA (50)': {'Range': 50, 'Color': 'green'},
        'SMA (100)': {'Range': 100, 'Color': 'orange'},
        'SMA (200)': {'Range': 200, 'Color': 'red'}
    }
    for sma, sma_info in s_mov_avg.items():
        plot.plot(dates,
                    close.rolling(sma_info['Range']).mean(),
                    color = sma_info['Color'],
                    label = sma,
                    linewidth = 2,
                    ls = "--")

def plot_rsi(plot, dates, close):
    plot.plot(dates[1:], RSI(close), color = 'purple', ls ="-.", label = "RSI 14")

def time_it(time):
    return dt.datetime.strptime(str(time), '%Y-%m-%d %H:%M:%S')

def get_candle(plot, stocks_info):
    column_color = {'column1': 'green', 'column2': 'red'}
    widths = {'width1': 0.5, 'width2': 0.05}

    up = stocks_info[stocks_info['Adj Close'] >= stocks_info['Open']]
    down = stocks_info[stocks_info['Adj Close'] < stocks_info['Open']]
    fig = plt.figure()
    plot.bar(up.index, up['Adj Close']-up['Open'], widths['width1'], bottom=up['Open'], color = column_color['column1'])
    plot.bar(up.index, up['High']-up['Adj Close'], widths['width2'], bottom=up['Close'], color = column_color['column1'])
    plot.bar(up.index, up['Low']-up['Open'], widths['width2'], bottom=up['Open'], color = column_color['column1'])

    plot.bar(down.index, down['Adj Close']-down['Open'], widths['width1'], bottom=down['Open'], color = column_color['column2'])
    plot.bar(down.index, down['High']-down['Open'], widths['width2'], bottom=down['Open'], color = column_color['column2'])
    plot.bar(down.index, down['Low']-down['Adj Close'], widths['width2'], bottom=down['Close'], color = column_color['column2'])


def get_plot(stock_info, start_date = '1900-01-01 00:00:00', end_date = '2077-01-01 00:00:00',candle = False ,cross_test = False, rsi = False, sma = False):
    """ Plot function.
    Plots daily close, RSI, golden cross, death cross, SMA for given stock info, time interval is set 1900 and 2077 by default.
    Time must be given  in format Y-M-D H:M:S
    """

    extras = int(candle)
    start = time_it(start_date)
    end = time_it(end_date)
    stock_data = stock_info["Stock Data"]
    stock_data = stock_data.loc[(stock_data.index >= start_date) & (stock_data.index <= end_date)]
    #start = dt.datetime.strptime(str(start_date), '%Y-%m-%d %H:%M:%S')
    #end = dt.datetime.strptime(str(end_date), '%Y-%m-%d %H:%M:%S')

    colors = {'red': '#ff207c', 'grey': '#42535b', 'blue': '#207cff', 'orange': '#ffa320', 'green': '#00ec8b'}
    config_ticks = {'size': 14, 'color': colors['grey'], 'labelcolor': colors['grey']}
    config_title = {'size': 18, 'color': colors['grey'], 'ha': 'left', 'va': 'baseline'}




    plt.rc('figure', figsize=(15, 10))
    fig, axes = plt.subplots(2 + extras , 1)
    fig.tight_layout(pad=3)
    fig.suptitle(stock_info["Symbol"] + ' Price and Volume', size=36, color=colors['grey'], x =0.25, y =1.05)
    vol = stock_data['Volume']
    close = stock_data['Adj Close']
    dates = stock_data.index
    plot_close = axes[0]
    plot_close.plot(dates, close)

    plot_close.yaxis.tick_right()
    plot_close.tick_params(axis='both', **config_ticks)
    plot_close.set_ylabel('Price (in TRY)', fontsize=14)
    plot_close.yaxis.set_label_position("right")
    plot_close.yaxis.label.set_color(color = 'grey')
    plot_close.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.5)
    plot_close.set_axisbelow(True)

    if cross_test == True:
        Golden, Death = [day for day in Cross_test(stock_data)[0] if day >= start and day <= end], [day for day in Cross_test(stock_data)[1] if day >= start and day <= end]
        plot_cross(plot_close,Golden, Death)

    if sma == True:
        plot_sma(plot_close, dates, close)
    
    if rsi == True:
        plot_rsi(plot_close,dates, close)

    if candle == True:
        plot_candle = axes[1]
        plot_candle.yaxis.tick_right()
        plot_candle.tick_params(axis='both', **config_ticks)
        plot_candle.set_ylabel('Price (in TRY)', fontsize=14)
        plot_candle.yaxis.set_label_position("right")
        plot_candle.yaxis.label.set_color(color = 'grey')
        plot_candle.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.5)
        plot_candle.set_axisbelow(True)
        get_candle(plot_candle, stock_data)
        format_borders(plot_candle)


        

    if (rsi + cross_test + sma) > 0:
        format_legend(plot_close)
    format_borders(plot_close)
    plot_close.set_title('Data between ' +start_date +" and " + end_date, fontdict=config_title, loc='left')





    plot_vol = axes[1 + extras]
    plot_vol.bar(dates, vol)
    
    plot_vol.yaxis.tick_right()
    plot_vol.tick_params(axis='both', **config_ticks)
    plot_vol.yaxis.set_label_position("right")
    plot_vol.set_xlabel('Date', fontsize=14)
    plot_vol.set_ylabel('Volume (in millions)', fontsize=14)
    plot_vol.yaxis.label.set_color(colors['grey'])
    plot_vol.xaxis.label.set_color(colors['grey'])

    format_borders(plot_vol)