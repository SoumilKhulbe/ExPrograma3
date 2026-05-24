import pygame
import random
from player import player
from fantasma import Fantasma
from explosao import Explosao
from mapa import Mapa

pygame.init()
pygame.mixer.init()
LARGURA = 960
ALTURA  = 704

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

mapa   = Mapa()
player = player(LARGURA, ALTURA)

explosao_sound = pygame.mixer.Sound("assets/som/roblox-explosion-sound_HNC20s9c.mp3")
ak_sound       = pygame.mixer.Sound("assets/som/Gun_2.wav")
pickup_sound   = pygame.mixer.Sound("assets/som/Shotgun_Pump.wav")
pickup_sound.set_volume(0.4)

death_sounds = [
    pygame.mixer.Sound("assets/som/lego-yoda-death-sound-effect.mp3"),
    pygame.mixer.Sound("assets/som/Oswald_Attract.wav"),
    pygame.mixer.Sound("assets/som/026_abnormality_dead_a_v1.wav"),
    pygame.mixer.Sound("assets/som/Dead.wav")
]
for sound in death_sounds:
    sound.set_volume(0.6)

spritesheet_items   = pygame.image.load('assets/PacManAssets-Items/PacManAssets-Items_0_0.png').convert_alpha()
super_ponto_sprite  = spritesheet_items.subsurface((16, 16, 16, 16))

fantasmas = [
    Fantasma(100, 100, "blinky", 100, 100),
    Fantasma(200, 100, "pinky",  200, 100),
    Fantasma(300, 100, "inky",   300, 100),
    Fantasma(400, 100, "clyde",  400, 100)
]

explosoes      = []
sprites_explosao = []

spritesheet_explosao = pygame.image.load("assets/guns/clipart2508851.png").convert_alpha()
largura_sprite = 480 // 5
altura_sprite  = 280 // 3

for linha in range(3):
    for coluna in range(5):
        sprite = spritesheet_explosao.subsurface(
            coluna * largura_sprite, linha * altura_sprite,
            largura_sprite, altura_sprite
        )
        sprite = pygame.transform.scale(sprite, (96, 96))
        sprites_explosao.append(sprite)

rodando = True

while rodando:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                player.atirar()

    # --- Movimento do player com colisão nas paredes do mapa ---
    keys = pygame.key.get_pressed()
    dx, dy  = 0, 0
    movendo = False

    if keys[pygame.K_LEFT]:
        dx = -player.velocidade
        player.direcao = 'esquerda'
        movendo = True
    elif keys[pygame.K_RIGHT]:
        dx = player.velocidade
        player.direcao = 'direita'
        movendo = True
    elif keys[pygame.K_UP]:
        dy = -player.velocidade
        player.direcao = 'cima'
        movendo = True
    elif keys[pygame.K_DOWN]:
        dy = player.velocidade
        player.direcao = 'baixo'
        movendo = True

    if movendo:
        player.contador_animacao += 1
        if player.contador_animacao >= 10:
            player.contador_animacao = 0
            player.sprite += 1
            if player.sprite >= 3:
                player.sprite = 0
    else:
        player.sprite = 0

    player.x = mapa.resolver_colisao_x(player.rect, dx)
    player.y = mapa.resolver_colisao_y(player.rect, dy)
    player.x = max(0, min(player.x, LARGURA - player.tamanho))
    player.y = max(0, min(player.y, ALTURA  - player.tamanho))
    player.rect.x = player.x
    player.rect.y = player.y

    # --- Coleta de itens do mapa (2 = item normal, 3 = power-up / arma) ---
    coletado = mapa.coletar(player.x, player.y)
    if coletado == 3:
        pickup_sound.play()
        player.pegar_arma()
    # coletado == 2 pode futuramente somar pontos, aumentar velocidade, etc.

    # --- Projéteis ---
    for projetil in player.projeteis[:]:
        projetil.mover()

        if (
            projetil.x < -100 or projetil.x > LARGURA + 100 or
            projetil.y < -100 or projetil.y > ALTURA  + 100
        ):
            if projetil in player.projeteis:
                player.projeteis.remove(projetil)
            continue

        if mapa.colide_parede(projetil.rect):
            if projetil in player.projeteis:
                player.projeteis.remove(projetil)
            continue

        for fantasma in fantasmas:
            if not fantasma.vivo:
                continue
            if projetil.rect.colliderect(fantasma.rect):
                death_sound = random.choice(death_sounds)
                death_sound.play()
                fantasma.morrer()
                if projetil.arma == "ak":
                    if projetil in player.projeteis:
                        player.projeteis.remove(projetil)
                elif projetil.arma == "bazuca":
                    explosao_sound.play()
                    explosoes.append(Explosao(projetil.x, projetil.y, sprites_explosao))
                    if projetil in player.projeteis:
                        player.projeteis.remove(projetil)

    # --- Explosões ---
    for explosao in explosoes[:]:
        explosao.atualizar()
        for fantasma in fantasmas:
            if fantasma.vivo:
                if explosao.rect.colliderect(fantasma.rect):
                    death_sound = random.choice(death_sounds)
                    death_sound.play()
                    fantasma.morrer()
        if explosao.finalizada:
            explosoes.remove(explosao)

    # --- Desenho ---
    TELA.fill((0, 0, 0))
    mapa.desenhar(TELA)

    for fantasma in fantasmas:
        fantasma.mover(player, LARGURA, ALTURA)
        fantasma.desenhar(TELA)
        if fantasma.vivo:
            if player.rect.colliderect(fantasma.rect):
                rodando = False

    for explosao in explosoes:
        explosao.desenhar(TELA)

    player.desenhar(TELA)
    pygame.display.update()

pygame.quit()