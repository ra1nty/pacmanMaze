from mazeparser import *
from mazesearch import *

if __name__ == "__main__":
    report_dir = './reports'
    solution_dir = './solutions'

    p1 = []
    p1_search = [
        ('bfs', None),
        ('dfs', None),
        ('gbfs','nearest_goal'),
        ('astar','nearest_goal'),
    ]
    p1.append(Maze("./data/mediumMaze.txt"))
    p1.append(Maze("./data/bigMaze.txt"))
    p1.append(Maze("./data/openMaze.txt"))
    
    p2 = []
    p2_search = [
        ('astar','mst','precomputed_dist'),
    ]
    p2.append(Maze("./data/tinySearch.txt"))
    p2.append(Maze("./data/smallSearch.txt"))
    p2.append(Maze("./data/mediumSearch.txt"))
    '''
    import os
    for the_file in os.listdir(report_dir):
        file_path = os.path.join(report_dir, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    '''
    # Part 1:
    for maze in p1:
        for i in p1_search:
            se = Search(maze, *i)
            se.run()
            se.save_solution_ascii(solution_dir)
            se.save_report(report_dir)
    '''
    # Part 2:
    for maze in p2:
        for i in p2_search:
            se = Search(maze, *i)
            se.run()
            se.save_solution_ascii(solution_dir)
            se.save_report(report_dir)
    '''
    '''
    m2 = Maze("./data/tinySearch.txt")
    bfsm2 = Search(m2, 'bfs', None)
    bfsm2.run()
    bfsm2.save_report(report_dir)
    '''
    #m3 = Maze("./data/bigMaze.txt")
    #bigsearch = Search(m3, 'astar', None)
    #bigsearch.run()
    #bigsearch.report()
    