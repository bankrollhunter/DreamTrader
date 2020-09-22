from datetime import datetime, timedelta
import os
import logging
import json
import pandas

from jqdatasdk import *
from jqdatasdk.api import get_fundamentals, get_index_stocks, get_industry_stocks, get_security_info
from jqdatasdk.utils import query



start_date = datetime.now() - timedelta(180)
end_date = datetime.now()



class DataSource:

    @staticmethod
    def authJQ(account, password):
        is_auth = auth(account, password)
        logging.info('auth result: {}'.format(is_auth))

    def __init__(self):
        super().__init__()

    @staticmethod
    def query_index_stocks(code):
        filepath = 'data/{}.json'.format(code)
        if(os.path.isfile(filepath)):
            logging.debug('lazy load data from {}'.format(filepath))
            with open(filepath, 'r') as f:
                return json.load(f)
        stocks = get_index_stocks(code)
        with open(filepath, 'w') as f:
            json.dump(stocks, f)
        return stocks

    @staticmethod
    def query_industry_stocks(industry_code):
        # For industry_code pls reference to https://www.joinquant.com/help/api/help?name=plateData
        filepath = 'data/{}.json'.format(industry_code)
        if(os.path.isfile(filepath)):
            logging.debug('lazy load data from {}'.format(filepath))
            with open(filepath, 'r') as f:
                return json.load(f)
        stocks = get_industry_stocks(industry_code)
        with open(filepath, 'w') as f:
            json.dump(stocks, f)
        return stocks

    @staticmethod
    def query_price_data(code):
        filepath = 'data/{}-{}.csv'.format(code,
                                           datetime.now().strftime("%Y-%m-%d"))
        if(os.path.isfile(filepath)):
            logging.debug('lazy load data from {}'.format(filepath))
            return pandas.read_csv(filepath)
        price = get_price(code, start_date=start_date,
                          end_date=end_date)
        price.to_csv(filepath)
        return price

    @staticmethod
    def query_security_info(code):
        filepath = 'data/stock-{}.json'.format(code)
        if(os.path.isfile(filepath)):
            logging.debug('lazy load data from {}'.format(filepath))
            with open(filepath, 'r') as f:
                return json.load(f)
        info = get_security_info(code)
        with open(filepath, 'w') as f:
            res = {'code': info.code, 'display_name': info.display_name,
                   'name': info.name,  'type': info.type,
                   'parent': info.parent}
            json.dump(res, f)
        return res

    @staticmethod
    def query_fundamentals(code):
        """
        Doc: https://www.joinquant.com/help/api/help?name=JQData#get_fundamentals-%E6%9F%A5%E8%AF%A2%E8%B4%A2%E5%8A%A1%E6%95%B0%E6%8D%AE
        capitalization: 总股本
        circulating_cap: 流通股本
        market_cap: 总市值
        circulating_market_cap: 流通市值
        turnover_ratio: 换手率
        pe_ratio: 市盈率(PE, TTM) 收盘价*总股本/归属母公司净利润
        pe_ratio_lry: 市盈率(PE) 以上一年度每股盈利计算的静态市盈率. 股价/最近年度报告EPS
        pb_ratio: 市净率(PB) 每股股价与每股净资产的比率. (股票在指定日期收盘价*截止当日公司总股本)/归属公司股东的权益
        ps_ratio: 市销率(PS, TTM) 市销率为股票价格与每股销售收入之比，市销率越小，通常被认为投资投资价值越高。（股票在指定日期的收盘价*总股本)/营业收入TTM
        pcf_ratio: 市现率(PCF, 现金流TTM) 市现率可用于评价股票的价格水平和风险水平。市现率=（股票在指定交易日期的收盘价 * 截至当日公司总股本）/现金及现金等价物净增加额TTM
        """
        q = query(valuation).filter(valuation.code == code)
        if(datetime.now().weekday() < 5):
            date = (datetime.now()-timedelta(14)).strftime("%Y-%m-%d")
        else:
            date = (datetime.now()-timedelta(16)).strftime("%Y-%m-%d")
        filepath = 'data/fundamentals-{}-{}'.format(code, date)
        if(os.path.isfile(filepath)):
            logging.debug('lazy load data from {}'.format(filepath))
            return pandas.read_csv(filepath)
        df = get_fundamentals(q, date)
        df.to_csv(filepath)
        return df
