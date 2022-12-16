## 策略回测引擎
### Matrix 回测控制组件
- 配置回测信息

    代码示例
    ```python
    from transmatrix import SimMatrix, Scheduler
    from transmatrix.trader import BaseStrategy, StrategyConfig
    from transmatrix.utils.tools import get_universe

    # 获取可交易的股票池
    CODES = get_universe('project_simulation/custom_universe.pkl')
    config = SimMatrix.MatrixConfig(
        
        {   
            # 回测模式 ：模拟市场 / 信号交易
            'mode' : 'simulation', # signal

            # 回测区间 ：[开始时间， 结束时间]
            'backtest_span': ['2021-01-01','2021-12-31'],

            # 因子订阅 ： [因子名 ：[因子表名，股票代码列表，字段集合，初始化窗口（天）]]
            'factors' : {
                'macd' : ['factor_data__stock_cn__tech__1day__macd', CODES, 'value', 10]
            },

            # 账户参数 
            'ini_cash' : 1000000
            # 'market_type': 'stock_cn'
            # 'ini_positon' : {}
            # 'fee' : 0
        }
    )

    # 实例化回测控制器对象
    matrix = SimMatrix.BaseMatrix(config)
    ```


### Strategy 策略管理组件

- 代码示例
    ```python
    # 继承模板类
    class Strategy(BaseStrategy)
    # 在Strategy类下实现回调函数：
    # 行情更新时回调
    def on_market_data_update(self, market):

        data = market.data
        macd = self.macd.query(self.time, 3)['value'][self.codes].mean().sort_values()
        
        buy_codes = macd.iloc[:2].index

        for code in buy_codes:
            # 获取某只股票的仓位
            pos = self.account.get_netpos(code)

            if  pos < self.max_pos:
                price = data.get('close', code)
                self.buy(price, 100, 'open', code, market.name)
   ``` 
  ---
  ```python
    # 用户自定义回调 支持 定时、定频、条件触发等机制
    callback_per_50min = Scheduler.FixFreqScheduler(name ='fixTimeScheduler50min',freq = '50min', matrix = matrix) 
    callback_at_10and14 = Scheduler.FixTimeScheduler(name = 'fixfreq10_14',matrix = matrix, milestones= ['10:01:00','13:59:00'])
  ```  
  ---
  ```python
    # 编写定时定频回调逻辑
    # 回调执行逻辑：每50分钟
    def callback50min(self):
        #打印回测系统时间
        print('callback50min', self.time)
        
    # 回调执行逻辑：每天10点和14点
    def callback10and14(self):
        #打印回测系统时间
        print('callback10and14', self.time)
  ```
  --- 
  ```python
    # 配置策略参数

    strategy_cfg = StrategyConfig(
    {   
        # 策略名称
        'name': 'strategy0',

        # 订阅行情（用于on_market_data_update回调）
        'subscribe_info':[
            # 行情表名，代码列表
            ['market_data__stock_cn__bar__1day', CODES]
        ],

        'kwargs' : {
            'max_pos': 300
        }

        # 自定义做和引擎 ：引擎编写可开放给用户(基于transmatrix.Basematcher interface)
        # 'match_mod': 'DayMatcher' 

        # 设置 发单 / 撤单延迟 （模拟 交易系统 --> 交易所 延迟)
        # 'insert_deley' : '0ms'
        # 'cancel_deley' : '0ms',
        # 设置 回报延迟 （模拟 交易所 --> 交易系统 延迟)
        # 'receive_delay': '0ms',
    })
  ```
  ---
  ```python
    # 实例化策略对象，传入matrix以实现策略注册
    strategy = Strategy(strategy_cfg, matrix)
  ```
  ---
  ```python
    # 初始化回测引擎
    matrix.init()
  ```
  ---
  ```python
    # 运行回测
    matrix.run()
    # 日志输出
  ```
  --- 
  ![](btlog.png)
  <div align=center>日志截图</div>

  --- 
  ```python
    # 分析接口
    matrix.analyze()

    # 运行后在 strategy 对象的 post_trade_analysis属性中获得回测评价数据
  ```
  代码示例
  ```python
    In:
    strategy.post_trade_analysis.__dict__.keys()
  ```
  ---
  ```  
    Out:
    dict_keys(['trade_table', 'daily_position', 'daily_netvalue', 'summary_stats'])
  ```
  --- 
  ```python
    In: # 查询交易记录
    strategy.post_trade_analysis.trade_table
  ```
  ![](tradetable.png)
  <div align=center>交易记录查询结果</div>

  ```python
    In: # 查询每日持仓
    strategy.post_trade_analysis.daily_position
  ```
  ![](dailypos.png)
  <div align=center>每日持仓查询结果</div>
  
  ```python
    In: # 查询每日净值
    strategy.post_trade_analysis.daily_netvalue
  ```
  ![](dailynav.png)
  <div align=center>每日净值查询结果</div>


## 因子研究引擎
### 开发组件

- 回测组件导入
```python    
from transmatrix.matrix import SignalMatrix 
import sys; sys.path.append('project_signal')
```
- 用户代码导入
```python
from signal2weights import *            # 自定义函数库
from strategy import ReverseSignal      # 策略代码
from evaluator import Eval              # 策略评估代码
```
- 因子编写组件
  - 在项目目录下的strategy.py中编写策略
  - ReverseSignal继承了策略模板SignalStrategy

  代码示例
```python
  from transmatrix.matrix.signal.base import SignalStrategy
  from transmatrix.data_api import Array3dPanel
  from scipy.stats import zscore

  class ReverseSignal(SignalStrategy):
      # 回测开始前引擎自动运行pre_transform函数已完成用户定义的矢量计算
      def pre_transform(self):
          if 'reverse' not in self.pv.fields:
              pv = self.pv.to_dataframes()
              ret = (pv['close'] / pv['close'].shift(1) - 1).fillna(0)
              reverse = -ret.rolling(window = 5, min_periods = 5).mean().fillna(0)
              reverse = zscore(reverse, axis = 1)
              ap = (pv['open'] + pv['close'] + pv['high'] + pv['low']) / 4
              self.pv.concat(Array3dPanel.from_dataframes({'reverse' : reverse}))

      # 回测过程中用户根据用户自定义的clock（时间戳序列）回调 on_clock 函数已实现因子生成逻辑
      def on_clock(self):
        self.update_signal(self.pv.get(field = 'reverse', codes = '*'))
```

- 因子评价组件
  - 在项目目录下的evaluator.py中编写策略
  - Eval继承了策略模板BaseEvaluator

  代码示例
```python
    from signal2weights import *
    from transmatrix.matrix.signal.base import BaseEvaluator
    import matplotlib.pyplot as plt
    
    class Eval(BaseEvaluator):
    
    # 回测结束后引擎将评价组件订阅的数据与策略生成的信号进行撮合处理生成 critc_data
    # critc函数：基于 critic_data 对象计算因子评价结果。
    # _process_base, _process_500, _process_ind为具体计算逻辑（因空间所限未展示代码）
    # show函数：将评价结果可视化 （因空间所限未展示代码）

    def critic(self, critic_data):

        perf = {}
        perf.update(self._process_base(critic_data))

        stats = perf['stats']
        stats.update(self._process_500(critic_data))
        stats = pd.DataFrame(pd.Series(stats, name = 'VALUE'))
        stats.index.name = 'FIELD'
        perf['stats'] = stats

        perf.update(self._process_ind(critic_data))
        self.perf = perf
        return perf

    
    def show(self): 
        ...
```
  

### 参数设置
- 回测参数
```python
mat_config = {   
    # 回测模式 ：模拟市场 / 信号交易
    'mode' : 'signal', # simulation

    # 回测区间 ：[开始时间， 结束时间]
    # 'backtest_span': [str(START), str(END)],
    'backtest_span': [START, END],

    # 股票代码列表
    'universe': CODES,

    # 是否剔除结算价异常的股票
    'check_codes' : False,

    # 因子订阅 ： [因子名 ：[因子表名，股票代码列表，字段集合，初始化窗口（天）]]
    'data': {
        'pv'       : ['stock__bar__1day', CODES, 'open,high,low,close,volume', 10],
        'cashflow' : ['ashare_cashflow',  CODES, 'net_profit,invest_loss',     10] 
    },

    'clock': '09:35:00', #TODO：测试日内多笔交易。

    # 账户参数 
    'ini_cash' : 1000000        
}
```
- 策略参数
```python
stra_config = {
    'name': 'reverseSignal',
}
```
- 评价参数
```python
eval_config = {
    'name': 'simpleAlaphaEval',
    'data': {
        'pv':   ['stock__bar__1day',CODES, 'open,high,low,close,volume', 10],
        'meta': ['stock__meta', CODES, 'is_300,is_500,industry1', 10]
    }
}
```
### 执行回测
```python
mat = SignalMatrix(mat_config)
eval = Eval(eval_config, mat)
strategy = ReverseSignal(stra_config, mat)
mat.init()
mat.run()
```
### 评价报告
- 因子评价报告有多个模板可供选择，全部内容可见用户自开发组件[评价与展示](Evaluator.md)文档。
#### 评价模板1
ic分析和收益分析
```python
eval.show()
```
![](report.jpg)
<div align=center>ic分析和收益分析结果展示1</div>
