# -*- coding:UTF-8 -*-
"""
pandas hello word

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

s = pd.Series([1,3,5,np.nan,6,8])

print(s)

dates = pd.date_range('20130101', periods=6)
print(dates)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
print(df)

df2 = pd.DataFrame({ 'A' : 1.,
                'B' : pd.Timestamp('20130102'),
                'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
                'D' : np.array([3] * 4,dtype='int32'),
                'E' : pd.Categorical(["test","train","test","train"]),
                'F' : 'foo' })

print(df2)
print(df2.dtypes)

# Viewing Data

print(df.head())
print(df.tail(3))

#Display the index, columns, and the underlying numpy data
print(df.index)
print(df.columns)
print(df.values)
print(df.describe())

#Transposing your data 行列变化
print(df.T)

# 依据某一行
print(df.sort_index(axis=1, ascending=False))
#依据每一列的值进行排序
df.sort_values(by='B')

# Selecting a single column, which yields a Series, equivalent to df.A
print(df['A'])

# Selecting via [], which slices the rows.
print(df[0:3])
# Selection by Label
df.loc[dates[0]]
df.loc[:,['A','B']]
df.loc['20130102':'20130104',['A','B']]

df.loc['20130102',['A','B']]




