#
# Genera grafos tipo mesh2D de n x m nodos
# ejecucion: python generaMesh2D.py archivo_salida n m
#
#
import sys
import networkx as nx


fileName = sys.argv[1]
n = int(sys.argv[2])
m = float(sys.argv[3])

G = nx.fast_gnp_random_graph(n,m)
W = nx.convert_node_labels_to_integers(G)

# Open a file
fo = open(fileName, "a")

heading = "%% random (%dx%f) \n" % (n, m)
fo.write(heading);
heading2 = "%d %d %d\n" % (W.number_of_nodes(), W.number_of_nodes(), W.number_of_edges())
fo.write(heading2);

for e in W.edges.data():
	arco = "%d %d\n" % (e[0]+1, e[1]+1)
	fo.write(arco)

# Close opend file
fo.close()