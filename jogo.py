import pygame
import random

from player import player
from fantasma import Fantasma
from explosao import Explosao
from mapa import Mapa
from hud import HUD

pygame.init()
pygame.mixer.init()

LARGURA     = 960
ALTURA_MAPA = 704
ALTURA_UI   =  96
ALTURA      = ALTURA_MAPA + ALTURA_UI

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("PAK47-MAN")

clock = pygame.time.Clock()

hud   = HUD()


explosao_sound = pygame.mixer.Sound("assets/som/roblox-explosion-sound_HNC20s9c.mp3")
pickup_sound   = pygame.mixer.Sound("assets/som/Shotgun_Pump.wav")
pickup_sound.set_volume(0.4)

death_sounds = [
    pygame.mixer.Sound("assets/som/lego-yoda-death-sound-effect.mp3"),
    pygame.mixer.Sound("assets/som/Oswald_Attract.wav"),
    pygame.mixer.Sound("assets/som/026_abnormality_dead_a_v1.wav"),
    pygame.mixer.Sound("assets/som/Dead.wav"),
    pygame.mixer.Sound("assets/som/tmp_7901-951678082.mp3"),
]
for sound in death_sounds:
    sound.set_volume(0.6)

victory_sound = pygame.mixer.Sound("assets/som/final-fantasy-vii-victory-fanfare-1.mp3")
spritesheet_explosao = pygame.image.load(
    "assets/guns/clipart2508851.png"
).convert_alpha()
game_over_sound = pygame.mixer.Sound("assets/som/1.41 Toby Fox - DELTARUNE Chapter 2 OST - 41 Dialtone.mp3")
game_over_sound.set_volume(0.6)
largura_sprite = 480 // 5
altura_sprite  = 280 // 3

sprites_explosao = []
for linha in range(3):
    for coluna in range(5):
        sprite = spritesheet_explosao.subsurface(
            coluna * largura_sprite,
            linha  * altura_sprite,
            largura_sprite,
            altura_sprite
        )
        sprite = pygame.transform.scale(sprite, (96, 96))
        sprites_explosao.append(sprite)

bgm = pygame.mixer.Sound("assets/som/Malkuth Battle Theme 3.wav")
bgm.set_volume(0.5)

def iniciar_jogo():
    global mapa, player_obj, fantasmas, explosoes

    mapa      = Mapa()
    player_obj = player(LARGURA, ALTURA_MAPA)
    explosoes  = []

    fantasmas = [
        Fantasma(13 * 32, 10 * 32, "blinky", 13 * 32, 10 * 32,     0),
        Fantasma(14 * 32, 10 * 32,  "pinky", 14 * 32, 10 * 32,  4000),
        Fantasma(15 * 32, 10 * 32,   "inky", 15 * 32, 10 * 32,  8000),
        Fantasma(16 * 32, 10 * 32,  "clyde", 16 * 32, 10 * 32, 12000),
    ]

menu_song = pygame.mixer.Sound("assets/som/Theme 03.wav")
menu_song.set_volume(1.5)
menu_song.play(-1)  # toca a música do menu em loop
estado = "inicio"

iniciar_jogo()

rodando = True

while rodando:

    clock.tick(60)

    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:

            
            if event.key == pygame.K_RETURN:
                if estado == "inicio":
                    estado = "jogando"
                    menu_song.stop()
                    game_over_sound.stop()  # para o som de game over caso esteja tocando
                    victory_sound.stop()
                    bgm.play(-1)  # toca a música de fundo em loop
                elif estado in ("game_over", "vitoria"):
                    iniciar_jogo()
                    estado = "jogando"
                    game_over_sound.stop()  # para o som de game over caso esteja tocando
                    victory_sound.stop()
                    bgm.play(-1)

            
            if event.key == pygame.K_ESCAPE:
                if estado in ("game_over", "vitoria"):
                    rodando = False

            
            if event.key == pygame.K_z:
                if estado == "jogando" and not player_obj.morrendo:
                    player_obj.atirar()

    
    if estado == "jogando":
        game_over_sound.stop()  # para o som de game over caso esteja tocando
        if player_obj.morrendo:
            terminou = player_obj.atualizar_morte()

            if terminou and player_obj.vidas <= 0:
                estado = "game_over"
                bgm.stop()
                victory_sound.stop()
                game_over_sound.play()

        else:
            player_obj.mover(mapa)
            coletado = mapa.coletar(
                player_obj.hitbox.centerx,
                player_obj.hitbox.centery
            )

            if coletado == 2:
                player_obj.pontos += 10

            elif coletado == 3:
                player_obj.pontos += 50
                pickup_sound.play()
                player_obj.pegar_arma()

            if coletado != 0 and mapa.completo():
                estado = "vitoria"
                bgm.stop()
                game_over_sound.stop()
                victory_sound.play()

            
            for projetil in player_obj.projeteis[:]:

                projetil.mover()

                if (
                    projetil.x < -100 or
                    projetil.x > LARGURA + 100 or
                    projetil.y < -100 or
                    projetil.y > ALTURA_MAPA + 100
                ):
                    if projetil in player_obj.projeteis:
                        player_obj.projeteis.remove(projetil)
                    continue

                if mapa.colide_parede(projetil.rect):

                    if projetil.arma == "bazuca":
                        explosao_sound.play()
                        explosoes.append(
                            Explosao(projetil.x, projetil.y, sprites_explosao)
                        )

                    if projetil.arma != "sniper":   # sniper atravessa paredes
                        if projetil in player_obj.projeteis:
                            player_obj.projeteis.remove(projetil)

                    continue

                for fantasma in fantasmas:

                    if not fantasma.vivo:
                        continue

                    if projetil.rect.colliderect(fantasma.hitbox):

                        random.choice(death_sounds).play()
                        fantasma.morrer()

                        if projetil.arma == "ak":
                            if projetil in player_obj.projeteis:
                                player_obj.projeteis.remove(projetil)

                        elif projetil.arma == "bazuca":
                            explosao_sound.play()
                            explosoes.append(
                                Explosao(projetil.x, projetil.y, sprites_explosao)
                            )
                            if projetil in player_obj.projeteis:
                                player_obj.projeteis.remove(projetil)

                        elif projetil.arma == "sniper":
                            pass   # sniper não é removida ao acertar fantasma

            
            for explosao in explosoes[:]:

                explosao.atualizar()

                for fantasma in fantasmas:
                    if fantasma.vivo:
                        if explosao.rect.colliderect(fantasma.hitbox):
                            random.choice(death_sounds).play()
                            fantasma.morrer()

                if explosao.finalizada:
                    explosoes.remove(explosao)

            
            for fantasma in fantasmas:

                fantasma.mover(player_obj, mapa, LARGURA, ALTURA_MAPA)

                if fantasma.vivo and fantasma.liberado:
                    if player_obj.hitbox.colliderect(fantasma.hitbox):
                        if not player_obj.morrendo:
                            player_obj.iniciar_morte()

    
    if estado == "inicio":

        hud.desenhar_inicio(TELA)

    else:
        
        TELA.fill((15, 15, 15))
        pygame.draw.rect(TELA, (0, 0, 0), (0, 0, LARGURA, ALTURA_MAPA))

        mapa.desenhar(TELA)

        for fantasma in fantasmas:
            fantasma.desenhar(TELA)

        for explosao in explosoes:
            explosao.desenhar(TELA)

        player_obj.desenhar(TELA)

        
        hud.desenhar_ui(
            TELA,
            player_obj.pontos,
            player_obj.arma,
            player_obj.vidas
        )

        
        if estado == "game_over":
            game_over_sound.play()
            hud.desenhar_game_over(TELA, player_obj.pontos)
            



        elif estado == "vitoria":
            hud.desenhar_vitoria(TELA, player_obj.pontos)
            

    pygame.display.update()

pygame.quit()
