import pygame
import random
from .settings import ENEMY_LARG, ENEMY_ALT, HEIGHT

# Lista de carros inimigos
CARROS_NORMAIS = [
    "assets/images/carro_vermelho.png",
    "assets/images/carro_azul.png",
    "assets/images/carro_verde.png",
    "assets/images/carro_amarelo.png",
    "assets/images/carro_roxo.png",
    "assets/images/carro_laranja.png",
    "assets/images/carro_azulclaro.png",
    "assets/images/carro_marrom.png"
]

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # escolhe carro aleatório
        imagem_path = random.choice(CARROS_NORMAIS)
        self.image = pygame.image.load(imagem_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (ENEMY_LARG, ENEMY_ALT))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        # posição inicial acima da tela
        self.rect.y = random.randint(-ENEMY_ALT * 2, -ENEMY_ALT)

    def update(self, velocidade):
        # desce o carro
        self.rect.y += velocidade
        # se passou da tela, remove e retorna "escaped"
        if self.rect.top > HEIGHT:
            self.kill()
            return "escaped"
        return None

