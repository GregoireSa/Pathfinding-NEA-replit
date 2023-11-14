import pygame
import random
import webbrowser
from time import sleep
import basicUI
import menu
import pathfinding


pygame.init()
WIDTH, HEIGHT = 1000,500
GRID_WIDTH, GRID_HEIGHT = 0.75*WIDTH,500
UI_WIDTH = WIDTH-GRID_WIDTH
win = pygame.display.set_mode((WIDTH,HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("dijkstra's algorithm")
CLOCK, FPS = pygame.time.Clock(), 60

BLANK_COLOUR = (20,20,20)
GRID_COLOUR = (50,50,50)
BARRIER_COLOUR = (100,100,100)
BORDER_COLOUR = (65,65,65)
START_COLOUR = (97,135,40)
FIN_COLOUR = (178,16,49)
PATH_COLOUR = (128,51,135)
VISITED_COLOUR = (5,5,5)
QUEUED_COLOUR = (0,100,100)
UI_MAIN_COLOUR = (30,30,30)
UI_BG_COLOUR = (50,50,50)
UI_TEXT_COLOUR = (100,100,100)

OBSTACLE_COLOURS = [BARRIER_COLOUR,BORDER_COLOUR]

CELL_GAP = 25
COLS = int(GRID_WIDTH//CELL_GAP)
ROWS = int(GRID_HEIGHT//CELL_GAP)

class cell:
    def __init__(self,row,col,width,colour=BLANK_COLOUR):
        self.row, self.col = row, col
        self.width = width
        self.x = self.col*self.width
        self.y = self.row*self.width
        self.neighbours = []
        self.colour = colour
        self.pathfind_prior = None

    def draw(self,win):
        pygame.draw.rect(win,self.colour,(self.x,self.y,self.width,self.width))
    def update_neighbours(self,rows,cols):
        self.neighbours = []
        if self.row > 0:
            self.neighbours.append(grid[self.row-1][self.col])
        if self.row < rows-1:
            self.neighbours.append(grid[self.row+1][self.col])
        if self.col > 0:
            self.neighbours.append(grid[self.row][self.col-1])
        if self.col < cols-1:
            self.neighbours.append(grid[self.row][self.col+1])

def dijkstra(start_cell,fin_cell):
    global win, WIDTH, HEIGHT, GRID_WIDTH, GRID_HEIGHT
    Q = []
    Q.append(start_cell)
    visited = []
    found = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.VIDEORESIZE:
                old_win = win
                WIDTH,HEIGHT = event.w,event.h
                GRID_WIDTH, GRID_HEIGHT = WIDTH*0.75, HEIGHT
                win = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
                win = old_win
                del old_win
        if not Q: break
        curr_cell = Q[0]
        if curr_cell == fin_cell:
            found = True
            break
        for neighbour in curr_cell.neighbours:
            c = neighbour.colour
            if c==BLANK_COLOUR or c==FIN_COLOUR:
                Q.append(neighbour)
                neighbour.colour = QUEUED_COLOUR
                neighbour.pathfind_prior = curr_cell
        visited.append(curr_cell)
        curr_cell.colour = VISITED_COLOUR
        Q.pop(0)
        pathfPage.load()
        start_cell.colour = START_COLOUR
        
    for row in grid:
        for n in row:
            if n.colour == VISITED_COLOUR or n.colour == QUEUED_COLOUR:
                n.colour = BLANK_COLOUR
    if found: # BACKTRACK
        fin_cell.colour = FIN_COLOUR
        curr_cell = fin_cell.pathfind_prior
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.VIDEORESIZE:
                    old_win = win
                    WIDTH,HEIGHT = event.w,event.h
                    GRID_WIDTH, GRID_HEIGHT = WIDTH*0.75, HEIGHT
                    win = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
                    win = old_win
                    del old_win
            if curr_cell == start_cell: break
            curr_cell.colour = PATH_COLOUR
            curr_cell = curr_cell.pathfind_prior
            pathfPage.load()
            sleep(.01)

def greedybfs(start_cell,fin_cell):
    visited = []
    open = []
    curr_cell = start_cell
    open.append(start_cell)
    found = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if curr_cell == fin_cell:
            found = True
            break
        best_cost = float('inf')
        best_cell = None
        for neighbour in curr_cell.neighbours:
            if neighbour not in open and (neighbour.colour == BLANK_COLOUR or neighbour.colour == FIN_COLOUR):
                neighbour.colour = QUEUED_COLOUR
                neighbour.pathfind_prior = curr_cell
                cost = abs(neighbour.col-fin_cell.col)+abs(neighbour.row-fin_cell.row)
                if cost < best_cost:
                    best_cost = cost
                    best_cell = neighbour
        
        open.append(best_cell)
        visited.append(curr_cell)
        curr_cell.colour = VISITED_COLOUR
        open.pop(0)
        curr_cell = open[0]
            
        for cell in open:
            if cell.colour != START_COLOUR: cell.colour = VISITED_COLOUR
        
        if curr_cell.colour != START_COLOUR: curr_cell.colour = VISITED_COLOUR
        
        start_cell.colour = START_COLOUR
        draw_surface()
        
    for row in grid:
        for n in row:
            if n.colour == VISITED_COLOUR or n.colour == QUEUED_COLOUR:
                n.colour = BLANK_COLOUR
    
    if found:
        fin_cell.colour = FIN_COLOUR
        curr_cell = fin_cell.pathfind_prior
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if curr_cell == start_cell: break
            curr_cell.colour = PATH_COLOUR
            curr_cell = curr_cell.pathfind_prior
            draw_surface()
            sleep(.1)
            
        
def bubblesort(arr): # bubble sort
    for i in range(1,len(arr)):
        for j in range (len(arr)-1):
            if arr[j] > arr[j+1]:
                temp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = temp
    return arr

def aStar(start_cell,fin_cell):
    global win, WIDTH, HEIGHT, GRID_WIDTH, GRID_HEIGHT
    visited = []
    open = []
    curr_cell = start_cell
    open.append([start_cell,float('inf')])
    found = False
    currG = 0
        
    def checkColour(colour):
        if colour != VISITED_COLOUR and colour not in OBSTACLE_COLOURS:
            return True
        return False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.VIDEORESIZE:
                old_win = win
                WIDTH,HEIGHT = event.w,event.h
                GRID_WIDTH, GRID_HEIGHT = WIDTH*0.75, HEIGHT
                win = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
                win = old_win
                del old_win
        currG += 1
        openNodes = [x[0] for x in open]
        if not openNodes: break
        if curr_cell == fin_cell:
            found = True
            break
        
        for neighbour in curr_cell.neighbours:
            if neighbour not in openNodes and checkColour(neighbour.colour):
                open.append([neighbour,float('inf')])
                if neighbour.colour == BLANK_COLOUR:
                    neighbour.colour = QUEUED_COLOUR
                    neighbour.pathfind_prior = curr_cell
        
        openNodes = [x[0] for x in open]
        for i,node in enumerate(openNodes):
            h = abs(node.row-fin_cell.row) + abs(node.col-fin_cell.col)
            open[i][1] = currG + h
        
        if curr_cell.colour != START_COLOUR: curr_cell.colour = VISITED_COLOUR
        visited.append(curr_cell)
        open.pop(openNodes.index(curr_cell))
        if not open: break
        openFcosts = [x[1] for x in open]
        curr_cell_idx = openFcosts.index(min(openFcosts))
        curr_cell = open[curr_cell_idx][0]
        
        draw_surface()
    
    if found:
        pass
        # curr_cell = fin_cell
        # while curr_cell is not None:
        #     if curr_cell == start_cell: break
        #     if curr_cell.colour != FIN_COLOUR:
        #         curr_cell.colour = PATH_COLOUR
        #     curr_cell = curr_cell.pathfind_prior
            
grid = []
def init_grid(): 
    global grid
    COLS = int(GRID_WIDTH//CELL_GAP)
    ROWS = int(GRID_HEIGHT//CELL_GAP)
    grid = []

    for i in range(ROWS):
        grid.append([])
        for j in range(COLS):
            if i == 0 or j == 0 or i == ROWS-1 or j == COLS-1:
                grid[i].append(cell(i,j,CELL_GAP,colour=BORDER_COLOUR))
            else:
                grid[i].append(cell(i,j,CELL_GAP))

    for row in grid:
        for n in row: n.update_neighbours(ROWS,COLS)
init_grid()

def draw_grid(rows,cols):
    pass
    # for i in range(cols):
    #     pygame.draw.line(win,GRID_COLOUR,(i*CELL_GAP,0),(i*CELL_GAP,GRID_HEIGHT))
    # for j in range(rows):
    #     pygame.draw.line(win,GRID_COLOUR,(0,j*CELL_GAP),(GRID_WIDTH,j*CELL_GAP))

selected_algo = 'dijstra'

def select_algo(algo):
    global selected_algo
    selected_algo = algo

# UI ELEMENTS:

buttons = []

def randomNodes():
    for row in grid:
        for n in row:
            if (n.colour == BLANK_COLOUR or n.colour == PATH_COLOUR) and random.randint(1,15) == 1:
                n.colour = BARRIER_COLOUR

def increaseGridSize():
    global CELL_GAP
    CELL_GAP += 5
    init_grid()
    draw_grid(ROWS,COLS)
    
def decreaseGridSize():
    global CELL_GAP
    if CELL_GAP > 5:
        CELL_GAP -= 5
        ROWS = int(GRID_HEIGHT//CELL_GAP)
        COLS = int(GRID_WIDTH//CELL_GAP)
        init_grid()
        draw_grid(ROWS,COLS)

randomButton = basicUI.button(win,"random",lambda:randomNodes(),(GRID_WIDTH+(WIDTH-GRID_WIDTH)//2-60,100),
                              fg=UI_TEXT_COLOUR,bg=GRID_COLOUR,group=buttons)

largerGrid = basicUI.button(win,"+",lambda:increaseGridSize(),(GRID_WIDTH+(WIDTH-GRID_WIDTH)//2-60,250),
                            fg=UI_TEXT_COLOUR,bg=GRID_COLOUR,group=buttons)
smallerGrid = basicUI.button(win,"-",lambda:decreaseGridSize(),(GRID_WIDTH+(WIDTH-GRID_WIDTH)//2,250),
                             fg=UI_TEXT_COLOUR,bg=GRID_COLOUR,group=buttons)

def resetGrid():
    for i,row in enumerate(grid):
        for j in range(len(row)):
            if i != 0 and i != ROWS-1 and j != 0 and j != COLS-1:
                grid[i][j].colour = BLANK_COLOUR
resetButton = basicUI.button(win,"reset",lambda:resetGrid(),(GRID_WIDTH+(WIDTH-GRID_WIDTH)//2-60,150),
                             fg=UI_TEXT_COLOUR,bg=GRID_COLOUR,group=buttons)
started = False
def startAlgo():
    started = True
startButton = basicUI.button(win,"start",lambda:startAlgo(),(GRID_WIDTH+(WIDTH-GRID_WIDTH)//2-60,200),
                             fg=UI_TEXT_COLOUR,bg=GRID_COLOUR,group=buttons)

algoChoice = basicUI.dropdown(win,"Algorithm",(GRID_WIDTH+(WIDTH-GRID_WIDTH)//2-60,300),fg=UI_TEXT_COLOUR,bg=GRID_COLOUR)
algoChoice.add_option("dijkstra",lambda:select_algo("dijkstra"))
algoChoice.add_option("A star",lambda:select_algo("astar"))
algoChoice.add_option("greedy BFS",lambda:select_algo("greedybfs"))
algoChoice.add_option("dynamic",lambda:select_algo("dynamic"))

def draw_surface():
    win.fill((255,255,255))
    for row in grid:
        for cell in row: cell.draw(win)
    draw_grid(ROWS,COLS)
    yMargin = 10
    pygame.draw.rect(win,UI_MAIN_COLOUR,(GRID_WIDTH,0,UI_WIDTH,HEIGHT))
    basicUI.text(win,"Pathfinding",GRID_WIDTH+(WIDTH-GRID_WIDTH)//2-75,yMargin,UI_TEXT_COLOUR,45)
    for button in buttons:
        button.update()
        button.draw()
    algoChoice.update()

    pygame.display.update()

def check_grid(condition):
    for row in grid:
        for cell in row:
            if cell.colour == condition:
                return True
    return False

def in_bounds(x,y):
    if pygame.mouse.get_pos()[0] > GRID_WIDTH:
        return False
    if x == 0 or y == 0 or x == ROWS-1 or y == COLS-1:
        return False
    return True


# def menu():
#     global win, WIDTH, HEIGHT, GRID_WIDTH, GRID_HEIGHT
#     running = True
#     start_button = basicUI.button(win,"START",lambda:main(),(0,0),fontsize=60,fg=UI_TEXT_COLOUR,bg=GRID_COLOUR)
#     start_button.new_center((WIDTH//2,HEIGHT//2-start_button.fontsize//1.5))
#     quit_button = basicUI.button(win,"QUIT",lambda:quit_func(),(0,0),fontsize=55,fg=UI_TEXT_COLOUR,bg=GRID_COLOUR)
#     quit_button.new_center((WIDTH//2,HEIGHT//2+quit_button.fontsize//1.5))
#     docs_button = basicUI.button(win,"DOCS",lambda:open_docs(),(0,0),fontsize=20,fg=UI_TEXT_COLOUR,bg=GRID_COLOUR)
#     margin = 10
#     docs_button.new_center((WIDTH-docs_button.bgRect.width//2-margin,margin+docs_button.fontsize//1.5))
#     while running:
#         CLOCK.tick(FPS)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#             if event.type == pygame.VIDEORESIZE:
#                 print("resizing")
#                 old_win = win
#                 WIDTH,HEIGHT = event.w,event.h
#                 GRID_WIDTH, GRID_HEIGHT = WIDTH*0.75, HEIGHT
#                 win = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
#                 win = old_win
#                 del old_win
                
#         win.fill(BLANK_COLOUR)
#         start_button.update()
#         quit_button.update()
#         docs_button.update()
#         start_button.draw()
#         quit_button.draw()
#         docs_button.draw()
#         pygame.display.update()

def open_docs():
    webbrowser.open("https://docs.google.com/document/d/1U96vEvA0jDv8XYHGnGShQUluY2gDUlA39RXWsx02tb4/edit")

def quit_func():
    pygame.quit()
    quit()

def main():
    global win, WIDTH, HEIGHT, GRID_WIDTH, GRID_HEIGHT, started
    running = True
    start_cell,fin_cell = None,None
    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                old_win = win
                WIDTH,HEIGHT = event.w,event.h
                GRID_WIDTH, GRID_HEIGHT = WIDTH*0.75, HEIGHT
                win = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
                win = old_win
                del old_win
                
        if pygame.mouse.get_pressed():
            mouse_pos = pygame.mouse.get_pos()
            x_coord = mouse_pos[1] // CELL_GAP
            y_coord = mouse_pos[0] // CELL_GAP
            if pygame.mouse.get_pressed()[0] and in_bounds(x_coord,y_coord):
                if not check_grid(START_COLOUR):
                    grid[x_coord][y_coord].colour = START_COLOUR    
                    start_cell = grid[x_coord][y_coord]
                elif not check_grid(FIN_COLOUR) and check_grid(START_COLOUR) and grid[x_coord][y_coord].colour != START_COLOUR:
                    grid[x_coord][y_coord].colour = FIN_COLOUR
                    fin_cell = grid[x_coord][y_coord]
                elif grid[x_coord][y_coord].colour != START_COLOUR and grid[x_coord][y_coord].colour != FIN_COLOUR:
                    grid[x_coord][y_coord].colour = BARRIER_COLOUR
            if pygame.mouse.get_pressed()[2] and in_bounds(x_coord,y_coord) and grid[x_coord][y_coord].colour:
                grid[x_coord][y_coord].colour = BLANK_COLOUR
                
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]:
            menu()
        
        if (keys_pressed[pygame.K_SPACE] and start_cell != None and fin_cell != None) or started:
            for i,row in enumerate(grid):
                for j in range(len(row)):
                    c = grid[i][j].colour
                    if c==VISITED_COLOUR or c==QUEUED_COLOUR or c==PATH_COLOUR:
                        grid[i][j].colour = BLANK_COLOUR
            dijkstra(start_cell,fin_cell)
            started = False
        if keys_pressed[pygame.K_r]:
            resetGrid()
        if keys_pressed[pygame.K_a] and start_cell != None and fin_cell != None:
            for i,row in enumerate(grid):
                for j in range(len(row)):
                    c = grid[i][j].colour
                    if c==VISITED_COLOUR or c==QUEUED_COLOUR or c==PATH_COLOUR:
                        grid[i][j].colour = BLANK_COLOUR
            aStar(start_cell,fin_cell)
        draw_surface()
    pygame.quit()
    quit()

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

currPage = 0
def toMenu():
    global currPage
    currPage = 0
def toPathfinding(): 
    global currPage
    currPage = 1
    
    
def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.VIDEORESIZE:
            prev_win = win
            WIDTH,HEIGHT = event.w,event.h
            GRID_WIDTH,GRID_HEIGHT = event.w*0.75, event.h
            win = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
            win.blit(prev_win,(0,0))
            del prev_win

menuPage = menu.Menu(win,WIDTH,HEIGHT,lambda:toPathfinding())
pathfPage = pathfinding.Pathfinding(win,WIDTH,HEIGHT,lambda:toMenu(),grid)

if __name__ == '__main__':
    running = True
    while running:
        
        event_handler()
        
        if currPage == 0: # main menu page
            menuPage.load()
        elif currPage == 1: # pathfinding page
            if not pathfPage.start_search:
                pathfPage.load()
            else:
                if pathfPage.start_cell != None and pathfPage.fin_cell != None:
                    for i,row in enumerate(pathfPage.grid):
                        for j in range(len(row)):
                            c = pathfPage.grid[i][j].colour
                            if c==VISITED_COLOUR or c==QUEUED_COLOUR or c==PATH_COLOUR:
                                grid[i][j].colour = BLANK_COLOUR
                    if pathfPage.selected_algo == 'dijkstra':
                        dijkstra(pathfPage.start_cell,pathfPage.fin_cell)
                    elif pathfPage.selected_algo == 'astar':
                        print("astar")
                    elif pathfPage.selected_algo == 'greedybfs':
                        greedybfs(pathfPage.start_cell,pathfPage.fin_cell)
                    elif pathfPage.selected_algo == "dynamic":
                        print("dynamic")
                    pathfPage.start_search = False
        pygame.display.update()
        
    pygame.quit()
    quit()