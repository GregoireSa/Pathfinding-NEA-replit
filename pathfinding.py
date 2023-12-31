import pygame
import random
import webbrowser
from time import sleep
import basicUI
import menu

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
    def update_neighbours(self,rows,cols,grid):
        self.neighbours = []
        if self.row > 0:
            self.neighbours.append(grid[self.row-1][self.col])
        if self.row < rows-1:
            self.neighbours.append(grid[self.row+1][self.col])
        if self.col > 0:
            self.neighbours.append(grid[self.row][self.col-1])
        if self.col < cols-1:
            self.neighbours.append(grid[self.row][self.col+1])

class Pathfinding:
    def __init__(self,win,width,height,menu_func):
        self.win = win
        self.width, self.height = width, height
        self.grid_width, self.grid_height = 0.75*width, height
        self.ui_width = self.width-self.grid_width
        self.menu_func = menu_func
        self.grid = []
        self.cellsize = 25
        self.rows = int(self.grid_height//self.cellsize)
        self.cols = int(self.grid_width//self.cellsize)
        self.show_lines = True
        self.buttons = []
        
        self.init_grid()
        
        self.start_search = False
        self.selected_algo = 'dijkstra'
        self.start_cell = None
        self.fin_cell = None
        
        # UI ELEMENTS:
        self.randomButton = basicUI.button(self.win,"random",lambda:self.randomFunc(),
                                           (self.grid_width+(self.width-self.grid_width)//2-60,100),
                                           fg=UI_TEXT_COLOUR,bg=UI_BG_COLOUR,group=self.buttons)
        self.resetButton = basicUI.button(self.win,"reset",lambda:self.resetFunc(),
                                          (self.grid_width+(self.width-self.grid_width)//2-60,150),
                                          fg=UI_TEXT_COLOUR,bg=UI_BG_COLOUR,group=self.buttons)
        self.startButton = basicUI.button(self.win,"start",lambda:self.startFunc(),
                                          (self.grid_width+(self.width-self.grid_width)//2-60,200),
                                          fg=UI_TEXT_COLOUR,bg=UI_BG_COLOUR,group=self.buttons)
        self.largerGridButton = basicUI.button(self.win,"+",lambda:self.largerGridFunc(),
                                               (self.grid_width+(self.width-self.grid_width)//2-60,250),
                                               fg=UI_TEXT_COLOUR,bg=UI_BG_COLOUR,group=self.buttons)
        self.smallerGridButton = basicUI.button(self.win,"-",lambda:self.smallerGridFunc(),
                                                (self.grid_width+(self.width-self.grid_width)//2,250),
                                                fg=UI_TEXT_COLOUR,bg=UI_BG_COLOUR,group=self.buttons)
        self.gridLinesButton = basicUI.button(self.win,"show lines", lambda:self.showLinesFunc(),
                                              (self.grid_width+(self.width-self.grid_width)//2-60,300),
                                              fg=UI_TEXT_COLOUR,bg=UI_BG_COLOUR,group=self.buttons)
        self.bwerdsYTButton = basicUI.button(self.win,"subscribe",lambda:self.bwerdsLinkFunc(),
                                             (self.grid_width+(self.width-self.grid_width)//2-60,350),
                                             fg=UI_TEXT_COLOUR,bg=UI_BG_COLOUR,group=self.buttons)
        self.algoSelector = basicUI.dropdown(self.win,"algorithm",
                                             (self.grid_width+(self.width-self.grid_width)//2-60,400),
                                             fg=UI_TEXT_COLOUR,bg=UI_BG_COLOUR)
        self.algoSelector.add_option("dijkstra",lambda:self.select_algo("dijkstra"))
        self.algoSelector.add_option("A star",lambda:self.select_algo("astar"))
        self.algoSelector.add_option("greedy BFS",lambda:self.select_algo("greedybfs"))
        self.algoSelector.add_option("dynamic",lambda:self.select_algo("dynamic"))
    
    def init_grid(self):
        self.grid = []
        self.cols = int(self.grid_width//self.cellsize)
        self.rows = int(self.grid_height//self.cellsize)
        
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                if i == 0 or j == 0 or i == self.rows-1 or j == self.cols-1:
                    self.grid[i].append(cell(i,j,self.cellsize,colour=BORDER_COLOUR))
                else:
                    self.grid[i].append(cell(i,j,self.cellsize))
        for row in self.grid:
            for n in row:
                n.update_neighbours(self.rows,self.cols,self.grid)
    
    def bwerdsLinkFunc(self):
        webbrowser.open("https://www.youtube.com/@bwerds1263")
    
    def randomFunc(self):
        if not self.start_search:
            for row in self.grid:
                for cell in row:
                    if (cell.colour == BLANK_COLOUR or cell.colour == PATH_COLOUR) and random.randint(1,15) == 1:
                        cell.colour = BARRIER_COLOUR
    def resetFunc(self):
        for i,row in enumerate(self.grid):
            for j in range(len(row)):
                if i != 0 and i != self.rows-1 and j != 0 and j != self.cols-1:
                    self.grid[i][j].colour = BLANK_COLOUR
        if self.start_search: self.start_search = False
    def startFunc(self):
        self.start_search = True
    def largerGridFunc(self):
        if not self.start_search and self.cellsize + 5 < min((self.grid_width,self.grid_height)):
            self.cellsize += 5
            self.cols = int(self.grid_width//self.cellsize)
            self.rows = int(self.grid_height//self.cellsize)
            self.resetFunc()
            self.init_grid()
    def smallerGridFunc(self):
        if not self.start_search and self.cellsize -5 > 0:
            self.cellsize -= 5
            self.cols = int(self.grid_width//self.cellsize)
            self.rows = int(self.grid_height//self.cellsize)
            self.resetFunc()
            self.init_grid()
    def showLinesFunc(self):
        self.show_lines = not self.show_lines
    def select_algo(self,algorithm):
        self.selected_algo = algorithm
    
    def in_bounds(self,x,y):
        if pygame.mouse.get_pos()[0] > self.grid_width:
            return False
        if x == 0 or y == 0 or x == self.rows-1 or y == self.cols-1:
            return False
        return True
    def check_grid(self,colour):
        for row in self.grid:
            for n in row:
                if n.colour == colour:
                    return n

    
    def draw_grid(self):
        for row in self.grid:
            for cell in row: cell.draw(self.win)
        if self.show_lines:
            for i in range(self.cols):
                pygame.draw.line(self.win,GRID_COLOUR,(i*self.cellsize,0),(i*self.cellsize,self.grid_height))
            for j in range(self.rows):
                pygame.draw.line(self.win,GRID_COLOUR,(0,j*self.cellsize),(self.grid_width,j*self.cellsize))
    
    def load(self):
        
        isStartCell = self.check_grid(START_COLOUR)
        isFinCell = self.check_grid(FIN_COLOUR)
        if not isStartCell: 
            self.start_cell = None
        else:
            self.start_cell = isStartCell
        if not isFinCell:
            self.fin_cell = None
        else:
            self.fin_cell = isFinCell
        
        # CHECK KEYS PRESSED
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.menu_func()
        if keys[pygame.K_r]:
            self.resetFunc()
        
        if pygame.mouse.get_pressed():
            mouse_pos = pygame.mouse.get_pos()
            x_coord = mouse_pos[1] // self.cellsize
            y_coord = mouse_pos[0] // self.cellsize
            if pygame.mouse.get_pressed()[0] and self.in_bounds(x_coord,y_coord):
                if not self.check_grid(START_COLOUR):
                    self.grid[x_coord][y_coord].colour = START_COLOUR    
                    self.start_cell = self.grid[x_coord][y_coord]
                elif not self.check_grid(FIN_COLOUR) and self.check_grid(START_COLOUR) and self.grid[x_coord][y_coord].colour != START_COLOUR:
                    self.grid[x_coord][y_coord].colour = FIN_COLOUR
                    self.fin_cell = self.grid[x_coord][y_coord]
                elif self.grid[x_coord][y_coord].colour != START_COLOUR and self.grid[x_coord][y_coord].colour != FIN_COLOUR:
                    self.grid[x_coord][y_coord].colour = BARRIER_COLOUR
            if pygame.mouse.get_pressed()[2] and self.in_bounds(x_coord,y_coord):
                self.grid[x_coord][y_coord].colour = BLANK_COLOUR
            
            # UPDATING GRID LINES BUTTON
            if self.show_lines:
                self.gridLinesButton.change_text("hide lines")
            else:
                self.gridLinesButton.change_text("show lines")
            
            # DRAW WINDOW
            self.win.fill((255,255,255))
            
            self.draw_grid()
            
            yMargin = 10
            pygame.draw.rect(self.win,UI_MAIN_COLOUR,(self.grid_width,0,self.ui_width,self.height))
            basicUI.text(self.win,"Pathfinding",self.grid_width+(self.width-self.grid_width)//2-75,
                         yMargin,UI_TEXT_COLOUR,45)
            for button in self.buttons:
                if not self.start_search or button == self.gridLinesButton:
                    button.update()
                button.draw()
            self.algoSelector.update()
            
            pygame.display.update()