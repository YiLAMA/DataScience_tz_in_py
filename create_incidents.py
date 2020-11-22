import numpy as np
import pandas as pd

M = 10
N = 100
df = pd.DataFrame({'feature1': np.random.randint(M, size=(N,)),
                   'feature2': np.random.randint(M, size=(N,)),
                   'time': np.random.rand(N)
                   })

df.to_csv('incidents/incidents100M10.csv', index_label='id')
