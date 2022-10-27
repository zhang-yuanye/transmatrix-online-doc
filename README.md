# 数据api文档
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


