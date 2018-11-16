from matplotlib import pyplot as plt
import numpy as np



def buildPlot(data, ylabel, filename):
    nb_ghost_type = 3
    ghost_type = ["dumby", "greedy", "smarty"]
    algorithms = ["Minimax", "Alphabeta", "Hminimax"]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    nb_algo = 3
    bar_width = .15
    
    for j in range(nb_ghost_type):
        plt.figure()
        plt.ylabel(ylabel)
        plt.xlabel("Ghost type: {}".format(ghost_type[j]))
        plt.xticks([])
        ax = plt.subplot(111)

        for i in range(nb_algo):
            plt.bar((0.05+ bar_width)*i, data[j][i], width=bar_width,color=colors[i])
            ax.legend(["{}".format(i) for i in algorithms],
                        loc='upper center', bbox_to_anchor=(0.5, -0.05),
                        fancybox=True, shadow=True, ncol=5)
        plt.savefig("{}_{}.svg".format(filename,ghost_type[j]), format="svg", bbox_inches='tight',pad_inches=0.0)
        plt.show()

# Dumby ghost
##[Minimax, Alphabeta, Hminimax]
dumby_score = [526, 526, 526]
dumby_time = [0.0305, 0.0184, 0.0062]
dumby_expanded = [243, 149, 34]

# Greedy ghost
#[Minimax, Alphabeta, Hminimax]
greedy_score = [526, 526, 526]
greedy_time = [0.0302, 0.0183, 0.0059]
greedy_expanded = [243, 149, 34]

# Smarty ghost
#[Minimax, Alphabeta, Hminimax]
smarty_score = [526, 526, 526]
smarty_time = [0.0289, 0.0195, 0.0083]
smarty_expanded = [243, 149, 34]

total_score = [
    dumby_score,
    greedy_score,
    smarty_score
]

run_times = [
    dumby_time,
    greedy_time,
    smarty_time
]

total_expanded = [
    dumby_expanded,
    greedy_expanded,
    smarty_expanded
]

buildPlot(run_times, "Running time (s)", "run_times")
buildPlot(total_expanded, "Number of expanded nodes", "total_expanded")
buildPlot(total_score, "Total score", "total_score")
