import pygame
from .settings import PLAYER_LARG, PLAYER_ALT, PISTA_XS


class Player(pygame.sprite.Sprite):
    """Classe do jogador (carro de polícia)."""

    def __init__(self, y_base: int):
        super().__init__()

        # Carrega imagens do carro com giroflex azul e vermelho
        self.image_v1 = pygame.image.load("assets/images/police_car_blue_left.png").convert_alpha()
        self.image_v2 = pygame.image.load("assets/images/police_car_red_left.png").convert_alpha()

        # Redimensiona para o tamanho do player
        self.image_v1 = pygame.transform.scale(self.image_v1, (PLAYER_LARG, PLAYER_ALT))
        self.image_v2 = pygame.transform.scale(self.image_v2, (PLAYER_LARG, PLAYER_ALT))

        self.images = [self.image_v1, self.image_v2]
        self.image_index = 0
        self.image = self.images[self.image_index]  # imagem inicial

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Posições das pistas e lane inicial
        self.pistas_x = PISTA_XS
        self.lane = 1  # começa na pista do meio
        self.rect.centerx = self.pistas_x[self.lane]
        self.rect.centery = y_base

        # Timer para piscar o giroflex
        self.flash_interval = 200  # ms por piscada
        self.last_update = pygame.time.get_ticks()

    def move_left(self):
        """Move para a esquerda se não estiver na primeira pista."""
        if self.lane > 0:
            self.lane -= 1
            self.rect.centerx = self.pistas_x[self.lane]

    def move_right(self):
        """Move para a direita se não estiver na última pista."""
        if self.lane < len(self.pistas_x) - 1:
            self.lane += 1
            self.rect.centerx = self.pistas_x[self.lane]

    def update(self):
        """Anima o giroflex alternando imagens."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.flash_interval:
            self.last_update = now
            self.image_index = (self.image_index + 1) % len(self.images)

            # mantém a posição central antes de trocar a imagem
            center = self.rect.center
            self.image = self.images[self.image_index]
            self.rect = self.image.get_rect(center=center)
            self.mask = pygame.mask.from_surface(self.image)

