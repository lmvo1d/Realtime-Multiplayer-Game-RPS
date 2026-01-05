import pygame
from network import Network

pygame.font.init()

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")

class Button:
    def __init__(self, text, x, y, surface):
        self.text = text
        self.x = x
        self.y = y
        self.surface = surface
        self.width = 150
        self.height = 100

    def draw(self, win):
        win.blit(self.surface, (self.x, self.y, self.width, self.height))
        # font = pygame.font.SysFont("comicsans", 30)
        # text = font.render(self.text, 1, (255, 255, 255))
        # win.blit(text, (self.x + self.width/2 - text.get_width()/2, self.y + self.height/2 - text.get_height()/2))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
        
def redraw_window(win, game, p):
    win.fill((255, 255, 255))

    font = pygame.font.SysFont("comicsans", 60)
    text = font.render("Rock Paper Scissors", 1, (0, 0, 0))
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/16 - text.get_height()/16))

    if not game.connected():
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Waiting for Player...", 1, (0, 0, 0))
        win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 30)
        text1 = font.render("Your Move", 1, (0, 0, 0))
        text2 = font.render("Opponent's Move", 1, (0, 0, 0))

        win.blit(text1, (80, 200))
        win.blit(text2, (430, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))

            else:
                text1 = font.render("...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))

            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))

            else:
                text2 = font.render("...", 1, (0, 0, 0))


        for btn in btns:
            btn.draw(win)

        if p == 0:
            win.blit(text1, (80, 300))
            win.blit(text2, (400, 300))
        else:
            win.blit(text1, (400, 300))
            win.blit(text2, (80, 300)) 

    pygame.display.update()

imgs = [
    pygame.transform.scale(pygame.image.load("rock.png"), (150, 150)),
    pygame.transform.scale(pygame.image.load("paper.png"), (150, 150)),
    pygame.transform.scale(pygame.image.load("scissors.png"), (150, 150))
]

btns = [Button("Rock", 50, 500, imgs[0]), 
        Button("Paper", 250, 500, imgs[1]), 
        Button("Scissors", 450, 500, imgs[2])]

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    p = int(n.getP())
    print("You are player", p)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
            if game is None:
                print("Lost connection to server")
                run = False
                break
            
        except Exception as e:
            print("Couldn't get game:", str(e))
            run = False
            break

        if game.bothWent():
            redraw_window(WIN, game, p)
            pygame.time.delay(500)

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == p):
                text = font.render("You Won!", 1, (0, 255, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255, 255, 0))
            else:
                text = font.render("You Lost!", 1, (255, 0, 0))

            WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

            n.send("reset")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if p == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redraw_window(WIN, game, p)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        WIN.fill((255, 255, 255))

        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Rock Paper Scissors", 1, (0, 0, 0))
        WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/16 - text.get_height()/16))

        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (0, 0, 0))
        WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

if __name__ == "__main__":
    while True:
        menu_screen()
