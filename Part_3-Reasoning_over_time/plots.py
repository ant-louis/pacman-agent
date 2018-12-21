import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

w_list = [1, 3, 5]
p_list = [0.0, 0.3, 0.5, 0.7, 1.0]

for w in w_list:
    for p in p_list:
        entropy = []
        for i in range(50):
            sample = pd.read_csv("Entropy_csv/Entropy_w{}_p{}_{}.csv".format(w,p,i))
            entropy.append(np.array(sample))
        average = np.mean(entropy, axis=0)
        std = np.std(entropy, axis=0)
        plt.plot(range(1,50),average, marker='s', mew=0.3, ms=3)

    plt.title('Variation of entropy when w = {}'.format(w), fontsize = '10')
    plt.legend(['p = 0.0','p = 0.3','p = 0.5','p = 0.7', 'p = 1.0'], fontsize = '10')
    plt.xlabel("Number of steps", fontsize='10')
    plt.ylabel("Entropy", fontsize='10')
    plt.savefig("Graphs/GraphEntropy{}.evs".format(w))

    plt.close()
            
