import pygame, random
pygame.init() # initializes all the modules

w, h = 300, 500
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Jumping Santa")
icon = pygame.image.load("images/SANTA.png")
pygame.display.set_icon(icon)

bg = pygame.image.load("images/snowfall.png")
bg = pygame.transform.scale(bg, (w,h))


base = pygame.image.load("images/base.png")

die_sound = pygame.mixer.Sound("sounds/die.wav")
point_sound = pygame.mixer.Sound("sounds/point.wav")
wing_sound = pygame.mixer.Sound("sounds/wing.wav")


class Santa:

    def __init__(self, pos):
        self.image = pygame.image.load("images/SANTA.png")
        self.image = pygame.transform.scale(self.image, (34,34))
        self.rect = self.image.get_rect() # -> (0,0)
        self.rect.x, self.rect.y = pos
        self.vel = 6
        self.jump = False
        self.score = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        if self.jump:
            self.rect.y -= self.vel
        else:
            self.rect.y += self.vel
        if self.rect.bottom > 400:
            self.rect.bottom = 400
        if self.rect.top < 0:
            self.rect.top = 0

    def collide(self, pipes):
        return self.rect.colliderect(pipes.trect) or self.rect.colliderect(pipes.brect) 

class Pipes:

    def __init__(self, pos):
        self.top_pipe = pygame.image.load("images/pipe-up.png")
        self.bottom_pipe = pygame.image.load("images/pipe-down.png")
        self.trect = self.top_pipe.get_rect()
        self.brect = self.bottom_pipe.get_rect()
        self.trect.x, self.trect.y = pos
        self.brect.x, self.brect.y = self.trect.x, self.trect.bottom+100
        self.vel = 8

    def draw(self, screen):
        screen.blit(self.top_pipe, self.trect)
        screen.blit(self.bottom_pipe, self.brect)

    def move(self, santa):
        self.trect.x -= self.vel
        self.brect.x -= self.vel

        if self.trect.right < 0:
            self.trect.x = 300
            self.brect.x = 300
            self.trect.y = random.randint(-150, -50)
            self.brect.y = self.trect.bottom + 100 #random.choice([50, 70 ])
            santa.score += 1
            point_sound.play()



FPS = 30
clock = pygame.time.Clock()


font = pygame.font.SysFont("Arial", 32, True)

def display_score(screen, score):
    text_surface = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text_surface, (10,10))

gameover_png = pygame.image.load("images/gameover.png")

def gameover(screen, s):

    run = True
    while run:

        screen.blit(bg, (0,0) )
        
        screen.blit(gameover_png, (60, 100))

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        display_score(screen, s.score)
        pygame.display.update()



def gamestart(screen):

    s = Santa((50,250))

    pipe_pos = [200, -100]
    p = Pipes(pipe_pos)

    run = True
    while run:

        screen.blit(bg, (0,0) )
        
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                s.jump = True
                wing_sound.play()
            
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                s.jump = False

        s.move()
        p.move(s)

        # GAMEOVER
        if s.collide(p):
            die_sound.play()
            gameover(screen, s)
            run = False

        p.draw(screen)
        s.draw(screen)
        display_score(screen, s.score)
        screen.blit(base, (0,400))
        pygame.display.update()


intro = pygame.image.load("images/intro.png")
SKY_BLUE = (63, 164, 193)
run = True
while run:

    screen.fill(SKY_BLUE)
    screen.blit(intro, (65,100) )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("QUIT")
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            gamestart(screen)

    pygame.display.update()
