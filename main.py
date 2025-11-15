import pygame
from code.settings import WIDTH, HEIGHT
from code.game import Game
from code import sounds

def main():
    pygame.init()
    pygame.mixer.init()
    sounds.load_sounds()  # carrega sons, incluindo menu_music

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Poli Rush")

    game = Game(screen)
    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()
