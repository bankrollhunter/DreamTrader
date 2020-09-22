from .dataSource import DataSource
from .trend import TrendAnalyze

from jqdatasdk import *
from jqdatasdk.api import get_fundamentals, get_industry_stocks, get_security_info
from jqdatasdk.utils import query
from tables import file
import talib
from datetime import datetime, timedelta
import json
import logging
from sqlalchemy.orm.query import Query
from .store import MongoDB


analyzePeriod = 5
longArrangeLimit = 5
ema20NegativeThreshold = -0.05
nearMovingAverageThreshold = 0.003


class MarketBreadth:
    def __init__(self):
        super().__init__()

    def report_daily_first_level_market_breadth(self):
        """
        1. 300 index
        2. HY001 energy
        3. HY002 meterial
        4. HY003 industry
        5. HY005 daily consume
        6. HY006 medical
        7. HY007 financial
        8. HY008 information&technology
        9. HY009 telecommunications
        10. HY010 public utilities
        11. HY011 real estate
        """
        logging.info('report first level market breadth')

        logging.info('HS300 index')
        stocks = DataSource.query_index_stocks('000300.XSHG')
        self.get_market_breadth(stocks)

        codes = {
            'HY001': '能源',
            'HY002': '材料',
            'HY003': '工业',
            'HY004': '可选消费',
            'HY005': '日常消费',
            'HY006': '医疗保健',
            'HY007': '金融',
            'HY008': '信息技术',
            'HY009': '电信服务',
            'HY010': '公共事业',
            'HY011': '房地产'
        }
        for k, v in codes.items():
            self.report_market_breadth(k, v)

        # 图片，write to report.

    def report_daily_second_level_market_breadth(self):
        """
        JQ行业: https://www.joinquant.com/help/api/help?name=plateData#%E8%81%9A%E5%AE%BD%E8%A1%8C%E4%B8%9A
        TODO: 清洁能源板块，光伏，电动车
        """
        codes = {
            'HY477': '啤酒',
            'HY478': '白酒',
            'HY479': '软饮料',
            'HY481': '食品加工和肉类',
            'HY504': '人寿与健康保险',
            'HY523': '半导体设备',
            'HY524': '半导体产品',
            'HY446': '消费电子',
            'HY572': '中药',
            'HY491': '生物科技',
            'HY492': '西药',
            'HY485': '医疗保健设备',
            'HY486': '医疗保健用品',
            'HY487': '保健护理产品经销商',
            'HY488': '保健护理服务',
            'HY435': '航空',
            'HY439': '机场服务',
            'HY449': '家用电器',
            'HY454': '鞋类',
            'HY493': '多元化银行',
            'HY494': '区域性银行',
            'HY496': '多元化金融',
            'HY501': '投资银行业与经纪业',
            'HY505': '多元化保险',
            'HY444': '汽车制造',
            'HY445': '摩托车制造',
            'HY576': '汽车零售',
            'HY426': '建筑机械与重型卡车',
            'HY466': '互联网零售',
            'HY601': '新能源发电业'

        }
        logging.info('report second level market breadth')
        for k, v in codes.items():
            self.report_market_breadth(k, v, enableDetail=False)

    def report_market_breadth(self, code, description, enableDetail=False):
        logging.info('report {} {}'.format(code, description))
        stocks = DataSource.query_industry_stocks(code)
        for it in stocks:
            if(enableDetail):
                logging.info(DataSource.query_security_info(it)
                             ['display_name'])
        self.get_market_breadth(stocks)

    def get_market_breadth(self, stocks=[], period=analyzePeriod):
        res = None
        for it in stocks:
            price = DataSource.query_price_data(it)
            aboveEMA20 = self.AboveEMA20(price.close)
            if(res is None):
                res = aboveEMA20
            else:
                res = res.add(aboveEMA20)
        for idx, item in res[-period:].items():
            logging.info("{} : {:.2%}".format(idx, item/len(stocks)))

    def AboveEMA20(self, close):
        ema20 = talib.EMA(close, timeperiod=20)
        res = close.copy()
        for idx, item in close.items():
            if(item > ema20[idx]):
                res[idx] = 1
            else:
                res[idx] = 0
        return res


# https://discourse.julialang.org/t/plotting-while-working-with-vs-code-remote-ssh/34309/7
# https://github.com/microsoft/vscode-remote-release/issues/452
