import pygame, sys, random
from pygame.locals import *

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Road Racing Game")

road = pygame.image.load("road.png")
car = pygame.image.load("car.png")
obstacle = pygame.image.load("obstacle.png")

carWidth, carHeight = car.get_rect().size
obstacleWidth, obstacleHeight = obstacle.get_rect().size

carX = width // 2 - carWidth // 2
carY = height - carHeight - 20
carSpeed = 4
carMovement = 0

obstacleX = random.randint(94, 710 - obstacleWidth)
obstacleY = -obstacleHeight
obstacleSpeed = 5

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (57, 181, 74)
ACTIVATED = (0, 120, 215)
DEACTIVATED = (180, 210, 230)
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

class Button:
    def __init__(self, color, x, y, width, height, text='', combo=False):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.combo = combo
        self.active = False

    def draw(self, screen):
        if self.combo:
            if self.active:
                pygame.draw.rect(screen, ACTIVATED, self.rect)
            else:
                pygame.draw.rect(screen, DEACTIVATED, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

buttons = []
buttons.append(Button(DEACTIVATED, 10, 10, BUTTON_WIDTH, BUTTON_HEIGHT, 'Easy', True))
buttons.append(Button(ACTIVATED, 120, 10, BUTTON_WIDTH, BUTTON_HEIGHT, 'Medium', True))
buttons.append(Button(DEACTIVATED, 230, 10, BUTTON_WIDTH, BUTTON_HEIGHT, 'Hard', True))
buttons.append(Button(GREEN, 630, 10, BUTTON_WIDTH, BUTTON_HEIGHT, 'Start', False))
buttons[1].active = True

playing = False
gameOver = False
points = 0

def paintPanel():
    screen.fill(WHITE)
    for button in buttons:
        button.draw(screen)
    font = pygame.font.Font("freesansbold.ttf", 15)
    screen.blit(font.render('Difficulty', True, BLACK), (135, 70))
    screen.blit(font.render('Points: ' + str(points), True, BLACK), (450, 30))
    screen.blit(road, (94, 100))
    screen.blit(road, (394, 100))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(pos):
                        if button.combo:
                            for b in buttons:
                                b.active = False
                            button.active = True
                            if button.text == 'Easy':
                                obstacleSpeed = 3
                            elif button.text == 'Medium':
                                obstacleSpeed = 5
                            else:
                                obstacleSpeed = 7
                        else:
                            playing = True
                            gameOver = False
                            points = 0
                            carX = width // 2 - carWidth // 2
                            carY = height - carHeight - 20
                            carMovement = 0
                            obstacleX = random.randint(94, 710 - obstacleWidth)
                            obstacleY = -obstacleHeight
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                carMovement = -carSpeed
            elif event.key == pygame.K_RIGHT:
                carMovement = carSpeed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                carMovement = 0
    
    if playing:
        carX += carMovement
        if carX < 94:
            carX = 94
        elif carX > 710 - carWidth:
            carX = 710 - carWidth
        obstacleY += obstacleSpeed
        if obstacleY > 500:
            obstacleX = random.randint(94, 710 - obstacleWidth)
            obstacleY = -obstacleHeight
            points += obstacleSpeed-2
        if carY < obstacleY + obstacleHeight-25 and carY + carHeight > obstacleY+25:
            if carX < obstacleX + obstacleWidth-25 and carX + carWidth > obstacleX+25:
                playing = False
                gameOver = True

    paintPanel()
    screen.blit(car, (carX, carY))
    screen.blit(obstacle, (obstacleX, obstacleY))

    if gameOver:
        font_game_over = pygame.font.Font("freesansbold.ttf", 50)
        game_over_text = font_game_over.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))

    pygame.display.flip()