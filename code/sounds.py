import pygame
import os
import sys

# ---------------- Inicialização do áudio ----------------
def _ensure_mixer():
    # Garante que o mixer do pygame esteja inicializado
    if not pygame.mixer.get_init():
        pygame.mixer.init()

# ---------------- Caminho base ----------------
if getattr(sys, 'frozen', False):  # executável
    BASE_DIR = os.path.dirname(sys.executable)
else:  # modo desenvolvimento
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Pasta de sons
SOUNDS_DIR = os.path.join(BASE_DIR, "assets", "sounds")

# ---------------- Carrega arquivos de som ----------------
def _find_asset(name_base, load_as_sound=False):
    # Procura o arquivo de som com extensões suportadas
    for ext in [".wav", ".ogg", ".mp3"]:
        path = os.path.join(SOUNDS_DIR, name_base + ext)
        if os.path.exists(path):
            if load_as_sound:
                try:
                    return pygame.mixer.Sound(path)
                except pygame.error:
                    return None
            return path  # retorna caminho se não for carregar
    return None

# Arquivos de música
menu_music_file = _find_asset("menu_music")
play_music_file = _find_asset("play_music")

# Sons curtos (efeitos)
crash_sound = None
batida_sound = None

def load_sounds():
    # Carrega os sons de efeito
    global crash_sound, batida_sound
    crash_sound = _find_asset("crash", load_as_sound=True)
    batida_sound = _find_asset("batida_music", load_as_sound=True)

# ---------------- Música de fundo ----------------
def play_menu_music():
    # Toca música do menu em loop
    _ensure_mixer()
    if menu_music_file:
        pygame.mixer.music.load(menu_music_file)
        pygame.mixer.music.play(-1)

def play_game_music():
    # Toca música do jogo em loop
    _ensure_mixer()
    if play_music_file:
        pygame.mixer.music.load(play_music_file)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

# ---------------- Efeitos sonoros ----------------
def play_crash():
    # Toca som de colisão
    if crash_sound:
        crash_sound.play()

def play_batida():
    # Toca som de batida curta
    if batida_sound:
        batida_sound.play()

