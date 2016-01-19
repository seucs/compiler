#coding=utf8
import matplotlib.pyplot as plt
from pylab import mpl

decision_node = dict(boxstyle="sawtooth", fc="0.8")
leaf_node = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-", connectionstyle="arc3")
# arrow_args = dict(facecolor='black', shrink=0.1)
# arrowprops = dict(facecolor = 'black', shrink = 0.1))


def setCh():
    # 指定默认字体
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # 解决保存图像时符号'-'显示为方块的问题
    mpl.rcParams['axes.unicode_minus'] = False


def plotNode(ax1, node_text, center_pt, parent_pt, node_type):
    ax1.annotate(
        s=node_text,  # 节点文本
        xy=parent_pt,  # 箭头始端坐标
        xycoords='axes fraction',  # string that indicates what type of coordinates 'xy' is
        xytext=center_pt,  # 节点中心坐标
        textcoords='axes fraction',  # string that indicates what type of coordinates 'text' is
        va='center',
        ha='center',
        bbox=node_type,
        arrowprops=arrow_args
    )


def createPlot():
    fig = plt.figure(num=1, facecolor="white")
    fig.clf()
    ax1 = plt.subplot(111, frameon=False)
    plotNode(
        ax1=ax1,
        node_text=u'AAA',
        center_pt=(0.5, 0.1),
        parent_pt=(0.1, 0.5),
        node_type=decision_node
    )
    plotNode(
        ax1=ax1,
        node_text=u'BBB',
        center_pt=(0.8, 0.1),
        parent_pt=(0.3, 0.8),
        node_type=leaf_node
    )
    plt.show()

if __name__ == "__main__":
    setCh()
    createPlot()