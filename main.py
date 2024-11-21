import pygame
import sys
from pygame.sprite import Sprite

class Shooter:
    def __init__(self, ss):
        angle=270
        self.screen=ss.screen
        self.image=pygame.image.load('images/shooter.png')
        self.r_image=pygame.transform.rotate(self.image, angle)
        self.r_rect=self.r_image.get_rect()
        self.r_rect.midleft=ss.screen_rect.midleft        
        self.moving_up=False
        self.moving_down=False        
        
    def update(self):
        if self.moving_up and self.r_rect.top > ss.screen_rect.top:
            self.r_rect.y-=2
        if self.moving_down and self.r_rect.bottom < ss.screen_rect.bottom:
            self.r_rect.y+=2

            
class Bullet(Sprite):
    def __init__(self, ss):
        super().__init__()
        self.b_rect=pygame.Rect(0,0,12,3)
        self.b_rect.midleft=ss.r_rect.midright
        self.b_color=(255,255,255)

    def update(self):
        self.b_rect.x+=5
        pygame.draw.rect(ss.screen, self.b_color,self.b_rect)
            
class SidewaysShooter:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((1000,600))
        pygame.display.set_caption('Sideways Shooter')
        self.screen_rect=self.screen.get_rect()
        self.bg_color=(0,0,13)
        self.clock=pygame.time.Clock()
        self.shooter=Shooter(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()

    def _fire_bullets(self):
        new_bullet=Bullet(self.shooter)
        self.bullets.add(new_bullet)

    def _update_bullets_group(self):
        for bullet in self.bullets.copy():
            if bullet.b_rect.right > self.screen_rect.right:
                self.bullets.remove(bullet)
    def _check_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
                
    def _check_keyup_events(self,event):
        if event.key==pygame.K_UP:
            self.shooter.moving_up=False
        elif event.key==pygame.K_DOWN:
            self.shooter.moving_down=False
        
    def _check_keydown_events(self,event):
        if event.key==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_UP:
            self.shooter.moving_up=True
        elif event.key==pygame.K_DOWN:
            self.shooter.moving_down=True
        elif event.key==pygame.K_SPACE:
            self._fire_bullets()
    
    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.bullets.update()
        self.screen.blit(self.shooter.r_image, self.shooter.r_rect)
        self.shooter.update()
        pygame.display.flip()
        
    def run_game(self):
        while 1:
            self._check_events()
            self._update_bullets_group()
            self._update_screen()
            self.clock.tick(60)
        
if __name__=='__main__':
    ss=SidewaysShooter()
    ss.run_game()
