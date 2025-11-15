import pygame
import random
from code.settings import WIDTH, HEIGHT, FPS, VEL_INICIAL, VEL_MAX, VEL_INCREMENTO, ENEMY_ALT, ENEMY_LARG
from code.background import Background
from code.player import Player
from code.enemy import Enemy
from code.ui import draw_header, draw_menu, draw_game_over, nivel_por_velocidade
from code.sounds import play_menu_music, play_game_music, play_batida
from code.Score import Score

STATE_MENU = "MENU"
STATE_PLAY = "PLAY"
STATE_CRASHING = "CRASHING"
STATE_OVER = "OVER"


class Game:
    """Classe principal do jogo."""

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 18, bold=True)
        self.bigfont = pygame.font.SysFont(None, 42, bold=True)
        self.smallfont = pygame.font.SysFont(None, 22, bold=True)
        self.btn_menu = pygame.Rect(WIDTH - 70, 13, 58, 28)
        self.state = STATE_MENU
        self.reset()
        self.score_screen = Score(self.screen)
        play_menu_music()

    def reset(self):
        """Reinicia variáveis e objetos para começar o jogo."""
        self.bg = Background()
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = Player(y_base=HEIGHT - 120)
        self.all_sprites.add(self.player)
        self.score = 0
        self.velocidade = VEL_INICIAL
        self.spawn_timer = 0
        self.spawn_rate = 850
        self.crash_time = 0

    def spawn_enemy(self):
        """Cria inimigos em posições livres."""
        max_tentativas = 30
        distancia_minima = ENEMY_ALT * 3
        for _ in range(max_tentativas):
            pista = random.choice(self.player.pistas_x)
            y_pos = random.randint(-ENEMY_ALT * 4, -ENEMY_ALT)
            pode_spawnar = True
            for e in self.enemies:
                if abs(e.rect.y - y_pos) < distancia_minima:
                    pode_spawnar = False
                    break
            if pode_spawnar:
                novo = Enemy()
                novo.rect.centerx = pista
                novo.rect.y = y_pos
                self.enemies.add(novo)
                self.all_sprites.add(novo)
                break

    def handle_events(self):
        """Trata eventos do teclado e mouse."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                # Menu ou game over: iniciar jogo
                if self.state in (STATE_MENU, STATE_OVER) and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.start_game()
                elif self.state == STATE_OVER and event.key == pygame.K_ESCAPE:
                    self.to_menu()
                elif self.state == STATE_PLAY:
                    # Movimenta jogador
                    if event.key == pygame.K_LEFT:
                        self.player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.player.move_right()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == STATE_MENU:
                    if self.menu_buttons[0].collidepoint(event.pos):
                        self.start_game()
                    elif self.menu_buttons[1].collidepoint(event.pos):
                        self.score_screen.show()
                    elif self.menu_buttons[2].collidepoint(event.pos):
                        return "QUIT"
                elif self.state == STATE_PLAY:
                    if self.btn_menu.collidepoint(event.pos):
                        self.to_menu()
                elif self.state == STATE_OVER:
                    if self.btn_over_retry.collidepoint(event.pos):
                        self.start_game()
                    elif self.btn_over_menu.collidepoint(event.pos):
                        self.to_menu()
        return None

    def start_game(self):
        """Inicia o jogo."""
        self.reset()
        self.state = STATE_PLAY
        self.game_start_time = pygame.time.get_ticks()
        play_game_music()
        self.spawn_timer = -1000

    def to_menu(self):
        """Volta para o menu principal."""
        self.state = STATE_MENU
        play_menu_music()

    def update(self, dt):
        """Atualiza jogo a cada frame."""
        if self.state == STATE_PLAY:
            self.player.update()
            self.bg.update(self.velocidade)
            for e in list(self.enemies):
                if e.update(self.velocidade) == "escaped":
                    self.score += 1
                    if self.velocidade < VEL_MAX:
                        self.velocidade = min(VEL_MAX, self.velocidade + VEL_INCREMENTO)
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_rate and len(self.enemies) < 3:
                self.spawn_timer = 0
                self.spawn_enemy()
            # colisão com inimigos
            if pygame.sprite.spritecollideany(self.player, self.enemies, pygame.sprite.collide_mask):
                pygame.mixer.music.pause()
                play_batida()
                self.score_screen.save(self.score)
                self.state = STATE_CRASHING
                self.crash_time = pygame.time.get_ticks()
        elif self.state == STATE_CRASHING:
            # espera antes de mostrar game over
            if pygame.time.get_ticks() - self.crash_time > 2000:
                self.state = STATE_OVER

    def draw(self):
        """Desenha todos os elementos na tela."""
        self.bg.draw(self.screen)
        self.all_sprites.draw(self.screen)

        if self.state == STATE_MENU:
            # desenha menu
            self.menu_buttons = draw_menu(self.screen, self.bigfont, self.smallfont)
        elif self.state in (STATE_PLAY, STATE_CRASHING):
            draw_header(self.screen, self.font, self.score, self.velocidade)
            # botão menu
            mouse_pos = pygame.mouse.get_pos()
            color = (240, 200, 60) if self.btn_menu.collidepoint(mouse_pos) else (30, 30, 30)
            text_color = (0, 0, 0) if self.btn_menu.collidepoint(mouse_pos) else (240, 240, 240)
            pygame.draw.rect(self.screen, color, self.btn_menu, border_radius=12)
            pygame.draw.rect(self.screen, (80, 80, 80), self.btn_menu, 2, border_radius=12)
            label = self.smallfont.render("Menu", True, text_color)
            self.screen.blit(label, (self.btn_menu.centerx - label.get_width() // 2,
                                     self.btn_menu.centery - label.get_height() // 2))
            # instrução inicial piscando
            if self.state == STATE_PLAY and pygame.time.get_ticks() < self.game_start_time + 3500:
                elapsed = pygame.time.get_ticks() - self.game_start_time
                frame = (elapsed // 300) % 12
                arrow_frames = ["PRESS", "< PRESS >", "< < PRESS > >", "< < < PRESS > > >", "PRESS", "< PRESS >",
                                "< < PRESS > >", "< < < PRESS > > >", "PRESS", "< PRESS >", "< < PRESS > >",
                                "< < < PRESS > > >"]
                instruction_text = arrow_frames[frame]
                rendered_text = self.smallfont.render(instruction_text, True, (240, 240, 240))
                text_rect = rendered_text.get_rect(center=(WIDTH // 2, self.player.rect.top - 40))
                self.screen.blit(rendered_text, text_rect)

        elif self.state == STATE_OVER:
            # tela de game over
            nome_nivel = nivel_por_velocidade(self.velocidade)
            self.btn_over_retry, self.btn_over_menu = draw_game_over(
                self.screen, self.bigfont, self.smallfont, self.score, nome_nivel
            )

        pygame.display.flip()

    def run(self):
        """Loop principal do jogo."""
        running = True
        while running:
            dt = self.clock.tick(FPS)
            action = self.handle_events()
            if action == "QUIT":
                running = False
            self.update(dt)
            self.draw()
