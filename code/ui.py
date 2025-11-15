import pygame
from .DBProxy import DBProxy  # <-- import do DB
from .settings import BRANCO, AMARELO, WIDTH, HEIGHT, BORDER_RADIUS, NOME_NIVEIS


def nivel_por_velocidade(vel):
    # retorna o nome do nível baseado na velocidade
    for a, b, nome in NOME_NIVEIS:
        if a <= vel <= b:
            return nome
    return NOME_NIVEIS[0][2]


# Função da barra de menu durante o jogo
def draw_header(surf, fonte, score, velocidade):
    nome_nivel = nivel_por_velocidade(velocidade)

    # Cria o header (fundo semi-transparente)
    header = pygame.Surface((WIDTH - 20, 40), pygame.SRCALPHA)
    pygame.draw.rect(header, (0, 0, 0, 120), header.get_rect(), border_radius=14)

    # Função auxiliar para desenhar texto com sombra
    def render_text_with_shadow(surface, font, text, color, pos, shadow_color=(50, 50, 50), offset=2):
        shadow = font.render(text, True, shadow_color)
        surface.blit(shadow, (pos[0] + offset, pos[1] + offset))
        surface.blit(font.render(text, True, color), pos)

    # Textos
    render_text_with_shadow(header, fonte, f"Score: {score}", BRANCO, (10, 8))
    render_text_with_shadow(header, fonte, f"Speed: {velocidade * 2:>3} km/h", BRANCO, (150, 8))
    render_text_with_shadow(header, fonte, f"Level: {nome_nivel}", AMARELO, (10, 8 + fonte.get_height()))

    # Desenha o header na tela
    surf.blit(header, (10, 8))


# Função do Menu inicial
def draw_menu(surf, bigfont, smallfont):
    mouse_pos = pygame.mouse.get_pos()

    # Abre conexão com o banco e pega high score
    db_proxy = DBProxy()
    record = db_proxy.get_high_score()
    db_proxy.close()

    # Cria o modal (fundo semi-transparente)
    modal = pygame.Surface((WIDTH - 40, HEIGHT - 200), pygame.SRCALPHA)
    pygame.draw.rect(modal, (0, 0, 0, 130), modal.get_rect(), border_radius=BORDER_RADIUS)

    # Desenha o modal primeiro
    surf.blit(modal, (20, 60))

    # Título
    title_text = "Poli Rush"
    title = bigfont.render(title_text, True, AMARELO)
    surf.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

    # Botões
    btns = [
        ("Play", (WIDTH // 2 - 80, 220, 160, 50)),
        (f"Record: {record}", (WIDTH // 2 - 80, 290, 160, 50)),
        ("Exit", (WIDTH // 2 - 80, 360, 160, 50)),
    ]

    rects = []

    for text, rect in btns:
        r = pygame.Rect(rect)
        rects.append(r)

        if r.collidepoint(mouse_pos):
            color_bg = AMARELO
            color_text = (0, 0, 0)
        else:
            color_bg = (30, 30, 30)
            color_text = BRANCO

        pygame.draw.rect(surf, color_bg, r, border_radius=12)
        pygame.draw.rect(surf, (80, 80, 80), r, 2, border_radius=12)

        label = smallfont.render(text, True, color_text)
        surf.blit(label, (r.centerx - label.get_width() // 2,
                          r.centery - label.get_height() // 2))

    return rects


# Função da tela de Game Over
def draw_game_over(surf, bigfont, smallfont, score, nome_nivel):
    # Cria o modal (fundo semi-transparente)
    modal = pygame.Surface((WIDTH - 40, 380), pygame.SRCALPHA)
    pygame.draw.rect(modal, (0, 0, 0, 130), modal.get_rect(), border_radius=BORDER_RADIUS)

    # Desenha o modal na tela antes de qualquer texto
    surf.blit(modal, (20, 120))

    # Títulos e informações com sombra para melhor leitura
    def render_text_with_shadow(font, text, color, x, y, shadow_color=(50, 50, 50), offset=2):
        shadow = font.render(text, True, shadow_color)
        surf.blit(shadow, (x + offset, y + offset))
        surf.blit(font.render(text, True, color), (x, y))

    title_x = WIDTH // 2 - bigfont.size("Game Over")[0] // 2
    title_y = 140
    render_text_with_shadow(bigfont, "Game Over", AMARELO, title_x, title_y)

    info_text = f"Score: {score}"
    info_x = WIDTH // 2 - smallfont.size(info_text)[0] // 2
    info_y = 200
    render_text_with_shadow(smallfont, info_text, BRANCO, info_x, info_y)

    level_text = f"Level: {nome_nivel}"
    level_x = WIDTH // 2 - smallfont.size(level_text)[0] // 2
    level_y = 230
    render_text_with_shadow(smallfont, level_text, BRANCO, level_x, level_y)

    # Botões
    btn_retry = pygame.Rect(WIDTH // 2 - 80, 300, 160, 50)
    btn_menu = pygame.Rect(WIDTH // 2 - 80, 370, 160, 50)
    mouse_pos = pygame.mouse.get_pos()

    # Retry button
    if btn_retry.collidepoint(mouse_pos):
        btn_color = (255, 255, 0)
        text_color = (0, 0, 0)
    else:
        btn_color = (30, 30, 30)
        text_color = BRANCO
    pygame.draw.rect(surf, btn_color, btn_retry, border_radius=12)
    pygame.draw.rect(surf, (80, 80, 80), btn_retry, 2, border_radius=12)
    label_retry = smallfont.render("Retry", True, text_color)
    surf.blit(label_retry, (btn_retry.centerx - label_retry.get_width() // 2,
                            btn_retry.centery - label_retry.get_height() // 2))

    # Menu button
    if btn_menu.collidepoint(mouse_pos):
        btn_color2 = (255, 255, 0)
        text_color2 = (0, 0, 0)
    else:
        btn_color2 = (30, 30, 30)
        text_color2 = BRANCO
    pygame.draw.rect(surf, btn_color2, btn_menu, border_radius=12)
    pygame.draw.rect(surf, (80, 80, 80), btn_menu, 2, border_radius=12)
    label_menu = smallfont.render("Menu", True, text_color2)
    surf.blit(label_menu, (btn_menu.centerx - label_menu.get_width() // 2,
                           btn_menu.centery - label_menu.get_height() // 2))

    return btn_retry, btn_menu


