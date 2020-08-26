from output import *

import os

listname = ["cycle_50",
            "cycle_200",
            "toroidalmesh_4",
            "toroidalmesh_15",
            "hamming4x5x5",
            "hamming2x2x5x6x7",
            "mesh9_9",
            "mesh50_20",
            "path_50",
            "path_200",
            "3dmesh_2_2_3",
            "3dmesh_4_4_68",
            "double_star_15_5",
            "double_star_40_20",
            "hypercube_4_16",
            "hypercube_7_128",
            "cbt_30",
            "cbt_500",
            "D-bcsstk01.mtx",
            "ash85.mtx",
            "662_bus.mtx",
            "caterpillar_5_4",
            "caterpillar_10_6",
            "random-graph-250-01",
            "random-graph-750-05",
            "R-dwt_503.mtx",
            "jgl009.mtx",
            "p1_100",
            "p21_200"
            ]

listname = [
    "3dmesh_2_2_3",
    "3dmesh_4_4_68",
    "662_bus.mtx",
    "ash85.mtx",
    "caterpillar_5_4",
    "caterpillar_10_6",
    "cbt_30",
    "cbt_500"
]

for elt in listname:
    os.system('./mutator.sh '+elt+'&')
