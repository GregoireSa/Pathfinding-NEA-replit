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


def dijkstra(start_cell,fin_cell,grid):
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
            #sleep(.01)

def greedybfs(start_cell,fin_cell,grid):
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
        pathfPage.load()
        
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
            pathfPage.load()
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
        
        pathfPage.load()
    
    if found:
        pass
        # curr_cell = fin_cell
        # while curr_cell is not None:
        #     if curr_cell == start_cell: break
        #     if curr_cell.colour != FIN_COLOUR:
        #         curr_cell.colour = PATH_COLOUR
        #     curr_cell = curr_cell.pathfind_prior



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
pathfPage = pathfinding.Pathfinding(win,WIDTH,HEIGHT,lambda:toMenu())

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
                                pathfPage.grid[i][j].colour = BLANK_COLOUR
                    if pathfPage.selected_algo == 'dijkstra':
                        dijkstra(pathfPage.start_cell,pathfPage.fin_cell,pathfPage.grid)
                    elif pathfPage.selected_algo == 'astar':
                        print("astar")
                    elif pathfPage.selected_algo == 'greedybfs':
                        greedybfs(pathfPage.start_cell,pathfPage.fin_cell,pathfPage.grid)
                    elif pathfPage.selected_algo == "dynamic":
                        print("dynamic")
                    pathfPage.start_search = False
                else:
                    pathfPage.start_search = False
        pygame.display.update()
        
    pygame.quit()
    quit()