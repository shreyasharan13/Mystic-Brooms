
import pygame as pg


class Harry(pg.sprite.Sprite):
    def __init__(self):
        super(Harry,self).__init__()
        self.img_list=[pg.image.load("mystic brooms/gallery/sprites/harryup.png").convert_alpha(),
                       pg.image.load("mystic brooms/gallery/sprites/harrydown.png").convert_alpha()
                       ]
        self.image_index=0
        self.image=self.img_list[self.image_index]
        self.rect=self.image.get_rect(center=(100,100))
        self.y_velocity=0
        self.gravity=10
        self.flap_speed=250
        self.anim_counter=0
        self.update_on=False

    def update(self,dt):
    
     if self.update_on:
          self.playAnimation()
          self.applyGravity(dt)

          if self.rect.y<=0:
            self.rect.y=0
            self.flap_speed=0
          elif self.rect.y>0 and self.flap_speed==0:
            
            self.flap_speed=250

    def applyGravity(self,dt):
          
          self.y_velocity+=self.gravity*dt
          self.rect.y+=self.y_velocity



    def flap(self,dt):
        self.y_velocity=-self.flap_speed*dt

    def playAnimation(self):
        if self.anim_counter==5:
            self.image=self.img_list[self.image_index]
            if self.image_index==0: self.image_index=1
            else: self.image_index=0
            self.anim_counter=0
        self.anim_counter+=1   

    def resetPosition(self):
        self.rect.center=(100,100)
        self.y_velocity=0
        self.anim_counter=0





