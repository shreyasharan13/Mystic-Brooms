import pygame as pg
from random import randint

class Tower:
    def __init__(self,move_speed): 
        self.img_up=pg.image.load("mystic brooms/gallery/sprites/towerup.png").convert_alpha()
        self.img_down=pg.image.load("mystic brooms/gallery/sprites/towerdown.png").convert_alpha()
        self.rect_up=self.img_up.get_rect()
        self.rect_down=self.img_down.get_rect()
        self.tower_distance=150
        self.rect_up.y=randint(190,330)
        self.rect_up.x=392
        self.rect_down.y=self.rect_up.y-self.tower_distance-self.rect_up.height
        self.rect_down.x=392
        self.move_speed=move_speed


    def drawTower(self,win):
        win.blit(self.img_up,self.rect_up)
        win.blit(self.img_down,self.rect_down)  

    def update(self,dt):
        self.rect_up.x-=self.move_speed*dt
        self.rect_down.x-=self.move_speed*dt      






