# DreamTrader

## 简述

自动化按照技术形态选股. 自动筛选，诸如多头排列，破线，拐头，交叉，大幅乖离的股票。

## 如何使用

#### 本地部署


1. 创建JQData的账号 (聚宽账户)。将config-example.json重命名为config.json. 并填入你的用户名和密码. config.json为你的配置文件.
2. 确保你的系统安装Python3, virtualenv. 执行安装脚本./install.sh. 如果没有virtualenv, 使用pip install -r requirements.txt直接安装依赖.
3. 并在当前项目目录下新建data和report目录用来存放数据，报告。
4. 执行脚本 ./daily_analyse.sh. 在report中会生成报告，如果出现NaN, 删除该报告，重新跑一遍

#### 报告

如果不想本地部署，可直接参考每天生成的报告[report](https://github.com/bankrollhunter/DreamTrader/tree/master/report)

通过搜索关键词的方式查看报告: 例如搜索Cross, 表示上穿均线. 同理：搜索Near，表示在均线附近。 下面即为一个报告的例子（EMA5上穿EMA20）：

```
EMA5 Cross EMA20 -----------------------------------------------
-----Stock trend report: 葛洲坝-----
{'code': '600068.XSHG', 'display_name': '葛洲坝', 'name': 'GZB', 'type': 'stock', 'parent': None}
above5: True
above20: True
above60: False
long arrange: False
ema5 bias: 0.03%
ema20 bias: -2.03%
ema5 > ema20: True
ema5 angle
0    2.831407
1    0.743188
2    0.495474
3    0.330321
4    0.220215
ema20 angle
0    0.449887
1    0.079645
2    0.072060
3    0.065197
4    0.058988
NATR
109    1.782584
110    1.721388
111    1.646210
112    1.611067
113    1.616929
114    1.586433
115    1.581460
116    1.468499
117    1.363606
118    1.266206
fundamental 
   Unnamed: 0        id         code  pe_ratio  turnover_ratio  pb_ratio  ps_ratio  pcf_ratio  capitalization  market_cap  circulating_cap  circulating_market_cap         day  pe_ratio_lyr
0           0  58842926  600068.XSHG    6.1095             NaN    0.8613     0.264    -8.2032       460477.75    273.5238        460477.75                273.5238  2020-10-02        5.0264


-----Stock trend report: 白云山-----
{'code': '600332.XSHG', 'display_name': '白云山', 'name': 'BYS', 'type': 'stock', 'parent': None}
above5: True
above20: True
above60: True
long arrange: False
ema5 bias: 2.03%
ema20 bias: -2.25%
ema5 > ema20: True
ema5 angle
0    14.913712
1    15.689533
2     0.797920
3     2.630971
4    46.864497
ema20 angle
0     0.423300
1     2.073672
2    -0.960409
3    -0.268781
4    16.274920
NATR
109    2.290150
110    2.237183
111    2.161124
112    2.075078
113    2.010978
114    1.996176
115    1.960134
116    1.982202
117    1.884676
118    2.240741
fundamental 
   Unnamed: 0        id         code  pe_ratio  turnover_ratio  pb_ratio  ps_ratio  pcf_ratio  capitalization  market_cap  circulating_cap  circulating_market_cap         day  pe_ratio_lyr
0           0  58843707  600332.XSHG   20.4035             NaN     1.964    0.7906    22.3721     162579.0938    490.8263      140589.0938                424.4385  2020-10-02       15.3918


-----Stock trend report: 上海银行-----
{'code': '601229.XSHG', 'display_name': '上海银行', 'name': 'SHYH', 'type': 'stock', 'parent': None}
above5: True
above20: True
above60: True
long arrange: False
ema5 bias: 0.26%
ema20 bias: 0.24%
ema5 > ema20: True
ema5 angle
0    2.245922
1    2.070104
2    0.616705
3    1.365821
4    1.864988
ema20 angle
0    0.087834
1    0.243169
2    0.001742
3    0.274411
4    0.521100
NATR
109    1.542799
110    1.490011
111    1.453183
112    1.492613
113    1.463176
114    1.489014
115    1.463425
116    1.434381
117    1.452409
118    1.476845
fundamental 
   Unnamed: 0        id         code  pe_ratio  turnover_ratio  pb_ratio  ps_ratio  pcf_ratio  capitalization  market_cap  circulating_cap  circulating_market_cap         day  pe_ratio_lyr
0           0  58844487  601229.XSHG    5.5824             NaN    0.7108      2.31     4.8913     1420652.875   1156.4114      1359614.375               1106.7261  2020-10-02        5.6973
```

## 项目结构

入口为main.py. 目前会筛选：

+ LongArrange: 多头排列
+ EMA20Bias: EMA20负向乖离过大
+ EMA5CrossEMA20: 短期均线上穿中期均线
+ 回踩EMA20,EMA60,EMA120
+ EMA20拐头

``` python
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
selector.filterChangeDirectionEMA20(
```

``` src
├── __init__.py
├── config.py
├── dataAnalyze.py 市场宽度
├── dataSource.py 数据源JQData
├── selector.py 股票筛选器
├── store.py 数据存储，待完成（MySQL or Mongo）
└── trend.py 个股趋势分析
```

## 已知的bug

1. 生成report时, 在生成行业市场宽度会有NaN. 解决方案：删除本地最新的report/daily-report-YYYY-MM-DD.txt, 再跑一边脚本。

## 如何贡献repo

1. 通过发PR的方式贡献代码
2. 开源社区可以选取TODO中, 自己愿意承担的任务，建立相应的issue，并assign给自己，进行开发
3. 有任何问题，直接提交issue即可

## TODO

1. 增加市场宽度图表
2. 增加美股数据源
3. 完善readme
4. 支持mysql或者mongo数据源
