import pygame

from player import player
from fantasma import Fantasma
from explosao import Explosao

pygame.init()
pygame.mixer.init()
LARGURA = 800
ALTURA = 600

TELA = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption("Pac-Man")

clock = pygame.time.Clock()

player = player(LARGURA, ALTURA)
explosao_sound = pygame.mixer.Sound("assets/som/roblox-explosion-sound_HNC20s9c.mp3")
ak_sound = pygame.mixer.Sound("assets/som/Gun_2.wav")
pickup_sound = pygame.mixer.Sound("assets/som/Shotgun_Pump.wav")
pickup_sound.set_volume(0.4)
spritesheet_items = pygame.image.load(
    'assets/PacManAssets-Items/PacManAssets-Items_0_0.png'
).convert_alpha()

super_ponto_sprite = spritesheet_items.subsurface(
    (16, 16, 16, 16)
)

super_pontos = [

    pygame.Rect(100, 100, 16, 16),
    pygame.Rect(700, 100, 16, 16),
    pygame.Rect(100, 500, 16, 16),
    pygame.Rect(700, 500, 16, 16)

]

fantasmas = [

    Fantasma(100, 100, "blinky"),
    Fantasma(200, 100, "pinky"),
    Fantasma(300, 100, "inky"),
    Fantasma(400, 100, "clyde")

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

    player.mover(LARGURA, ALTURA)

    for super_ponto in super_pontos[:]:

        if player.rect.colliderect(super_ponto):

            super_pontos.remove(super_ponto)

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

        for fantasma in fantasmas:

            if fantasma.vivo == False:
                continue

            if projetil.rect.colliderect(fantasma.rect):

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

    for explosao in explosoes[:]:

        explosao.atualizar()

        for fantasma in fantasmas:

            if fantasma.vivo:

                if explosao.rect.colliderect(fantasma.rect):

                    fantasma.morrer()

        if explosao.finalizada:

            explosoes.remove(explosao)

    TELA.fill((0, 0, 0))

    for super_ponto in super_pontos:

        TELA.blit(
            super_ponto_sprite,
            (super_ponto.x, super_ponto.y)
        )

    for fantasma in fantasmas:

        fantasma.mover(player, LARGURA, ALTURA)

        if fantasma.vivo:

            fantasma.desenhar(TELA)

            if player.rect.colliderect(fantasma.rect):

                pygame.quit()

    for explosao in explosoes:

        explosao.desenhar(TELA)

    player.desenhar(TELA)

    pygame.display.update()

pygame.quit()