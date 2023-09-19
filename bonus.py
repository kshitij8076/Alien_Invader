import pygame
import random
import math
pygame.init()
pygame.mixer.init()
scree_width = 600
scree_height = 600

# adding music
pygame.mixer.music.load("background-music.mp3")
pygame.mixer.music.play()

# creating window for game
window = pygame.display.set_mode((scree_width,scree_height))
pygame.display.set_caption("Space-Invader")
fps = 60
# icon
player = pygame.image.load("spaceship.png")
pygame.display.set_icon(player)

def create_score(score):
    fonts = pygame.font.SysFont(None, 55)
    text_score = fonts.render("Score:"+str(score),True,(255,255,255))
    window.blit(text_score,(50,10))
def ufo(x,y):
    window.blit(player,(x,y))

def alien(x,y,enemies):
    window.blit(pygame.image.load(enemies),(x,y))

def fire(x,y,bullet):
    global trigger
    window.blit(bullet,(x,y))


# game loop
def gameloop():
    # background
    background = pygame.image.load("beautiful-shining-stars-night-sky.jpg")
    # variables
    exit_game = False
    game_over = False
    clock = pygame.time.Clock()

    # UFO
    ufo_x = 260
    ufo_y = 450
    velocity = 40

    # alien
    enemy = ['alien.png','alien-2.png','alien-3.png']
    enemy_x = []
    enemy_y = 0
    enemy_vel_x = 2
    enemy_vel_y = 3
    for i in range(100):
        enemy_x.append(random.randint(0, 536))
    numb = random.randint(0, 80)
    rand_alien = random.randint(0,2)

    # bullet
    bullet = pygame.image.load("bullet.png")
    bullet_x = 0
    bullet_y = 420
    trigger = False

    # scores
    scores = 0

    # PLAYER NAME
    player_name = input("Enter your name")
    while not exit_game:
        if game_over:
            window.fill((0,0,0))
            window.blit(background,(0,0))
            over = pygame.font.SysFont(None,55)
            rend_over = over.render(f"Game is over {player_name} score is "+str(scores),True,(255,255,255))
            window.blit(rend_over,(20,300))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open("player.txt", "a") as file:
                        file.write(f"{player_name},{scores}\n")
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        with open("player.txt", "a") as file:
                            file.write(f"{player_name},{scores}\n")

                        gameloop()
            pygame.display.update()
            clock.tick(fps)
        else:
            window.fill((0,0,0))
            window.blit(background,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        ufo_x-= velocity
                    if event.key == pygame.K_RIGHT:
                        ufo_x+=velocity
                    if event.key == pygame.K_SPACE:
                        trigger = True
                        bullet_x = ufo_x + 16
                        # fire(bullet_x , bullet_y,bullet)

            ufo(ufo_x,ufo_y)

            # bullet
            if bullet_y <0:
                trigger = False
                bullet_y = 420
            if trigger:
                fire(bullet_x,bullet_y,bullet)
                bullet_y-=20

            # enemy movement
            if scores>100:
                enemy_vel_x=2.5
                # enemy_vel_y+=0.1
            if scores>200:
                enemy_vel_x+=2.8

            if enemy_x[numb]<0:
                enemy_x[numb]+=enemy_vel_x
            if enemy_x[numb]>436:

                enemy_x[numb]-=enemy_vel_x
            enemy_y+=enemy_vel_y
            enemy_x[numb]+=enemy_vel_x
            if enemy_y>600:
                game_over = True
            alien(enemy_x[numb], enemy_y,enemy[rand_alien])

            # collision
            distance = math.pow(math.pow(bullet_x-enemy_x[numb],2)+math.pow(bullet_y-enemy_y,2),1/2)
            if distance<20 :
                scores += 10
                numb = random.randint(0, 80)
                rand_alien = random.randint(0,2)
                enemy_y = 0
                alien(enemy_x[numb],enemy_y,enemy[rand_alien])

            # giving boundaries
            if ufo_x>536 :
                ufo_x = 536
            elif ufo_x<0:
                ufo_x=0

            create_score(scores)
            pygame.display.update()
            clock.tick(fps)
            

    pygame.quit()
    quit()
gameloop()