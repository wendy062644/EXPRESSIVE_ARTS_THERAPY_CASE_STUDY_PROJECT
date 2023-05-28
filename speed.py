import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

difficulty = "Easy"
fall_interval = 1.0  # 方块下落间隔时间（秒）
block_speed = 2.0
lives = 2
bullet_speed = 10

fig, ax1 = plt.subplots()
x = []
y1 = []
y2 = []
y3 = []

for i in np.arange(0, 600, 0.1):
    elapsed_time = round(i, 1)
    fall_interval_speed = fall_interval - math.sqrt(elapsed_time)*0.02 #生成方塊/秒
    block_speed_control = block_speed + math.sqrt(elapsed_time)*0.1  #方塊掉落速度
    bullet_speed_control = bullet_speed + math.sqrt(elapsed_time)*0.2 #子彈速度
    y1.append(fall_interval_speed)
    y2.append(block_speed_control)
    y3.append(bullet_speed_control)
    x.append(i)

ax1.plot(x, y1, label = '生成速度')
ax1.plot(x, y2, label = '掉落速度')
ax1.plot(x, y3, label = '子彈速度')
plt.legend()
plt.show()