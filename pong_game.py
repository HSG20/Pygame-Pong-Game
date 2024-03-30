import pygame, os, sys, random
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

player_score = 0
machine_score = 0
player_sets = 0
machine_sets = 0
dificultad = 6.5

width,height = 1000,700
mainSurface = pygame.display.set_mode((width,height))
pygame.display.set_caption('pong');
black = pygame.Color(0, 0, 0)
letra50 = pygame.font.SysFont("Arial", 50)
letra30 = pygame.font.SysFont("Arial", 30)

facil_text_pos = (width/2-272,height/2-100,200,100)
dificil_text_pos = (width/2+114,height/2-100,200,100)
twoplayer_text_pos = (width/2-215,height/2+100,200,100)

facil_button_pos = (width/2-300,height/2-120,200,100)
dificil_button_pos = (width/2+100,height/2-120,200,100)
twoplayer_button_pos = (width/2-300,height/2+80,600,100)

texto_victoria1 = letra30.render(f"FELICIDADES JUGADOR 1, HAS GANADO", True, (255,255,255))
texto_victoria2 = letra30.render(f"FELICIDADES JUGADOR 2, HAS GANADO", True, (255,255,255))
texto_derrota = letra30.render(f"HAS PERDIDO", True, (255,255,255))
# bat init
bat1 = pygame.image.load('pong_bat.png')
bat2 = pygame.image.load('pong_bat.png')
player1Y = height/2
player2Y = height/2
player1X = 50
player2X = width-50
batRect1 = bat1.get_rect()
batRect2 = bat2.get_rect()

# ball init
velocidad = 8
ball = pygame.image.load('ball.png')
ballRect = ball.get_rect()
bx, by = (width/2, 3*height/4)
sx, sy = (velocidad, velocidad)
ballRect.center = (bx, by)
ballserved = False
menu = True
twoplayer = False

obstacle = pygame.image.load('obstacle.png')
obstacles = []

def random_obstacle(player):
    obstacleY = random.randint(30,height-30)
    obstacleX = (random.randint(0, 190) + 180) + (player*430)
    obs_width = obstacle.get_width()
    obs_height = obstacle.get_height()
    obstacle_rect = Rect(obstacleX, obstacleY, obs_width, obs_height)
    obstacles.append(obstacle_rect)
    return obstacles

batRect1.midtop = (player1X, player1Y)
batRect2.midtop = (player2X, player2Y)

while True:
    
    mainSurface.fill(black)
    # events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            if mouse[0] > facil_button_pos[0] and mouse[0] < facil_button_pos[0]+facil_button_pos[2] and mouse[1] > facil_button_pos[1] and mouse[1] < facil_button_pos[1]+facil_button_pos[3]:
                dificultad = 6.5
                menu = False
            if mouse[0] > dificil_button_pos[0] and mouse[0] < dificil_button_pos[0]+dificil_button_pos[2] and mouse[1] > dificil_button_pos[1] and mouse[1] < dificil_button_pos[1]+dificil_button_pos[3]:
                dificultad = 8.5
                menu = False
            if mouse[0] > twoplayer_button_pos[0] and mouse[0] < twoplayer_button_pos[0]+twoplayer_button_pos[2] and mouse[1] > twoplayer_button_pos[1] and mouse[1] < twoplayer_button_pos[1]+twoplayer_button_pos[3]:
                dificultad = 0
                twoplayer = True
                menu = False
        
    keys = pygame.key.get_pressed()
    if keys[K_UP] and not menu:
        player2Y -= 10
        batRect2.midtop = (player2X, player2Y)
        ballserved = True
    if keys[K_DOWN] and not menu:
        player2Y += 10
        batRect2.midtop = (player2X, player2Y)
        ballserved = True
    if keys[K_w] and twoplayer:
        player1Y -= 10
        batRect1.midtop = (player1X, player1Y)
        ballserved = True
    if keys[K_s] and twoplayer:
        player1Y += 10
        batRect1.midtop = (player1X, player1Y)
        ballserved = True
    
    if player1Y <= 10:
        player1Y = 10
    if player1Y >= height-65:
        player1Y = height-65
    
    if player2Y <= 10:
        player2Y = 10
    if player2Y >= height-65:
        player2Y = height-65
    
    if ballserved:
        bx += sx
        by += sy
        ballRect.center = (bx, by)
    
    if not twoplayer: #maquina
        diferencia = 1 if (batRect1.center[1]-by) == 0 else (batRect1.center[1]-by)
        if sx < 0 and abs(diferencia) > dificultad: #solo se mueve si la pelota va hacia ella, ademas se evita el traqueteo al condicionar su movimiento a solo cuanto la diferencia supera cierto umbral 
            batRect1.center = (player1X, batRect1.center[1]-dificultad*(diferencia/abs(diferencia)))
        
    if (bx <= 0):
        player_score = 6 if player_score == 4 else player_score + 1
        bx, by = (width/2, (3*height/4) if (-1)**player_score > 0 else (height/4))
        sx, sy = (velocidad, velocidad)
        ballRect.center = (bx, by)
        ballserved = False
        player1Y = height/2
        player2Y = height/2
        batRect1.center = (player1X, player1Y)
        batRect2.center = (player2X, player2Y)
        sy *= (-1)**player_score
        
    if (bx >= width - 8):
        machine_score = 6 if machine_score == 4 else machine_score + 1
        bx, by = (width/2, (3*height/4) if (-1)**machine_score > 0 else (height/4))
        sx, sy = (-velocidad, velocidad)
        ballRect.center = (bx, by)
        ballserved = False
        player1Y = height/2
        player2Y = height/2
        batRect1.center = (player1X, player1Y)
        batRect2.center = (player2X, player2Y)
        sy *= (-1)**machine_score
        
    if (by <= 0):
        by = 0
        sy *= -1
    if (by >= height - 8):
        by = 700 - 8
        sy *= -1
    
    if ballRect.colliderect(batRect1):
        bx = player1X + 12
        sx *= -1
        sy = (by-batRect1.center[1])/3
        obstacles = random_obstacle(1)
        
    if ballRect.colliderect(batRect2):
        bx = player2X - 12
        sx *= -1
        sy = (by-batRect2.center[1])/3
        obstacles = random_obstacle(0)
        
    if len(obstacles) > int(6 if dificultad == 6.5 else 15):
        del obstacles[0]
        
    obstacleHitIndex = ballRect.collidelist(obstacles)
    if obstacleHitIndex >= 0:
        hit_obs = obstacles[obstacleHitIndex]

        # Verificar colisión y cambiar dirección según el lado del obstáculo
        if (sx > 0 and bx - 8 < hit_obs.x) or (sx < 0 and bx + 8 > hit_obs.x + hit_obs.width):
            sx *= -1
        else:
            sy *= -1
        # Eliminar el obstáculo
        del obstacles[obstacleHitIndex]


    if player_score >= 5:
        machine_score = 0
        player_score = 0
        player_sets += 1
        obstacles = []
        
    if machine_score >= 5:
        machine_score = 0
        player_score = 0
        machine_sets += 1
        obstacles = []
        
    score_text = letra50.render(f"{machine_score}       {player_score}", True, (200,200,200))
    sets_text = letra30.render(f"{machine_sets}              {player_sets}", True, (200,200,200))
    menu_text = letra50.render("ESCOGE LA DIFICULTAD", True, (200,200,200))
    facil_text = letra50.render("FÁCIL", True, (0,0,0))
    dificil_text = letra50.render("DIFÍCIL", True, (0,0,0))
    twoplayer_text = letra50.render("DOS JUGADORES", True, (0,0,0))
        
    if not menu:
        for obs in obstacles:
            mainSurface.blit(obstacle, obs)
        mainSurface.blit(score_text, (425,50))
        mainSurface.blit(sets_text, (429,100))
        mainSurface.blit(ball, ballRect)
        mainSurface.blit(bat1, batRect1)
        mainSurface.blit(bat2, batRect2)
        pygame.draw.line(mainSurface,(255,255,255), (width/2, 0), (width/2, height))
    
    else:
        mainSurface.blit(menu_text, (208,height/2-250))
        pygame.draw.rect(mainSurface, (0,255,0), facil_button_pos, 0)
        pygame.draw.rect(mainSurface, (255,0,0), dificil_button_pos, 0)
        pygame.draw.rect(mainSurface, (255,255,0),twoplayer_button_pos,0)
        mainSurface.blit(facil_text, facil_text_pos)
        mainSurface.blit(dificil_text, dificil_text_pos)
        mainSurface.blit(twoplayer_text, twoplayer_text_pos)
    
    if player_sets == 3 or machine_sets == 3:
        bx, by = (width/2, 3*height/4)
        sx, sy = (velocidad,velocidad)
        mainSurface.fill((0,0,0))
        if player_sets == 3:
            mainSurface.blit(texto_victoria1,(width/2-290,height/2-50))
        elif twoplayer:
            mainSurface.blit(texto_victoria2,(width/2-290,height/2-50))
        else:
            mainSurface.blit(texto_derrota,(width/2-100,height/2-50))
        pygame.display.update()
        player_sets = 0
        machine_sets = 0
        twoplayer = False
        menu = True
        pygame.time.wait(3000)
    
    fpsClock.tick(60)
    pygame.display.update()