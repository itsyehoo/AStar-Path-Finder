
import pygame
import math 
from queue import PriorityQueue

#Setting up the display
WIDTH = 800 
WINDOW =  pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Alporithm")

#Defining Colors (change Later)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col
        
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_startNode(self):
        return self.color == ORANGE

    def is_endNode(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def create_startNode(self):
        self.color = BLUE

    def create_endNode(self):
        self.color = ORANGE

    def create_closed(self):
        self.color = RED

    def create_open(self):
        self.color = GREEN

    def create_barrier(self):
        self.color = BLACK

    def create_path(self):
        self.color = YELLOW

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))
        
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

#Comparing two Nodes together (LT is Less Than)
    def __lt__(self, other):
        return False

#Getting the Distance between two nodes
def distance(Node1, Node2):
    x1, y1 = Node1
    x2, y2 = Node2
    return abs(x1 - x2) + abs(y1 - y2) #Returns absolute distance 

def reconstruct_path(came_from, current, draw):
    	while current in came_from:
            current = came_from[current]
            current.make_path()
            draw()

#A* Algorithm
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = distance(start.get_pos(), end.get_pos())
    
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + distance(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()
        
        if current != start:
            current.make_closed()
    
    return False

#Creating a Grid
def create_grid(rows, width):
    grid = []
    gap = width // rows #Width of each node (cube) in the grid
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

#Creating the Grid Lines
def draw_grid(win, rows, width):
    gap = width // rows #Width of each node (cube) in the grid
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) #Creating horizontal lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width)) #Creating vertical lines

def draw_nodes(window, grid, rows, width):
    window.fill(WHITE)
    
    for row in grid:
        for node in row:
            node.draw(window)
        
    draw_grid(window, rows, width)
    pygame.display.update()

#Getting Mouse Position
def get_clicked_pos(position, rows, width):
    gap = width // rows #Width of each node (cube) in the grid
    y, x = position
    
    row = y // gap
    col = x // gap
    
    return row, col

#Main 
def main(window, width):
    ROWS = 50
    grid = create_grid(ROWS, width)
    
    start = None
    end = None
    
    run = True
    while run:
        draw_nodes(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                position = pygame.mouse.get_position()
                row, col = get_clicked_pos(position, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.create_start()
                
                elif not end and node != start:
                    end = node
                    end.create_end()
                
                elif node != end and node != start:
                    node.create_barrier()
            
            elif pygame.mouse.get_pressed()[2]: # RIGHT
                position = pygame.mouse.get_pos()
                row, col = get_clicked_pos(position, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    algorithm(lambda: draw_nodes(window, grid, ROWS, width), grid, start, end)
                    
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = create_grid(ROWS, width)

pygame.quit()

main(WINDOW, WIDTH)
