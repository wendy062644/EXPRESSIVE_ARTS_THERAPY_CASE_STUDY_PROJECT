import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv')
difficulty = input('Choose Difficulty (Easy. Normal. Hard.): ')
df = df[df['Difficulty'] == difficulty]
df = df.reset_index(drop=True)

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

plt.title(difficulty)
ax1.bar(df.index.values, df['Score'], color = 'tab:blue') #柱狀圖
ax1.tick_params(axis='y', labelcolor = 'tab:blue') #定義左側數字顏色
ax1.set_ylabel('Score', c = 'tab:blue') #左側Y軸名稱

ax2.plot(df.index.values, df['Elapsed Time'], c = 'tab:red') #折線圖
ax2.tick_params(axis='y', labelcolor = 'tab:red') #定義右側數字顏色
ax2.set_ylabel('Time(s)', c = 'tab:red') #右側Y軸名稱
plt.show()