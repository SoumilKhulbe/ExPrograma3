import pygame
import random

from player import player
from fantasma import Fantasma
from explosao import Explosao
from mapa import Mapa

pygame.init()
pygame.mixer.init()

LARGURA = 960

ALTURA_MAPA = 704
ALTURA_UI = 96

ALTURA = ALTURA_MAPA + ALTURA_UI

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pac-Man")

clock = pygame.time.Clock()

fonte = pygame.font.SysFont("arial", 32)

mapa = Mapa()

player = player(LARGURA, ALTURA_MAPA)

explosao_sound = pygame.mixer.Sound(
    "assets/som/roblox-explosion-sound_HNC20s9c.mp3"
)

pickup_sound = pygame.mixer.Sound(
    "assets/som/Shotgun_Pump.wav"
)

pickup_sound.set_volume(0.4)

death_sounds = [

    pygame.mixer.Sound(
        "assets/som/lego-yoda-death-sound-effect.mp3"
    ),

    pygame.mixer.Sound(
        "assets/som/Oswald_Attract.wav"
    ),

    pygame.mixer.Sound(
        "assets/som/026_abnormality_dead_a_v1.wav"
    ),

    pygame.mixer.Sound(
        "assets/som/Dead.wav"
    )
]

for sound in death_sounds:
    sound.set_volume(0.6)

fantasmas = [

    Fantasma(
        13 * 32,
        10 * 32,
        "blinky",
        13 * 32,
        10 * 32,
        0
    ),

    Fantasma(
        14 * 32,
        10 * 32,
        "pinky",
        14 * 32,
        10 * 32,
        4000
    ),

    Fantasma(
        15 * 32,
        10 * 32,
        "inky",
        15 * 32,
        10 * 32,
        8000
    ),

    Fantasma(
        16 * 32,
        10 * 32,
        "clyde",
        16 * 32,
        10 * 32,
        12000
    )
]

explosoes = []

sprites_explosao = []

spritesheet_explosao = pygame.image.load(
    "assets/guns/clipart2508851.png"
).convert_alpha()

largura_sprite = 480 // 5
altura_sprite = 280 // 3

for linha in range(3):

    for coluna in range(5):

        sprite = spritesheet_explosao.subsurface(

            coluna * largura_sprite,
            linha * altura_sprite,

            largura_sprite,
            altura_sprite
        )

        sprite = pygame.transform.scale(
            sprite,
            (96, 96)
        )

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

    player.mover(mapa)

    coletado = mapa.coletar(

        player.hitbox.centerx,
        player.hitbox.centery
    )

    if coletado == 2:
        player.pontos += 10

    elif coletado == 3:

        player.pontos += 50

        pickup_sound.play()

        player.pegar_arma()

    for projetil in player.projeteis[:]:

        projetil.mover()

        if (

            projetil.x < -100 or
            projetil.x > LARGURA + 100 or

            projetil.y < -100 or
            projetil.y > ALTURA_MAPA + 100
        ):

            if projetil in player.projeteis:
                player.projeteis.remove(projetil)

            continue

        if mapa.colide_parede(projetil.rect):

            if projetil.arma == "bazuca":

                explosao_sound.play()

                explosoes.append(

                    Explosao(

                        projetil.x,
                        projetil.y,

                        sprites_explosao
                    )
                )

            if projetil.arma != "sniper":

                if projetil in player.projeteis:
                    player.projeteis.remove(projetil)

            continue

        for fantasma in fantasmas:

            if fantasma.vivo == False:
                continue

            if projetil.rect.colliderect(fantasma.hitbox):

                death_sound = random.choice(
                    death_sounds
                )

                death_sound.play()

                fantasma.morrer()

                if projetil.arma == "ak":

                    if projetil in player.projeteis:
                        player.projeteis.remove(projetil)

                elif projetil.arma == "bazuca":

                    explosao_sound.play()

                    explosoes.append(

                        Explosao(

                            projetil.x,
                            projetil.y,

                            sprites_explosao
                        )
                    )

                    if projetil in player.projeteis:
                        player.projeteis.remove(projetil)

                elif projetil.arma == "sniper":

                    pass

    for explosao in explosoes[:]:

        explosao.atualizar()

        for fantasma in fantasmas:

            if fantasma.vivo:

                if explosao.rect.colliderect(
                    fantasma.hitbox
                ):

                    death_sound = random.choice(
                        death_sounds
                    )

                    death_sound.play()

                    fantasma.morrer()

        if explosao.finalizada:
            explosoes.remove(explosao)

    TELA.fill((15, 15, 15))

    pygame.draw.rect(
        TELA,
        (0, 0, 0),
        (0, 0, LARGURA, ALTURA_MAPA)
    )

    mapa.desenhar(TELA)

    for fantasma in fantasmas:

        fantasma.mover(
            player,
            mapa,
            LARGURA,
            ALTURA_MAPA
        )

        fantasma.desenhar(TELA)

        if fantasma.vivo:

            if player.hitbox.colliderect(
                fantasma.hitbox
            ):

                rodando = False

    for explosao in explosoes:
        explosao.desenhar(TELA)

    player.desenhar(TELA)

    pygame.draw.rect(
        TELA,
        (25, 25, 25),
        (0, ALTURA_MAPA, LARGURA, ALTURA_UI)
    )

    texto_pontos = fonte.render(
        f"PONTOS: {player.pontos}",
        True,
        (255, 255, 255)
    )

    TELA.blit(
        texto_pontos,
        (20, ALTURA_MAPA + 25)
    )

    texto_arma = fonte.render(
        f"ARMA: {player.arma}",
        True,
        (255, 255, 0)
    )

    TELA.blit(
        texto_arma,
        (350, ALTURA_MAPA + 25)
    )

    pygame.display.update()

pygame.quit()