from matplotlib import pyplot as plt
import numpy as np
def buildPlot(title, array, ylabel, filename):
    nb_maps = 3
    maps = ["small", "medium", "large"]
    algorithms = ["dfs", "bfs", "ucs", "astar"]
    colors = ['#a7d49b', '#92ac86', '#696047', '#55251d']
    nb_algo = 4
    bar_width = .5
    
    for j in range(nb_maps):
        plt.figure(figsize=(8, 5))
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel("Map: {}".format(maps[j]))
        plt.xticks([])

        for i in range(nb_algo):
            plt.bar(0.+bar_width*i, array[j][i], width=bar_width,color=colors[i])
            plt.legend(["Algo {}".format(i) for i in algorithms])

        plt.savefig("{}_{}.svg".format(filename,maps[j]), format="svg")
        plt.show()


#[DFS BFS UCS A*]
small_layout_score = [500, 502, 502, 666]
small_layout_time = [0.00146, 0.00172, 0.00168, 0.00666]
small_layout_expanded = [15, 16, 16, 15]


#[DFS BFS UCS A*]
medium_layout_score = [414, 570, 570, 570]
medium_layout_time = [0.0512, 7.695, 8.245, 6.000]
medium_layout_expanded = [326, 17432, 53390, 53000]


#[DFS BFS UCS A*]
large_layout_score = [319, 434, 434, 434]
large_layout_time = [0.111, 0.619, 0.966, 0.966 ]
large_layout_expanded = [378, 2134, 2000, 2000 ]

total_score = [
    small_layout_score,
    medium_layout_score,
    large_layout_score
]

run_times = [
    small_layout_time,
    medium_layout_time,
    large_layout_time
]

total_expanded = [
    small_layout_expanded,
    medium_layout_expanded,
    large_layout_expanded
]

buildPlot("Running times of different search algorithms", run_times, "Running time (s)", "run_times")
buildPlot("Total number of expanded nodes for different search algorithms", total_expanded, "Number of expanded nodes", "total_expanded")
buildPlot("Total score for different search algorithms", total_score, "Total score", "total_score")
