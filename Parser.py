from output import *
import time

class Parser:
    # initialize parameters for stock graph information
    def __init__(self):
        self.data = []
        self.edges = []
        self.StEn = []
        self.Size = 0
        self.name = ""
        #self.numEdges = 0
        return

    # function who read a file from a path give in paramater
    def load(self, path):
        start_time = time.time()
        content = []
        tmp = path.split("/")
        self.name = tmp[-1][:-4]
        #debug(self.name)
        with open(path) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            line = content[1].split(' ')
            self.Size = int(line[0])
            #self.edges = int(line[1])

            #self.data = [[]]*(self.Size+1)

            for i in range(0,self.Size):
                self.data.append([])

            self.edges = 0
            last = 0

            # reading and stocking of edges from the file
            
            for i in range(2, len(content)):
                line = content[i].split(' ')
                self.data[int(line[0])-1].append(int(line[1])-1)
                self.data[int(line[1])-1].append(int(line[0])-1)
                self.edges += 1

            print("loading complete in %s seconds" % (time.time() - start_time ))
        return