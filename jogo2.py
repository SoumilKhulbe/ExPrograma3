import pygame
import random

from player import player
from fantasma import Fantasma
from explosao import Explosao
from mapa import Mapa

pygame.init()
pygame.mixer.init()

LARGURA = 960
ALTURA = 704

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pac-Man")

clock = pygame.time.Clock()

mapa = Mapa()

player = player(LARGURA, ALTURA)

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

        player.rect.centerx,
        player.rect.centery
    )

    if coletado == 3:

        pickup_sound.play()

        player.pegar_arma()

    for projetil in player.projeteis[:]:

        projetil.mover()

        if (

            projetil.x < -100 or
            projetil.x > LARGURA + 100 or

            projetil.y < -100 or
            projetil.y > ALTURA + 100
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

                mapa.destruir_parede(

                    projetil.rect.centerx,
                    projetil.rect.centery
                )

            if projetil.arma != "sniper":

                if projetil in player.projeteis:
                    player.projeteis.remove(projetil)

            continue

        for fantasma in fantasmas:

            if fantasma.vivo == False:
                continue

            if projetil.rect.colliderect(fantasma.rect):

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
                    fantasma.rect
                ):

                    death_sound = random.choice(
                        death_sounds
                    )

                    death_sound.play()

                    fantasma.morrer()

        if explosao.finalizada:
            explosoes.remove(explosao)

    TELA.fill((0, 0, 0))

    mapa.desenhar(TELA)

    for fantasma in fantasmas:

        fantasma.mover(
            player,
            mapa,
            LARGURA,
            ALTURA
        )

        fantasma.desenhar(TELA)

        if fantasma.vivo:

            if player.rect.colliderect(
                fantasma.rect
            ):

                rodando = False

    for explosao in explosoes:
        explosao.desenhar(TELA)

    player.desenhar(TELA)

    pygame.display.update()

pygame.quit()