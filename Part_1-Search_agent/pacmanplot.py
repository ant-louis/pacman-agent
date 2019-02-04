from matplotlib import pyplot as plt
import numpy as np
def buildPlot(data, ylabel, filename):
    nb_maps = 3
    maps = ["small", "medium", "large"]
    algorithms = ["DFS", "BFS", "UCS", "A*"]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    nb_algo = 4
    bar_width = .15
    
    for j in range(nb_maps):
        plt.figure()
        plt.ylabel(ylabel)
        plt.xlabel("Map: {}".format(maps[j]))
        plt.xticks([])
        ax = plt.subplot(111)

        for i in range(nb_algo):
            plt.bar((0.05+ bar_width)*i, data[j][i], width=bar_width,color=colors[i])
            ax.legend(["{}".format(i) for i in algorithms],
                        loc='upper center', bbox_to_anchor=(0.5, -0.05),
                        fancybox=True, shadow=True, ncol=5)
        plt.savefig("{}_{}.svg".format(filename,maps[j]), format="svg", bbox_inches='tight',pad_inches=0.0)
        plt.show()


#[DFS BFS UCS A*]
small_layout_score = [500, 502, 502, 502]
small_layout_time = [0.00202, 0.00212, 0.00211, 0.00229]
small_layout_expanded = [15, 15, 15, 14]


#[DFS BFS UCS A*]
medium_layout_score = [414, 570, 570, 570]
medium_layout_time = [0.0749, 9.905, 8.941, 8.652]
medium_layout_expanded = [361, 16688, 12517, 11293]


#[DFS BFS UCS A*]
large_layout_score = [319, 434, 434, 434]
large_layout_time = [0.165, 0.859, 0.843, 0.630]
large_layout_expanded = [371, 1966, 1908, 1203]

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

buildPlot(run_times, "Running time (s)", "run_times")
buildPlot(total_expanded, "Number of expanded nodes", "total_expanded")
buildPlot(total_score, "Total score", "total_score")
