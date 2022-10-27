# 常用的矢量计算工具函数

### 代码所需要导入的库
    import pandas as pd
    import numpy as np
    from scipy.stats import zscore
    from statsmodels.stats.weightstats import DescrStatsW


### vec_norm - 按行进行归一化操作

    def vec_norm(df):  
        return pd.DataFrame(df.values / np.expand_dims(df.sum(axis = 1).values, -1), index = df.index, columns= df.columns)

### norm - 按列进行归一化操作

    def norm(ser):
        return ser / ser.sum()

### cross_universe - 同标签的矩阵点乘

    def cross_universe(df, universe):
        assert all(df.index == universe.index)
        assert all(df.columns == universe.columns)
        arr = df.values * universe.values
        return pd.DataFrame(arr, index = df.index, columns = df.columns)

### universe2list - 输出列之和大于0的列索引

    def universe2list(df):
        df = df.T
        I = np.squeeze(np.argwhere(df.values.sum(axis = 1) > 0))
        return list(df.iloc[I].index)

### keep_universe - 输出df[universe]    
    def keep_universe(df, universe):
        if type(universe) is list: 
            return df[universe]
        elif type(universe) is pd.DataFrame:
            return df[universe2list(universe)]
        else: 
            raise TypeError(f'unsupported universe type {type(universe)}')

### vec_top_weights - 输出前百分比因子值 
* 输入 

名称|类型|说明
---|---|---
df|DataFrame|因子暴露组合
percent|float|投资组合选取百分比（默认为0.1）
ascending|bool|因子升序规则（默认False）
universe|DataFrame|可投资股票池

    def vec_top_weights(df, percent = 0.1, ascending = False, universe = None):
        if universe: df = cross_universe(df, universe)   
        num = np.ceil(len(df.columns) * percent)

        if ascending: arr = df.rank(axis = 1).values
        else: arr = (-df).rank(axis = 1).values

        arr[arr <= num] = 1; arr[arr > num] = 0
        arr = arr / np.expand_dims(arr.sum(axis = 1), -1)
    
        return pd.DataFrame(arr, index=df.index, columns=df.columns)

### vec_longshort_weights - 输出因子多空组合
#### 输入 

名称|类型|说明
---|---|---
df|DataFrame|因子暴露组合
percent|float|投资组合两端百分比（默认为0.1）
ascending|bool|因子升序规则（默认False）
universe|DataFrame|可投资股票池

    def vec_longshort_weights(df, percent = 0.1, ascending = False, universe = None):
        if universe: df = cross_universe(df, universe) 
        num = np.ceil(len(df.columns) * percent)
    
        if  ascending: 
            long = df.rank(axis = 1).values
            short = (-df).rank(axis = 1).values
        else: 
            long = (-df).rank(axis = 1).values
            short = df.rank(axis = 1).values
        
        long[long <= num] = 1; long[long > num] = 0
        long = 0.5 * long / np.expand_dims(long.sum(axis = 1), -1)

        short[short <= num] = 1; short[short > num] = 0
        short = 0.5 * short / np.expand_dims(short.sum(axis = 1), -1)
        short = -short

    return pd.DataFrame(long + short, index=df.index, columns=df.columns)

### vec_quantile_weights - 输出按照因子暴露排序的投资组合
#### 输入 

名称|类型|说明
---|---|---
df|DataFrame|因子暴露组合
bins|int|分组数量（默认为10）
ascending|bool|因子升序规则（默认False）
universe|DataFrame|可投资股票池

#### 输出
* res：输出bins个按照因子暴露降序（或升序）排列的投资组合。


    def vec_quantile_weights(df, bins = 10, ascending = False, universe = None):
        if universe: df = cross_universe(df, universe) 
        num = np.ceil(len(df.columns) * 1 / bins)
        res = {}

        if ascending: rank = df.rank(axis = 1).values
        else: rank = (-df).rank(axis = 1).values

        for i in range(bins):
            arr = np.zeros_like(rank)
            start = i * num
            end = start + num
            arr[(start <= rank) & (rank < end)] = 1
            arr = arr / np.expand_dims(arr.sum(axis = 1), -1)
            res[i+1] = pd.DataFrame(arr, index=df.index, columns=df.columns)
        return res
    
### vec_rankIC - 输出因子的IC（信息系数）
#### 输入

名称|类型|说明
---|---|---
factor_panel|DataFrame|因子暴露
ret_panel|DataFrame|对应因子组合收益率

    def vec_rankIC(factor_panel: pd.DataFrame, ret_panel: pd.DataFrame):
        return factor_panel.T.corrwith(ret_panel.T, method = 'spearman').mean()

### vec_rankICIR - 计算因子的IC（信息系数）和IR（信息比率）
#### 输入

名称|类型|说明
---|---|---
factor_panel|DataFrame|因子暴露
ret_panel|DataFrame|对应因子组合收益率

    def vec_rankICIR(factor_panel: pd.DataFrame, ret_panel: pd.DataFrame):
        ser = factor_panel.T.corrwith(ret_panel.T, method = 'spearman')
        ic = ser.mean()
        ir = ic / ser.std()
        return ic, ir

### vec_zscore - 输出Z-Score处理后的因子值

def vec_zscore(df: pd.DataFrame):
    return zscore(df, axis = 1)

### vec_nav - 输出投资组合的加权累积收益率
#### 输入

名称|类型|说明
---|---|---
weights|DataFrame|投资组合投资权重
ret|DataFrame|对应投资组合股票收益率

    def vec_nav(weights: pd.DataFrame, ret:pd.DataFrame):
        nav = 1
        for w, r in zip(weights.values, ret.values):
            mult = (w * r).sum() + 1
            if np.isnan(mult): mult = 1
            nav *= mult
        return nav

### vec_nav_wt_ser - 输出投资组合的加权累积收益率与逐日加权累积收益率
#### 输入

名称|类型|说明
---|---|---
weights|DataFrame|投资组合投资权重
ret|DataFrame|对应因子组合收益率

def vec_nav_wt_ser(weights: pd.DataFrame, ret:pd.DataFrame):
    nav = 1
    nav_ser = []
    for w, r in zip(weights.values, ret.values):
        mult = (w * r).sum() + 1
        if np.isnan(mult): mult = 1
        nav *= mult
        nav_ser.append(nav)
    return nav, nav_ser


### vec_nav_sharp_mdd_wt_sers - 计算投资组合基本信息
#### 输入

名称|类型|说明
---|---|---
weights|DataFrame|投资组合权重
ret|DataFrame|组合对应股票收益率

#### 计算结果
* nav:组合累积收益率
* sharp：组合夏普比率
* mdd：最大回撤
* nav_ser：逐日累积收益率
* dd_ser：逐日回撤


    def vec_nav_sharp_mdd_wt_sers(weights: pd.DataFrame, ret:pd.DataFrame):
        """
        yearly sharp refers to: 
        https://stackoverflow.com/questions/2413522/weighted-standard-deviation-in-numpy
        """
        counter = 0
        nav = 1
        max_nav = 1
        nav_ser = []
        dd_ser = []
        yl_ret_ser = []
        yl_nav_ser = [1]

        for w, r in zip(weights.values, ret.values):

            counter += 1

        mult = (w * r).sum() + 1  #计算当期收益率
        if np.isnan(mult): mult = 1
        nav *= mult
        if nav > max_nav: max_nav = nav    
        dd_ser.append(nav-max_nav)   #计算回撤
        nav_ser.append(nav)

        if counter == 250:   #假设一年250天
            yl_ret_ser.append(nav / yl_nav_ser[-1] - 1)
            yl_nav_ser.append(nav)
            counter = 0

        if counter > 0:
            last_year_weight = counter / 250
            yl_ret_ser.append(250 / last_year_weight * (nav / yl_nav_ser[-1] - 1)) 

        weights = np.ones(len(yl_ret_ser))
        weights[-1] = last_year_weight
        reduce = DescrStatsW(np.array(yl_ret_ser) - 1, weights)
        sharp = reduce.mean / reduce.std
        mdd = np.min(dd_ser)    #最大回撤
        return nav, sharp, mdd, nav_ser, 

### melt - 输出投资组合的逆透视

    def melt(df, name):
        return df.reset_index().\
            melt(id_vars = ['index']).\
            rename(columns = {'index':'datetime','variable':'codes','value':name})
