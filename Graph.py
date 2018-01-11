import heapq
import sys

class Vertex:
    def __init__(self, data, index):
        self.data = data
        self.index = index

class Graph:

    def __init__(self, undirected=True):
        self.size = 0
        self.vList = []
        self.vMap = {}
        self.adjList = []
        self.undirected = undirected
        self.weights = {}

    def addEdge(self, v1, v2, weight):
        if v1 not in self.vMap:
            i1 = self.size
            self.size += 1
            self.addVertex(v1, i1)
        else: i1 = self.vMap[v1].index
        if v2 not in self.vMap:
            i2 = self.size
            self.size += 1
            self.addVertex(v2, i2)
        else: i2 = self.vMap[v2].index

        self.adjList[i1].add(i2)
        edge = str(i1) + "," + str(i2)
        self.weights[edge] = weight

        if(self.undirected):
            self.adjList[i2].add(i1)
            edge = str(i2) + "," + str(i1)
            self.weights[edge] = weight

    def addVertex(self, vData, index):
        vertex = Vertex(vData, index)
        self.adjList.append(set([]))
        self.vList.append(vertex)
        self.vMap[vData] = vertex

    def getNeighbors(self,v):
        if v<0 or v>=self.size:
            print('error: v index out of bounds')
            return set()
        return self.adjList[v]

    def getEdgeWeight(self,v1,v2):
        if v1 < 0 or v2 < 0:
            print('error: v index out of bounds')
            return 0
        edge = str(v1) + "," + str(v2)
        return self.weights[edge]

    def printGraph(self):
        print 'Number of Nodes = ', self.size
        for vertex in self.vList:
            data = vertex.data
            vId = vertex.index
            neighbors = self.getNeighbors(vId)
            print data, ' Connections = '
            for n in neighbors:
                neighbor = self.vList[n]
                print '   ', neighbor.data
            print ''

    #Depth first search:
    def dfs(self):
        time = 0
        visited = set()
        topList = []
        for v in self.vList:
            if v.index not in visited:
                self.dfsVisit(v.index, visited, topList)
        return topList
    def dfsVisit(self, vertexId, visited, topList):
        visited.add(vertexId)
        neighbors = self.getNeighbors(vertexId)
        for n in neighbors:
            if n not in visited:
                self.dfsVisit(n, visited, topList)
        topList.append(vertexId)

    def bfs(self, startVertexId):
        bfsList = []
        bfsVisited = set([])
        bfsList = self.bfsVisit(startVertexId, bfsVisited, bfsList)
        return bfsList
    def bfsVisit(self, vertexId, bfsVisited, bfsList):
        bfsVisited.add(vertexId)
        bfsList.append(vertexId)
        neighbors = self.getNeighbors(vertexId)
        for n in neighbors:
            if n not in bfsVisited:
                self.bfsVisit(n, bfsVisited, bfsList)
        return bfsList

    def buildShortestPathTable(self, source):
        distanceTable = {}
        predecessorTable = {}
        for i in range(len(self.vList)):
            distanceTable[i] = sys.maxint
            predecessorTable[i] = 'na'

        distanceTable[source] = 0
        predecessorTable[source] = 'na'
        visited = set()
        beenQueued = set()
        queue = [(0, source)]
        beenQueued.add(source)
        while len(queue) > 0:
            distInfo = heapq.heappop(queue)
            v = distInfo[1]
            vDist = distInfo[0]
            visited.add(v)
            neighbors = self.getNeighbors(v)
            for n in neighbors:
                if n not in visited:
                    nDist = vDist + self.getEdgeWeight(v,n)
                    currentDistance = distanceTable[n]
                    if nDist < currentDistance:
                        predecessorTable[n] = v
                        distanceTable[n] = nDist
                        #Update queue distance:
                        if n in beenQueued:
                            queue.remove((currentDistance, n))
                            heapq.heappush(queue, (nDist, n))

                    if n not in beenQueued:
                        heapq.heappush(queue, (nDist, n))

        self.distanceTable = distanceTable
        self.predecessorTable = predecessorTable

    def shortestPath(self,source, dest):
        if source not in self.vMap or dest not in self.vMap:
            return 'Path does not exist.'
        dest = self.vMap[dest].index #Get adjList index of destination
        source = self.vMap[source].index #Get adjList index of source
        self.buildShortestPathTable(source)
        stack = [self.vList[dest].data]
        currentVertex = self.predecessorTable[dest]
        while currentVertex != source:
            v = self.vList[currentVertex].data
            stack.insert(0, v)
            currentVertex = self.predecessorTable[currentVertex]
        stack.insert(0, self.vList[source].data)
        return stack

g = Graph()
g.addEdge(1,2,6)
g.addEdge(2,3,1)
g.addEdge(3,4,7)
g.addEdge(3,5,11)
g.addEdge(3,6,66)
g.addEdge(4,9,11)
g.addEdge(9,7,1)
g.addEdge(11,2,12)
g.addEdge(3,3,1)
g.addEdge(4,44,1)

path = g.shortestPath(1,11)
print path


''''''
