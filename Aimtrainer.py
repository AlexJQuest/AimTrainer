import pygame
import math
import time
import random


pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

Target_increment = 400
Target_event = pygame.USEREVENT

Target_padding = 30


BG_Colour = (0,25,40)

LIVES = 3

Labelfont = pygame.font.SysFont("comicsans",24)

class Target:
    Max_Size = 30
    Growth_Rate = 0.2
    Colour = "red"
    Colour_Second = "white"
    
    def __init__(self, x , y):
        self.x = x
        self.y = y 
        self.size = 0
        self.grow = True
    
    def update(self):
        if self.size + self.Growth_Rate >= self.Max_Size: #size checker of tagret
            self.grow= False
            
        if self.grow: #grow target
            self.size += self.Growth_Rate
        else: #shrink target
            self.size -= self.Growth_Rate
            
    def draw(self, win): #draw traget circcles
        pygame.draw.circle(WIN, self.Colour, (self.x , self.y), self.size) 
        pygame.draw.circle(WIN, self.Colour_Second, (self.x , self.y), self.size * 0.8) 
        pygame.draw.circle(WIN, self.Colour, (self.x , self.y), self.size * 0.6) 
        pygame.draw.circle(WIN, self.Colour_Second, (self.x , self.y), self.size * 0.4) 
        pygame.draw.circle(WIN, self.Colour, (self.x , self.y), self.size* 0.2)
        
    def collide (self, x,y):
        distance = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return distance <= self.size  


def draw(win,targets):
    win.fill(BG_Colour) #clear field
    
    for target in targets:
        target.draw(win) #draw target
        
    
        

def formattime(secs):
    milli = math.floor(int(secs*1000 %1000)/100)
    seconds = int(round(secs%60,1))
    minutes = int(seconds // 60 )
    return f"{minutes:02d}:{seconds:02d}:{milli}"

def drawtopbar(win, elapsedtime, targetspressed, misses):
    
    pygame.draw.rect(win, "grey", (0,0,WIDTH,50))
    timelable = Labelfont.render(f"Time:{formattime(elapsedtime)}",1,"white")
    
    
    speed= round(targetspressed / elapsedtime, 1)
    speedlabel = Labelfont.render(f"Speed: {speed} t/s",1, "White")
    hitslabel = Labelfont.render(f"Hits: {targetspressed} t/s",1, "White")
    liveslabel = Labelfont.render(f"Lives: {LIVES-misses} t/s",1, "White")
    
    win.blit(timelable, (5,5))
    win.blit(speedlabel, (200,5))
    win.blit(hitslabel, (450,5))
    win.blit(liveslabel, (650,5))
    

def endscreen(win, elapsedtime, targetspressed, clicks):
    win.fill(BG_Colour)
    speed= round(targetspressed / elapsedtime, 1)
    speedlabel = Labelfont.render(f"Speed: {speed} t/s",1, "White")
    hitslabel = Labelfont.render(f"Hits: {targetspressed} t/s",1, "White")
    accuracy = round(targetspressed/clicks*100,1)
    accuracylabel = Labelfont.render(f"Accuracy: {accuracy} t/s",1, "White")
    timelable = Labelfont.render(f"Time:{formattime(elapsedtime)}",1,"white")
    win.blit(timelable, (getmiddle(timelable),100))
    win.blit(speedlabel, (getmiddle(speedlabel),200))
    win.blit(hitslabel, (getmiddle(hitslabel),300))
    win.blit(accuracylabel, (getmiddle(accuracylabel),4))
    
    pygame.display.update()
    
    run =True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()
 

def getmiddle(surface):
    return WIDTH/2 - surface.get_width()/2

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targetpressed = 0
    clicks = 0
    misses = 0 
    starttime = time.time()
    
    pygame.time.set_timer(Target_event, Target_increment) #eventy every timer increment
    
    while run:
        
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsedtime = time.time() - starttime
        
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 run = False
                 break
             if event.type == Target_event:
                 x = random.randint(Target_padding, WIDTH - Target_padding) #add padding
                 y = random.randint(Target_padding + 50, HEIGHT - Target_padding) #add padding
                 target = Target(x,y)
                 targets.append(target)   
                 
             if event.type == pygame.MOUSEBUTTONDOWN: #check click
                 click = True
                 clicks += 1
                 
                 
        for target in targets:
             target.update()
             
             if target.size <= 0:
                 targets.remove(target)
                 misses += 1
                 
             if click and target.collide(*mouse_pos):
                targets.remove(target)
                targetpressed += 1
                     
        if misses >= LIVES:
            endscreen(WIN, elapsedtime, targetpressed, clicks) #endgame
             
        draw(WIN, targets)
        drawtopbar(WIN, elapsedtime, targetpressed, misses)
        pygame.display.update() #update pygame field
         
    pygame.quit()
    
if __name__ ==  "__main__":
     main()