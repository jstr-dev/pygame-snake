import pygame 
import random
import time 
import copy
import math

game_title = "Snake"
game_resolution = (600, 600)
game_snake = game_resolution[0] // 20

colour_black = (0, 0, 0)
colour_white = (255, 255, 255)
colour_blue = (0, 0, 255)

STATE_LEFT = 1 
STATE_RIGHT = 2 
STATE_UP = 3 
STATE_DOWN = 4

GAME_ENDED = False

def drawText(surface, text, font, xPos, yPos, colour=(0,0,0), align = False):
    textSurface = font.render(text, True, colour)
    adjustedX, adjustedY = 0, 0

    if align:
        surfaceRect = textSurface.get_rect()
        if align == 'right':
            adjustedX -= surfaceRect.width
        elif align == 'centre':
            adjustedX -= math.floor(surfaceRect.width / 2)
            adjustedY -= math.floor(surfaceRect.height / 2)

    surface.blit(textSurface, (xPos + adjustedX, yPos + adjustedY))
    return textSurface

game_highscore = 0 
def loadHighScore():
    with open("score.txt", "r") as score: 
        global game_highscore
        game_highscore = int(score.read())
        score.close() 

def setHighScore(score):
    with open("score.txt", "w") as wscore: 
        wscore.write(str(game_highscore))
        wscore.close()

def main():
    pygame.init() 
    pygame.display.set_caption(game_title)

    surface = pygame.display.set_mode(game_resolution)
    loadHighScore()

    global GAME_ENDED
    global game_highscore

    state = 0
    xPos, yPos = 0, 0
    snake = [[xPos, yPos]]
    food = [random.randint(1, 19) * game_snake, random.randint(1, 19) * game_snake]

    difficulty = {
        "Easy": 0.2, 
        "Normal": 0.1,
        "Hard": 0.05,
        "Extreme": 0.02
    }

    FONT_SCORE = pygame.font.SysFont("verdana", 30)

    running = True
    while running: 
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                running = False
                break 
            elif (event.type == pygame.KEYDOWN) and not GAME_ENDED:
                if event.key == pygame.K_RIGHT and state != STATE_LEFT: 
                    state = STATE_RIGHT
                elif event.key == pygame.K_LEFT and state != STATE_RIGHT: 
                    state = STATE_LEFT  
                elif event.key == pygame.K_UP and state != STATE_DOWN: 
                    state = STATE_UP 
                elif event.key == pygame.K_DOWN and state != STATE_UP: 
                    state = STATE_DOWN 
            elif (event.type == pygame.KEYDOWN) and GAME_ENDED: 
                GAME_ENDED = False 
                xPos, yPos = 0, 0
                snake = [[xPos, yPos]]

        if not running: break

        # trailing bodies
        o_snake = snake.copy()
        for i in range(1, len(snake)):
            if state == 0: continue 
            snake[i] = copy.deepcopy(o_snake[i - 1])

        # snake movement
        if state == STATE_RIGHT: 
            snake[0][0] += game_snake
        elif state == STATE_LEFT: 
            snake[0][0] -= game_snake
        elif state == STATE_UP: 
            snake[0][1] -= game_snake 
        elif state == STATE_DOWN: 
            snake[0][1] += game_snake

        # making the snake go to the other side of the screen
        if snake[0][0] >= game_resolution[0]: 
            snake[0][0] = 0
        elif snake[0][0] < 0:
            snake[0][0] = game_resolution[0] - game_snake
        elif snake[0][1] >= game_resolution[1]:
            snake[0][1] = 0 
        elif snake[0][1] < 0:
            snake[0][1] = game_resolution[1] - game_snake

        # loss 
        for i in range(0, len(snake)):
            for x in range(i + 1, len(snake)):
                if snake[i] == snake[x]:
                    GAME_ENDED = True 
                    state = 0

                    if game_highscore < len(snake) - 1: 
                        game_highscore = len(snake) - 1 
                        setHighScore(game_highscore)

        # eating food
        if snake[0][0] == food[0] and snake[0][1] == food[1]:
            food = [random.randint(1, 19) * game_snake, random.randint(1, 19) * game_snake]

            xAdd = (state == STATE_LEFT or state == STATE_RIGHT) and game_snake or 0
            yAdd = (state == STATE_UP or state == STATE_DOWN) and game_snake or 0
            newBody = [snake[len(snake) - 1][0] + xAdd, snake[len(snake) - 1][1] + yAdd]
            snake.append(newBody)

        # drawing snake and food
        surface.fill(colour_black)
        for k, i in enumerate(snake):
            if k > 0:
                pygame.draw.rect(surface, colour_white, (i[0] + 4, i[1] + 4, game_snake - 8, game_snake - 8))
            else:
                pygame.draw.rect(surface, colour_white, (i[0] + 1, i[1] + 1, game_snake - 2, game_snake - 2))

        pygame.draw.rect(surface, colour_blue, (food[0], food[1], game_snake, game_snake))

        drawText(surface, f"Score: {len(snake) - 1}", FONT_SCORE, game_resolution[0] / 2, 40, colour=(255, 255, 255), align='centre')
        drawText(surface, f"High Score: {game_highscore}", FONT_SCORE, game_resolution[0] / 2, game_resolution[1] - 60, colour=(255, 255, 255), align='centre')

        if GAME_ENDED: 
            drawText(surface, "Game over!", FONT_SCORE, game_resolution[0] / 2, game_resolution[1] / 2, colour=(255, 255, 255), align='centre')
            drawText(surface, "Press any key to start again.", FONT_SCORE, game_resolution[0] / 2, game_resolution[1] / 2 - 40, colour=(255, 255, 255), align='centre')

        pygame.display.update()
        time.sleep(difficulty["Easy"])
main()
