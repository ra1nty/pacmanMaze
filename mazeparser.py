from graphics import *

class Maze:

    WALL = '%'
    DOT = '.'
    START = 'P'

    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as f:
            read_data = f.read()
        self.start = None
        self.dots = []
        self.maze_raw = self.__parse(read_data)

    
    def __parse(self, data):
        maze_raw = []
        rcoor = 0
        ccoor = 0
        for node in data:
            if node == '\n':
                ccoor = 0
                rcoor += 1
            else:
                if node != '%':
                    maze_raw.append((rcoor, ccoor))
                    if node == self.START:
                        if self.start:
                            raise Exception('Error : Multiple start points')
                        self.start = (rcoor, ccoor)
                    elif node == self.DOT:
                        self.dots.append((rcoor, ccoor))
                ccoor += 1
        return maze_raw


    def printMaze(self, w=800, l=600, node_size=10):
        win = GraphWin("Maze", w, l)
        for (x, y) in self.maze_raw:
            r = Rectangle(Point(node_size*x, node_size*y), Point(node_size*x+node_size, node_size*y+node_size))
            r.draw(win)
        for (x, y) in self.dots:
            c = Circle(Point(node_size*x+node_size/2, node_size*y+node_size/2), node_size/4)
            c.draw(win)
        msg = Text(Point(node_size*self.start[0]+node_size/2, node_size*self.start[1]+node_size/2), "S")
        msg.draw(win)
        win.getMouse()
        return win