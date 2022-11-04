# Transmatrix 使用手册
## 数据库操作
### Database
> 连接数据库类
- properties:
  >名称|类型|说明
  >----|----|----
  jdbc_http_proxy|String|jdbc代理服务器url,如"localhost:9009"
  real_conn|String|timelyre数据库url,如"jdbc:hive2://localhost:10600/"
  db_name|String|数据库名称
  source|String|数据表类型,如"timelyre"
- methods:
- show_tables 显示数据库全部表名
- 代码样例
```
    In: 
    from transmatrix.data_api import Database
    db = Database()
    db.show_tables()
```
---
```
    Out:
    ['ashare_cashflow',
    'benchmark',
    'factor_data__stock_cn__tech__1day__macd',
    'factor_data__stock_cn__tech__1day__macd_xxx',
    'factor_data__stock_cn__tech__1day__macd_yyy',
    'future_cn__bar__1min',
    'market_data__future_cn__bar__1min',
    'market_data__stock_cn__bar__1day',
    'market_data__stock_cn__bar__1s',
    'market_data__stock_cn__bar__30min',
    'market_data__stock_cn__bar__3s',
    'market_data__stock_cn__tick__1s',
    'match_info__stock_cn__tick__1s',
    'meta_data__future_cn__1day',
    'stock__bar__1day',
    'stock__bar__1day_new',
    'stock__bar__1day_new2',
    'stock__meta',
    'stock_names',
    'stock_names_mapper',
    'test_insert',
    'trade_calendar']
```
- show_column_info 显示数据表字段数据类型
    - 参数:
        >名称|类型|说明
        >----|----|----
        table_name|String|数据表名
- 代码样例
```
    In:
    db.show_column_info('stock__bar__1day')
```
---
```
    Out:
    ['datetime DATETIME',
    'open NUMERIC',
    'high NUMERIC',
    'low NUMERIC',
    'close NUMERIC',
    'volume NUMERIC',
    'amount NUMERIC',
    'code CHAR']
```
- create_table 在数据库中建表
    - 参数:
        >名称|类型|说明
        >----|----|----
        table_name|String|数据表名
        table_type|String|数据表类型
        column_info|Dict/String|字段信息,如{'datetime':'timestamp',<br>'high':'float','low':'float',<br>'open':'float','close':'float'}
        timecol|String|时序列列名
        tags|String|索引列列名
        uniqcols|String|主键字段,联合主键写在同一字符串中用','号隔开
- 代码样例
```
    In:
    db.create_table('stock_data','timelyre',<br>column_info={'datetime':'timestamp','high':'float','low':'float','open':'float','close':'float','code':'string'},timecol='datetime',tags='code')
```
---
```
    Out:
```
- delete_table 删除数据表
    - 参数:
        table_name|String|数据表名
- 代码样例
```
    In:
    db.delete('stock_data')
```
---
```
    Out:
```
- insert_value 插入数据
    - 参数:
        >名称|类型|说明
        >----|----|----
        table_name|String|数据表名
        value|String/tuple/list|待插入数据
- 代码样例
```
    In:
    db.insert_value('stock_data',('2021-01-01 09:01:00',100.1,80.1,90.1,95.1,'002140.SH'))
```
---
```
    Out:
```
- insert_values 批量插入数据
    - 参数:
      >名称|类型|说明
      >----|----|----
      table_name|String|数据表名
      values|List/tuple/dataframe|插入数据
- 代码样例
```
    In:
    data = [['2021-01-01 09:02:00',110.1,85.2,93.1,96.4,'002140.SH'],
            ['2021-01-01 09:03:00',109.4,89.3,94,99.2,'002140.SH']]
    db.insert_values('stock_data', data)
```
- insert_df 插入dataframe数据
    - 参数
      >名称|类型|说明
      >----|----|----
      table_name|String|数据表名
      df|dataframe|插入数据,dataframe格式
- 代码样例
```
    In:
    import pandas as pd
    data = pd.DataFrame(data, columns=['datetime','high','low','open','close','code'])
    db.insert_df('stock_data', data)
```
- load_csv 导入csv文件到数据表
    - 参数
      >名称|类型|说明
      >----|----|----
      table_name|String|数据表名
      path|String|csv文件路径
      skip_head|bool|是否删除表头
- 代码样例
```
    In:
    path = '/root/test.csv'
    db.load_csv('stock_data', path)
```
- query 查询数据表
    - 参数
      >名称|类型|说明
      >----|----|----
      table_name|String|数据表名
      fields|List/String|字段名
      start|String/date/datetime|查询起始时间
      end|String/date/datetime|查询截止时间
      universe|String/List|查询代码
- 代码样例
```
    In:
    df = db.query('stock__meta',start='2022-08-01',end='2022-08-04',fields='insdustry2,market',universe='000004.SZSE,000065.SZSE')
    print(df)
```
---
```
    Out:
            insdustry2 market         code            datetime
    0       软件服务    深主板  000004.SZSE 2022-08-01 15:00:00
    1       软件服务    深主板  000004.SZSE 2022-08-02 15:00:00
    2       软件服务    深主板  000004.SZSE 2022-08-03 15:00:00
    3       建筑工程    深主板  000065.SZSE 2022-08-01 15:00:00
    4       建筑工程    深主板  000065.SZSE 2022-08-02 15:00:00
    5       建筑工程    深主板  000065.SZSE 2022-08-03 15:00:00
```
- query_calendar 查询交易日
    - 参数
    >名称|类型|说明
    >----|----|----
    start|String|查询起始日期
    end|String|查询截止日期
    exchange|String|交易所名称
    table_name|String|交易日存储表名
- 代码样例
```
    In:
    dates = db.query_calendar('2022-09-01','2022-09-20',exchange='SSE',table_name='trade_calendar')
    print(dates)
```
---
```
    Out:
    [datetime.date(2022, 9, 1), datetime.date(2022, 9, 2), datetime.date(2022, 9, 5),
    datetime.date(2022, 9, 6), datetime.date(2022, 9, 7), datetime.date(2022, 9, 8),
    datetime.date(2022, 9, 9), datetime.date(2022, 9, 13), datetime.date(2022, 9, 14),
    datetime.date(2022, 9, 15), datetime.date(2022, 9, 16), datetime.date(2022, 9, 19),
    datetime.date(2022, 9, 20)]
```
## 数据api
### 代码所需要导入的库
    from IPython.core.interactiveshell import InteractiveShell 
    InteractiveShell.ast_node_interactivity = "all"
    from datetime import datetime, date, timedelta
    import pandas as pd
    import numpy as np

### 数据库与数据结构
#### Dataset
>用于描述一个数据集合
- 参数:
    >名称|类型|说明
    >---|---|---
     table_name|String|表名
     strat_time/end_time|[str, datetime, date] |开始 / 结束 时间 
     codes|list（指定集合） / '*'（取表中所有代码） / None(defualt, 取表中所有代码)|股票代码集合
     fields|list（指定集合） / '*'（取表中所有字段） / None(defualt, 取表中所有字段)|字段集合
     panel_catagory|'price-volume' / 'finance-report', defalut|区分是否是财报数据
  - methods:
      - load_data 加载数据
- 样例


    In：
    from transmatrix.data_api import Dataset

    dataset = Dataset(
        table_name = 'stock__bar__1day',
        start_time = '20210101',
        codes = ['000001.SZSE','000002.SZSE'],
        fields = ['open','high','low','close','volume'],
        end_time = '20210120',
    ).load_data()

    type(dataset)
    Out:





---
---
#### Array3dPanel
 > 数据集合对象
 - properties:
    >名称|说明
    >---|---
     data | ndarray 数据
     idx  | 时间戳序列
     fields | 字段集合
     codes  | 代码集合
     cursor | 当前游标位置 <br>初始化为-1，由回测引擎控制。 <br> 给定回测引擎时间T，游标为idx中T时刻之前最新一条数据对应的序号。
 - 样例


    In：
    type(dataset.data)
    dataset.data.shape
    dataset.idx
    dataset.fields
    dataset.codes
    dataset.cursor

    Out:
    numpy.ndarray
    (12, 5, 2)
    {Timestamp('2021-01-04 15:00:00'): 0,
    Timestamp('2021-01-05 15:00:00'): 1,
    Timestamp('2021-01-06 15:00:00'): 2,
    Timestamp('2021-01-07 15:00:00'): 3,
    Timestamp('2021-01-08 15:00:00'): 4,
    Timestamp('2021-01-11 15:00:00'): 5,
    Timestamp('2021-01-12 15:00:00'): 6,
    Timestamp('2021-01-13 15:00:00'): 7,
    Timestamp('2021-01-14 15:00:00'): 8,
    Timestamp('2021-01-15 15:00:00'): 9,
    Timestamp('2021-01-18 15:00:00'): 10,
    Timestamp('2021-01-19 15:00:00'): 11}

    {'low': 0, 'volume': 1, 'close': 2, 'high': 3, 'open': 4}
   
    {'000001.SZSE': 0, '000002.SZSE': 1}

    -1


--- 
- 构造方法:
    - 1. 利用 Dataset.load_data （见上文）
    - 2. from_dataframes
        - 类方法
        - 通过形为 {name : pd.Dataframe} 的字典实例化数据集合

- 样例


    In:
    from transmatrix.data_api import Array3dPanel

    idx = list(pd.date_range('20210101 09:30:00','20210105 09:30:00'))
    codes = ['000001.SZSE','000002.SZSE']

    panelA = pd.DataFrame(index = idx, columns = codes).fillna(1) 
    panelB = pd.DataFrame(index = idx, columns = codes).fillna(2) 

    panel3d = Array3dPanel.from_dataframes({'A': panelA, 'B': panelB})

    panel3d.data.shape
    panel3d.idx
    panel3d.fields
    panel3d.codes

    Out:
    (5, 2, 2)

    {Timestamp('2021-01-01 09:30:00'): 0,
    Timestamp('2021-01-02 09:30:00'): 1,
    Timestamp('2021-01-03 09:30:00'): 2,
    Timestamp('2021-01-04 09:30:00'): 3,
    Timestamp('2021-01-05 09:30:00'): 4}

    {'A': 0, 'B': 1}

    {'000001.SZSE': 0, '000002.SZSE': 1}

---
- methods: 转化为字典
    - to_dataframes

- 样例


    In：
    panel3d.to_dataframes()

    Out:
    {'A':                      000001.SZSE  000002.SZSE
    2021-01-01 09:30:00            1            1
    2021-01-02 09:30:00            1            1
    2021-01-03 09:30:00            1            1
    2021-01-04 09:30:00            1            1
    2021-01-05 09:30:00            1            1,
    'B':                      000001.SZSE  000002.SZSE
    2021-01-01 09:30:00            2            2
    2021-01-02 09:30:00            2            2
    2021-01-03 09:30:00            2            2
    2021-01-04 09:30:00            2            2
    2021-01-05 09:30:00            2            2}
---

- concate: 向数据中加入新的字段 (同频拼接)
    - 参数: other(dataframe)

- 样例


    In:
    other = Array3dPanel.from_dataframes(
        {
            'C':pd.DataFrame(index = idx, columns = codes).fillna(3),
            'D':pd.DataFrame(index = idx, columns = codes).fillna(4),
        }
    )
    panel3d.concat(other)

    panel3d.data.shape
    panel3d.idx
    panel3d.fields
    panel3d.codes

    Out:
    (5, 4, 2)
    {Timestamp('2021-01-01 09:30:00'): 0,
    Timestamp('2021-01-02 09:30:00'): 1,
    Timestamp('2021-01-03 09:30:00'): 2,
    Timestamp('2021-01-04 09:30:00'): 3,
    Timestamp('2021-01-05 09:30:00'): 4}
    {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    {'000001.SZSE': 0, '000002.SZSE': 1}

---
- calibrate: 匹配timestamps, 保留有效数据。
    对于timestamps 中的任意一个时间戳, 匹配该时间之后的第一条数据。
    - 参数: tiemstamps(datetime)
-样例
  


    In:
    '校准后:'
    panel3d.calibrate(clock_steps)
    panel3d.data.shape
    panel3d.to_dataframes()

    Out:
    '校准后:'
    (5, 2, 2)
    {'twap':                      000001.SZSE  000002.SZSE
    2021-01-01 09:35:00            1            1
    2021-01-02 09:35:00            1            1
    2021-01-03 09:35:00            1            1
    2021-01-04 09:35:00            1            1
    2021-01-05 09:35:00            1            1,
    'vwap':                      000001.SZSE  000002.SZSE
    2021-01-01 09:35:00            2            2
    2021-01-02 09:35:00            2            2
    2021-01-03 09:35:00            2            2
    2021-01-04 09:35:00            2            2
    2021-01-05 09:35:00            2            2}

---
### 数据查询接口
- query: 通过外部时间查询最新数据
  - 参数: 
    >名称|类型|说明
    >---|---|---
     time|datetime|表名
     periods |int | 返回N条数据
     start_time |datetime | 返回某时刻之后的数据
     window |timedelta | 返回一段时间的数据
    
  - 输出: 形如 {filed_name : dataframe}的字典

-样例


    In:
    panel3d.query(datetime(2021,1,4,9,36), periods = 3)

    Out:
    {'twap':                      000001.SZSE  000002.SZSE
    2021-01-02 09:35:00            1            1
    2021-01-03 09:35:00            1            1
    2021-01-04 09:35:00            1            1,
    'vwap':                      000001.SZSE  000002.SZSE
    2021-01-02 09:35:00            2            2
    2021-01-03 09:35:00            2            2
    2021-01-04 09:35:00            2            2}
    
    In:
    panel3d.query(datetime(2021,1,4,9,36), start_time = datetime(2021,1,3,9,30))

    Out:
    {'twap':                      000001.SZSE  000002.SZSE
    2021-01-03 09:35:00            1            1
    2021-01-04 09:35:00            1            1,
    'vwap':                      000001.SZSE  000002.SZSE
    2021-01-03 09:35:00            2            2
    2021-01-04 09:35:00            2            2}

    In:
    panel3d.query(datetime(2021,1,4,9,36), window = timedelta(days=2))

    Out:
    {'twap':                      000001.SZSE  000002.SZSE
    2021-01-03 09:35:00            1            1
    2021-01-04 09:35:00            1            1,
    'vwap':                      000001.SZSE  000002.SZSE
    2021-01-03 09:35:00            2            2
    2021-01-04 09:35:00            2            2}


---
- get: 返回某个字段 *游标* 位置最新一条数据
    - 参数:
    >名称|类型
    >---|---
     fileds|[string]
     codes |[string] /string /* / None
    - 输出: array / float

- 样例


    In:
    panel3d.cursor = 3
    panel3d.get(field = 'twap')
    panel3d.get(field = 'twap', codes = '000001.SZSE')

    Out:
    array([1, 1])

    1

---
- get_fields: 返回多个字段 *游标* 位置最新一条数据
    - 参数:
    >名称|类型
    >---|---
     fileds|[string]
     codes |[string] /string /* / None

- 样例


    In:
    twap, vwap = panel3d.get_fields(['twap','vwap'])
    twap, vwap

    Out:
    (array([1, 1]), array([2, 2]))

---
- get_window:返回某个字段 *游标* 位置最新一条数据
    - 参数:
    >名称|类型|说明
    >---|---|---
     length|int|窗口长度
     filed |string| 字段名
     codes |[string]/ string/ * / None | 代码列表

- 样例


    In:
    twap = panel3d.get_window(3,'twap')
    vwap = panel3d.get_window(3,'vwap')
    {'twap': twap,
    'vwap': vwap}
    Out:
    {'twap': array([[1, 1],
    [1, 1],
    [1, 1]]),
    'vwap': array([[2, 2],
    [2, 2],
    [2, 2]])} 



### 因子数据接口


    from transmatrix.data_api import Array3dPanel

    pv = strategy.pv
    pv : Array3dPanel  # [时间，字段，股票代码]

    f'fields: {pv.fields}' # 通过 fields 属性查看 数据中包含的字段

    # 转为df字典:
    dfs = pv.to_dataframes()
    dfs.keys()

    # 通过字段名访问相应的因子
    dfs['close'].head()

    #每个dataframe的行列索引一致：行为时间， 列为股票代码
    assert all(dfs['close'].index == dfs['open'].index)
    assert all(dfs['close'].columns == dfs['open'].columns)

    Out:
    "fields: {'high': 0, 'close': 1, 'low': 2, 'open': 3, 'volume': 4, 'reverse': 5}"
    dict_keys(['high', 'close', 'low', 'open', 'volume', 'reverse'])
    DataFrame 暂略
* concat方法


    from transmatrix.data_api import Array3dPanel

    pv = strategy.pv.copy()
    # 模拟插入2个字段场景
    new1 = pd.DataFrame(
       np.random.randn(*pv.shape), 
       index = pv.pdidx, columns = pv.codes
    )
    new2 = pd.DataFrame(
        np.random.randn(*pv.shape),
        index = pv.pdidx, columns = pv.codes
    )

    f'转化前: {pv.fields}'
    pv.concat(
        Array3dPanel.from_dataframes(
                {
                    'new1':new1,
                    'new2':new2,
                }
        )
    )
    f'转化后: {pv.fields}'

    Out:
    "转化前: {'high': 0, 'close': 1, 'low': 2, 'open': 3, 'volume': 4, 'reverse': 5}"
    "转化后: {'high': 0, 'close': 1, 'low': 2, 'open': 3, 'volume': 4, 'reverse': 5, 'new1': 6, 'new2': 7}"


### 行情查询接口
* 1.查询一条数据
  * 1.1 返回所有股票的close值 
  >pv.get('close‘)

  * 样例


    In:
    close_slice = pv.get('close') 
    close_slice; close_slice.shape

    Out:
    array([16.82, 19.12, 19.6 , ..., 16.4 ,  6.66,  5.46])
    (3474,)


  * 1.2 返回某只股票的close值
    >pv.get('close', code)
  * 样例


    In:
    close_slice = pv.get('close','000001.SZSE') 
    close_slice

    Out:
    16.82


  * 1.3 返回部多只票的close值
    >pv.get('close', list(codes))

  * 样例


    In:
    close_slice = pv.get('close',['000001.SZSE','000002.SZSE']) 
    close_slice

    Out:
    array([16.82, 19.12])

  * 1.4 返回全部股票的多个字段
    >pv.get_fields(['close','open'])
    
  * 样例


    In:
    close_slice, open_slice = pv.get_fields(['close','open']) 
    f'close : {close_slice}, shape = {close_slice.shape}'
    f'open  : {open_slice},  shape = {open_slice.shape}'

    Out:
    'close : [16.82 19.12 19.6  ... 16.4   6.66  5.46], shape = (3474,)'
    'open  : [16.76 19.35 19.38 ... 16.32  6.44  5.23],  shape = (3474,)'


  * 1.5 返回单只股票的多个字段
    >pv.get_fields(['close','open'], code)
  
  * 样例


    In:
    close_slice, open_slice = pv.get_fields(['close','open'],'000001.SZSE')
    f'close : {close_slice}'
    f'open  : {open_slice}'

    'close : 16.82'
    'open  : 16.76'

  * 1.6 返回多只股票的多个字段
    >pv.get_fields(['close','open'], list(code))
  * 样例


    In:
    close_slice, open_slice = pv.get_fields(['close','open'],['000001.SZSE','000002.SZSE'])
    f'close : {close_slice}'
    f'open  : {open_slice}'

    Out:
    'close : [16.82 19.12]'
    'open  : [16.76 19.35]'



* 2. 查询多条数据'


    pv.cursor = 100

  * 1.1 返回所有股票的close值'
    >pv.get_window(period, 'close')
     
  * 样例


    In:
    close_array = pv.get_window(10, 'close') 
    close_array
    f'shape: {close_array.shape}'

    Out:
    array([[12.92, 28.02, 21.4 , ...,  8.89,  9.89,  5.72],
        [12.85, 28.13, 21.42, ...,  8.91,  9.63,  5.82],
        [12.44, 27.36, 20.45, ...,  8.5 ,  8.75,  5.52],
        ...,
        [12.35, 26.82, 21.25, ...,  7.57,  8.99,  5.45],
        [12.37, 27.  , 23.1 , ...,  7.8 ,  9.33,  5.63],
        [12.49, 27.62, 23.44, ...,  7.68,  9.23,  5.63]])
    'shape: (10, 3474)'


  * 1.2 返回某只股票的close值' 
    >pv.get_window(period, 'close',code) 
    
  * 样例


    In:
    close_array = pv.get_window(10, 'close','000001.SZSE') 
    close_array
    f'shape: {close_array.shape}'

    Out:



  * 1.3 返回部多只票的close值' 
    >pv.get_window(10, 'close',list(code)) 

  * 样例


    In:
    close_array = pv.get_window(10, 'close',['000001.SZSE','000002.SZSE']) 
    close_array
    f'shape: {close_array.shape}'

    Out:
    array([[12.92, 28.02],
        [12.85, 28.13],
        [12.44, 27.36],
        [12.38, 27.26],
        [12.56, 27.52],
        [12.4 , 27.36],
        [12.29, 26.72],
        [12.35, 26.82],
        [12.37, 27.  ],
        [12.49, 27.62]])
    'shape: (10, 2)'



### 财务数据接口

    from transmatrix.data_api import FinancePanelData  #引入财报数据的接口
    from datetime import datetime, timedelta
    time = datetime(2021,11,1)

* cashflow.query - 财报数据查询接口
  >cashflow.query(time, periods/window/start_time)
  * 样例
  
    
    In： 
    strategy.cashflow.query(time,periods = 4)
    strategy.cashflow.query(time,window = timedelta(days = 90 * 3))
    strategy.cashflow.query(time,start_time = datetime(2021,3,1))

    Out:
    长表格 略

## 因子研究引擎
### 模块导入
- 相关包导入
```
from IPython.core.interactiveshell import InteractiveShell 
InteractiveShell.ast_node_interactivity = "all"
import pickle
from datetime import date
```
- 回测组件导入
```
from transmatrix.matrix import SignalMatrix 
import sys; sys.path.append('project_signal')
```
- 用户代码导入
```
from signal2weights import *            # 自定义函数库
from strategy import ReverseSignal      # 策略代码
from evaluator import Eval              # 策略评估代码
```
### 参数设置
- 回测参数
```
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
```
stra_config = {
    'name': 'reverseSignal',
}
```
- 评价参数
```
eval_config = {
    'name': 'simpleAlaphaEval',
    'data': {
        'pv':   ['stock__bar__1day',CODES, 'open,high,low,close,volume', 10],
        'meta': ['stock__meta', CODES, 'is_300,is_500,industry1', 10]
    }
}
```
### 执行回测
```
mat = SignalMatrix(mat_config)
eval = Eval(eval_config, mat)
strategy = ReverseSignal(stra_config, mat)
mat.init()
mat.run()
```
### 评价数据
```
critc = strategy.critic_data['simpleAlaphaEval']
critc.keys()
critc['open'].head()
idx = critc['open'].index
col = critc['open'].columns
for df in critc.values(): 
    assert all(df.index == idx)
    assert all(df.columns == col)
eval.show()
```
- Out:
```
stats
                              VALUE
FIELD                              
Factor                      reverse
dates       2019-01-02 ~ 2021-12-30
ICMean                     0.031483
ICIR                       0.249612
TopRetTol                  0.454342
TopRetYL                    0.15581
TopSharpYL                 0.643648
TopMdd                    -0.426957
LRetTol                    0.475413
LSRetYL                    0.163036
LSSharpYL                  0.587572
LSMdd                     -0.108428
ICMean_500                 0.020579
ICIR_500                   0.136651
```
```
history
                     top_nav_ser  top_dd_ser  ls_nav_ser  ls_dd_ser
2019-01-02 09:35:00     0.991502   -0.008498    1.002249   0.000000
2019-01-03 09:35:00     1.018063    0.000000    1.005035   0.000000
2019-01-04 09:35:00     1.040050    0.000000    1.004872  -0.000164
2019-01-07 09:35:00     1.040096    0.000000    1.008196   0.000000
...
2021-12-30 09:35:00     1.454342    0.000000    1.475413  -0.003520
[729 rows x 4 columns]
```
![](eval_result.png)
```
                IC        IR
汽车        0.033415  0.228193
有色金属      0.026542  0.132984
房地产       0.039574  0.237196
机械        0.035178  0.272614
商贸零售      0.025890  0.160810
计算机       0.036651  0.256086
纺织服装      0.031159  0.173879
建材        0.030335  0.160413
银行        0.026005  0.086392
煤炭        0.041114  0.168604
交通运输      0.032781  0.190664
通信        0.042726  0.245770
电力设备及新能源  0.034581  0.236672
电子        0.035033  0.234525
国防军工      0.042172  0.212301
电力及公用事业   0.049894  0.272249
家电        0.033847  0.190110
传媒        0.027724  0.173397
石油石化      0.033474  0.140050
食品饮料      0.012830  0.065597
钢铁        0.031554  0.139091
非银行金融     0.040312  0.177449
消费者服务     0.029505  0.137259
农林牧渔      0.029716  0.137623
...
轻工制造      0.028279  0.186095
基础化工      0.029878  0.209850
医药        0.023873  0.156810
建筑        0.044323  0.269292
```
- 添加因子
```
import numpy as np
import pandas as pd
from transmatrix.data_api import Array3dPanel
pv = strategy.pv
pv : Array3dPanel  # [时间，字段，股票代码]
f'fields: {pv.fields}' # 通过 fields 属性查看 数据中包含的字段
dfs = pv.to_dataframes()
dfs.keys()
dfs['close'].head() # 通过字段名访问相应的因子
assert all(dfs['close'].index == dfs['open'].index)   #每个dataframe的行列索引一致：行为时间， 列为股票代码
assert all(dfs['close'].columns == dfs['open'].columns)
'concat方法'
pv = strategy.pv.copy()
new1 = pd.DataFrame(                            # 模拟插入2个字段场景
       np.random.randn(*pv.shape), 
       index = pv.pdidx, columns = pv.codes
)
new2 = pd.DataFrame(
       np.random.randn(*pv.shape), 
       index = pv.pdidx, columns = pv.codes
)
f'转化前: {pv.fields}'
pv.concat(
      Array3dPanel.from_dataframes(
            {
                  'new1':new1,
                  'new2':new2,
            }
      )
)
f'转化后: {pv.fields}'
```
- Out:
```
'concat方法'
"转化前: {'volume': 0, 'high': 1, 'low': 2, 'open': 3, 'close': 4, 'reverse': 5}"
"转化后: {'volume': 0, 'high': 1, 'low': 2, 'open': 3, 'close': 4, 'reverse': 5, 'new1': 6, 'new2': 7}"
```
- 回测内部数据查询
```
'查询接口：根据回测引擎内部时间，查询最新数据'
'1.查询一条数据'
print('_'*80)
'1.1 返回所有股票的close值' 
close_slice = pv.get('close') 
close_slice; close_slice.shape
print('_'*80)
'1.2 返回某只股票的close值' 
close_slice = pv.get('close','000001.SZSE') 
close_slice
print('_'*80)
'1.3 返回部多只票的close值' 
close_slice = pv.get('close',['000001.SZSE','000002.SZSE']) 
close_slice
print('_'*80)
'1.4 返回全部股票的多个字段'
close_slice, open_slice = pv.get_fields(['close','open']) 
f'close : {close_slice}, shape = {close_slice.shape}'
f'open  : {open_slice},  shape = {open_slice.shape}'
print('_'*80)
'1.5 返回单只股票的多个字段'
close_slice, open_slice = pv.get_fields(['close','open'],'000001.SZSE')
f'close : {close_slice}'
f'open  : {open_slice}'
print('_'*80)
'1.6 返回多只股票的多个字段'
close_slice, open_slice = pv.get_fields(['close','open'],['000001.SZSE','000002.SZSE'])
f'close : {close_slice}'
f'open  : {open_slice}'
print('_'*80)
```
- Out:

```
'查询接口：根据回测引擎内部时间，查询最新数据'
'1.查询一条数据'
'1.1 返回所有股票的close值'
array([16.81999969, 19.12000084, 19.60000038, ..., 16.39999962,
        6.65999985,  5.46000004])
(3474,)
'1.2 返回某只股票的close值'
16.81999969482422
'1.3 返回部多只票的close值'
array([16.81999969, 19.12000084])
'1.4 返回全部股票的多个字段'
'close : [16.81999969 19.12000084 19.60000038 ... 16.39999962  6.65999985\n  5.46000004], shape = (3474,)'
'open  : [16.76000023 19.35000038 19.37999916 ... 16.31999969  6.44000006\n  5.23000002],  shape = (3474,)'
'1.5 返回单只股票的多个字段'
'close : 16.81999969482422'
'open  : 16.760000228881836'
'1.6 返回多只股票的多个字段'
'close : [16.81999969 19.12000084]'
'open  : [16.76000023 19.35000038]'
```
---
```
'2. 查询多条数据'
pv.cursor = 100
print('_'*80)
'1.1 返回所有股票的close值' 
close_array = pv.get_window(10, 'close') 
close_array
f'shape: {close_array.shape}'
print('_'*80)
'1.2 返回某只股票的close值' 
close_array = pv.get_window(10, 'close','000001.SZSE') 
close_array
f'shape: {close_array.shape}'
print('_'*80)
'1.3 返回部多只票的close值' 
close_array = pv.get_window(10, 'close',['000001.SZSE','000002.SZSE']) 
close_array
f'shape: {close_array.shape}'
print('_'*80)
```
- Out:
```
'2. 查询多条数据'
'1.1 返回所有股票的close值'
array([[12.92000008, 28.02000046, 21.39999962, ...,  8.89000034,
         9.89000034,  5.71999979],
       [12.85000038, 28.12999916, 21.42000008, ...,  8.90999985,
         9.63000011,  5.82000017],
       [12.43999958, 27.36000061, 20.45000076, ...,  8.5       ,
         8.75      ,  5.51999998],
       ...,
       [12.35000038, 26.81999969, 21.25      , ...,  7.57000017,
         8.98999977,  5.44999981],
       [12.36999989, 27.        , 23.10000038, ...,  7.80000019,
         9.32999992,  5.63000011],
       [12.48999977, 27.62000084, 23.44000053, ...,  7.67999983,
         9.22999954,  5.63000011]])
'shape: (10, 3474)'
'1.2 返回某只股票的close值'
array([12.92000008, 12.85000038, 12.43999958, 12.38000011, 12.56000042,
       12.39999962, 12.28999996, 12.35000038, 12.36999989, 12.48999977])
'shape: (10,)'
'1.3 返回部多只票的close值'
array([[12.92000008, 28.02000046],
       [12.85000038, 28.12999916],
       [12.43999958, 27.36000061],
       [12.38000011, 27.26000023],
       [12.56000042, 27.52000046],
       [12.39999962, 27.36000061],
       [12.28999996, 26.71999931],
       [12.35000038, 26.81999969],
       [12.36999989, 27.        ],
       [12.48999977, 27.62000084]])
'shape: (10, 2)'
```
- 财务数据查询
```
from transmatrix.data_api import FinancePanelData
from datetime import datetime, timedelta
time = datetime(2021,11,1)
strategy.cashflow.query(time,periods = 4)
strategy.cashflow.query(time,window = timedelta(days = 90 * 3))
strategy.cashflow.query(time,start_time = datetime(2021,3,1))
```
- Out:
![](financial_result.png)