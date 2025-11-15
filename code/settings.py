import pygame

# Tela
WIDTH, HEIGHT = 500, 800  # tamanho da tela
FPS = 30  # taxa de atualização

# Pistas
PISTAS = 3  # quantidade de faixas
MARGEM_LATERAL = 100  # espaço verde nas laterais
AREA_PISTA_LARGURA = WIDTH - (MARGEM_LATERAL * 2)
PISTA_LARGURA = AREA_PISTA_LARGURA // PISTAS
PISTA_XS = [MARGEM_LATERAL + PISTA_LARGURA * i + PISTA_LARGURA // 2 for i in range(PISTAS)]

# Cores
COR_FUNDO = (25, 25, 30)
COR_PISTA = (80, 80, 80)
COR_FAIXA = (180, 180, 180)
COR_VERDE = (50, 150, 70)
BRANCO = (240, 240, 240)
VERMELHO = (220, 60, 60)
AMARELO = (240, 200, 60)

# Tamanhos dos carros
PLAYER_LARG, PLAYER_ALT = 90, 170
ENEMY_LARG, ENEMY_ALT = 80, 150

# Velocidade
VEL_INICIAL = 10
VEL_MAX = 100
VEL_INCREMENTO = 1  # aumenta 1 a cada carro desviado

# Interface
FONT_NAME = "arial"
BORDER_RADIUS = 28  # bordas arredondadas

# Nome Níveis
NOME_NIVEIS = [
    (0, 4, "Asphalt Turtle"),
    (5, 9, "Couch Racer"),
    (10, 14, "Aspiring Driver"),
    (15, 19, "Floor It"),
    (20, 24, "High Speed"),
    (25, 29, "Pro Street Racer"),
    (30, 34, "Lightning"),
    (35, 39, "Insane"),
    (40, 1000, "Asphalt Legend")
]
