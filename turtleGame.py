import pygame
import sys
import random
import math
from pygame.locals import *

class TurtleSprite(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("turtle_sprite2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x=random.randrange(0,599)
        self.rect.y=100+random.randrange(100,400)

class BirdSprite(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("bird.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x=random.randrange(0,599)
        self.rect.y=100+random.randrange(0,600)

class TrashSprite(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("trash.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, random.randrange(0,360))
        self.rect = self.image.get_rect()
        self.rect.x=random.randrange(0,599)
        self.rect.y=random.randrange(0,600)

pygame.init()


#Set the screen size
DISPLAYSURF = pygame.display.set_mode((600,600))

#Random ugly yellow lights
YELLOW = [pygame.Color(255,255,204),pygame.Color(255,255,153),pygame.Color(255,255,102),pygame.Color(255,255,51),pygame.Color(255,255,0)]

SURFSTEPS=100
SURF = [0]*(SURFSTEPS+1)

#Nice waves at the beach
for i in range(0,SURFSTEPS+1):
    SURF[i]=(-math.pi)+((math.pi*2/SURFSTEPS)*i)
    
#Surf position - back and forth
SURFPOS=0
SURFDIRECTION=1


#Control the FPS
clock = pygame.time.Clock()

#surf sounds
beach_sound = pygame.mixer.Sound("ocean_edge.wav")
seagull_sound = pygame.mixer.Sound("seagull_sound.wav")
pygame.mixer.music.load('island_music_x.wav')
pygame.mixer.music.play(-1)

#turtle sprite
turtleSprite = TurtleSprite((100,100))

#bird sprite
birdSprite = BirdSprite((100,100))

#trash sprite
trashSprite1 = TrashSprite((100,100))
trashSprite2 = TrashSprite((100,100))
trashSprite3 = TrashSprite((100,100))
trashSprite4 = TrashSprite((100,100))



orientation=3

hold=0
endgametext=""
#Game loop begins
while True:

    #ANIMATE THE BEACH

    if(SURFPOS==0):
        SURFDIRECTION=1
        pygame.mixer.Sound.play(beach_sound)
        
    if(SURFPOS==SURFSTEPS):
        SURFDIRECTION=-1
        pygame.mixer.Sound.play(beach_sound)

    surflength = abs(int(SURF[SURFPOS]*15))
    oceanlength = abs(int(SURF[SURFPOS]*5))

    #Flickering ugly yellow light
    pygame.draw.rect(DISPLAYSURF, YELLOW[random.randrange(0,4)], pygame.Rect(0, 0, 599, 99))
    #SAND
    pygame.draw.rect(DISPLAYSURF, pygame.Color(210,180,140), pygame.Rect(0, 99, 599, 399+surflength))
    #FOAM
    pygame.draw.rect(DISPLAYSURF, pygame.Color(176,196,222), pygame.Rect(0,399+surflength,599,499-surflength))
    #SEA
    pygame.draw.rect(DISPLAYSURF, pygame.Color(25,25,112), pygame.Rect(0, 499+oceanlength, 599, 99-oceanlength))

    SURFPOS=SURFPOS+SURFDIRECTION

    turtleSpeed=5

    if abs(turtleSprite.rect.x - trashSprite1.rect.x) <30 and abs(turtleSprite.rect.y - trashSprite1.rect.y) < 30 :
       turtleSpeed=1
    if abs(turtleSprite.rect.x - trashSprite2.rect.x) <30 and abs(turtleSprite.rect.y - trashSprite2.rect.y) < 30 :
       turtleSpeed=1
    if abs(turtleSprite.rect.x - trashSprite3.rect.x) <30 and abs(turtleSprite.rect.y - trashSprite3.rect.y) < 30 :
       turtleSpeed=1
    if abs(turtleSprite.rect.x - trashSprite4.rect.x) <30 and abs(turtleSprite.rect.y - trashSprite4.rect.y) < 30 :
       turtleSpeed=1

    if turtleSpeed==1:
        endgametext="Trash makes turtle slow!"
        hold=30
        
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
       orientation=1
       turtleSprite.rect.x=turtleSprite.rect.x-turtleSpeed
       if turtleSprite.rect.x<0:
           turtleSprite.rect.x=turtleSprite.rect.x=0
    if pressed[pygame.K_RIGHT]:
       orientation=3
       turtleSprite.rect.x=turtleSprite.rect.x+turtleSpeed
       if turtleSprite.rect.x>570:
           turtleSprite.rect.x=570
    if pressed[pygame.K_UP]:
       orientation=0
       turtleSprite.rect.y=turtleSprite.rect.y-turtleSpeed
       if turtleSprite.rect.y<0:
           turtleSprite.rect.y=0
    if pressed[pygame.K_DOWN]:
       orientation=2
       turtleSprite.rect.y=turtleSprite.rect.y+turtleSpeed
       if turtleSprite.rect.y>570:
           turtleSprite.rect.y=570

    #move the turtle
    imageFlip=int(SURFPOS%3)
    rot_image = turtleSprite.image.subsurface(imageFlip*30,0,30,30)
    rot_image = pygame.transform.rotate(rot_image, orientation*90)
    DISPLAYSURF.blit(rot_image, turtleSprite.rect )

    #move the bird
    leftBird=False
    if(birdSprite.rect.y > turtleSprite.rect.y):
        birdSprite.rect.y = birdSprite.rect.y-3
    if(birdSprite.rect.y < turtleSprite.rect.y):
        birdSprite.rect.y = birdSprite.rect.y+3
    if(birdSprite.rect.x > turtleSprite.rect.x):
        birdSprite.rect.x = birdSprite.rect.x-3
        leftBird=True
    if(birdSprite.rect.x < turtleSprite.rect.x):
        birdSprite.rect.x = birdSprite.rect.x+3
        leftBird=False
    
    imageFlip=int(SURFPOS%9)
    row=0
    if imageFlip>4:
        row=1
        imageFlip=imageFlip-5
    print(imageFlip)
    rot_image = birdSprite.image.subsurface(imageFlip*80,row*75,70,70)
    if(leftBird==True):
        rot_image = pygame.transform.flip(rot_image,True,False)
    DISPLAYSURF.blit(rot_image, birdSprite.rect )

    if(SURFPOS%30==30):
        pygame.mixer.Sound.play(seagull_sound)
    
    #redraw the trash
    DISPLAYSURF.blit(trashSprite1.image, trashSprite1.rect )
    DISPLAYSURF.blit(trashSprite2.image, trashSprite2.rect )
    DISPLAYSURF.blit(trashSprite3.image, trashSprite3.rect )
    DISPLAYSURF.blit(trashSprite4.image, trashSprite4.rect )

    if hold > 0:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(endgametext, True, (0,255,0),(0,0,128))
        textRect = text.get_rect()
        textRect.center = (300, 300)
        DISPLAYSURF.blit(text, textRect )
        hold=hold-1
    else:
        #endgame
        if(turtleSprite.rect.y>500):
            endgametext="Turtle wins in the sea!"
            hold=30
            turtleSprite.rect.x=random.randrange(0,599)
            turtleSprite.rect.y=100+random.randrange(100,400)

        if(turtleSprite.rect.y<100):
            endgametext="Turtle got lost in the lights!"
            hold=30
            turtleSprite.rect.x=random.randrange(0,599)
            turtleSprite.rect.y=100+random.randrange(100,400)

        if(abs(turtleSprite.rect.y-birdSprite.rect.y)<5 and abs(turtleSprite.rect.x-birdSprite.rect.x )< 5):
            endgametext="Turtle got eaten!"
            hold=30
            turtleSprite.rect.x=random.randrange(0,599)
            turtleSprite.rect.y=100+random.randrange(100,400)
    
    

    #Update the clock tick
    dt = clock.tick(25)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

