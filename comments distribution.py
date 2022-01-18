import pandas as pd

df = pd.read_excel('/Users/lidiiamelnyk/Downloads/Копия youtube comments.xlsx', sheet_name= None)
df1 = pd.read_excel('/Users/lidiiamelnyk/Downloads/youtube comments.xlsx', sheet_name= None)
df2 = pd.read_excel('/Users/lidiiamelnyk/Downloads/geschlechtsveränderung.xlsx', sheet_name= None)

dictionaries = [df, df1, df2]
length_dictionary = {"Name":[],"Length":[]}
for element in dictionaries:
    for key, sub_df in element.items():
        l = 0
        for i, row in sub_df.iterrows():
            for k in str(row['Comment']).split('/n'):
                if k != 'nan':
                    l = l +1
            for m in str(row['Reply']).split('/n'):
                if m != 'nan':
                    l = l + 1
        length_dictionary['Name'].append(key)
        length_dictionary['Length'].append(l)
import matplotlib.pyplot as plt


print(sum(length_dictionary['Length']))
plt.ylabel('Length of the comment')
plt.xlabel('Number of comments')
plt.plot(sorted(length_dictionary['Length'], reverse = True))
plt.show()