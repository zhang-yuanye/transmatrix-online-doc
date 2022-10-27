# 运行函数
### 运行实例
    from transmatrix.workflow.run_yaml import run_matrix
    #运行回测函数
    mat = run_matrix('project_signal/config.yaml')
    from transmatrix.data_api import PanelDataBase
    # 创建PanelDataBase
    db = PanelDataBase()
* show_tables() - 展示什么呢……


    In:
    db.show_tables()

    Out:
    ['ashare_cashflow',
     'benchmark',
     'cash_dividend',
     'dividend_info',
     'ex_factor_data',
     'factor_data__stock_cn__bar__1s__matchinfo',
     'factor_data__stock_cn__fundamental__1day__pe_ratio',
     'factor_data__stock_cn__fundamental__1day__roe',
     'factor_data__stock_cn__tech__1day__macd',
     'factor_data__stock_cn__tech__1day__momentum',
     'factor_data__stock_cn__tech__1s__matchinfo',
     'factor_data__stock_cn__tech__2s_matchinfo',
     'factor_data__stock_cn__tech__30min__rsi',
     'factor_data__stock_cn__tech__bar__1day__bolling_down',
     'factor_data__stock_cn__tech__bar__1s__matchinfo',
     'ipo_date_data',
     'is_st_data',
     'is_suspended_data',
     'market_data__future_cn__bar__1min',
     'market_data__future_cn__tick__1s',
     'market_data__future_cn__tick__2s',
     'market_data__future_cn__tick__500ms',
     'market_data__stock_cn__bar__1day',
     'market_data__stock_cn__bar__1day__special',
     'market_data__stock_cn__bar__1day__sse__table_for_performance__pre',
     'market_data__stock_cn__bar__1min',
     'market_data__stock_cn__bar__1s',
     'market_data__stock_cn__bar__2s',
     'market_data__stock_cn__bar__30min',
     'market_data__stock_cn__bar__3s',
     'market_data__stock_cn__bar__4s',
     'market_data__stock_cn__bar__5min',
     'market_data__stock_cn__tick__1s',
     'market_data__stock_cn__tick__2s',
     'market_data__stock_cn_fqtest__bar__1day',
     'match_info__future_cn__tick__1s',
     'match_info__future_cn__tick__2s',
     'match_info__future_cn__tick__500ms',
     'match_info__stock_cn__bar__1s',
     'match_info__stock_cn__bar__2s',
     'match_info__stock_cn__tick__1s',
     'match_info__stock_cn__tick__2s',
     'meta_data__future_cn__1day',
     'split_info',
     'stock__bar__1day',
     'stock__meta',
     'stock_dividend',
     'stock_names',
     'stock_names_mapper',
     'tick_matcher_test',
     'trade_calendar']

    mat.strategies
    Out:
    {'ReverseSignal': <strategy.ReverseSignal at 0x7fe24158d340>}
    
    mat.evaluators

    Out:
    {'SimpleAlphaEval': <evaluator.Eval at 0x7fe1e0190ac0>}

    mat.evaluators['SimpleAlphaEval'].show()