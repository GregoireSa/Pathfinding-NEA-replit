import pygame
import random
import webbrowser
from time import sleep
import basicUI
pygame.init()

UI_TEXT_COLOUR = (100,100,100)
BUTTON_COLOUR = (50,50,50)
BG_COLOUR = (20,20,20)

class Menu:
    def __init__(self,win,width,height,main_func):
        self.win = win
        self.width = width
        self.height = height
        self.main_func = main_func
        
        self.buttons = []
        self.margin = 10
        
        self.start_button = basicUI.button(self.win,"START",lambda:self.main_func(),(0,0),fontsize=60,fg=UI_TEXT_COLOUR,bg=BUTTON_COLOUR)
        self.start_button.new_center((self.width//2,self.height//2-self.start_button.fontsize//1.5))
        self.buttons.append(self.start_button)
        self.quit_button = basicUI.button(self.win,"QUIT",lambda:self.quit_func(),(0,0),fontsize=55,fg=UI_TEXT_COLOUR,bg=BUTTON_COLOUR)
        self.quit_button.new_center((self.width//2,self.height//2+self.quit_button.fontsize//1.5))
        self.buttons.append(self.quit_button)
        self.docs_button = basicUI.button(self.win,"DOCS",lambda:self.docs_func(),(0,0),fontsize=20,fg=UI_TEXT_COLOUR,bg=BUTTON_COLOUR)
        self.docs_button.new_center((self.width-self.docs_button.bgRect.width//2-self.margin,self.margin+self.docs_button.fontsize//1.5))
        self.buttons.append(self.docs_button)
    
    def quit_func(self):
        pygame.quit()
        quit()
    def docs_func(self):
        webbrowser.open("https://docs.google.com/document/d/1U96vEvA0jDv8XYHGnGShQUluY2gDUlA39RXWsx02tb4/edit")
    
    def load(self):
        self.win.fill(BG_COLOUR)
        for button in self.buttons:
            button.update()
            button.draw()
        pygame.display.update()


def main():print("main")
if __name__ == '__main__':
    WIDTH, HEIGHT = 1000,500
    win = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
    mainMenu = Menu(win,WIDTH,HEIGHT,lambda:main())
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.VIDEORESIZE:
                old_win = win
                WIDTH,HEIGHT = event.w,event.h
                win = pygame.display.set_mode((event.w,event.h))
                win.blit(old_win,(0,0))
                del old_win
            mainMenu.load()
            
        