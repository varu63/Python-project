import math
import random
import time
import pygame

# Initializes Pygame
pygame.init()

# Creates a window of size 800x600.

Width,Hight= 800,600
Win = pygame.display.set_mode((Width,Hight))
pygame.display.set_caption("Aim Trainer")

# Sets the time interval for new targets, padding, background color, player lives, top bar height, and font.


TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
BG_COLOR = (0,25,40)
LIVES = 3
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("comicsans",24)

# Represents the red and white circle target.
class Target:
    MAX_SIZE = 30
    GROWTH_RATE=0.2
    COLOR = "red"
    SECOND_COLOR = "white"
   
    # Initializes position and size.
    def __init__(self,x ,y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True
        
    # Grows and shrinks the circle.
    def Upadate(self):
        if self.size + self.GROWTH_RATE>=self.MAX_SIZE:
            self.grow = False
        if self.grow:
            self.size+=self.GROWTH_RATE
        else:
            self.size-=self.GROWTH_RATE
    
    # Draws multiple concentric circles.
    def draw(self,win):
        pygame.draw.circle(win , self.COLOR,(self.x ,self.y),self.size)
        pygame.draw.circle(win , self.SECOND_COLOR,(self.x ,self.y),self.size * 0.8)
        pygame.draw.circle(win , self.COLOR,(self.x ,self.y),self.size * 0.6)
        pygame.draw.circle(win , self.SECOND_COLOR,(self.x ,self.y),self.size * 0.4)
    
    # Checks if a mouse click hit the target.
    def collide(self,x,y):
        dis = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return dis <= self.size

# Checks if a mouse click hit the target.
def draw(win,targets):
    win.fill(BG_COLOR) 

    for target in targets:
        target.draw(win)
    
# Formats time to MM:SS:MS.
def formate_time(secs):
    milli = math.floor(int(secs*1000%1000)/100)
    second = int(round(secs%60 ,1))
    minutes = int(secs // 60)
    return f"{minutes :02d}:{second : 02d}:{milli : 02d}"

# Draws top bar showing:{Time elapsed ,Speed (targets/sec) , Hits , Lives left }
def draw_top_bar(win,elapsed_time , targets_pressed , misses):
    pygame.draw.rect(win,"grey",(0,0,Width ,TOP_BAR_HEIGHT ))
    time_label = LABEL_FONT.render(f"{formate_time(elapsed_time)}",1,"black")
    
    speed = round(targets_pressed / elapsed_time ,1)
    speed_label = LABEL_FONT.render(f"Speed : {speed} t/s" ,1 , "black")
    
    hits_label = LABEL_FONT.render(f"Hits:{targets_pressed}" ,1 ,"black")

    live_label = LABEL_FONT.render(f"Live:{LIVES - misses}" ,1 ,"black")

    win.blit(time_label,(5,5))
    win.blit(speed_label,(140,5))
    win.blit(hits_label,(340,5))
    win.blit(live_label,(440,5))
 
# Shows the final score after losing:{Time , Speed , Hits , Accuracy}
# Waits for a key or quit event to close.
def end_screen(win , elpsed_time ,tardets_pressed , clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"{formate_time(elpsed_time)}",1,"white")
    
    speed = round(tardets_pressed / elpsed_time ,1)
    speed_label = LABEL_FONT.render(f"Speed : {speed} t/s" ,1 , "white")
    
    hits_label = LABEL_FONT.render(f"Hits:{tardets_pressed}" ,1 ,"white")

    accuracy = round(tardets_pressed / clicks *100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy:{accuracy} %" ,1 ,"white")

    win.blit(time_label,(get_middle(time_label),100))
    win.blit(speed_label,(get_middle(speed_label),200))
    win.blit(hits_label,(get_middle(hits_label),300))
    win.blit(accuracy_label,(get_middle(accuracy_label),400))

    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()
            
# Centers a surface horizontally on the screen.
def get_middle(surface):
    return Width/2-surface.get_width()/2


def main():
    run = True
    clock = pygame.time.Clock()
    targets = []

    target_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT,TARGET_INCREMENT)
    while run:
        clock.tick(60)
        click = False
        elapsed_time = time.time() - start_time
        mou_postion = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run == False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING ,Width - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT ,Hight - TARGET_PADDING)
                target = Target(x,y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1


        for target in targets:
            target.Upadate()

            if target.size<=0:
                targets.remove(target)
                misses +=1

            if click and target.collide(*mou_postion):
                targets.remove(target)
                target_pressed += 1

        if misses >= LIVES:
            end_screen(Win, elapsed_time ,target_pressed ,clicks)

        draw(Win,targets) 
        draw_top_bar(Win,elapsed_time ,target_pressed , misses )
        pygame.display.update()


    pygame.quit()

# Starts the game.
if __name__=="__main__":
    main()