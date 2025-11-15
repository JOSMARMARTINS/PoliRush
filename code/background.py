import pygame
import random
from .settings import WIDTH, HEIGHT, COR_VERDE, COR_PISTA, MARGEM_LATERAL, PISTA_LARGURA, COR_FAIXA

# cores extras
COR_ZEBRA_VERMELHA = (214, 64, 68)
COR_ZEBRA_BRANCA = (232, 239, 242)
COR_LINHA_AMARELA = (211, 176, 82)  # linha lateral amarela

ESPACO_ARVORE_CERCA = 20  # distância mínima entre árvore e cerca

# ---------------- Classe árvore ----------------
class Arvore:
    # árvore lateral com retângulo e limite de colisão
    def __init__(self, rect, delimitador_x):
        self.rect = rect
        self.delimitador_x = delimitador_x

    @property
    def x(self): return self.rect.x
    @x.setter
    def x(self, value): self.rect.x = value

    @property
    def y(self): return self.rect.y
    @y.setter
    def y(self, value): self.rect.y = value

    @property
    def top(self): return self.rect.top
    @property
    def topleft(self): return self.rect.topleft

# ---------------- Classe Background ----------------
class Background:
    # fundo: grama, pista, cercas, faixas e árvores
    def __init__(self, qtde_inicial=8):
        self.offset = 0  # deslocamento para animação
        self.arvores = []

        # carrega imagens
        self.arvore_img = pygame.image.load("assets/images/arvore.png").convert_alpha()
        self.arvore_img = pygame.transform.scale(self.arvore_img, (40, 50))

        self.grama_img = pygame.image.load("assets/images/grama.png").convert()
        self.grama_img = pygame.transform.scale(self.grama_img, (40, 40))

        self.cerca_img = pygame.image.load("assets/images/cercabranca.png").convert_alpha()
        self.cerca_img = pygame.transform.scale(self.cerca_img, (20, 60))

        # adiciona árvores iniciais
        self.inicializar_arvores(qtde_inicial)

    # cria árvore em posição livre
    def spawn_arvore(self, velo=0, y_pos=None):
        margem_vertical = self.arvore_img.get_height() + 50
        max_tentativas = 50
        DELIMITADOR_X = min(40, 10 + int(velo / 3))

        for _ in range(max_tentativas):
            lado = random.choice(['esquerda', 'direita'])

            if lado == 'esquerda':
                x_min = 0
                x_max = MARGEM_LATERAL - self.cerca_img.get_width() - self.arvore_img.get_width() - ESPACO_ARVORE_CERCA
            else:
                x_min = WIDTH - MARGEM_LATERAL + self.cerca_img.get_width() + ESPACO_ARVORE_CERCA
                x_max = WIDTH - self.arvore_img.get_width()

            x = max(x_min, min(random.randint(x_min, x_max), x_max))
            y_pos_final = -random.randint(50, 300) if y_pos is None else y_pos

            rect = self.arvore_img.get_rect()
            rect.topleft = (x, y_pos_final)

            # checa colisão com outras árvores
            colisao = any(abs(a.x - rect.x) < self.arvore_img.get_width() + 10 and
                          abs(a.y - rect.y) < margem_vertical
                          for a in self.arvores)
            if not colisao:
                return Arvore(rect, DELIMITADOR_X)

        return Arvore(rect, DELIMITADOR_X)

    # adiciona árvores iniciais sem sobreposição
    def inicializar_arvores(self, quantidade=8):
        tentativas = 0
        while len(self.arvores) < quantidade and tentativas < quantidade * 10:
            y_pos = random.randint(0, HEIGHT - self.arvore_img.get_height())
            arv = self.spawn_arvore(velo=0, y_pos=y_pos)
            overlap = any(abs(arv.x - a.x) < self.arvore_img.get_width() + 10 and
                          abs(arv.y - a.y) < self.arvore_img.get_height() + 50
                          for a in self.arvores)
            if not overlap:
                self.arvores.append(arv)
            tentativas += 1

    # atualiza fundo e árvores
    def update(self, velo):
        incremento = max(1, int(velo / 6))  # velocidade das linhas, zebra e cerca
        self.offset = (self.offset + incremento) % 60

        for i, a in enumerate(self.arvores):
            a.y += incremento
            if a.top > HEIGHT:
                self.arvores[i] = self.spawn_arvore(velo=velo)

    # desenha todo o cenário
    def draw(self, surf):
        espaco_lateral = 0
        linha_amarela_largura = 6
        linha_cinza_largura = 6
        zebra_largura = 10
        ciclo_altura = 30
        espaco_cerca_final = 8

        # grama nas laterais
        for x in [0, WIDTH - MARGEM_LATERAL]:
            for y in range(-self.grama_img.get_height(), HEIGHT + self.grama_img.get_height(), self.grama_img.get_height()):
                for xi in range(x, x + MARGEM_LATERAL, self.grama_img.get_width()):
                    surf.blit(self.grama_img, (xi, y + self.offset))

        # pista principal
        pygame.draw.rect(surf, COR_PISTA, (MARGEM_LATERAL, 0, WIDTH - 2*MARGEM_LATERAL, HEIGHT))

        # linhas laterais, zebra e cercas
        lados = [('esquerda', MARGEM_LATERAL), ('direita', WIDTH - MARGEM_LATERAL)]
        for lado, pista_x in lados:
            if lado == 'esquerda':
                x_amarela = pista_x - espaco_lateral - linha_amarela_largura
                pygame.draw.rect(surf, COR_LINHA_AMARELA, (x_amarela, -self.offset, linha_amarela_largura, HEIGHT + self.offset))
                x_cinza = x_amarela - linha_cinza_largura
                pygame.draw.rect(surf, COR_PISTA, (x_cinza, -self.offset, linha_cinza_largura, HEIGHT + self.offset))
                x_zebra = x_cinza - zebra_largura
                for y in range(-ciclo_altura*2, HEIGHT, ciclo_altura*2):
                    pygame.draw.rect(surf, COR_ZEBRA_VERMELHA, (x_zebra, y + self.offset, zebra_largura, ciclo_altura))
                    pygame.draw.rect(surf, COR_ZEBRA_BRANCA, (x_zebra, y + self.offset + ciclo_altura, zebra_largura, ciclo_altura))
                x_cerca = x_zebra - self.cerca_img.get_width() - espaco_cerca_final
                for y in range(-self.cerca_img.get_height(), HEIGHT + self.cerca_img.get_height(), self.cerca_img.get_height()):
                    surf.blit(self.cerca_img, (x_cerca, y + self.offset))
            else:
                x_amarela = pista_x + espaco_lateral
                pygame.draw.rect(surf, COR_LINHA_AMARELA, (x_amarela, -self.offset, linha_amarela_largura, HEIGHT + self.offset))
                x_cinza = x_amarela + linha_amarela_largura
                pygame.draw.rect(surf, COR_PISTA, (x_cinza, -self.offset, linha_cinza_largura, HEIGHT + self.offset))
                x_zebra = x_cinza + linha_cinza_largura
                for y in range(-ciclo_altura*2, HEIGHT, ciclo_altura*2):
                    pygame.draw.rect(surf, COR_ZEBRA_VERMELHA, (x_zebra, y + self.offset, zebra_largura, ciclo_altura))
                    pygame.draw.rect(surf, COR_ZEBRA_BRANCA, (x_zebra, y + self.offset + ciclo_altura, zebra_largura, ciclo_altura))
                x_cerca = x_zebra + zebra_largura + espaco_cerca_final
                for y in range(-self.cerca_img.get_height(), HEIGHT + self.cerca_img.get_height(), self.cerca_img.get_height()):
                    surf.blit(self.cerca_img, (x_cerca, y + self.offset))

        # faixas centrais
        for i in range(1, 3):
            x = MARGEM_LATERAL + PISTA_LARGURA * i
            bloco_altura = 40
            espacamento = 20
            ciclo = bloco_altura + espacamento
            for y in range(-ciclo, HEIGHT, ciclo):
                pygame.draw.rect(surf, COR_FAIXA, (x - 2, y + self.offset, 4, bloco_altura), border_radius=2)

        # desenha árvores
        for a in self.arvores:
            surf.blit(self.arvore_img, a.topleft)
