##################  SOURCES  ###################
# - Mr. Cozort, Kids Can Code 

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random

vec = pg.math.Vector2

# game settings: Screen size and frames per second
WIDTH = 1440
HEIGHT = 880
FPS = 30

# player settings: speed and starting score
PLAYER_GRAV = 0.0
PLAYER_FRIC = 0.1
SCORE = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#places colors in a group for easy access
colorlist = (WHITE, BLACK, RED, GREEN, BLUE)

# draws score in game

def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)


############### sprites: player controlled square and boundries ####################

# creates green player controlled square
class Player(Sprite):
    # characterises the square's color, size, speed, and center and boundries
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.hitx = 0
        self.hity = 0
        self.colliding = False
    # binds keys to movements made by square; holding key accelerates square in specific direction
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.y = 0
            self.acc.x = -0.5
        if keys[pg.K_d]:
            self.acc.y = 0
            self.acc.x = 0.5
        if keys[pg.K_w]:
            self.acc.y = -0.5
        if keys[pg.K_s]:
            self.acc.y = 0.5
        self.acc.x += self.vel.x * -0.1
        self.acc.y += self.vel.y * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
    # theoretically makes player incacaple of phasing through walls on x and y axis
    # only works when player touches center of walls
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, all_platforms, False)
            if hits:
                self.colliding = True
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                if hits[0].rect.centerx > self.rect.centerx and xdiff > ydiff:
                    self.pos.x = hits[0].rect.left - self.rect.width/2
                if hits[0].rect.centerx < self.rect.centerx and xdiff > ydiff:
                    self.pos.x = hits[0].rect.right + self.rect.width/2
                self.vel.x = 0
                self.centerx = self.pos.x
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, all_platforms, False)
            if hits:
                self.colliding = True
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                if hits[0].rect.centery > self.rect.centery and xdiff < ydiff:
                    self.pos.y = hits[0].rect.top - self.rect.height/2
                if hits[0].rect.centery < self.rect.centery and xdiff < ydiff:
                    self.pos.y = hits[0].rect.bottom + self.rect.height/2
                self.vel.y = 0
                self.centery = self.pos.y
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False

 
    #defines changes to the square that will happen upon movement and collisions both directly and intirectly caused by input
    #constantly redraws screen to show the movement of the player
    def update(self):
        self.acc = vec(0,0)
        self.controls()
        # friction
        self.rect.center = self.pos
        self.acc += self.vel * PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rect.center = self.pos
        self.hitx = self.hitx
        self.hity = self.hity
# platforms: simple rectangles that obstruct movement
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y






# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
  
# create groups: used to organize interactions between player and walls
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
all_mobs = pg.sprite.Group()


# ------------------- instantiate classes -------------------------
player = Player()
# side walls: main boundry
leftborder = Platform(0, 0, 20, 880)
rightborder = Platform(1420, 0, 1440, 880)
topborder = Platform(0, 0, 1440, 20)
bottomborder = Platform(0, 860, 1440, 20)

#innerwalls: inner boundries, create 'rooms'
w1 = Platform(460, 500, 20, 220)
w2 = Platform(960, 500, 20, 220)
w3 = Platform(480, 620, 160, 20)
w4 = Platform(800, 620, 160, 20)
w5 = Platform(20, 480, 180, 20)
w6 = Platform(320, 480, 160, 20)
w7 = Platform(960, 480, 160, 20)
w8 = Platform(1240, 480, 180, 20)
w9 = Platform(400, 320, 20, 160)
w10 = Platform(1020, 320, 20, 160)
w11 = Platform(620, 160, 200, 200)
w12 = Platform(400, 20, 20, 180)
w13 = Platform(1020, 20, 20, 180)


# -------------- adding instances to groups ----------------
###### Adding player and platforms to sprite group,
all_sprites.add(player)
all_sprites.add(leftborder)
all_sprites.add(rightborder)
all_sprites.add(topborder)
all_sprites.add(bottomborder)
all_sprites.add(w1)
all_sprites.add(w2)
all_sprites.add(w3)
all_sprites.add(w4)
all_sprites.add(w5)
all_sprites.add(w6)
all_sprites.add(w7)
all_sprites.add(w8)
all_sprites.add(w9)
all_sprites.add(w10)
all_sprites.add(w11)
all_sprites.add(w12)
all_sprites.add(w13)
###### Adding platforms to platforms group

all_platforms.add(leftborder)
all_platforms.add(rightborder)
all_platforms.add(topborder)
all_platforms.add(bottomborder)
all_platforms.add(w1)
all_platforms.add(w2)
all_platforms.add(w3)
all_platforms.add(w4)
all_platforms.add(w5)
all_platforms.add(w6)
all_platforms.add(w7)
all_platforms.add(w8)
all_platforms.add(w9)
all_platforms.add(w10)
all_platforms.add(w11)
all_platforms.add(w12)
all_platforms.add(w13)




# add player to all sprites group
all_sprites.add(player)


# Game loop; constantly updates screen based on inputs from player
running = True
while running:
    # keep the loop running using clock
    clock.tick(FPS)

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.jump()
    
    ############ Update ##############
    # update all sprites
    all_sprites.update()

    ############ Draw ################
    # draw the background screen
    screen.fill(BLACK)
    # draw text
    draw_text("POINTS: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    # draw all sprites
    all_sprites.draw(screen)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()