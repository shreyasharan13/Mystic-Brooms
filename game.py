import pygame as pg
import sys,time
from harry import Harry
from tower import Tower
pg.init()


class Game:
    def __init__(self):
        #setting windows for config
        self.width=392
        self.height=512
        #self.scale_factor=1.5
        self.win=pg.display.set_mode((self.width,self.height))
        self.clock=pg.time.Clock()
        self.move_speed=250
        self.start_monitoring=False
        self.score=0
        self.font=pg.font.Font("mystic brooms/gallery/sprites/font.ttf",30)
        self.crash_sound = pg.mixer.Sound("mystic brooms/gallery/audio/hit.wav")
        self.fly_sound = pg.mixer.Sound("mystic brooms/gallery/audio/wing.wav")
        self.score_text=self.font.render("Score: 0",True,(255,255,255))
        self.score_text_rect=self.score_text.get_rect(center=(50,30))
        self.restart_text=self.font.render("Restart",True,(255,255,255))
        self.restart_text_rect=self.restart_text.get_rect(center=(196,475))
        self.crash_sound_played = False
        self.harry=Harry()
        self.is_enter_pressed=False
        self.is_game_started=True
        self.towers=[]
        self.tower_generate_counter=56
        self.setUpBgAndGround()
        self.play_music()
        self.high_score=self.loadHighScore()
        self.gameloop()
        

    def gameloop(self):
        last_time=time.time()
        while True:
            #calculatimg delta time
            new_time=time.time()
            dt=new_time-last_time
            last_time=new_time

            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and self.is_game_started:
                    if event.key == pg.K_RETURN:
                        self.is_enter_pressed=True  
                        self.harry.update_on=True
                        self.fly_sound.play()    
                    if event.key == pg.K_SPACE and self.is_enter_pressed:
                        self.harry.flap(dt)
                        self.fly_sound.play()    
                if event.type==pg.MOUSEBUTTONUP:
                    if self.restart_text_rect.collidepoint(pg.mouse.get_pos()):
                        self.restartGame()


            self.updateEverything(dt)
            self.checkCollisions() 
            self.checkScore()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60) #humara game 60 fps se zda na chle


    def play_music(self):
        # You can replace 'path_to_your_music_file' with the actual path to your music file
        pg.mixer.music.load('mystic brooms/gallery/sprites/bgmusic.mp3')
        pg.mixer.music.play(-1) # -1 means loop foreve  


    def loadHighScore(self):
        try:
            with open("high_score.txt", "r") as file:
                high_score = int(file.read())
                return high_score
        except FileNotFoundError:
            return 0

    def saveHighScore(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))    

    def restartGame(self):
        self.score=0 
        self.score_text=self.font.render("Score: 0",True,(255,255,255))
        self.is_enter_pressed=False
        self.is_game_started=True
        self.crash_sound_played = False
        self.harry.resetPosition()
        self.towers.clear()
        self.tower_generate_counter=56
        self.harry.update_on=True
        self.play_music()
        if self.score > self.high_score:
            self.high_score = self.score
            self.saveHighScore()

    def checkScore(self):
            if len(self.towers)>0:
                    if (self.harry.rect.left>self.towers[0].rect_down.left and
                        self.harry.rect.right< self.towers[0].rect_down.right and not self.start_monitoring):
                        self.start_monitoring=True
                    if self.harry.rect.left > self.towers[0].rect_down.right and self.start_monitoring:
                        self.start_monitoring=False  
                        self.score+=1
                        self.score_text=self.font.render(f"Score: {self.score}",True,(255,255,255))
                        
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.saveHighScore()    

    
    def checkCollisions(self):
        if len(self.towers):
            if self.harry.rect.bottom>445:
                if not self.crash_sound_played:
                    self.harry.update_on=False
                    self.is_enter_pressed=False
                    self.is_game_started=False
                    self.crash_sound.play()
                    self.crash_sound_played = True
                    pg.mixer_music.stop()


            if (self.harry.rect.colliderect(self.towers[0].rect_down) or 
            self.harry.rect.colliderect(self.towers[0].rect_up)):
                if not self.crash_sound_played:
                    self.is_enter_pressed=False
                    self.is_game_started=False
                    self.crash_sound.play()
                    self.crash_sound_played = True
                    pg.mixer_music.stop()
                
    
    
    def updateEverything(self,dt): 
        if self.is_enter_pressed:
            #moving the ground
            self.ground1_rect.x-=int(self.move_speed*dt)
            self.ground2_rect.x-=int(self.move_speed*dt)
            if self.ground1_rect.right<0:
                self.ground1_rect.x=self.ground2_rect.right
            if self.ground2_rect.right<0:
                self.ground2_rect.x=self.ground1_rect.right  
            #generating towers
            if self.tower_generate_counter>55:
                self.towers.append(Tower(self.move_speed))
                self.tower_generate_counter=0
            self.tower_generate_counter+=1
            #moving the towers
            for tower in self.towers:
                tower.update(dt)  
            #moving the birds      
            if len(self.towers)!=0:
                if self.towers[0].rect_up.right<0:
                    self.towers.pop(0)

        self.harry.update(dt)



    def drawEverything(self):
        self.win.blit(self.bg_img,(0,0))

        for tower in self.towers:
            tower.drawTower(self.win)


        self.win.blit(self.ground1_img,self.ground1_rect)
        self.win.blit(self.ground2_img,self.ground2_rect)
        self.win.blit(self.harry.image,self.harry.rect)
        self.win.blit(self.score_text,self.score_text_rect)
        if not self.is_game_started:
            self.win.blit(self.restart_text,self.restart_text_rect)

        high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        high_score_text_rect = high_score_text.get_rect(center=(self.width // 1.23, 30))
        self.win.blit(high_score_text, high_score_text_rect)    
                           



    def setUpBgAndGround(self):
        self.bg_img=pg.image.load("mystic brooms/gallery/sprites/bg.png").convert()
        self.ground1_img=pg.image.load("mystic brooms/gallery/sprites/ground.png").convert()
        self.ground2_img=pg.image.load("mystic brooms/gallery/sprites/ground.png").convert()
        
        self.ground1_rect=self.ground1_img.get_rect()
        self.ground2_rect=self.ground2_img.get_rect()
        
        self.ground1_rect.x=0  #464
        self.ground2_rect.x=self.ground1_rect.right
        self.ground1_rect.y=435
        self.ground2_rect.y=435

game=Game()
## 435 ground, bird img height = 35 