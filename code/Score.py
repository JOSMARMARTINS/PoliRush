import sys
import pygame
from pygame import Surface, Rect, KEYDOWN, K_ESCAPE
from pygame.font import Font
from code.DBProxy import DBProxy
from code.sounds import play_menu_music
from code.Const import C_YELLOW, C_WHITE
from .settings import BORDER_RADIUS

class Score:
    """Tela de scores do jogo."""

    def __init__(self, window: Surface):
        self.window = window
        self.modal_width, self.modal_height = 400, 400

        # Superfície do modal
        self.surf = pygame.Surface((self.modal_width, self.modal_height), pygame.SRCALPHA)
        pygame.draw.rect(
            self.surf,
            (0, 0, 0, 140),  # fundo semitransparente
            self.surf.get_rect(),
            border_radius=BORDER_RADIUS
        )
        self.rect = self.surf.get_rect(center=(window.get_width() // 2, window.get_height() // 2))

        # botão Menu
        self.btn_menu = Rect(window.get_width() - 70, 13, 58, 28)
        self.smallfont = pygame.font.SysFont(None, 22, bold=True)

        # imagem de fundo
        self.bg_image = pygame.image.load("assets/images/ScoreBg.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (window.get_width(), window.get_height()))

    def draw_button_menu(self):
        """Desenha botão Menu."""
        mouse_pos = pygame.mouse.get_pos()
        hover = self.btn_menu.collidepoint(mouse_pos)
        color = (240, 200, 60) if hover else (30, 30, 30)
        text_color = (0, 0, 0) if hover else (240, 240, 240)
        pygame.draw.rect(self.window, color, self.btn_menu, border_radius=12)
        pygame.draw.rect(self.window, (80, 80, 80), self.btn_menu, 2, border_radius=12)
        label = self.smallfont.render("Menu", True, text_color)
        self.window.blit(label, (self.btn_menu.centerx - label.get_width() // 2,
                                 self.btn_menu.centery - label.get_height() // 2))

    def save(self, score: int):
        """Salva score no banco automaticamente."""
        play_menu_music()
        db_proxy = DBProxy()
        db_proxy.save(score)
        db_proxy.close()

    def show(self):
        play_music = True
        db_proxy = DBProxy()
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        running = True
        center_x = self.rect.centerx

        # Configurações de fonte e espaçamento
        data_font_size = 18
        linha_altura = 30

        # Colunas: posição | play | score | data
        col_pos_x = self.rect.left + 20  # posição 1°, 2°...
        col_play_x = self.rect.left + 70  # número do play do DB
        col_score_x = self.rect.left + 140  # coluna do score
        col_date_x = self.rect.left + 280  # coluna da data/hora

        while running:
            # Fundo
            self.window.blit(self.bg_image, (0, 0))
            self.window.blit(self.surf, self.rect)

            # Títulos
            self.score_text(40, 'TOP 10 SCORE', C_YELLOW, (center_x, self.rect.top + 40))

            # Cabeçalho das colunas
            self.score_text(18, 'POS', C_YELLOW, (col_pos_x, self.rect.top + 90))
            self.score_text(18, 'PLAY', C_YELLOW, (col_play_x, self.rect.top + 90))
            self.score_text(18, 'SCORE', C_YELLOW, (col_score_x, self.rect.top + 90))
            self.score_text(18, 'TIME  - DATA    ', C_YELLOW, (col_date_x, self.rect.top + 90))

            # Desenha os scores
            for idx, player_score in enumerate(list_score):
                play, score, date = player_score
                y_pos = self.rect.top + 130 + idx * linha_altura

                self.score_text(data_font_size, f'{idx + 1:02d}°', C_YELLOW, (col_pos_x, y_pos))
                self.score_text(data_font_size, f'{play:03d}', C_YELLOW, (col_play_x, y_pos))
                self.score_text(data_font_size, f'{score:05d}', C_YELLOW, (col_score_x, y_pos))
                self.score_text(data_font_size, f'{date}', C_YELLOW, (col_date_x, y_pos))

            # Botão Menu
            self.draw_button_menu()
            pygame.display.flip()

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_menu.collidepoint(event.pos):
                        running = False

    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        """Desenha texto centralizado."""
        font: Font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)
        surf: Surface = font.render(text, True, text_color).convert_alpha()
        rect: Rect = surf.get_rect(center=text_center_pos)
        self.window.blit(surf, rect)
