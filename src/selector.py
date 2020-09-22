import json
import logging
from datetime import datetime

from .trend import TrendAnalyze
from .dataSource import DataSource

ema20NegativeThreshold = -0.05
nearMovingAverageThreshold = 0.003


class WatchList:
    def __init__(self):
        super().__init__()

    @staticmethod
    def writeReport(name, report):
        with open('watchingStocks/daily-stock-{}-{}.json'.format(name, datetime.now().strftime('%Y-%m-%d')), 'w') as f:
            json.dump(report, f)


class StockSelector:
    def __init__(self, stocks):
        super().__init__()
        self.stocks = stocks

    def filterLongArrange(self):
        logging.info(
            'long arrange -----------------------------------------------')
        report = []
        for it in self.stocks:
            trend = TrendAnalyze(it)
            if(trend.longArrange):
                report.append(DataSource.query_security_info(it)
                              ['display_name'])
                trend.report()

    def filterLongEM5CrossEMA20(self):
        logging.info(
            'EMA5 Cross EMA20 -----------------------------------------------')
        ret = []
        for it in self.stocks:
            trend = TrendAnalyze(it)
            if(trend.longEMA5CrossEMA20):
                report = trend.report()
                ret.append(report)

        WatchList.writeReport('EMA5CrossEMA20', ret)
        return ret

    def filterNearEMA20(self):
        logging.info(
            'Near EMA20 -----------------------------------------------')
        ret = []
        for it in self.stocks:
            trend = TrendAnalyze(it)
            if(trend.nearCloseNearEMA20):
                report = trend.report()
                ret.append(report)
        WatchList.writeReport('NearEMA20', ret)

    def filterNearEMA60(self):
        logging.info(
            'Near EMA60 -----------------------------------------------')
        ret = []
        for it in self.stocks:
            trend = TrendAnalyze(it)
            if(trend.nearCloseNearEMA60):
                report = trend.report()
                ret.append(report)
        WatchList.writeReport('NearEMA60', ret)

    def filterNearEMA120(self):
        logging.info(
            'Near EMA120 -----------------------------------------------')
        ret = []
        for it in self.stocks:
            trend = TrendAnalyze(it)
            if(trend.nearCloseNearEMA120):
                report = trend.report()
                ret.append(report)
        WatchList.writeReport('NearEMA120', ret)

    def filterNegativeEMA20Bias(self, threshold=ema20NegativeThreshold):
        logging.info('EMA20 Negative Bias. Threshold: {}'.format(threshold))
        for it in self.stocks:
            trend = TrendAnalyze(it)
            if(trend.ema20Bias < threshold):
                trend.report()

    def filterChangeDirectionEMA5(self):
        logging.info('EMA5 Long Change direction')
        ret = []
        for it in self.stocks:
            trend = TrendAnalyze(it)
            if(trend.longChangeEMA5Direction):
                report = trend.report()
                ret.append(report)

        WatchList.writeReport('changeDirectionEMA5', ret)

    def filterChangeDirectionEMA20(self):
        logging.info('EM20 Long Change direction')
        ret = []
        for it in self.stocks:
            trend = TrendAnalyze(it)
            if(trend.longChangeEMA20Direction):
                report = trend.report()
                ret.append(report)

        WatchList.writeReport('changeDirectionEMA20', ret)
