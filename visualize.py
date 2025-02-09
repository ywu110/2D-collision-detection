import matplotlib.pyplot as plt

from datastruct import KDTree
from simulation import Ball



list_points = [(3, 6), (17, 15), (13, 15), (6, 12), (9, 1), (2, 7), (10, 19)]
list_balls = [Ball(x, y, 1, 0, 0, "red") for x, y in list_points]

tree = KDTree(list_balls)

def plot_tree(node, ax, min_x, max_x, min_y, max_y):
    if node is None:
        return
    
    if node.plane == 0:
        # plot the node point
        ax.plot(node[0], node[1], 'ro')
        ax.text(node[0], node[1], f"({node[0]}, {node[1]})", 
        horizontalalignment='center',
        verticalalignment='bottom',
        color='blue')
        # plot the vertical line
        ax.plot([node[0], node[0]], [min_y, max_y], 'o-')
        plot_tree(node.left, ax, min_x, node[0], min_y, max_y)
        plot_tree(node.right, ax, node[0], max_x, min_y, max_y)
    else:
        # plot the node point
        ax.plot(node[0], node[1], 'ro')
        ax.text(node[0], node[1], f"({node[0]}, {node[1]})", 
        horizontalalignment='center',
        verticalalignment='bottom',
        color='blue')
        # plot the horizontal line
        ax.plot([min_x, max_x], [node[1], node[1]], 'o-')
        plot_tree(node.left, ax, min_x, max_x, min_y, node[1])
        plot_tree(node.right, ax, min_x, max_x, node[1], max_y)
    
fig, ax = plt.subplots()
ax.set_xlim(0, 20)
ax.set_ylim(0, 20)
plot_tree(tree.root, ax, 0, 20, 0, 20)
plt.show()