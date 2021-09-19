# import pygame library
import pygame
import time
import copy
from pygame.constants import KEYDOWN
import random

from boards import *
 
# initialise the pygame font
pygame.font.init()
 
# Total window
screen = pygame.display.set_mode((500, 620))
 
# Title and Icon
pygame.display.set_caption("SUDOKU - BACKTRACKING")

run = True
displayResult = False
hasError = False
start = time.time()
play = False
interactive = False
dif = 500 / 9
fnt = pygame.font.SysFont("comicsans", 40)
final_time = fnt.render("Time: " + " 0.0", 1, (0,0,0))
dificulty = 2
random_int = random.randint(0,2)
grid = copy.deepcopy(intermediary[random_int])
grid_original = copy.deepcopy(intermediary[random_int])
 
# Load test fonts for future use
font1 = pygame.font.SysFont("comicsans", 40)
font2 = pygame.font.SysFont("comicsans", 20)

def format_time(secs):
    sec = secs%60
    minute = secs//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

# Function to draw required lines for making Sudoku grid
def draw():
    # Draw the lines
    for i in range (9):
        for j in range (9):
            if grid[j][i] != 0:
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (255, 255, 255), (i * dif, j * dif, dif + 1, dif + 1))
 
                # Fill grid with default numbers specified
                if grid[j][i] == grid_original[j][i]:
                    color = (0, 0, 0)
                else:
                    color = (255, 0, 0)
                text1 = font1.render(str(grid[j][i]), 1, color)
                screen.blit(text1, (i * dif + 15, j * dif + 15))
    # Draw lines horizontally and verticallyto form grid
    for i in range(10):
        if i % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)
    
    if play and not interactive:
        global fnt, final_time
        play_time = round(time.time() - start)
        text = fnt.render("Time: " + format_time(play_time), 1, (0,0,0))
        final_time = text
        screen.blit(text, (540 - 190, 585))
 
# Check if the value entered in board is valid
def valid(board, i, j, value):
    for it in range(9):
        if board[i][it] == value:
            return (False, "coluna")
        if board[it][j] == value:
            return (False, "linha")

    box_x = i // 3
    box_y = j // 3

    for i in range(box_x * 3, box_x * 3 + 3):
        for j in range (box_y * 3, box_y * 3 + 3):
            if board[i][j] == value:
                return (False, "quadrado")
    return (True, "")

# Check if has an empty value in board.
# If has, return that position.
# Otherwise, return None.
def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None
 
# Solves the sudoku board using Backtracking Algorithm
def solve(grid, i, j):
    find = find_empty(grid)
    if not find:
        return True
    else:
        i, j = find
    pygame.event.pump()
    
    for it in range(1, 10):
        valido, motivo = valid(grid, i, j, it)
        if valido:
            grid[i][j] = it
            update_screen()
            if solve(grid, i, j):
                return True
            else:
                grid[i][j] = 0

            update_screen()
        if interactive:
            pause = True
            feedback(it, i, j, motivo)
            pygame.display.update()
            while pause:
                event = pygame.event.wait()
                if event.type == KEYDOWN:  # Unpausing
                    update_screen()
                    pause = False
    return False

def update_screen():
    screen.fill((255, 255, 255))
    draw()
    pygame.display.update()
    pygame.time.delay(50)
 
# Display feedback for interactive game
def feedback(it, linha, coluna, motivo):
    frase1 = "Tentativa de posicionar o número " + str(it)
    frase2 = "na linha " + str(linha+1) +", coluna " + str(coluna+1) + ", "
    frase3 = "porém há um mesmo número na mesma " + str(motivo) + "."
    text1 = font2.render(frase1, 1, (0, 0, 0))
    text2 = font2.render(frase2, 1, (0, 0, 0))
    text3 = font2.render(frase3, 1, (0, 0, 0))
    screen.blit(text1, (15, 515))       
    screen.blit(text2, (15, 530))
    screen.blit(text3, (15, 545))
 
# Display instruction for the game
def instruction():
    text1 = font2.render("Pressione R para reiniciar", 1, (0, 0, 0))
    text2 = font2.render("Pressione 1 para solução automática", 1, (0, 0, 0))
    text3 = font2.render("Pressione 2 para solução interativa", 1, (0, 0, 0))
    text4 = font2.render("Pressione D para trocar a dificuldade", 1, (0, 0, 0))
    screen.blit(text1, (15, 515))       
    screen.blit(text2, (15, 530))
    screen.blit(text3, (15, 545))
    screen.blit(text4, (15, 560))
 
# Display options when solved
def result():
    text1 = font1.render("FINISHED", 1, (0, 0, 0))
    screen.blit(text1, (15, 585))

def render_difficulty():
    if dificulty == 1:
        string = "FÁCIL"
        color = (0, 200, 0)
    elif dificulty == 2:
        string = "MÉDIA"
        color = (0, 80, 255)
    elif dificulty == 3:
        string = "DIFÍCIL"
        color = (255, 0, 0)
    text1 = font2.render(str("Dificuldade: " + string), 1, color)
    screen.blit(text1, (540 - 175, 515))

def change_difficulty():
    global dificulty, grid, grid_original
    if dificulty == 1:
        dificulty = 2
        grid = copy.deepcopy(intermediary[2])
        grid_original = copy.deepcopy(intermediary[2])
    elif dificulty == 2:
        dificulty = 3
        grid = copy.deepcopy(hard[random_int])
        grid_original = copy.deepcopy(hard[random_int])
    elif dificulty == 3:
        dificulty = 1
        grid = copy.deepcopy(easy[random_int])
        grid_original = copy.deepcopy(easy[random_int])

# The loop thats keep the window running
while run:

    # White color background
    screen.fill((255, 255, 255))
    draw()
    # Loop through the events stored in event.get()
    for event in pygame.event.get():
        # Quit the game window
        if event.type == pygame.QUIT:
            run = False
        # Get the number to be inserted if key pressed   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                play = True
                interactive = False
            if event.key == pygame.K_2:
                play = True
                interactive = True
            if event.key == pygame.K_r:
                displayResult = False
                hasError = False
                play = False
                grid = grid_original
            if event.key == pygame.K_d:
                random_int = random.randint(0,2)
                change_difficulty()
    if play:
        start = time.time()
        if solve(grid, 0, 0) == False:
            hasError = True
        else:
            displayResult = True
        play = False

    if displayResult:
        result()    
           
    draw()
    instruction()
    render_difficulty()
    if not interactive:
        screen.blit(final_time, (540 - 190, 585))
 
    # Update window
    pygame.display.update() 
 
# Quit pygame window   
# pygame.quit()    