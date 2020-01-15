import matplotlib.pyplot as plt
import numpy as np

# x=np.arange(2)
# #数据集
# y1=[0.3756378817393345,0.439613179]
# y2=[0.044776057,0.016285403]
# #误差列表
# std_err1=[0.268591239,0.187222041]
# std_err2=[0.112354063,0.0704330924060792]
# tick_label=['lightsalmon', 'lightseagreen']
#
# error_params1=dict(elinewidth=1,ecolor='black',capsize=1)#设置误差标记参数
# error_params2=dict(elinewidth=1,ecolor='black',capsize=1)#设置误差标记参数
# #设置柱状图宽度
# bar_width=0.4
# #绘制柱状图，设置误差标记以及柱状图标签
# plt.bar(x,y1,bar_width,color=['lightsalmon', 'lightseagreen'],yerr=std_err1,error_kw=error_params1,label='tag A')
# plt.bar(x+bar_width,y2,bar_width,color=['lightsalmon', 'lightseagreen'],yerr=std_err2,error_kw=error_params2,label='tag B')
# ax.set_xticklabels(('A', 'B', 'C', 'D', 'E'))
#
# plt.xticks(x+bar_width/2,tick_label)#设置x轴的标签
# #设置网格
# plt.grid(True,axis='y',ls=':',color='r',alpha=0.3)
# #显示图例
# plt.legend()
# #显示图形
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

n_groups = 2
# specialTrialData
# meansBeforeAwayMidlineByNoise = [0.465197681979688,0.454545454545454]
# stdBeforeAwayMidlineByNoise = [0.0300109377451112,7.93016446160826E-18]
#
# meansAfterAwayMidlineByNoise = [0.0812113791186189,0]
# stdAfterAwayMidlineByNoise = [0.0165817876636744,0]

# totalTrialData
# meansBeforeAwayMidlineByNoise = [0.334969269512538,0.20738174048174]
# stdBeforeAwayMidlineByNoise = [0.0459495658908522,0.0330138819015878]
#
# meansAfterAwayMidlineByNoise = [0.0441573093640124,0.0154007936507936]
# stdAfterAwayMidlineByNoise = [0.005566417968126444,0.00385452346000212]


# meansFirstIntentionStep=[6.941176471,6]
# stdFirstIntentionStep=[2.955086931,0]

consist = [0.71153846, 0.28846154]
inconsist = [0, 1]


fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = ax.bar(index, consist, bar_width,
                error_kw=error_config, color=['lightsalmon', 'lightsalmon'],
                label='human')

rects2 = ax.bar(index + bar_width, inconsist, bar_width,
                error_kw=error_config, color=['lightseagreen', 'lightseagreen'],
                label='model')
ax.set_xlabel('consist and inconsist')
ax.set_ylabel('ratio')
ax.set_title('first intention predict final goal')
ax.set_xticks(index)
ax.set_xticklabels(('consist', 'inconsist'))
ax.legend()

# rects1 = ax.bar(index, meansFirstIntentionStep, bar_width,
#                 alpha=1, color=['lightsalmon', 'lightseagreen'],
#                 yerr=stdFirstIntentionStep, error_kw=error_config,
#                )
# ax.set_xlabel('participants')
# ax.set_ylabel('step')
# ax.set_title('speical trial first intention step')
# ax.set_xticks(index )
# ax.set_xticklabels(('human','model'))
# ax.legend()
# fig.tight_layout()

plt.show()
