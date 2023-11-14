"""
A package including a variety of UI functions including:
- Text elements
- input elements (dropdown selection, buttons)
"""

import pygame, time, random
pygame.init()

def text(surface,info,x,y,colour=(0,0,0),size=30):
    textfont = pygame.font.Font(None,size)
    text = textfont.render(info,True,colour)
    text_rect = text.get_rect(topleft=(x,y))
    surface.blit(text,text_rect)

class button:
    def __init__(self,surface,text,command,pos,fontsize=30,fg=(0,0,0),bg=(255,255,255)):
        self.surface = surface
        self.command = command
        self.fg, self.bg = fg, bg
        self.pos = pos
        self.clickState = False
        
        self.text = text
        self.fontsize = fontsize
        self.font = pygame.font.Font(None,self.fontsize)
        self.info = self.font.render(self.text,True,self.fg)
        self.fgRect = self.info.get_rect(topleft=pos)
        self.bgRect = self.fgRect.inflate(20,20)
        self.fgRect.center = self.bgRect.center
        
    def update(self):
        
        mouse_pos = pygame.mouse.get_pos()
        if self.bgRect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and self.clickState == False:
            self.clickState = True
            self.command()
        if not pygame.mouse.get_pressed()[0] and self.clickState == True:
            self.clickState = False
            
    def draw(self):
        pygame.draw.rect(self.surface,self.bg,self.bgRect)
        pygame.draw.rect(self.surface,self.fg,self.bgRect,width=2)
        self.surface.blit(self.info,self.fgRect)
        
    def new_center(self,ctr):
        self.fgRect.center = ctr
        self.bgRect.center = ctr

class dropdown:
    def __init__(self,surface,text,pos,fontsize=30,fg=(0,0,0),bg=(255,255,255),padx=30,pady=20):
        self.surface = surface
        self.fg, self.bg = fg, bg
        self.pos = pos
        self.state = False # False = Closed, True = Open
        self.clickState = False
        self.isCooldown = False
        self.cooldownTimer = 0
        
        self.text = text
        self.fontsize = fontsize
        self.font = pygame.font.Font(None,self.fontsize)
        self.padx, self.pady = padx, pady
        self.dropPadx,self.dropPady = 30,20
        self.borderWidth = 2
        
        self.barTxt = self.font.render(self.text,True,self.fg)
        self.barRect1 = self.barTxt.get_rect(topleft=pos)
        self.barRect2 = self.barRect1.inflate(self.padx,self.pady)
        
        self.dropTxt = self.font.render("v",True,self.fg)
        self.dropPos = (self.barRect2.topright[0]+self.dropPadx//2 - self.borderWidth//2,
                        self.barRect2.topright[1]+self.dropPady//2)
        self.dropRect1 = self.dropTxt.get_rect(topleft=self.dropPos)
        self.dropRect2 = self.dropRect1.inflate(self.dropPadx,self.dropPady)
        
        self.options = []
        self.optBoxes = []
        self.optHeight = 0

        self.optWidth = self.barRect2.width
        self.optPos = self.barRect2.bottomleft[0],self.barRect2.bottomleft[1] - self.borderWidth//2
        self.optRect = pygame.Rect(self.optPos[0],self.optPos[1],self.optWidth,self.optHeight)
    
    def update(self):

        mouse_pos = pygame.mouse.get_pos()
        if self.dropRect2.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and self.clickState == False:
            self.clickState = True
            if self.state == False: # Open
                self.dropTxt = self.font.render("^",True,self.fg)
                self.state = True
            elif self.state == True: # Closed
                self.dropTxt = self.font.render("v",True,self.fg)
                self.state = False
        if not pygame.mouse.get_pressed()[0] and self.clickState == True:
            self.clickState = False
                
        # Main Bar:
        pygame.draw.rect(self.surface,self.bg,self.barRect2)
        pygame.draw.rect(self.surface,self.fg,self.barRect2,width=self.borderWidth)
        self.surface.blit(self.barTxt,self.barRect1)
        # Drop button:
        pygame.draw.rect(self.surface,self.bg,self.dropRect2)
        pygame.draw.rect(self.surface,self.fg,self.dropRect2,width=self.borderWidth)
        self.surface.blit(self.dropTxt,self.dropRect1)
        # Options:
        if self.state == True and len(self.options) > 0:
            pygame.draw.rect(self.surface,self.bg,self.optRect)
            pygame.draw.rect(self.surface,self.fg,self.optRect,width=self.borderWidth)
            
            for box in self.optBoxes: # box[0] = Large rect (rect2), box[1] = text rect (rect1), box[2] = text, box[3] = command
                
                if box[0].collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and self.clickState == False:
                    self.clickState = True
                    box[3]()
                    self.barTxt = box[2]
                if not pygame.mouse.get_pressed()[0] and self.clickState == True:
                    self.clickState = False
                
                pygame.draw.rect(self.surface,self.bg,box[0])
                pygame.draw.rect(self.surface,self.fg,box[0],width=self.borderWidth)
                self.surface.blit(box[2],box[1])
    
    def add_option(self,text,command):
        
        self.options.append((text,command))
        if len(self.options) == 1:
            txtPos = (self.barRect2.bottomleft[0], self.barRect2.bottomleft[1] - self.borderWidth//2)
        else:
            txtPos = (self.optBoxes[-1][0].bottomleft[0], self.optBoxes[-1][0].bottomleft[1] - self.borderWidth//2) # previous txtRect2

        txt = self.font.render(text,True,self.fg)
        txtRect1 = txt.get_rect(topleft=(0,0))
        txtRect2 = txtRect1.inflate(self.padx,self.pady)
        txtRect2.topleft = txtPos
        txtRect2.width = self.barRect2.width
        txtRect1.center = txtRect2.center
        
        self.optBoxes.append([txtRect2,txtRect1,txt,command])
        self.optRect.height += self.fontsize


if __name__ == '__main__':
    win = pygame.display.set_mode((500,500))
    def rand():print(random.randint(1,100))
    def dij():print("dijkstra")
    def Astar():print("A star")
    b = button(win,"random number thing",lambda:rand(),(100,100))
    d = dropdown(win,"dijkstra",(200,300),fontsize=25,padx=275)
    d.add_option("dijkstra",lambda:dij())
    d.add_option("A star",lambda:Astar())
    while True:
        pygame.time.Clock().tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
        win.fill((255,255,255))
        b.update()
        d.update()
        pygame.display.update()