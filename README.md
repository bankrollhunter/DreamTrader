# DreamTrader

## 简述

自动化按照技术形态选股. 自动筛选，诸如多头排列，破线，拐头，交叉，大幅乖离的股票。

## 如何使用

#### 本地部署

1. 创建JQData的账号。将config-example.json, 重命名. 并填入你的用户名和密码
2. 执行脚本 ./daily_analyse.sh

#### 报告

如果不想本地部署，可直接参考每天生成的报告[report](https://github.com/bankrollhunter/DreamTrader/tree/master/report)

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
