from src.dataAnalyze import MarketBreadth
from src.selector import StockSelector
from src.trend import TrendAnalyze
from src.dataSource import DataSource
from src.config import Config
import logging
from datetime import datetime


# generate report to file
daily_report_file_path = 'report/daily-report-{}.txt'.format(
    datetime.now().strftime('%Y-%m-%d'))


logging.basicConfig(format='%(message)s', level=logging.INFO,filename=daily_report_file_path)
# logging.basicConfig(format='%(message)s', level=logging.INFO)

logging.info('Welcome!!!')
config = Config('./config.json')
config.loadConfig()
DataSource.authJQ(config.config['JQAccount'], config.config['JQPassword'])
market = MarketBreadth()
market.report_daily_first_level_market_breadth()
market.report_daily_second_level_market_breadth()

selector = StockSelector(DataSource.query_index_stocks('000300.XSHG'))
selector.filterLongArrange()
selector.filterNegativeEMA20Bias()
selector.filterLongEM5CrossEMA20()
selector.filterNearEMA20()
selector.filterNearEMA60()
selector.filterNearEMA120()
selector.filterChangeDirectionEMA20()

good_stock = ['603885.XSHG', '600031.XSHG', '002607.XSHE',
              '600031.XSHG', '603787.XSHG', '000610.XSHE', '002127.XSHE']

logging.info('good stock')
for it in good_stock:
    trend = TrendAnalyze(it)
    trend.report()
