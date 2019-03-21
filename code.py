#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 01:28:37 2019

@author: jeanettelin, kiannamills, mallikavarkhedi, audreyzhang
"""
import pygame
import random
import pygame.locals
 
# Global constants

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK =  (255, 0, 200)
PURPLE = (40,0,109)
L_BLUE = (141, 191, 255)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Arrays of bear images. Each increase in index increases the bear size by 108%
bear1= pygame.image.load('graphic/bear1.png')
bear1= pygame.transform.scale(bear1, (65,100))
bear1Inc1 = pygame.transform.scale(bear1, (int(65*1.08),int(100*1.08)))
bear1Inc2 = pygame.transform.scale(bear1, (int(65*1.08*1.08),int(100*1.08*1.08)))
bear1Inc3 = pygame.transform.scale(bear1, (int(65*1.08*1.08*1.08),int(100*1.08*1.08*1.08)))
bear1Arr = [bear1, bear1Inc1, bear1Inc2, bear1Inc3]


bear2= pygame.image.load('graphic/bear2.png')
bear2= pygame.transform.scale(bear2, (65,100))
bear2Inc1 = pygame.transform.scale(bear2, (int(65*1.08),int(100*1.08)))
bear2Inc2 = pygame.transform.scale(bear2, (int(65*1.08*1.08),int(100*1.08*1.08)))
bear2Inc3 = pygame.transform.scale(bear2, (int(65*1.08*1.08*1.08),int(100*1.08*1.08*1.08)))
bear2Arr = [bear2, bear2Inc1, bear2Inc2, bear2Inc3]

bear_l= pygame.image.load('graphic/bear_walk_left.png')
bear_l= pygame.transform.scale(bear_l, (65,100))
bear_lInc1 = pygame.transform.scale(bear_l, (int(65*1.08),int(100*1.08)))
bear_lInc2 = pygame.transform.scale(bear_l, (int(65*1.08*1.08),int(100*1.08*1.08)))
bear_lInc3 = pygame.transform.scale(bear_l, (int(65*1.08*1.08*1.08),int(100*1.08*1.08*1.08)))
bear_lArr = [bear_l, bear_lInc1, bear_lInc2, bear_lInc3]

bear_r= pygame.image.load('graphic/bear_walk_right.png')
bear_r= pygame.transform.scale(bear_r, (65,100))
bear_rInc1 = pygame.transform.scale(bear_r, (int(65*1.08),int(100*1.08)))
bear_rInc2 = pygame.transform.scale(bear_r, (int(65*1.08*1.08),int(100*1.08*1.08)))
bear_rInc3 = pygame.transform.scale(bear_r, (int(65*1.08*1.08*1.08),int(100*1.08*1.08*1.08)))
bear_rArr = [bear_r, bear_rInc1, bear_rInc2, bear_rInc3]


#Load images of coin, life, bonus, enemy, box, background, cover, start
coin= pygame.image.load('graphic/coin.png')
coin= pygame.transform.scale(coin, (45,44))

bonus= pygame.image.load('graphic/bonus.png')
bonus= pygame.transform.scale(bonus, (52,74))

enemy= pygame.image.load('graphic/enemy1.png')
enemy= pygame.transform.scale(enemy, (65,100))

box= pygame.image.load('graphic/box.png')
box= pygame.transform.scale(box, (350,150))

background = pygame.image.load('graphic/background.png')

cover= pygame.image.load('graphic/cover.png')
cover= pygame.transform.scale(cover, (800,600))

bullet = pygame.image.load('graphic/bullet.png')
bullet = pygame.transform.scale(bullet, (19,25))

final_box= pygame.image.load('graphic/final_box.png')
final_box= pygame.transform.scale(final_box, (351,177))
 
 
class Player(pygame.sprite.Sprite):
   
 
    def __init__(self):
        """ Constructor function """
 
        super(Player,self).__init__()
 
        
        self.index = 0
        self.width = 65
        self.height = 100
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)
        self.image.set_colorkey((0,0,0))
        self.image.blit(bear1Arr[self.index], (0,0))
 
        self.rect = self.image.get_rect()
 
        self.change_x = 0
        self.change_y = 0
 
        self.level = None
        self.score = 0

        self.lives = 5
        self.restart = False
        self.reachedEnd = False
 
    def update(self):
        # Gravity
        self.calc_grav()
 
        self.rect.x += self.change_x
 
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for enemy in enemy_hit_list:
            if self.change_x > 0:
                self.rect.right = enemy.rect.left
            elif self.change_x < 0:
                self.rect.left = enemy.rect.right
            self.restart = True

        final_hit_list = pygame.sprite.spritecollide(self, self.level.final_list, False)
        for final in final_hit_list:
            if self.change_x > 0:
                self.rect.right = final.rect.left
            elif self.change_x < 0:
                self.rect.left = final.rect.right
            self.reachedEnd = True
            return

        if self.rect.y == SCREEN_HEIGHT - self.rect.height:
            self.restart = True
            return
            
 
        self.rect.y += self.change_y
 
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            self.change_y = 0
 
            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x

        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        for enemy in enemy_hit_list:
            if self.change_y > 0:
                self.rect.bottom = enemy.rect.top
            elif self.change_y < 0:
                self.rect.top = enemy.rect.bottom
            pygame.mixer.music.pause()
            enemyNoise = pygame.mixer.music.load('gameSounds/ouch.wav')
            pygame.mixer.music.play()
            self.change_y = 0
            self.restart = True

        if self.rect.y == SCREEN_HEIGHT - self.rect.height:
            self.restart = True
            return 

        coin_hit_list = pygame.sprite.spritecollide(self, self.level.coin_list, False)
        for coin in coin_hit_list:
            coin.kill()
            pygame.mixer.music.pause()
            coinNoise = pygame.mixer.music.load('gameSounds/coinSound.mp3')
            pygame.mixer.music.play()
            self.incPoints()

        final_hit_list = pygame.sprite.spritecollide(self, self.level.final_list, False)
        for final in final_hit_list:
            if self.change_x > 0:
                self.rect.right = final.rect.left
            elif self.change_x < 0:
                self.rect.left = final.rect.right
            self.reachedEnd = True
            return

 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def increase(self):
        print("increase")
        self.index +=1
        if self.index == 1:
            self.image = pygame.transform.scale(self.image, (int(65*1.08),int(100*1.08)))
            self.width = int(65*1.08)
            self.height = int(100*1.08)
            self.rect.width = int(65*1.08)
            self.rect.height = int(100*1.08)
            self.change_x = 0
            self.change_y = 0
        if self.index == 2:
            self.image = pygame.transform.scale(self.image, (int(65*1.08*1.08),int(100*1.08*1.08)))
            self.width = int(65*1.08*1.08)
            self.height = int(100*1.08*1.08)
            self.rect.width = int(65*1.08*1.08)
            self.rect.height = int(100*1.08*1.08)
            self.change_x = 0
            self.change_y = 0
        if self.index == 3:
            self.image = pygame.transform.scale(self.image, (int(65*1.08*1.08*1.08),int(100*1.08*1.08*1.08)))
            self.width = int(65*1.08*1.08*1.08)
            self.height = int(100*1.08*1.08*1.08)
            self.rect.width = int(65*1.08*1.08*1.08)
            self.rect.height = int(100*1.08*1.08*1.08)
            self.change_x = 0
            self.change_y = 0
      

 
    def jump(self):
        self.image.fill(BLACK)
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(bear2Arr[self.index], (0,0))
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def fireBullet(self):
        bullet = Bullet()
        bullet.rect.x = self.rect.x + 20
        bullet.rect.y = self.rect.y + 20
        bullet.player = self
        bullet.level = self.level
        self.level.bullet_list.add(bullet)

 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.image.fill(BLACK)
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(bear_lArr[self.index], (0,0))
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.image.fill(BLACK)
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(bear_rArr[self.index], (0,0))
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.image.fill(BLACK)
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(bear1Arr[self.index], (0,0))
        self.change_x = 0

    def incPoints(self):
        self.score += 20


class Enemy(pygame.sprite.Sprite):
    """ Enemy that can harm the player """
    change_x = 0
    change_y = 0
 
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    level = None
    player = None

    def __init__(self, width, height):

        super(Enemy,self).__init__()

        self.image = pygame.Surface([65,100])
        self.image.fill(BLACK)
        self.image.set_colorkey((0,0,0))
        self.image.blit(enemy, (0,0))

        self.rect = self.image.get_rect()

    def update(self):
 
        self.rect.x += self.change_x
 
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right
 
        self.rect.y += self.change_y
 
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom
 
        
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
 
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    level = None
    player = None

    def __init__(self):
        super(Bullet,self).__init__()
 
        self.image = pygame.Surface([19, 25])
        self.image.fill(BLACK)
        self.image.set_colorkey((0,0,0))
        self.image.blit(bullet, (0,0))

 
        self.rect = self.image.get_rect()
    def enemyHitMusic(self):
        pygame.mixer.music.pause()
        enemyNoise = pygame.mixer.music.load('gameSounds/ouch.wav')
        pygame.mixer.music.play()
 
    def update(self):
        """ Move the bullet. """
        self.rect.x += 6

        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, True)
        for enemy in enemy_hit_list:
            self.level.bullet_list.remove(self)
            self.level.enemy_list.remove(enemy)
            self.player.score += 50
            self.enemyHitMusic()
            


class Boost(pygame.sprite.Sprite):
    """ Boost that can help the player """
    change_x = 0
    change_y = 0
 
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    level = None
    player = None

    def __init__(self, width, height):

        super(Boost,self).__init__()

        self.image = pygame.Surface([52,74])
        self.image.fill(BLACK)
        self.image.set_colorkey((0,0,0))
        self.image.blit(bonus, (0,0))

        self.rect = self.image.get_rect()
    def update(self):
 
        self.rect.x += self.change_x
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            self.player.increase()
            pygame.mixer.music.pause()
            powerUpNoise = pygame.mixer.music.load('gameSounds/PowerUpSound.mp3')
            pygame.mixer.music.play()
            self.kill()
            
            
 
        self.rect.y += self.change_y
 
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
 
            self.kill()
 
      
            self.change_x *= -1

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super(Platform,self).__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(L_BLUE)
        self.image.set_colorkey((0,0,0))
        self.image.blit(box, (-10,-30))
 
        self.rect = self.image.get_rect()

class FinalPlatform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super(FinalPlatform,self).__init__()
 
        self.image = pygame.Surface([351, 177])
        self.image.fill(BLACK)
        self.image.set_colorkey((0,0,0))
        self.image.blit(final_box, (0,0))
 
        self.rect = self.image.get_rect()
 
 
class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """
    change_x = 0
    change_y = 0
 
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
 
    player = None
 
    level = None
 
    def update(self):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """
 
        self.rect.x += self.change_x
 
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
 
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right
 
        self.rect.y += self.change_y
 
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
 
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom
 
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift 
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1
 

class Coin(pygame.sprite.Sprite):
    """coins for the user to gain points"""
    def __init__(self, x, y):
        super(Coin,self).__init__()
        self.image = pygame.image.load('graphic/coin.png').convert()
        self.image = pygame.transform.scale(self.image,(45,44))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()

    def update(self):
 
        self.rect.x += self.change_x
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            self.player.increase()
            pygame.mixer.music.pause()
            powerUpNoise = pygame.mixer.music.load('gameSounds/PowerUpSound.mp3')
            pygame.mixer.music.play()
            self.kill()
            
 
            
 
        self.rect.y += self.change_y
 
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
 
            self.kill()
 
 
            self.change_x *= -1
 
class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()
        self.boost_list = pygame.sprite.Group()
        self.final_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.player = player
         
        self.background = background
     
        self.world_shift = 0
        self.level_limit = -3000
 
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
        self.boost_list.update()
        self.bullet_list.update()
        self.final_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(PURPLE)
        screen.blit(self.background, (0,0))
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.coin_list.draw(screen)
        self.boost_list.draw(screen)
        self.final_list.draw(screen)
        self.bullet_list.draw(screen)

 
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything:
        """
 
        self.world_shift += shift_x
 
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for coin in self.coin_list:
            coin.rect.x += shift_x

        for final in self.final_list:
            final.rect.x += shift_x

        for boost in self.boost_list:
            boost.rect.x += shift_x


    def restart(self, player):
        player.lives -= 1
        player.score -= 50
        self.shift_world(-self.world_shift)
        player.rect.x = 300
        player.rect.y = SCREEN_HEIGHT - player.rect.height - 300

 
 
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        Level.__init__(self, player)
 
        self.level_limit = -4000
 
        level = [[210, 40, 300, 300],
                 [210, 40, 500, 500],
                 [210, 40, 800, 400],
                 [210, 40, 1000, 500],
                 [210, 40, 1120, 280],
                 [300, 40, 2000, 300],
                 [300, 40, 2500, 500],
                 [210, 40, 2700, 200],
                 [120, 40, 3000, 400],
                 [200, 40, 3200, 250]
                 ]
 
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
            #add coins to random platforms 
            if (random.randint(1,3)%2 != 0):
                num = platform[0]/70
                for i in range(0,num):
                    c = Coin(platform[2]+ i,platform[3]- 100)
                    c.rect.x = platform[2]+ (i*100)
                    c.rect.y = platform[3]- 100
                    c.change_x = 0
                    c.player = self.player
                    c.level = self
                    self.coin_list.add(c)
            if (random.randint(1,3)%2 == 0):
                enemy = Enemy(50,70)
                enemy.rect.x = platform[2]+ 100
                enemy.rect.y = platform[3]- 100
                enemy.boundary_left = platform[2] 
                enemy.boundary_right = platform[2] + 200
                enemy.change_x = 1
                enemy.player = self.player
                enemy.level = self
                self.enemy_list.add(enemy)
 
        # Add a custom moving platform
        block = MovingPlatform(70, 40)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1700
        block.change_x = 2
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        boost = Boost(50, 50)
        boost.rect.x = 600
        boost.rect.y = 400
        boost.boundary_left = 550
        boost.boundary_right = 650
        boost.change_x = 0
        boost.player = self.player
        boost.level = self
        self.boost_list.add(boost)
        
        boost = Boost(50, 50)
        boost.rect.x = 820
        boost.rect.y = 200
        boost.boundary_left = 770
        boost.boundary_right = 550
        boost.change_x = 0
        boost.player = self.player
        boost.level = self
        self.boost_list.add(boost)

        block = FinalPlatform(150, 30)
        block.rect.x = 3500
        block.rect.y = 200
        block.player = self.player
        block.level = self
        self.final_list.add(block)
 
 
class Level_02(Level):
    """ Definition for level 2. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        Level.__init__(self, player)
 
        self.level_limit = -5000
 
        level = [[210, 40, 300, 300],
                 [210, 40, 500, 550],
                 [210, 40, 800, 400],
                 [210, 40, 1000, 500],
                 [210, 40, 1120, 280],
                 [210, 40, 1200, 280],
                 [300, 40, 2000, 300],
                 [300, 40, 2500, 500],
                 [210, 40, 2700, 200],
                 [120, 40, 3000, 400],
                 [70, 40, 3200, 300]
                 ]
 
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
            # Add coins to random platforms
            if (random.randint(1,3)%2 != 0):
                num = platform[0]/70
                for i in range(0,num):
                    c = Coin(platform[2]+ i,platform[3]- 100)
                    c.rect.x = platform[2]+ (i*100)
                    c.rect.y = platform[3]- 100
                    c.change_x = 0
                    c.player = self.player
                    c.level = self
                    self.coin_list.add(c)
 
        block = MovingPlatform(70, 70)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -2
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(70,70)
        block.rect.x = 1700
        block.rect.y = 300
        block.boundary_top = 150
        block.boundary_bottom = 500
        block.change_y = -2
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(70,70)
        block.rect.x = 3400
        block.rect.y = 300
        block.boundary_top = 300
        block.boundary_bottom = 500
        block.change_y = -2
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        boost = Boost(50, 50)
        boost.rect.x = 1000
        boost.rect.y = 400
        boost.change_x = 1
        boost.boundary_left= 1400
        boost.boundary_right = 1800
        boost.player = self.player
        boost.level = self
        self.boost_list.add(boost)
 
        block = FinalPlatform(150, 30)
        block.rect.x = 3600
        block.rect.y = 250
        block.player = self.player
        block.level = self
        self.final_list.add(block)
 
def main():
    """ Main Program """
    pygame.init()
    pygame.event.get()
 
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Space Bear")
 
    player = Player()
 
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
 
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 300
    player.rect.y = SCREEN_HEIGHT - player.rect.height- 300
    active_sprite_list.add(player)
 
    start = True
    done = False
    gameOver = False

    font = pygame.font.Font(None, 36)
 
    clock = pygame.time.Clock()
 
    # Main Program 
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                    pygame.mixer.music.pause()
                    jumpNoise = pygame.mixer.music.load('gameSounds/jumpSound.mp3')
                    pygame.mixer.music.play()
                # If hit by enemy or fall on ground, restart level
                if player.restart == True:
                    pygame.mixer.music.pause()
                    enemyNoise = pygame.mixer.music.load('gameSounds/ouch.wav')
                    pygame.mixer.music.play()
                    current_level.restart(player)
                    player.restart = False
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
                if event.key == pygame.K_SPACE:
                    player.fireBullet()
                # If hit by enemy or fall on ground, restart level
                if player.restart == True:
                    current_level.restart(player)
                    player.restart = False

               
            if player.lives == 0:
                gameOver = True



        active_sprite_list.update()
 
        current_level.update()

 
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
 
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)
 

        if player.reachedEnd:
            if current_level_no < len(level_list)-1:
                player.rect.x = 300
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
                player.score += 100
                player.reachedEnd = False
            else:
                #done = True
                gameOver = True

             
 
       
        output_string1 = "Score: {0}".format(player.score)
        output_string2 = "Lives: {0}".format(player.lives)
        output_string3 = "Level {0}".format(current_level_no+1)
        score_text = font.render(output_string1, True, WHITE)
        lives_text = font.render(output_string2, True, WHITE)
        level_text = font.render(output_string3, True, WHITE)

        if gameOver:
            text = font.render("Game Over", True, WHITE)
            text_rect = text.get_rect()
            text_x = screen.get_width() / 2 - text_rect.width / 2
            text_y = screen.get_height() / 2 - text_rect.height / 2
            screen.blit(text, [text_x, text_y])
            

        else:
            while start:
                for event in pygame.event.get():
                    print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
                screen.fill(PURPLE)
                screen.blit(cover,(0,0))
                text = font.render("Space Bear", True, WHITE)
                text_rect = text.get_rect()
                text_x = screen.get_width() / 2 - text_rect.width / 2
                text_y = screen.get_height()/3 - text_rect.height/3
                screen.blit(text, [text_x, text_y])
                
                pygame.draw.rect(screen, WHITE,(350,300,100,50))
                s_text = font.render("START", True, BLACK)
                text_rect = text.get_rect()
                text_x = 350 + 10
                text_y = 300 + 10
                screen.blit(s_text, [text_x, text_y])
                
                click = pygame.mouse.get_pressed()
                if click[0]==1:
                    start= False
                      
                pygame.display.update()
                clock.tick(15)

            current_level.draw(screen)
            active_sprite_list.draw(screen)
            screen.blit(score_text, [650, 50])
            screen.blit(lives_text, [650, 80])
            screen.blit(level_text, [50, 50])
        

 
        clock.tick(60)
 
        pygame.display.flip()
 

    pygame.quit()
    
 
if __name__ == "__main__":
    main()


