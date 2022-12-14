# TransMatrix配置文件说明
## yaml文件基本说明

- 用户可以在编程环境中以一个config.yaml作为入口进行一次回测研究  
命令行调用  :  Matrix -p CONFIG_PATH  
Python调用 :  transmatrix.matrix.run_matrix(CONFIG_PATH)  
支持通过 相对路径引用 .yaml/.pkl/.py/.pyc等格式的文件  
当引用 .yaml 格式的文件时，会将该文件第一层级下的同名字段加入引用位置  
当引用 .pkl  格式的文件时，系统会自动读取该文件并传入引用位置  
.py/.pyc 只允许在名为 "class" 的key下配置，用于定位用户自开发代码  
注意:为保障策在其他环境中可复现，建议用户不要引用config.yaml所在项目(关于项目的定义详见产品说明文档)外的文件

## 引用方法说明
* include  
引用其他yaml  
* 字段覆盖规则：  
    1: 任务入口文件具备最高优先级, i.e., 析出的配置中包含入口文件中的所有字段，任何被引用文件相应位置的信息都将被覆盖。  
    2: include 多个文件时， 先引用的文件优先级高于后饮用的文件
```yaml
include:  
    - [config-path1]  
    - [config-path2]  
```

## 投研引擎核心控制组件
```yaml
matrix:

    # 研究模式: 
        # signal:       股票alpha因子研究
        # simulation :  模拟交易
    mode: signal

    # 回测起止时间
    span: [2019-01-01, 2021-12-30]

    # 用户自定义的交易票池
    # e.g. 此处引用了同级别目录下的 xxx.pkl文件
    # 用户可以自行定义交易票池,以列表 列表、字符串或文件的形式传入
    universe: &universe custom_universe.pkl  

    
    # 触发因子计算逻辑的时间 [signal模式特有] 
    # e.g. '09:35:00'表示每天 09:35分进行计算一次因子
    # 一般而言clock时间应当与真实策略交易时间频率一致
    # 支持日内因子: e.g. '09:35:00,11:00:00,14:00:00'
    clock: '09:35:00'   

    # 数据订阅
    data:
        # 定义一个回测中可调用的数据结构
        # e.g.名称为pv, 则可以在策略代码中使用 .pv调取到该数据
        # 每个数据是一个 Array3dPanel 实例（api使用方式详见在线文档data-api部分)
        pv: 
            # 数据配置信息: 可以理解为一条SQL语句的
            - default                        # 数据库名 
            - stock_bar_daily                # 表名 
            - *universe                      # 股票代码范围
            - open,high,low,close,volume     # 选取字段
            - 10                             # 数据buffer窗口，单位：日 (回测引擎会自动查询回测开始时间之前N天的数据，以保障在回测开始时能够拿到因子计算所需的数据)
        
        # 可订阅多个数据结构,每个数据结构可为任意频率数据
        # e.g. 上面 pv 订阅了日线数据，而下述 ashare_cashflow为财报数据（季频）
        cashflow:
            - ashare_cashflow
            - *universe
            - net_profit,invest_loss
            - 10

        # "Signal" 为 TransMatrix系统关键字
        # 当配置 Signal 数据块时，系统自动进入"已入库因子评价"模式
        # 注意事项：1.此时应当保证 data 字段下面只有 Signal 一个数据块。 2.此时不允许

        # Signal:
            # - private_database
            # - daily_alpha_research
            # - macd
            # - *universe
            # - 0 

    # [signal模式特有][因子库项目特有]
    # 是否将因子保存至因子库 【关于因子库的定义详见产品文档】
    # 目标表为因子所在因子库项目对应的因子表
    # 系统自动将因子(对应表的字段) 命名为strategy字段下的策略名（见下方strategy部分）
    save_signal: False

    # [signal模式特有]
    # 是否自动调用 evaluator.show()方法
    # 系统支持多种因子评价报告模板(详见测试用例 project_signal_templeteA/B/C/D)
    show_report: True

    # ---------------------------------------------------------------------------------------------------
    # 是否输出系统日志 （日志默认保存在config.yaml入口文件同级目录下的 log 文件夹中)
    logging: False

    # 全局变量（在回测运行的过程中不可修改)
    # 调用方式: Matrix实例 调用 .context, Strategy / evaluator 实例调用 .matrix_context
    context:
        long  : 26
        short : 12
        diff  : 9
    # ---------------------------------------------------------------------------------------------------
```
    

## 策略代码组件
```yaml
# 用户通过继承 SignalStrategy（因子研究）或 BaseStrategy（模拟交易） 编写策略逻辑

# 【注意】：当 matrix:data 下面配置了 Signal 字段时，系统自动进入"已入库因子评价"模式，该模式下无需用户编写策略（不允许配置strategy）
strategy:

    # 策略名 [signal模式下为因子名]
    reverse_signal:
        # 策略代码信息
        class: 
            # 代码文件路径, 支持.py / .pyc 等python代码文件，
            # 支持相对路径 e.g. ../strategy.py 为 config.yaml所在路径的上一级目录下的strategy.py文件
            - strategy.py   
            # 类名
            - ReverseSignal
    
    # 可配置多个策略
    # trendy_signal:
        # class: 
            # - strategy.py
            # - TrendySignal

# 因子评价组件（分析器） [signal模式特有]
# 用户通过继承 BaseEvaluator 实现因子分析逻辑
```

## 分析器组件
* 【注意】：系统允许 config.yaml 中不包含 analyzer 字段，此时系统自动进入因子计算模式，该模式下系统只负责生产因子（供后续用户自行分析或落库等操作使用）

```yaml
analyzer:

    # 分析器名称
    SimpleAlphaEval:

        # 分析器配置信息
        class:
            # 代码文件路径, 支持.py / .pyc 等python代码文件，
            - evaluator.py
            # 类名
            - Eval
        
        # 数据订阅
        data: 
            # 定义一个回测中可调用的数据结构（与matrix下的data字段配置方式一致）
            # 注意：系统保证了 analyzer 下订阅的数据在策略回测过程中不会被strategy调用
            # 因子 analyzer 原则上可以订阅 收益率 等未来信息，而不必担心未来函数问题

            # 数据配置信息: 可以理解为一条SQL语句的
            pv: 
                - default        
                - stock_bar_daily
                - *universe
                - open,high,low,close,volume
                - 10
            meta:
                - default
                - stock_meta_temp
                - *universe
                - is_300,is_500,industry1
                - 10
        
    # 可配置多个分析器 
    # 例如:
    # DefalutEvaluator:
        # class:
            # - ../evaluator.py
            # - EvalFull
        # data: 
            # pv: 
                # - default
                # - stock_returns
                # - *universe
                # - close2close,vwap2vwap
                # - 0
        # benchmark: ['000300.SH']
```

