class MazeTree:

    DEFAULT_FIELD = {}
    
    def __init__(self, m, field=None):
        self.maze_raw = m.maze_raw
        self.maze_dots = m.dots
        self.maze_start = m.start
        self.meta = dict()
        
        for tup in self.maze_raw:
            self.meta[tup] = dict()
            for fieldname in self.DEFAULT_FIELD.keys():
                self.meta[tup][fieldname] = self.DEFAULT_FIELD[fieldname]
            if field:
                for fieldname in field.keys():
                    self.meta[tup][fieldname] = field[fieldname]

    def root(self):
        return Node(self, *self.maze_start)

    def __getitem__(self, tup):
        x,y = tup
        return Node(self, x, y)


class Node:
        
    def __init__(self, mt, x=0, y=0):
        self.xcoor = x
        self.ycoor = y
        self.maze_tree = mt
        self.isdot = (x,y) in mt.maze_dots
        for name in mt.meta[(x,y)].keys():
            setattr(self, name, mt.meta[(x,y)][name]) 

    def neighbors(self):
        nb = []
        if (self.xcoor+1, self.ycoor) in self.maze_tree.maze_raw:
            nb.append((self.xcoor+1, self.ycoor))
        if (self.xcoor, self.ycoor+1) in self.maze_tree.maze_raw:
            nb.append((self.xcoor, self.ycoor+1))
        if (self.xcoor-1, self.ycoor) in self.maze_tree.maze_raw:
            nb.append((self.xcoor-1, self.ycoor))
        if (self.xcoor, self.ycoor-1) in self.maze_tree.maze_raw:
            nb.append((self.xcoor, self.ycoor-1))
        return nb

    def setField(self, field, val):
        setattr(self, field, val)
        self.maze_tree.meta[self.getCoor()][field] = val

    def getCoor(self):
        return (self.xcoor, self.ycoor)
