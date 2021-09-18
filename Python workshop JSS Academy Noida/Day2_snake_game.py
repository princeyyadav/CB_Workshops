import pygame, random
pygame.init() # initializes all the modules

# screen
w, h = 500, 500 # width, height
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("SNAKE GAME")

r = 10

pos = [300,300]
snake_color = (250, 35, 119)
snake_pos = [[300,300], [320,300], [340,300], [360,300]]

def draw_snake(screen, snake_pos):
    for pos in snake_pos:
        pygame.draw.circle(screen, snake_color, pos, r)

step = 20
left = (-step, 0)
right = (step, 0)
up = (0, -step)
down = (0, step)

direction = left # current direction

# apple 
apple_pos = [400, 400]

# FPS
fps = 50
clock = pygame.time.Clock()

# score
score = 0
font = pygame.font.SysFont("Arial", 32, True)

def display_score(screen, score):
    text_surface = font.render("Score: "+str(score), True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))


# timer
timer = 0

run = True
while run:

    screen.fill((123, 202, 38)) # fills the background
    clock.tick(fps)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            print("Quit")
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != right:
                # print("LEFT")
                direction = left
            if event.key == pygame.K_RIGHT and direction != left:
                # print("RIGHT")
                direction = right
            if event.key == pygame.K_UP and direction != down:
                # print("UP")
                direction = up
            if event.key == pygame.K_DOWN and direction != up:
                direction = down
        
    # movement
    timer += 1
    if timer % 5 == 0:
        snake_pos = [[snake_pos[0][0]+direction[0], snake_pos[0][1]+direction[1]]] + snake_pos[:-1]
        timer = 0

    # score
    if snake_pos[0] == apple_pos:
        score += 1
        # print(score)
        # respawn apple
        apple_pos[0] = (random.randint(2*r, w-(2*r))//step)*step
        apple_pos[1] = (random.randint(2*r, h-(2*r))//step)*step
        snake_pos.append(snake_pos[-1])

    # gameover
    for pos in snake_pos[1:]:
        if snake_pos[0] == pos:
            print("GAMEOVER")
            run = False
    
    # draw apple
    pygame.draw.circle(screen, (200,0,0), apple_pos, r)
    
    # draw snake
    draw_snake(screen, snake_pos)

    # display score
    display_score(screen, score)
    
    pygame.display.update()
