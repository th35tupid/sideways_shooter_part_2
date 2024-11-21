import pygame
import sys
from pygame.sprite import Sprite
from random import randint

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
            self.r_rect.y-=5
        if self.moving_down and self.r_rect.bottom < ss.screen_rect.bottom:
            self.r_rect.y+=5

            
class Bullet(Sprite):
    def __init__(self, ss):
        super().__init__()
        self.b_rect=pygame.Rect(0,0,12,3)
        self.b_rect.midleft=ss.r_rect.midright
        self.b_color=(255,255,255)
        self.rect=self.b_rect
    def update(self):
        self.b_rect.x+=10
        pygame.draw.rect(ss.screen, self.b_color,self.b_rect)


class Alien(Sprite):
    def __init__(self,ss):
        super().__init__()
        self.a_image=pygame.image.load('images/alien.png')
        self.a_rect=self.a_image.get_rect()
        self.rect=self.a_rect

    def update(self):
        self.x=float(self.a_rect.x)
        self.x-=0.4
        self.a_rect.x=int(self.x)
        ss.screen.blit(self.a_image, self.a_rect)            
        for alien in ss.aliens.copy():
            if alien.a_rect.x <= 0:
                ss.aliens.remove(alien)
                
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
        self.last_creation_time=pygame.time.get_ticks()
        self.create_aliens_delay=900
        
    def _fire_bullets(self):
        new_bullet=Bullet(self.shooter)
        self.bullets.add(new_bullet)

    def _update_bullets_group(self):
        for bullet in self.bullets.copy():
            if bullet.b_rect.right > self.screen_rect.right:
                self.bullets.remove(bullet)
                
    def _create_aliens(self):
        alien=Alien(self)
        alien.a_rect.x=randint(6*ss.shooter.r_rect.width, ss.screen_rect.width - alien.a_rect.width)        
        alien.a_rect.y=randint(2, ss.screen_rect.height - alien.a_rect.height)
        self.aliens.add(alien)
                
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
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        self.bullets.update()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_create_time >= self.create_aliens_delay:
            self._create_aliens()
            self.last_create_time = current_time
        self.aliens.update()
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
