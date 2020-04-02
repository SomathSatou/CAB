from output import *

class Parser:
    def __init__(self):
        self.data = []
        self.edges = []
        self.StEn = []
        self.Size = 0
        #self.numEdges = 0
        return

    def load(self, path):
        content = []
        with open(path) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            line = content[1].split(' ')
            self.Size = int(line[0])
            #self.edges = int(line[1])

            #self.data = [[]]*(self.Size+1)

            for i in range(0,self.Size):
                self.data.append([])
                self.edges.append([])

            last = 0
            for i in range(2, len(content)):
                line = content[i].split(' ')
                self.data[int(line[0])-1].append(int(line[1]))
                self.data[int(line[1])-1].append(int(line[0]))

            print('loading complete')
        return