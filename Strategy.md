# 策略代码
### 代码所需要导入的库
    from transmatrix.matrix.signal.base import SignalStrategy
    from transmatrix.data_api import Array3dPanel
    from scipy.stats import zscore
###  策略引用
    class ReverseSignal(SignalStrategy):

### pre_transform - 一个简单的策略
* 将近五个交易日的收益率进行平均，得到 reverse 因子

    
    def pre_transform(self):
        pv = self.pv.to_dataframes()
        ret = (pv['close'] / pv['close'].shift(1) - 1).fillna(0)
        reverse = -ret.rolling(window = 5, min_periods = 5).mean().fillna(0)  #近五个交易日收益率的平均
        reverse = zscore(reverse, axis = 1)
        self.pv.concat(Array3dPanel.from_dataframes({'reverse': reverse}))
        
    def on_clock(self):
        self.update_signal(self.pv.get(field = 'reverse', codes = '*'))