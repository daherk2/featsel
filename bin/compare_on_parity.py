import os
import argparse
import numpy as np
import subprocess
import re
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

import plotly
import plotly.graph_objs as go


# Initial definitions
algorithms = ["pucs", "spec_cmi"]
alg_color = {"pucs" : "red", "spec_cmi" : "blue"}
z_order = {"pucs" : 1, "spec_cmi" : 2}
cost_functions = {"pucs" : "mce", "spec_cmi" : "mce"}
gen_parity_path = "/home/gustavo/cs/machine_learning_data/" + \
        "parity_problem/gen_parity_instance.py"


# Parsing parameters
parser = argparse.ArgumentParser (description = 'Compares feature' + \
        'selection algorithms on parity machine learning problems.')
parser.add_argument ("n0", type = int, 
        help = "Minimum number of features.")
parser.add_argument ("nf", type = int, 
        help = "Maximum number of features.")
parser.add_argument ("ns", type = int, 
        help = "Number of features step.")
parser.add_argument ("sample_size", type = int, 
        help = "Number of samples in each training set.")
parser.add_argument ("m", type = int, 
        help = "Number of repetitions.")
args = parser.parse_args()
min_n = args.n0
max_n = args.nf
n_step = args.ns
sample_size = args.sample_size
m = args.m

# Define the number of points in the graph (on each dimension)
n_points = int ((max_n - min_n) / n_step) + 1


# Defines k
min_k = int (.25 * min_n + 1)
max_k = int (.75 * max_n + 1)
k_step = int ((max_k - min_k) / n_points) + 1

x = np.arange (min_n, max_n + 1, n_step)
y = np.arange (min_k, max_k + 1, k_step)
X, Y = np.meshgrid (x, y)
alg_Z = {}
for alg in algorithms:
    alg_Z[alg] = np.zeros ((len (y), len (x)))

n_i = 0
k_i = 0
for n in range (min_n, max_n + 1, n_step):
    for k in range (min_k, max_k + 1, k_step):

        if (k >= n):
            continue

        print ("n = " + str (n) + " and k = " + str (k))
        avg_error = {}
        for alg in algorithms:
            avg_error[alg] = 0.0

        for i in range (m):
            # generate problem input
            tst_size = int (sample_size * .5)
            dataset_name = 'parity_' + str (n) + "_" + str (k) + \
                "_" + str (i) + ".dat"
            dataset_file = "input/tmp/" + dataset_name
            trn_dataset_file = "input/tmp/trn_" + dataset_name
            tst_dataset_file = "input/tmp/tst_" + dataset_name
            sys_call = 'python ' + " ".join (str (x) for x in 
                [gen_parity_path, n, k, sample_size + tst_size]) + \
                " > " + dataset_file
            os.system (sys_call)
            os.system ("head -n " + str (sample_size) + " " + \
                dataset_file + " > " + tst_dataset_file)
            os.system ("tail -n " + str (tst_size) + " " + 
                dataset_file + " > " + trn_dataset_file)
            
            # validate with each algorithm
            for alg in algorithms:
                # Performs feature selection
                result = subprocess.check_output (["bin/featsel", 
                     "-f", trn_dataset_file,
                     "-n", str (n),
                     "-l", "2",
                     "-c", cost_functions[alg],
                     "-a", alg])
                result = result.decode ()
                matching = re.search ('<(\d+)\>\s+\:\s+(\S+)', result)
                selected_features = matching.group (1)
                
                # Validates 
                result = subprocess.check_output (["perl",
                    "bin/svm_validation.pl", trn_dataset_file,
                    tst_dataset_file, str (n), selected_features])
                result = result.decode ()
                matching = re.search ('.*:\s+(\d+\.?\d*).*', result)
                v_error = float (matching.group (1))
                avg_error[alg] += v_error

        for alg in algorithms:
            print ("For n = " + str (n) + ", k = " + str (k) + " and alg = " + alg)
            avg_error[alg] /= m
            print (avg_error[alg])
            print ("\n")
            alg_Z[alg][k_i][n_i] = avg_error[alg]

        k_i = k_i + 1
    k_i = 0
    n_i += 1

# fig = plt.figure ()
# ax = plt.axes (projection='3d')
    
# alg = "pucs"
# for alg in algorithms:
#     Z = alg_Z[alg]
#     ax.plot_surface (X, Y, Z, color=alg_color[alg], alpha=.7, zorder=z_order[alg])    

# plt.xlabel ("Number of features")
# plt.ylabel ("Number of relevant features")
# plt.title ('Average error on parity learning')
# plt.show()

surf_data1 = [
    go.Surface(x=X, y=Y, z=alg_Z["pucs"], 
        autocolorscale=False,
        colorscale=[[0, 'rgba(0, 0,0, 0)'], [1, 'rgba(255,0,0, .4)']],
        cmin=-1 ,
        cmax=-1,
        ids=["Number of features", "Number of relevant features", "Average error"],
        showscale=False),
    go.Surface(x=X, y=Y, z=alg_Z["spec_cmi"], 
        autocolorscale=False,
        colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(50,50,200, .4)']],
        cmin=-1,
        cmax=-1,
        showscale=False)
]

layout = go.Layout (
    title='Average error on Parity problem',
    scene=dict (
        
        xaxis=dict (
            title='Number of features.'
        ),
        yaxis=dict (
            title='Number of relevant features.',
        ),
        zaxis=dict (
            title='Average error.',
        )
    )
)

fig1 = go.Figure (data=surf_data1, layout=layout)
plotly.offline.plot(fig1)