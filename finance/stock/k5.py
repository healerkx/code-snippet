
import pandas
import tushare as ts
import os
import sys
import datetime

def fetch_today_all_share_data(dest_path):
    """
    """
    all_info_file = os.path.join(dest_path, 'all')
    all_shares = None
    if os.path.exists(all_info_file):
        all_shares = pandas.read_pickle(all_info_file)
    else:
        all_shares = ts.get_today_all()
        all_shares.to_pickle(all_info_file)

    count = len(all_shares.values)
    counter = 0
    last_percent = 0
    print('Today has %d shares' % count)
    for v in all_shares.values:
        counter += 1
        percent = 100 * counter // count
        if percent != last_percent:
            last_percent = percent
            print('Current %d %%' % percent)
        yield v

# 根据股票的code获取5分钟K线数据, 并且dump到文件
def get_share_data_by_code(code, today, path):
    """
    code: Share code, 股票代码
    today: Date in format YYYY-MM-DD, 日期
    path: Dest path, 目标路径
    """
    filename = os.path.join(path, code)
    if os.path.exists(filename):
        return pandas.read_pickle(filename)
    else:
        data = ts.get_hist_data(code, start=today, ktype='5')

        data.to_pickle(os.path.join(path, code))
        return data


k5_path = os.getcwd()
config_file = os.path.join(k5_path, 'k5.config')
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

for v in fetch_today_all_share_data(dest_path):
    code = v[0]
    name = v[1]
    print('Saving %s(%s)' % (name, code))
    get_share_data_by_code(code, today, dest_path)


