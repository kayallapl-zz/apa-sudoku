# import pygame library
import pygame
from pygame.constants import KEYDOWN
 
# initialise the pygame font
pygame.font.init()
 
# Total window
screen = pygame.display.set_mode((500, 620))
 
# Title and Icon
pygame.display.set_caption("SUDOKU SOLVER USING BACKTRACKING")
# img = pygame.image.load('icon.png')
# pygame.display.set_icon(img)
 
x = 0
y = 0
dif = 500 / 9
val = 0
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
 
# Load test fonts for future use
font1 = pygame.font.SysFont("comicsans", 40)
font2 = pygame.font.SysFont("comicsans", 20)
def get_cord(pos):
    global x
    x = pos[0] // dif
    global y
    y = pos[1] // dif
 
# Highlight the cell selected
def draw_box():
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif-3, (y + i)*dif), (x * dif + dif + 3, (y + i)*dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ( (x + i)* dif, y * dif ), ((x + i) * dif, y * dif + dif), 7)  
 
# Function to draw required lines for making Sudoku grid        
def draw():
    # Draw the lines
        
    for i in range (9):
        for j in range (9):
            if grid[i][j] != 0:
 
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (255, 255, 255), (i * dif, j * dif, dif + 1, dif + 1))
 
                # Fill grid with default numbers specified
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 15, j * dif + 15))
    # Draw lines horizontally and verticallyto form grid          
    for i in range(10):
        if i % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)     
 
# Fill value entered in cell     
def draw_val(val):
    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x * dif + 15, y * dif + 15))   
 
# Raise error when wrong value entered
def raise_error1():
    text1 = font1.render("WRONG !!!", 1, (0, 0, 0))
    screen.blit(text1, (20, 570)) 
def raise_error2():
    text1 = font1.render("Wrong !!! Not a valid Key", 1, (0, 0, 0))
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
            global x, y
            x = i
            y = j
            # white color background\
            screen.fill((255, 255, 255))
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(50)
            if solve(grid, i, j):
                return True
            else:
                grid[i][j] = 0
            # white color background\
            screen.fill((255, 255, 255))
         
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(50)
        pause = True
        print("\n tentando: ")
        print(it)
        print("\n na posição: ")
        print(i, j)
        print("\nnão conseguiu pq:  ")
        print(motivo)
        while pause:
            event = pygame.event.wait()
            if event.type == KEYDOWN:  # Unpausing
                pause = False
    return False 
 
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
run = True
flag1 = 0
flag2 = 0
interactive = 0
rs = 0
error = 0
# The loop thats keep the window running
while run:
     
    # White color background
    screen.fill((255, 255, 255))
    # Loop through the events stored in event.get()
    for event in pygame.event.get():
        # Quit the game window
        if event.type == pygame.QUIT:
            run = False 
        # Get the mouse position to insert number   
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            pos = pygame.mouse.get_pos()
            get_cord(pos)
        # Get the number to be inserted if key pressed   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT:
                x += 1
                flag1 = 1
            if event.key == pygame.K_UP:
                y -= 1
                flag1 = 1
            if event.key == pygame.K_DOWN:
                y += 1
                flag1 = 1   
            if event.key == pygame.K_1:
                flag2 = 1
            # if event.key == pygame.K_2:
            #     val = 2   
            # if event.key == pygame.K_3:
            #     val = 3
            # if event.key == pygame.K_4:
            #     val = 4
            # if event.key == pygame.K_5:
            #     val = 5
            # if event.key == pygame.K_6:
            #     val = 6
            # if event.key == pygame.K_7:
            #     val = 7
            # if event.key == pygame.K_8:
            #     val = 8
            # if event.key == pygame.K_9:
            #     val = 9 
            # if event.key == pygame.K_RETURN:
            #     flag2 = 1
            # If D is pressed reset the board to default
            if event.key == pygame.K_d:
                rs = 0
                error = 0
                flag2 = 0
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
    if flag2 == 1:
        if solve(grid, 0, 0) == False:
            error = 1
        else:
            rs = 1
        flag2 = 0   
    if val != 0:           
        draw_val(val)
        # print(x)
        # print(y)
        if valid(grid, int(x), int(y), val) == True:
            grid[int(x)][int(y)] = val
            flag1 = 0
        else:
            grid[int(x)][int(y)] = 0
            raise_error2()  
        val = 0   
       
    if error == 1:
        raise_error1() 
    if rs == 1:
        result()       
    draw() 
    if flag1 == 1:
        draw_box()      
    instruction()   
 
    # Update window
    pygame.display.update() 
 
# Quit pygame window   
# pygame.quit()    