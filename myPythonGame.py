import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 1000, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Game!")

LIVES_FONT = pygame.font.SysFont('arialblack', 30)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

YELLOW_HIT = pygame.USEREVENT + 2
RED_HIT = pygame.USEREVENT + 1

FPS = 60
BOARDER = pygame.Rect(WIDTH//2 - 10, 0, 10, HEIGHT)

IMAGE_WIDTH, IMAGE_HEIGHT = (50, 45)

IMAGE_Y = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
IMAGE_YT = pygame.transform.rotate(pygame.transform.scale(IMAGE_Y, (IMAGE_WIDTH, IMAGE_HEIGHT)), 270)
IMAGE_R = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'spaceship_red.png')), 90)
IMAGE_RT = pygame.transform.scale((IMAGE_R), (IMAGE_WIDTH, IMAGE_HEIGHT))

VALUE = 1
BULLETS_SPEED = 6
MAX_BULLETS = 5

SPACE_THEME = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'starwars2.png')), (WIDTH, HEIGHT))

LIVES_FONT = pygame.font.SysFont('arialblack', 50)
WINNER_FONT = pygame.font.SysFont('arialblack', 110)


def draw_diaplay(yellow, red, yellow_bullets, red_bullets, yellow_lives, red_lives):
    WINDOW.blit(SPACE_THEME, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BOARDER)
    red_lives_text = LIVES_FONT.render("Lives: " + str(red_lives), 1, WHITE)
    yellow_lives_text = LIVES_FONT.render("Lives: " + str(yellow_lives), 1, WHITE)
    WINDOW.blit(red_lives_text, (10, 10))
    WINDOW.blit(yellow_lives_text, (WIDTH - yellow_lives_text.get_width() - 10, 10))

    WINDOW.blit(IMAGE_YT, (yellow.x, yellow.y))
    WINDOW.blit(IMAGE_RT, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    pygame.display.update()


def red_moves(key_selected, red):
    if key_selected[pygame.K_s] and red.x - VALUE > 0: #Left Movement
        red.x -= VALUE
    if key_selected[pygame.K_f] and red.x + VALUE + red.width < BOARDER.x: #Right Movement
        red.x += VALUE
    if key_selected[pygame.K_e] and red.y - VALUE > 0: #Up Movement
        red.y -= VALUE
    if key_selected[pygame.K_d] and red.y + VALUE + red.height < HEIGHT: #Down Movement
        red.y += VALUE

def yellow_moves(key_selected, yellow):
    if key_selected[pygame.K_j] and yellow.x - VALUE > BOARDER.x + BOARDER.width: #Left Movement
        yellow.x -= VALUE
    if key_selected[pygame.K_l] and yellow.x + VALUE + yellow.width < WIDTH: #Right Movement
        yellow.x += VALUE
    if key_selected[pygame.K_i] and yellow.y - VALUE > 0: #Up Movement
        yellow.y -= VALUE
    if key_selected[pygame.K_k] and yellow.y + VALUE + yellow.height < HEIGHT - 5: #Down Movement
        yellow.y += VALUE

def control_bullets(red_bullets, yellow_bullets, red, yellow):
    for bullet in red_bullets:
        bullet.x += BULLETS_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)
    
    for bullet in yellow_bullets:
        bullet.x -= BULLETS_SPEED
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

def draw_red_winner(text):
    draw_red_text = WINNER_FONT.render(text, 1, RED)
    WINDOW.blit(draw_red_text, (WIDTH/2 - draw_red_text.get_width() / 2, HEIGHT/2 - draw_red_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def draw_yellow_winner(text):
    draw_yellow_text = WINNER_FONT.render(text, 1, YELLOW)
    WINDOW.blit(draw_yellow_text, (WIDTH/2 - draw_yellow_text.get_width() / 2, HEIGHT/2 - draw_yellow_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    

def main():
    red = pygame.Rect(100, 250, IMAGE_WIDTH, IMAGE_HEIGHT)
    yellow = pygame.Rect(850, 250, IMAGE_WIDTH, IMAGE_HEIGHT)

    yellow_lives = 15
    red_lives = 15

    red_bullets = []
    yellow_bullets = []

    clck = pygame.time.Clock()
    run = True
    while run:
        clck.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LALT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 5, 2)
                    red_bullets.append(bullet)

                if event.key == pygame.K_RALT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 5, 2)
                    yellow_bullets.append(bullet)

            if event.type == YELLOW_HIT:
                yellow_lives -= 1

            if event.type == RED_HIT:
                red_lives -= 1

        if red_lives <= 0:
            win_yellow_text = "Yellow Wins!"
            draw_yellow_winner(win_yellow_text)
            break

        if yellow_lives <= 0:
            win_red_text = "Red Wins!"
            draw_red_winner(win_red_text)
            break
    
        key_selected = pygame.key.get_pressed()

        red_moves(key_selected, red)
        yellow_moves(key_selected, yellow)        
        control_bullets(red_bullets, yellow_bullets, red, yellow)
        draw_diaplay(yellow, red, yellow_bullets, red_bullets, yellow_lives, red_lives)
    
    pygame.quit()


if __name__ == "__main__":
    main()
