import logging
import json
from .dataSource import DataSource
import talib

analyzePeriod = 5
longArrangeLimit = 5
ema20NegativeThreshold = -0.05
nearMovingAverageThreshold = 0.003


class TrendAnalyze:
    def __init__(self, code=None):
        super().__init__()
        self.code = code
        self.price = DataSource.query_price_data(code)
        self.ema5 = talib.EMA(self.price.close, timeperiod=5)
        self.ema20 = talib.EMA(self.price.close, timeperiod=20)
        self.ema60 = talib.EMA(self.price.close, timeperiod=60)
        self.ema120 = talib.EMA(self.price.close, timeperiod=120)
        self.tr = abs(self.price.high - self.price.low)

    @property
    def isAboveEMA5(self):
        return bool(self.price.close.values[-1] > self.ema5.values[-1])

    @property
    def isAboveEMA20(self):
        return bool(self.price.close.values[-1] > self.ema20.values[-1])

    @property
    def isAboveEMA60(self):
        return bool(self.price.close.values[-1] > self.ema60.values[-1])

    @property
    def isAboveEMA120(self):
        return bool(self.price.close.values[-1] > self.ema120.values[-1])

    @property
    def longCloseCrossEMA5(self):
        return bool(self.price.close.values[-2] < self.ema5.values[-2] and self.price.close.values[-1] > self.ema5.values[-1])

    @property
    def longEMA5CrossEMA20(self):
        return bool(self.ema5.values[-2] < self.ema20.values[-2] and self.ema5.values[-1] > self.ema20.values[-1])

    @property
    def shortCloseCrossEMA5(self):
        return bool(self.price.close.values[-2] > self.ema5.values[-2] and self.price.close.values[-1] < self.ema5.values[-1])

    @property
    def nearCloseNearEMA20(self):
        return abs(self.price.close.values[-1]-self.ema20.values[-1])/self.price.close.values[-1] < nearMovingAverageThreshold

    @property
    def nearCloseNearEMA60(self):
        return abs(self.price.close.values[-1]-self.ema60.values[-1])/self.price.close.values[-1] < nearMovingAverageThreshold

    @property
    def nearCloseNearEMA120(self):
        return abs(self.price.close.values[-1]-self.ema120.values[-1])/self.price.close.values[-1] < nearMovingAverageThreshold

    @property
    def shortEMA5CrossEMA20(self):
        return self.ema5.values[-2] > self.ema20.values[-2] and self.ema5[-1] < self.ema20.values[-1]

    @property
    def longArrange(self):
        for i in range(longArrangeLimit):
            if(self.ema5.values[-i-1] < self.ema20.values[-i-1] or self.ema20.values[-i-1] < self.ema60.values[-i-1]):
                return False
        return True

    @property
    def ema5Bias(self):
        return (self.ema5.values[-1]-self.ema20.values[-1])/self.ema20.values[-1]

    @property
    def ema20Bias(self):
        return (self.ema20.values[-1]-self.ema60.values[-1])/self.ema60.values[-1]

    @property
    def natr(self):
        # Normalized Average True Range (NATR)
        natr = talib.NATR(self.price.high, self.price.low,
                          self.price.close, timeperiod=14)
        return natr[-analyzePeriod*2:]

    @property
    def atr(self):
        atr = talib.ATR(self.price.high, self.price.low,
                        self.price.close, timeperiod=14)
        return atr[-analyzePeriod*2:]

    @property
    def longChangeEMA5Direction(self):
        if(self.ema5Angle.values[-2] < 0 and self.ema5Angle.values[-1] > 0):
            return True
        return False

    @property
    def longChangeEMA20Direction(self):
        if(self.ema20Angle.values[-2] < 0 and self.ema20Angle.values[-1] > 0):
            return True
        return False

    @property
    def ema5Angle(self):
        prev = self.ema5.copy()[-analyzePeriod-1:-1]
        now = self.ema5.copy()[-analyzePeriod:]
        now = now.reset_index(drop=True)
        prev = prev.reset_index(drop=True)
        tmp = now.sub(prev)
        angle = talib.ATAN(tmp)*180/3.1416
        return angle

    @property
    def ema20Angle(self):
        prev = self.ema20.copy()[-analyzePeriod-1:-1]
        now = self.ema20.copy()[-analyzePeriod:]
        now = now.reset_index(drop=True)
        prev = prev.reset_index(drop=True)
        tmp = now.sub(prev)
        angle = talib.ATAN(tmp)*180/3.1416
        return angle

    def report(self):
        """
        report all factor's. We could buy it. and test it in the future.
        According to stock performance, adjust weight of each factor.
        Build a quantitative score system.

        TODO:
        1. EPS. EPS(rate) EPS增长率
        2. ROE
        3. Revenue growth rate. (营收增长率)
        4. 现金营业收入比率
        5. 经营活动现金流净额增长率
        6. 固定资产周转率
        """

        logging.info('-----Stock trend report: {}-----'.format(
            DataSource.query_security_info(self.code)['display_name']))
        logging.info(DataSource.query_security_info(self.code))
        logging.info('above5: {}'.format(self.isAboveEMA5))
        logging.info('above20: {}'.format(self.isAboveEMA20))
        logging.info('above60: {}'.format(self.isAboveEMA60))
        logging.info('long arrange: {}'.format(self.longArrange))
        logging.info('ema5 bias: {:.2%}'.format(self.ema5Bias))
        logging.info('ema20 bias: {:.2%}'.format(self.ema20Bias))
        logging.info('ema5 > ema20: {}'.format(self.ema5Bias > self.ema20Bias))
        logging.info('ema5 angle')
        logging.info(self.ema5Angle.to_string())
        logging.info('ema20 angle')
        logging.info(self.ema20Angle.to_string())
        logging.info('NATR')
        logging.info(self.natr.to_string())
        logging.info('fundamental ')
        logging.info(DataSource.query_fundamentals(self.code).to_string())
        logging.info('\n')
        return {
            'display_name': DataSource.query_security_info(self.code)['display_name'],
            'above5': self.isAboveEMA5,
            'above20': self.isAboveEMA20,
            'above60': self.isAboveEMA60,
            'long arrange:': self.longArrange,
            'ema5 bias': self.ema5Bias,
            'ema20 bias': self.ema20Bias,
            'Bias: ema5 > ema20': bool(self.ema5Bias > self.ema20Bias),
            'ema5 angle': json.loads(self.ema5Angle.to_json()),
            'ema20 angle': json.loads(self.ema20Angle.to_json()),
            'NATR': json.loads(self.natr.to_json()),
            'fundamental': json.loads(DataSource.query_fundamentals(self.code).to_json())
        }
