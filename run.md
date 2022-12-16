# 运行函数
### 运行实例
```python
from transmatrix.workflow.run_yaml import run_matrix
#运行回测函数
mat = run_matrix('project_signal/config.md')
from transmatrix.data_api import PanelDataBase
# 创建PanelDataBase
db = PanelDataBase()
```

```python
mat.strategies
```
```
Out:
{'ReverseSignal': <strategy.ReverseSignal at 0x7fe24158d340>}
```
```python
mat.evaluators
```
```
Out:
{'SimpleAlphaEval': <evaluator.Eval at 0x7fe1e0190ac0>}
```
```python
mat.evaluators['SimpleAlphaEval'].show()
```
