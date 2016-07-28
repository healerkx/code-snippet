
import pandas
import tushare as ts
import os
import sys
import datetime


# 根据股票的code获取日K线数据, 并且dump到文件
def save_share_data_by_code(code, start, path):
    """
    code: Share code, 股票代码
    start: YYYY-MM-DD
    path: Dest path, 目标路径
    """

    filename = os.path.join(path, code)
    # print(filename)
    if not os.path.exists(filename):
        data = ts.get_hist_data(code, start=start, ktype='D')
        if data is not None and len(data.values) != 0:
            data.to_csv(filename, encoding='utf-8')



k5_path = os.getcwd()
config_file = os.path.join(k5_path, 'daydata.config')
with open(config_file) as file:
    for line in file.readlines():
        if line.startswith('dest-path'):
            ashare_path = line[line.index('=') + 1:]

if len(ashare_path) == 0:
    print("Please provide dest-path for saving data")
    exit()

if len(sys.argv) == 1:
    now = datetime.datetime.now() 
    today = now.strftime("%Y-%m-%d")
else:
    today = sys.argv[1]


dest_path = os.path.join(ashare_path, today)

if not os.path.exists(dest_path):
    os.mkdir(dest_path)

print("Start to save share data of the date (%s)" % today)


# stock_basics about
stock_basics = os.path.join(ashare_path, 'stock_basics')
if not os.path.exists(stock_basics):
    stocks = ts.get_stock_basics()
    stocks.to_csv(stock_basics, encoding='utf-8')

stock_basics_data = pandas.read_csv(stock_basics, encoding='utf-8')


daydata_path = os.path.join(ashare_path, 'daydata')
if not os.path.exists(daydata_path):
    os.mkdir(daydata_path)

for stock in stock_basics_data.values:
    code = "%0.6d" % (stock[0])
    name = stock[1]
    print("%s %s" % (code, name))
    save_share_data_by_code(code, '2014-01-01', daydata_path)







