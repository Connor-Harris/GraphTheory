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
        print('Number of Nodes = ', self.size)
        for vertex in self.vList:
            data = vertex.data
            vId = vertex.index
            neighbors = self.getNeighbors(vId)
            print(data, ' Connections = ')
            for n in neighbors:
                neighbor = self.vList[n]
                print('   ', neighbor.data)
            print()

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

    #Breadth first search
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

    #Dijkstra's single source shortest path algorithm
    def buildShortestPathTable(self, source):
        distanceTable = {}
        predecessorTable = {}
        for i in range(len(self.vList)):
            distanceTable[i] = sys.maxsize
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

    #Returns the shortest path from source to dest vertices (if a path exists).
    #Dijkstra's algorithm DOES NOT work with negative edges.
    def shortestPath(self,source, dest, buildTable=True):
        if source not in self.vMap or dest not in self.vMap:
            return 'Path does not exist.'
        dest = self.vMap[dest].index #Get adjList index of destination
        source = self.vMap[source].index #Get adjList index of source
        if buildTable:
            self.buildShortestPathTable(source)
        stack = [self.vList[dest].data]
        currentVertex = self.predecessorTable[dest]
        while currentVertex != source:
            v = self.vList[currentVertex].data
            stack.insert(0, v)
            currentVertex = self.predecessorTable[currentVertex]
        stack.insert(0, self.vList[source].data)
        return stack


    #Prim's Algorithm
    # @return: A new Graph object that represents
    #           a minimum spanning tree for this graph
    def minSpanTree(self):
        if self.size == 0:
            return Graph(undirected=True)

        mst = Graph(undirected=True)

        s = 0
        edgeQueue = []
        inMST = set([s])
        beenQueued = set([])

        sNeighbors = self.getNeighbors(s)
        for n in sNeighbors:
            w = self.getEdgeWeight(s, n)
            edge = (w, (s,n))
            heapq.heappush(edgeQueue, edge)
            beenQueued.add(edge)

        while len(edgeQueue) > 0:
            edge = heapq.heappop(edgeQueue)
            weight = edge[0]
            v1 = edge[1][0]
            v2 = edge[1][1]

            #Check if this should be skipped.
            if v1 in inMST and v2 in inMST: continue

            v1d = self.vList[v1].data
            v2d = self.vList[v2].data
            mst.addEdge(v1d,v2d,weight)
            if v1 not in inMST: inMST.add(v1)
            if v2 not in inMST: inMST.add(v2)

            if len(inMST) == self.size:
                return mst

            neighbors = self.getNeighbors(v2)
            for n in neighbors:
                w = self.getEdgeWeight(v2, n)
                nEdge = (w, (v2,n))
                if nEdge not in beenQueued:
                    heapq.heappush(edgeQueue, nEdge)
                    beenQueued.add(nEdge)

    #Returns the sum of all edge-weights
    def getTreeWeight(self):
        totalWeight = 0
        counted = set()
        for i in range(len(self.adjList)):
            for n in self.adjList[i]:
                if (i,n) in counted:
                    continue
                w = self.getEdgeWeight(i, n)
                totalWeight += w
                counted.add((i,n))
                if self.undirected:
                    counted.add((n,i))
        return totalWeight
