import pygame
import os
pygame.init()

def path_file(file_name):
    folder_path = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder_path, file_name)
    return path


WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 40
YELLOW = (255, 210, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_RED = (150, 0, 0)
DARK_GREEN = (0, 150, 0)

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

fon = pygame.image.load(path_file("Village.jpg"))
fon = pygame.transform.scale(fon, (WIN_WIDTH, WIN_HEIGHT))

fon2 = pygame.image.load(path_file("fon2.jpg"))
fon2 = pygame.transform.scale(fon2, (WIN_WIDTH, WIN_HEIGHT))

win_img = pygame.image.load(path_file("Win.jpg"))
win_img = pygame.transform.scale(win_img, (WIN_WIDTH, WIN_HEIGHT))

lose_img = pygame.image.load(path_file("Lose.jpg"))
lose_img = pygame.transform.scale(lose_img, (WIN_WIDTH, WIN_HEIGHT))

music_win = pygame.mixer.Sound(path_file("win.wav"))
music_lose = pygame.mixer.Sound(path_file("lose.wav"))
music_shoot = pygame.mixer.Sound(path_file("slingshot_shoot.wav"))
music_transform = pygame.mixer.Sound(path_file("transformation.wav"))

music_lose.set_volume(0.15)
music_shoot.set_volume(0.4)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (width, height))


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def __init__(self, x, y, width, height, img, speed):
        super().__init__(x, y, width, height, img)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        
        if self.rect.left > WIN_WIDTH or self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, width, height, color, text, px_x, px_y):
        self.color = color
        self.px_x = px_x
        self.px_y = px_y
        self.rect = pygame.Rect(x, y, width, height)
        self.font30 = pygame.font.SysFont("sans serif", 30)
        self.text = self.font30.render(text, True, BLACK)
    def btn_show(self):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.text, (self.rect.x + self.px_x, self.rect.y + self.px_y))

btn_start = Button(50, 250, 100, 50, GREEN, "START", 17, 17)
btn_exit = Button(650, 250, 100, 50, RED, "EXIT", 17, 17)


class Player(GameSprite):
    def __init__(self, x, y, width, height, img):
        super().__init__(x, y, width, height, img)
        self.speed_x = 0
        self.speed_y = 0
        self.width = width
        self.height = height
        self.direction = "right"
        self.image_r = self.image
        self.image_l = pygame.transform.flip(self.image, True, False)

    def update(self):
        if self.rect.left > 0 and self.speed_x < 0 or self.speed_x > 0 and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speed_x
        if lvl == 1:
            walls_collide = pygame.sprite.spritecollide(self, walls, False)
            if self.speed_x > 0:
                for wall in walls_collide:
                    self.rect.right = min(self.rect.right, wall.rect.left)
            elif self.speed_x < 0:
                for wall in walls_collide:
                    self.rect.left = max(self.rect.left, wall.rect.right)

            if self.rect.top > 0 and self.speed_y < 0 or self.speed_y > 0 and self.rect.bottom < WIN_HEIGHT:
                self.rect.y += self.speed_y
            walls_collide = pygame.sprite.spritecollide(self, walls, False)
            if self.speed_y < 0:
                for wall in walls_collide:
                    self.rect.top = max(self.rect.top, wall.rect.bottom)
            elif self.speed_y > 0:
                for wall in walls_collide:
                    self.rect.bottom = min(self.rect.bottom, wall.rect.top)
        elif lvl == 2:
            walls_collide = pygame.sprite.spritecollide(self, walls2, False)
            if self.speed_x > 0:
                for wall in walls_collide:
                    self.rect.right = min(self.rect.right, wall.rect.left)
            elif self.speed_x < 0:
                for wall in walls_collide:
                    self.rect.left = max(self.rect.left, wall.rect.right)

            if self.rect.top > 0 and self.speed_y < 0 or self.speed_y > 0 and self.rect.bottom < WIN_HEIGHT:
                self.rect.y += self.speed_y
            walls_collide = pygame.sprite.spritecollide(self, walls2, False)
            if self.speed_y < 0:
                for wall in walls_collide:
                    self.rect.top = max(self.rect.top, wall.rect.bottom)
            elif self.speed_y > 0:
                for wall in walls_collide:
                    self.rect.bottom = min(self.rect.bottom, wall.rect.top)

    def shoot(self):
        if self.direction == "right":
            bullet = Bullet(self.rect.right, self.rect.centery, 10, 10, path_file("stone.png"), 5)
            bullets.add(bullet)
        if self.direction == "left":
            bullet = Bullet(self.rect.left - 10, self.rect.centery, 10, 10, path_file("stone.png"), -5)
            bullets.add(bullet)
        
        
    def change_img(self, image_ch):
        self.image = pygame.image.load(image_ch)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image_r = self.image
        self.image_l = pygame.transform.flip(self.image, True, False)

        

class Enemy(GameSprite):
    def __init__(self, x, y, width, height, file_name, speed, direction, min_coord, max_coord):
        super().__init__(x, y, width, height, file_name)
        self.speed = speed
        self.direction = direction
        self.min_coord = min_coord
        self.max_coord = max_coord

    def update(self):
        if self.direction == "right" or self.direction == "left":
            if self.direction == "left":
                self.rect.x -= self.speed
            if self.direction == "right":
                self.rect.x += self.speed

            if self.rect.right >= self.max_coord:
                self.direction = "left"
            if self.rect.left <= self.min_coord:
                self.direction = "right"
        
        if self.direction == "up" or self.direction == "down":
            if self.direction == "up":
                self.rect.y -= self.speed
            if self.direction == "down":
                self.rect.y += self.speed
                
            if self.rect.bottom >= self.max_coord:
                self.direction = "up"
            if self.rect.top <= self.min_coord:
                self.direction = "down"
            




player = Player(50, 50, 100, 100, path_file("Hero.jpg"))

bullets = pygame.sprite.Group()

enemies = pygame.sprite.Group()
enemy = Enemy(400, 325, 100, 100, path_file("Enemy.png"), 4, "left", 175, 500)
enemy2 = Enemy(12.5, 400, 100, 100, path_file("Enemy.png"), 4, "down", 200, 600)
enemy3 = Enemy(500, 50, 100, 100, path_file("Enemy.png"), 4, "left", 50, 625)
enemy4 = Enemy(400, 500, 100, 100, path_file("Enemy.png"), 4, "left", 200, 500)
enemies.add(enemy, enemy2, enemy3, enemy4)

enemies2 = pygame.sprite.Group()
enemy1 = Enemy(175, 200, 100, 100, path_file("enemy1.png"), 5, "left", 125, 450)
enemy2 = Enemy(350, 200, 100, 100, path_file("enemy2.png"), 4, "down", 200, 500)
enemy3 = Enemy(500, 325, 100, 100, path_file("enemy3.png"), 4, "down", 185, 500)
enemies2.add(enemy1, enemy2, enemy3)

door = GameSprite(700, 0, 100, 100, path_file("Door.png"))
key = GameSprite(175, 525, 50, 50, path_file("key.png"))
win = GameSprite(650, 400, 150, 100, path_file("win_dish.jpg"))

walls = pygame.sprite.Group()
wall_1 = GameSprite(0, 150, 125, 50, path_file("wood.jpg"))
wall_2 = GameSprite(125, 150, 50, 150, path_file("wood.jpg"))
wall_3 = GameSprite(125, 450, 50, 150, path_file("wood.jpg"))
wall_4 = GameSprite(175, 450, 200, 50, path_file("wood.jpg"))
wall_5 = GameSprite(300, 200, 75, 100, path_file("wood.jpg"))
wall_6 = GameSprite(500, 300, 50, 300, path_file("wood.jpg"))
wall_7 = GameSprite(300, 150, 400, 50, path_file("wood.jpg"))
wall_8 = GameSprite(650, 0, 50, 475, path_file("wood.jpg"))
walls.add(wall_1, wall_2, wall_3, wall_4, wall_5, wall_6, wall_7, wall_8)

walls2 = pygame.sprite.Group()
wall_1 = GameSprite(0, 150, 125, 50, path_file("stone.jpg"))
wall_2 = GameSprite(75, 150, 50, 350, path_file("stone.jpg"))
wall_3 = GameSprite(75, 500, 750, 50, path_file("stone.jpg"))
wall_4 = GameSprite(250, 150, 375, 50, path_file("stone.jpg"))
wall_5 = GameSprite(250, 310, 70, 70, path_file("stone.jpg"))
wall_6 = GameSprite(450, 150, 50, 125, path_file("stone.jpg"))
wall_7 = GameSprite(450, 425, 50, 125, path_file("stone.jpg"))
wall_8 = GameSprite(600, 150, 50, 125, path_file("stone.jpg"))
wall_9 = GameSprite(600, 425, 50, 125, path_file("stone.jpg"))
wall_10 = GameSprite(650, 225, 150, 50, path_file("stone.jpg"))

walls2.add(wall_1,wall_2, wall_3, wall_4, wall_5, wall_6, wall_7, wall_8, wall_9, wall_10)

game = True
play = True
openable = False
one_time = True
power = 1
lvl = 0
if lvl == 0 and game == True:
    pygame.mixer.music.load(path_file("menumusic.wav"))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if lvl == 0:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if btn_start.rect.collidepoint(x, y):
                    btn_start.color = DARK_GREEN
                    btn_start.rect.width = 125
                    btn_start.rect.height = 75
                    btn_start.px_x = 30
                    btn_start.px_y = 30
                    btn_start.rect.y = 290
                    btn_start.rect.x = 40
                    
                elif btn_exit.rect.collidepoint(x, y):
                    btn_exit.color = DARK_RED
                    btn_exit.rect.width = 125
                    btn_exit.rect.height = 75
                    btn_exit.px_x = 35
                    btn_exit.px_y = 30
                    btn_exit.rect.y = 290
                    btn_exit.rect.x = 640
                else:
                    btn_start.color = GREEN
                    btn_start.rect.width = 100
                    btn_start.rect.height = 50
                    btn_start.px_x = 17
                    btn_start.px_y = 17
                    btn_start.rect.y = 300
                    btn_start.rect.x = 50

                    btn_exit.color = RED
                    btn_exit.rect.width = 100
                    btn_exit.rect.height = 50
                    btn_exit.px_x = 25
                    btn_exit.px_y = 17
                    btn_exit.rect.y = 300
                    btn_exit.rect.x = 650
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if btn_start.rect.collidepoint(x, y):
                    lvl = 1
                    pygame.mixer.music.load(path_file("backgroundmusic.wav"))
                    pygame.mixer.music.set_volume(0.15)
                    pygame.mixer.music.play(-1)
                elif btn_exit.rect.collidepoint(x, y):
                    game = False
                

        elif lvl == 1 or lvl == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speed_x = 5
                    player.direction = "right"
                    player.image = player.image_r
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speed_x = -5
                    player.direction = "left"
                    player.image = player.image_l
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speed_y = 5
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speed_y = -5
                if event.key == pygame.K_SPACE:
                    player.shoot()
                    music_shoot.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.speed_x = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.speed_x = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speed_y = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speed_y = 0
                  
    if lvl == 0:
        window.fill(YELLOW)
        btn_start.btn_show()
        btn_exit.btn_show()
    elif lvl == 1:
        if play == True:
            window.blit(fon, (0, 0))

            player.reset()
            player.update()
            if openable == False:
                key.reset()

            enemies.draw(window)
            enemies.update()

            bullets.draw(window)
            bullets.update()

            door.reset()
            walls.draw(window)

            if pygame.sprite.collide_rect(player, door):
                if openable == True:
                    lvl = 2
                    music_win.play()
                else:
                    player.rect.y += 10
            
            if pygame.sprite.spritecollide(player, enemies, False):
                play = False
                window.blit(lose_img, (0, 0))
                pygame.mixer.music.stop()
                music_lose.play()
            
            if pygame.sprite.collide_rect(player, key):
                openable = True
            
            pygame.sprite.groupcollide(bullets, walls, True, False)

            if pygame.sprite.groupcollide(bullets, enemies, True, True):
                if len(enemies.sprites()) == 0:
                    player.change_img(path_file("Sogeking.png"))
                    music_transform.set_volume(0.2)
                    music_transform.play()
                    power = 2
    elif lvl == 2:
        if play == True:
            window.blit(fon2, (0, 0))
            enemies2.draw(window)
            enemies2.update()
            player.reset()
            player.update()
            win.reset()
            bullets.draw(window)
            bullets.update()
            walls2.draw(window)
            pygame.sprite.groupcollide(bullets, walls2, True, False)
            if one_time == True:
                walls.empty()
                player.rect.x = 25
                player.rect.y = 50
                one_time = False
            if pygame.sprite.spritecollide(player, enemies2, False):
                play = False
                window.blit(lose_img, (0, 0))
                pygame.mixer.music.stop()
                music_lose.play()
            if pygame.sprite.collide_rect(win, player) and openable == True:
                play = False
                window.blit(win_img, (0,0))
                pygame.mixer_music.stop()
                music_win.play()

            if power >= 2:
                pygame.sprite.groupcollide(bullets, enemies2, True, True)



#! red
#? blue
#TODO orange
# green
#* light green
#// gray crossed

    clock.tick(FPS)
    pygame.display.update()
