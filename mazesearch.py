from mazetree import *
import math
import time
from collections import deque

class Search:
    SEARCH_NAME = {
        'astar' : 'A*',
        'bfs' : 'Breadth-first search',
        'gbfs' : 'Greedy Best-first search',
        'dfs' : 'Depth-first search',
    }
    def __init__(self, maze, method=None, heuristic=None, dist_func='manhattan'):
        self.maze = maze
        self.mazename = maze.filename.split('/')[-1].split('.')[0]
        self.mazetree = MazeTree(maze)

        self.methodname = self.SEARCH_NAME[method]
        self.method = method

        self.open_set = deque()
        self.closed_set = list()
        
        self.dots = self.mazetree.maze_dots

        self.precedent = dict()

        self.heuristic = heuristic
        if heuristic:
            self.heuristic = getattr(self, heuristic)
            self.gscore = dict()
            self.fscore = dict()
            self.dist_func = getattr(self, dist_func)
        self.pairwise_dist = None
        self.path = []
        self.expanded = 1
        self.start_time = None
        self.end_time = None

    def construct_path(self, tup):
        path = [tup]
        (x,y),left_state = tup
        while self.precedent.get(((x,y),left_state), None):
            path.append(self.precedent[((x,y),left_state)])
            (x,y),left_state = self.precedent[((x,y),left_state)]
        path.reverse()
        return path

    def check_goal(self, tup):
        (x, y), dotstate = tup
        if self.mazetree[x,y].isdot:
            newstate = dotstate - frozenset([(x,y)])
            return newstate
        else:
            return dotstate
    
    def run(self):
        self.start_time = time.time()
        getattr(self, 'run_' + self.method)()
        self.end_time = time.time()

    def run_astar(self):
        self.open_set.append((self.mazetree.maze_start, frozenset(self.dots)))  # put in starting point
        self.fscore[(self.mazetree.maze_start, frozenset(self.dots))] = self.heuristic(self.mazetree.maze_start, self.dots)
        self.gscore[(self.mazetree.maze_start, frozenset(self.dots))] = 0 # initialize starting dots gscore to 0

        while self.open_set:
            self.expanded += 1
            self.open_set = sorted(self.open_set, key=lambda x : self.fscore.get(x, float('inf')), reverse=True) # sort Fscore
            (x, y), dotstate = self.open_set.pop()
            currgscore = self.gscore.get(((x,y), dotstate), float('inf'))
            self.closed_set.append(((x, y), dotstate)) # add to closed set
            newdotstate = self.check_goal(((x, y), dotstate)) # find the goal
            if len(newdotstate) == 0: # goal state
                self.path = self.construct_path(((x,y), dotstate)) # construct path
                break
            neighbors = self.mazetree[x, y].neighbors()
            for ncoor in neighbors:
                if (ncoor, newdotstate) not in self.open_set and (ncoor, newdotstate) not in self.closed_set:
                    self.open_set.append((ncoor, newdotstate))
                
                newgscore = currgscore + 1
                if newgscore < self.gscore.get((ncoor, newdotstate), float('inf')):
                    self.precedent[ncoor, newdotstate] = ((x, y), dotstate)
                    #print("add pre for {0}".format((ncoor, newdotstate)))
                    self.gscore[ncoor, newdotstate] = newgscore
                    self.fscore[ncoor, newdotstate] = newgscore + self.heuristic(ncoor, newdotstate)

    def run_bfs(self):
        self.open_set.append((self.mazetree.maze_start, frozenset(self.dots)))  # put in starting point  
        while self.open_set:
            self.expanded += 1
            (x, y), dotstate = self.open_set.popleft()
            self.closed_set.append(((x, y), dotstate)) # add to closed set
            newdotstate = self.check_goal(((x, y), dotstate)) # find the goal
            if len(newdotstate) == 0: # goal state
                self.path = self.construct_path(((x,y), dotstate)) # construct path
                break
            neighbors = self.mazetree[x, y].neighbors()
            for ncoor in neighbors:
                if (ncoor, newdotstate) not in self.open_set and (ncoor, newdotstate) not in self.closed_set:
                    self.open_set.append((ncoor, newdotstate))
                    self.precedent[ncoor, newdotstate] = ((x, y), dotstate)
    
    def run_dfs(self):
        self.open_set.append((self.mazetree.maze_start, frozenset(self.dots)))  # put in starting point  
        while self.open_set:
            self.expanded += 1
            (x, y), dotstate = self.open_set[-1]
            newdotstate = self.check_goal(((x, y), dotstate)) # find the goal
            if len(newdotstate) == 0: # goal state
                self.path = self.construct_path(((x,y), dotstate)) # construct path
                break
            neighbors = self.mazetree[x, y].neighbors()
            added = 0
            for ncoor in neighbors:
                if (ncoor, newdotstate) not in self.open_set and (ncoor, newdotstate) not in self.closed_set:
                    added = 1
                    self.open_set.append((ncoor, newdotstate))
                    self.precedent[ncoor, newdotstate] = ((x, y), dotstate)
            if added == 0:
                self.open_set.pop()
                self.closed_set.append(((x, y), dotstate)) # add to closed set
    
    def run_gbfs(self):
        self.open_set.append((self.mazetree.maze_start, frozenset(self.dots)))  # put in starting point
        self.fscore[(self.mazetree.maze_start, frozenset(self.dots))] = self.heuristic(self.mazetree.maze_start, self.dots)
        while self.open_set:
            self.expanded += 1
            self.open_set = sorted(self.open_set, key=lambda x : self.fscore.get(x, float('inf')), reverse=True) # sort Fscore
            (x, y), dotstate = self.open_set.pop()
            self.closed_set.append(((x, y), dotstate)) # add to closed set
            newdotstate = self.check_goal(((x, y), dotstate)) # find the goal
            if len(newdotstate) == 0: # goal state
                self.path = self.construct_path(((x,y), dotstate)) # construct path
                break
            neighbors = self.mazetree[x, y].neighbors()
            for ncoor in neighbors:
                if (ncoor, newdotstate) not in self.open_set and (ncoor, newdotstate) not in self.closed_set:
                    self.open_set.append((ncoor, newdotstate))
                    self.precedent[ncoor, newdotstate] = ((x, y), dotstate)
                    self.fscore[ncoor, newdotstate] = self.heuristic(ncoor, newdotstate)
    
    def nearest_goal(self, coor, goals):
        dist = float('inf')
        tcoor = None
        cx, cy = coor
        for (gx, gy) in goals:
            cdist = abs(cx-gx) + abs(cy-gy) 
            if cdist < dist:
                tcoor = (gx, gy)
                dist = cdist
        return dist
    
    def count_goal(self, coor, goals):
        return len(goals)
    
    def nearest_ngoal(self, coor, goals):
        cx, cy = coor
        cdist = [abs(cx-gx) + abs(cy-gy) for (gx, gy) in goals] 
        cdist.sort()
        n= 3
        return sum(cdist[:n])/n
    
    def mst(self, coor, goals):

        cx, cy = coor
        cdist = [abs(cx-gx) + abs(cy-gy) for (gx, gy) in goals] 
        cdist.sort()
    
        '''
        build MST
        '''
        from scipy.sparse import csr_matrix
        from scipy.sparse.csgraph import minimum_spanning_tree
        import numpy as np
        l = len(goals)
        gl = [x for x in goals]
        mat = np.zeros((l,l))
        for i in range(l):
            dot1 = gl[i]
            for j in range(i+1, l):
                dot2 = gl[j]
                mat[i][j] = self.precomputed_dist(dot1, dot2)
    
        X = csr_matrix(mat)
        mst = minimum_spanning_tree(X)
        return mst.sum() + cdist[0]

    def save_solution_ascii(self, soldir='./solutions'):
        mazename = self.maze.filename.split('/')[-1].split('.')[0]
        l = []
        rcoor = 0
        with open(self.maze.filename) as fileobj:
            for line in fileobj:
                l.append(list(line))
        
        goal_ord = 0
        import string
        lengend = list(range(1,9)) + list(string.ascii_lowercase)
        for ((rcoor, ccoor), nil) in self.path:
            if (rcoor, ccoor) in self.dots:
                (l[rcoor])[ccoor] = str(lengend[goal_ord])
                goal_ord += 1
            elif (l[rcoor])[ccoor] != 'P':
                (l[rcoor])[ccoor] = '.'

        with open(soldir + '/' + self.mazename + '_'+self.method + '_sol.txt', 'w') as fd_out:
            fd_out.writelines([''.join(ll) for ll in l])

    def report(self):
        print("-"*30)
        print("{0} search for {1}".format(self.methodname, self.mazename))
        print("Finished in : %.3f seconds" % (self.end_time - self.start_time))
        print("Solution:")
        print([i[0] for i in self.path])
        print("\nSolution Cost : "+str(len(self.path) - 1))
        print("Node Expanded : "+str(self.expanded))
        print("-"*30)
    
    def save_report(self, repdir='./reports'):
        l = [
            "-"*30,
            "{0} search for {1}".format(self.methodname, self.mazename),
            "Finished in : %.3f seconds" % (self.end_time - self.start_time),
            "Solution:",
            '->'.join(['('+','.join([str(x) for x in i[0]])+')' for i in self.path]),
            "\nSolution Cost : "+str(len(self.path) - 1),
            "Node Expanded : "+str(self.expanded),
        ]
        with open(repdir + '/' + self.mazename + '_report.txt', 'a') as fd_out:
            fd_out.write('\n'.join(l)+'\n')
    
    def generate_pairwise_distance(self):
        self.pairwise_dist = dict()
        l = len(self.dots)
        for j in range(l):
            self.pairwise_dist[self.dots[j]] = dict()
        for i in range(l):
            dot1 = self.dots[i]
            for j in range(i+1, l):
                dot2 = self.dots[j]
                '''
                mini BFS to find pairwise shortest path
                '''
                frontier = deque([dot1])
                closed = []
                precedent_pairwise = dict()
                path = []
                while frontier:
                    (x, y) = frontier.popleft()
                    closed.append((x,y))
                    if (x,y) == dot2:
                        p = precedent_pairwise.get((x,y), None)
                        while p != dot1:
                            path.append(p)
                            p = precedent_pairwise.get(p, None)
                        self.pairwise_dist[dot2][dot1] = path + [dot1]
                        path.reverse()
                        self.pairwise_dist[dot1][dot2] = path + [dot2]
                        break
                    neighbors = self.mazetree[x, y].neighbors(auto_precedent=False, include_parent=True)
                    for ncoor in neighbors:
                        if ncoor not in frontier and ncoor not in closed:
                            frontier.append(ncoor)
                            precedent_pairwise[ncoor] = (x, y)
        
    def precomputed_dist(self, tup1, tup2):
        if self.pairwise_dist is None:
            self.generate_pairwise_distance()
        return len(self.pairwise_dist.get(tup1).get(tup2))

    def manhattan(self, tup1, tup2):
        return abs(tup1[0]-tup2[0]) + abs(tup1[1]-tup2[1])