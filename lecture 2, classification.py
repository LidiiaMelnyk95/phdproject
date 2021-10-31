import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv("/Users/lidiiamelnyk/Downloads/Train_rev1.csv", index_col=None)
data['Log1pSalary'] = np.log1p(data['SalaryNormalized']).astype('float32')

plt.figure(figsize=[8, 4])
plt.subplot(1, 2, 1)
plt.hist(data["SalaryNormalized"], bins=20);

plt.subplot(1, 2, 2)
plt.hist(data['Log1pSalary'], bins=20)
plt.show()