# import pygame library
import pygame
import time
from pygame.constants import KEYDOWN
 
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
final_time = fnt.render("Time: " + "0.0", 1, (0,0,0))

# Default Sudoku Board.
grid = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

grid_original = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
 
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
            if grid[i][j] != 0:
 
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (255, 255, 255), (i * dif, j * dif, dif + 1, dif + 1))
 
                # Fill grid with default numbers specified
                if grid[i][j] == grid_original[i][j]:
                    color = (0, 0, 0)
                else:
                    color = (255, 0, 0)
                text1 = font1.render(str(grid[i][j]), 1, color)
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
        play_time = round(time.time() - start)
        global fnt
        text = fnt.render("Time: " + format_time(play_time), 1, (0,0,0))
        global final_time
        final_time = text
        screen.blit(text, (540 - 200, 580))
 
# Raise error when wrong value entered
def raise_error():
    text1 = font1.render("WRONG !!!", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))
 
# Check if the value entered in board is valid
def valid(m, i, j, val):
    for it in range(9):
        if m[i][it] == val:
            return (False, "coluna")
        if m[it][j] == val:
            return (False, "linha")
    it = i // 3
    jt = j // 3
    for i in range(it * 3, it * 3 + 3):
        for j in range (jt * 3, jt * 3 + 3):
            if m[i][j] == val:
                return (False, "quadrado")
    return (True, "")

# Check if has an empty value in board.
# If has, return that position.
# Otherwise, return None.
def find_empty(bo):
    for j in range(len(bo)):
        for i in range(len(bo[0])):
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
    frase3 = "porém há um mesmo número na mesma " + str(motivo)
    text1 = font2.render(frase1, 1, (0, 0, 0))
    text2 = font2.render(frase2, 1, (0, 0, 0))
    text3 = font2.render(frase3, 1, (0, 0, 0))
    screen.blit(text1, (20, 520))       
    screen.blit(text2, (20, 540))
    screen.blit(text3, (20, 560))
 
# Display instruction for the game
def instruction():
    text1 = font2.render("Pressione D para reiniciar", 1, (0, 0, 0))
    text2 = font2.render("Pressione 1 para solução automática", 1, (0, 0, 0))
    text3 = font2.render("Pressione 2 para solução interativa", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))       
    screen.blit(text2, (20, 540))
    screen.blit(text3, (20, 560))
 
# Display options when solved
def result():
    text1 = font1.render("FINISHED", 1, (0, 0, 0))
    screen.blit(text1, (20, 580))   

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
            if event.key == pygame.K_d:
                displayResult = False
                hasError = False
                play = False
                grid = [
                    [7, 8, 0, 4, 0, 0, 1, 2, 0],
                    [6, 0, 0, 0, 7, 5, 0, 0, 9],
                    [0, 0, 0, 6, 0, 1, 0, 7, 8],
                    [0, 0, 7, 0, 4, 0, 2, 6, 0],
                    [0, 0, 1, 0, 5, 0, 9, 3, 0],
                    [9, 0, 4, 0, 6, 0, 0, 0, 5],
                    [0, 7, 0, 3, 0, 0, 0, 1, 2],
                    [1, 2, 0, 0, 0, 7, 4, 0, 0],
                    [0, 4, 9, 2, 0, 6, 0, 0, 7]
                ]
    if play:
        start = time.time()
        if solve(grid, 0, 0) == False:
            hasError = True
        else:
            displayResult = True
        play = False
       
    if hasError:
        raise_error() 

    if displayResult:
        result()    
           
    draw()
    instruction()
    if not interactive:
        screen.blit(final_time, (540 - 200, 580))
 
    # Update window
    pygame.display.update() 
 
# Quit pygame window   
# pygame.quit()    