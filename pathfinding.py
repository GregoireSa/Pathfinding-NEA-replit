import pygame
import random
import webbrowser
from time import sleep
import basicUI

BLANK_COLOUR = (20,20,20) # VERY DARK GRAY
GRID_COLOUR = (50,50,50) # DARK GRAY
BARRIER_COLOUR = (100,100,100) # LIGHT GRAY
BORDER_COLOUR = (65,65,65) # GRAY
START_COLOUR = (97,135,40) # PURPLE  233,184,36
FIN_COLOUR = (178,16,49) # ORANGE 250, 160, 90 238,147,34
PATH_COLOUR = (128,51,135) # DARK RED 170, 40, 40
VISITED_COLOUR = (5,5,5) # GREEN 0,255,0 33,156,144
QUEUED_COLOUR = (0,100,100) # RED 255,0,0
UI_MAIN_COLOUR = (30,30,30)
UI_TEXT_COLOUR = (100,100,100)

class Pathfinding:
    def __init__(self,win,width,height,menu_func,grid):
        self.win = win
        self.width, self.height = width, height
        self.grid_width, self.grid_height = 0.75*width, height
        self.menu_func = menu_func
        self.grid = grid
        self.cellsize = 25
        self.rows = int(self.grid_height//self.cellsize)
        self.cols = int(self.grid_width//self.cellsize)
        
        self.start_search = False
        self.selected_algo = ''

    def reset_grid(self):
        for i,row in enumerate(self.grid):
            for j in range(len(row)):
                if i != 0 and i != self.rows-1 and j != 0 and j != self.cols-1:
                    self.grid[i][j].colour = BLANK_COLOUR
    
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
                    return True
        return False
    
    def load(self):
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.menu_func()
        if keys[pygame.K_r]:
            self.reset_grid()
        
        if pygame.mouse.get_pressed():
            mouse_pos = pygame.mouse.get_pos()
            x_coord = mouse_pos[1] // self.cellsize
            y_coord = mouse_pos[0] // self.cellsize
            if pygame.mouse.get_pressed()[0] and self.in_bounds(x_coord,y_coord):
                if not self.check_grid(START_COLOUR):
                    self.grid[x_coord][y_coord].colour = START_COLOUR    
                    start_cell = self.grid[x_coord][y_coord]
                elif not self.check_grid(FIN_COLOUR) and self.check_grid(START_COLOUR) and self.grid[x_coord][y_coord].colour != START_COLOUR:
                    self.grid[x_coord][y_coord].colour = FIN_COLOUR
                    fin_cell = self.grid[x_coord][y_coord]
                elif self.grid[x_coord][y_coord].colour != START_COLOUR and self.grid[x_coord][y_coord].colour != FIN_COLOUR:
                    self.grid[x_coord][y_coord].colour = BARRIER_COLOUR
            
        
        
        