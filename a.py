import pygame
import os
import time
import random

pygame.init()
screen = pygame.display.set_mode([1400,800])



running = True

color_gummigut = (250, 182, 45)
color_empty = (230, 170, 30)
color_2 = (40, 182, 45)
color_4 = (60, 182, 45)
color_8 = (80, 182, 45)
color_16 = (100, 182, 45)
color_32 = (120, 182, 45)
color_64 = (140, 182, 45)
color_128 = (160, 182, 45)
color_256 = (180, 182, 45)
color_512 = (200, 182, 45)
color_1024 = (220, 182, 45)
color_2048 = (240, 182, 45)

class Block(pygame.sprite.Sprite):
        def __init__(self, x, y, i, j):
            pygame.sprite.Sprite.__init__(self)
            self.rect = pygame.Rect(x, y, 150, 150)
            self.score = 2
            self.image = pygame.image.load('media\\2.png')
            self.image = pygame.transform.scale(self.image, (150, 150))
            self.pos = (i, j)
        def draw(self):
            screen.blit(self.image, self.rect)


       
positions_level_1 = [[(36,36),    (228.5, 36),    (421, 36),    (613.5, 36)],
                     [(36,228.5), (228.5, 228.5), (421, 228.5), (613.5, 228.5)],
                     [(36,421),   (228.5, 421),   (421, 421),   (613.5, 421)],
                     [(36,613.5), (228.5, 613.5), (421, 613.5), (613.5, 613.5)]]



# Creating sprite group
all_blocks =   [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]


cnt = 0


def add_block():  # generates block on random position with value of 2 or 4
    global cnt
    if cnt == 16:
        return

    i, j = random.randint(0, 3), random.randint(0, 3)
    
    while (all_blocks[i][j] != 0):
        i, j = random.randint(0, 3), random.randint(0, 3)
    
    
    all_blocks[i][j] = 2*(random.randint(1, 2))
    cnt = cnt + 1

## creating initial 2 random blocks
add_block()
add_block()


def check_gameover():
    
    for i in range(4):
        for j in range(4):

            x = all_blocks[i][j]

            if x==0:
                return False

            if (j+1 < 4) and (x == all_blocks[i][j+1]):
                return False
            
            if (i+1 < 4) and (x == all_blocks[i+1][j]):
                return False

    print("game over")

    return True


def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText

font = "docktrin.ttf"
yellow=(255, 255, 20)

def display_gameover():
    global score, all_blocks

    screen.fill(color_gummigut)
    title=text_format("Game Over", font, 75, yellow)
    title_rect=title.get_rect()
    xy=800/2 - (title_rect[2]/2) 
    screen.blit(title, (xy, 200))

    score_text = text_format("score: " + str(score), font, 75, yellow)
    title_rect=title.get_rect()
    xy=800/2 - (title_rect[2]/2)
    screen.blit(score_text, (xy, 300))

    timee = game_time()
    score_text = text_format("Time: " + str(timee), font, 75, yellow)
    title_rect=title.get_rect()
    xy=800/2 - (title_rect[2]/2)
    screen.blit(score_text, (xy, 400))

    pygame.display.update()
    time.sleep(3)
    
    reset_game()

def reset_game():
    global cnt, score, all_blocks
    score = 0
    cnt = 0
    all_blocks =   [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
    add_block()
    add_block()


def animation_right(i,j, x,y):

    # i,j = position of initial block
    # x,y = position of final block

    nextFrame = time.clock() + 30    # 30ms period of each frame 
    frame = 0

    while (frame < 5):
        posInit = positions_level_1[i][j]
        posFinal = positions_level_1[x][y]


        step = (posFinal[0]-posInit[0]) / 5     # step = (x1 - x0) / (frame period) 

        if time.clock() > nextFrame:  
            frame = (frame+1)

            image = pygame.image.load("media\\" + str(all_blocks[i][j]) + ".png")
            image = pygame.transform.scale(image, (150, 150))
            screen.blit(image, (positions_level_1[i][j][0], positions_level_1[i][j][1] + step*frame, 150, 150))
        
        print(positions_level_1[i][j][1] + step*frame + " ")
        pygame.quit()
        exit()


def move_right():
    global cnt, score 
    for i in range(0,4,1):
        for j in range(2,-1,-1):

            if all_blocks[i][j] != 0:
        
                k = j
                
                if all_blocks[i][k+1] == 0:  # if the way is empty, move forward 
                    
                    while (k < 3) and (all_blocks[i][k+1] == 0):
                        all_blocks[i][k+1] = all_blocks[i][k]
                        all_blocks[i][k] = 0 
                        k = k+1

                if (k < 3) and (all_blocks[i][k+1] == all_blocks[i][k]):  # if they have equal value, add them
                    # animation_right(i,k,i,k+1)
                    all_blocks[i][k] = 0
                    all_blocks[i][k+1] *= 2
                    score += all_blocks[i][k+1]
                    print(score)
                    cnt -= 1        

def move_left():
    global cnt, score
    for i in range(0,4,1):
        for j in range(1,4,1):

            if all_blocks[i][j] != 0:
        
                k = j
                
                if all_blocks[i][k-1] == 0:  # if the way is empty, move forward 
            
                    while (k > 0) and (all_blocks[i][k-1] == 0):
                        all_blocks[i][k-1] = all_blocks[i][k]
                        all_blocks[i][k] = 0 
                        k = k-1

                if (k > 0) and (all_blocks[i][k-1] == all_blocks[i][k]):  # if they have equal value, add them
                    all_blocks[i][k] = 0
                    all_blocks[i][k-1] *= 2
                    score += all_blocks[i][k-1]
                    print(score)
                    cnt -= 1  

def move_down():
    global cnt,score
    for j in range(0,4,1):
        for i in range(2,-1,-1):

            if all_blocks[i][j] != 0:
        
                k = i
                
                if all_blocks[k+1][j] == 0:  # if the way is empty, move forward 
                    
                    while (k < 3) and (all_blocks[k+1][j] == 0):
                        all_blocks[k+1][j] = all_blocks[k][j]
                        all_blocks[k][j] = 0 
                        k = k+1

                if (k < 3) and (all_blocks[k+1][j] == all_blocks[k][j]):  # if they have equal value, add them
                    all_blocks[k][j] = 0
                    all_blocks[k+1][j] *= 2
                    score += all_blocks[k+1][j]
                    print(score)
                    cnt -= 1        

def move_up():
    global cnt,score
    for j in range(0,4,1):
        for i in range(1,4,1):

            if all_blocks[i][j] != 0:
        
                k = i
                
                if all_blocks[k-1][j] == 0:  # if the way is empty, move forward 
            
                    while (k > 0) and (all_blocks[k-1][j] == 0):
                        all_blocks[k-1][j] = all_blocks[k][j]
                        all_blocks[k][j] = 0 
                        k = k-1

                if (k > 0) and (all_blocks[k-1][j] == all_blocks[k][j]):  # if they have equal value, add them
                    all_blocks[k][j] = 0
                    all_blocks[k-1][j] *= 2
                    score += all_blocks[k-1][j]
                    print(score)
                    cnt -= 1      


def draw_objects():
    screen.fill(color_gummigut)
    
    # background
    x, y = 30, 30
    for i in range (4):
        for j in range (4):
            pygame.draw.rect(screen, (color_empty), (x*(i+1)+162.5*i, y*(j+1)+162.5*j, 162.5, 162.5))

    # objects
    for i in range (4):
        for j in range(4):
            if all_blocks[i][j] != 0:
                image = pygame.image.load("media\\" + str(all_blocks[i][j]) + ".png")
                image = pygame.transform.scale(image, (150, 150))
                screen.blit(image, (positions_level_1[i][j][0], positions_level_1[i][j][1], 150, 150))
    

    # score
    global score, best_score, best_score_time

    fonts = "FrozencaScriptTypeface.ttf"
    title=text_format("SCORE: " + str(score), fonts, 40, yellow)
    title_rect=title.get_rect()
    screen.blit(title, (850, 50))

    title=text_format("BEST SCORE: " + str(best_score), fonts, 40, yellow)
    title_rect=title.get_rect()
    screen.blit(title, (850, 110))

    title=text_format("BEST SCORE TIME: " + str(best_score_time), fonts, 40, yellow)
    title_rect=title.get_rect()
    screen.blit(title, (850, 170))





    pygame.display.update()


    pygame.display.flip()

def check_keyboard():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                move_left()
            if event.key == pygame.K_RIGHT:
                move_right()
            if event.key == pygame.K_UP:
                move_up()
            if event.key == pygame.K_DOWN:
                move_down()
            
            add_block()

import datetime
def game_time():
    global start_time, score, best_score, best_score_time

    # рассчет времени игры
    end_time = datetime.datetime.now()
    time_difference = end_time - start_time
    print(time_difference)

    # best score ~ vest_score_time
    if score > best_score:
        best_score = score
        best_score_time = time_difference


    return time_difference

score = 0
best_score = 0
best_score_time = "00:00:00"
start_time = datetime.datetime.now()

# def menu():

#     screen.fill(color_gummigut)

#     button1_text = "Level 1: 2048"

#     button2_text = "Level 2: 16384"

#     button3_text = "Level 3: 131072"
   

#     global score

#     screen.fill(color_gummigut)
#     buttun1=text_format(button1_text, font, 75, yellow)
#     buttun1_rect=buttun1.get_rect()
#     xy=800/2 - (buttun1_rect[2]/2) 
#     screen.blit(buttun1, (xy, 200))

#     buttun2 = text_format(button2_text, font, 75, yellow)
#     buttun2_rect=buttun2.get_rect()
#     xy=800/2 - (buttun2_rect[2]/2)
#     screen.blit(buttun2, (xy, 300))

#     buttun3 = text_format(button3_text, font, 75, yellow)
#     buttun3_rect=buttun3.get_rect()
#     xy=800/2 - (buttun3_rect[2]/2)
#     screen.blit(buttun3, (xy, 400))

#     pygame.display.update()
#     pygame.display.flip()

# def menu_keyboard():
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             mouse_pos = event.pos
#             if button1_rect.collidepoint(mouse_pos):
#                 choice_1()
#             elif button2_rect.collidepoint(mouse_pos):
#                 choice_2()
#             elif button3_rect.collidepoint(mouse_pos):
#                 choice_3()

while running:

    run_game = True

    # display_menu = True

    # if display_menu:
    #     menu()

    if run_game:

        if check_gameover():
            display_gameover()

        check_keyboard()

        draw_objects()
    
    


   

pygame.quit()