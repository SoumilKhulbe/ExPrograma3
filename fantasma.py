import pygame
import random
import math

class Fantasma:

    def __init__(self, x, y, tipo, spawn_x, spawn_y, atraso):

        self.x = x
        self.y = y

        self.frame = 0
        self.contador_animacao = 0

        self.tamanho = 32
        self.velocidade = 2

        self.tipo = tipo

        self.rect = pygame.Rect(
            self.x,
            self.y,
            32,
            32
        )

        self.sprites = {

            "blinky": [

                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_0_0.png"),
                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_0_1.png"),
                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_0_2.png"),
                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_0_3.png")
            ],

            "pinky": [

                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_1_0.png"),
                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_1_1.png"),
                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_1_2.png"),
                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_1_3.png")
            ],

            "inky": [

                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_2_0.png"),
                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_2_1.png"),
                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_2_2.png"),
                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_2_3.png")
            ],

            "clyde": [

                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_3_0.png"),
                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_3_1.png"),
                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_3_2.png"),
                pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_3_3.png")
            ]
        }

        self.spawn_x = spawn_x
        self.spawn_y = spawn_y

        self.vivo = True

        self.liberado = False

        self.atraso = atraso

        self.tempo_inicio = pygame.time.get_ticks()

        self.modo = "ativo"

        self.tempo_modo = pygame.time.get_ticks()

        self.alvos_descanso = {

            "blinky": (750, 50),
            "pinky": (50, 50),

            "inky": (50, 550),
            "clyde": (750, 550)
        }

        self.mover_x = self.velocidade
        self.mover_y = 0

    def alinhado_no_tile(self):

        tolerancia = self.velocidade

        alinhado_x = (
            abs((self.rect.centerx % 32) - 16)
            <= tolerancia
        )

        alinhado_y = (
            abs((self.rect.centery % 32) - 16)
            <= tolerancia
        )

        return alinhado_x and alinhado_y

    def escolher_melhor_direcao(self, alvo_x, alvo_y, mapa):

        direcoes = [

            (self.velocidade, 0),
            (-self.velocidade, 0),

            (0, self.velocidade),
            (0, -self.velocidade)
        ]

        melhor_distancia = 999999

        melhor_x = self.mover_x
        melhor_y = self.mover_y

        for dx, dy in direcoes:

            if dx == -self.mover_x and dy == -self.mover_y:
                continue

            teste = self.rect.copy()

            teste.x += dx
            teste.y += dy

            if mapa.colide_parede(teste):
                continue

            distancia = math.sqrt(

                (alvo_x - teste.x) ** 2 +
                (alvo_y - teste.y) ** 2
            )

            if distancia < melhor_distancia:

                melhor_distancia = distancia

                melhor_x = dx
                melhor_y = dy

        return melhor_x, melhor_y

    def mover(self, jogador, mapa, largura, altura):

        if self.vivo == False:

            agora = pygame.time.get_ticks()

            if agora - self.tempo_morte >= 3000:

                self.vivo = True

                self.x = self.spawn_x
                self.y = self.spawn_y

            return

        if self.liberado == False:

            agora = pygame.time.get_ticks()

            if agora - self.tempo_inicio >= self.atraso:

                self.liberado = True

            else:
                return

        agora = pygame.time.get_ticks()

        if self.modo == "ativo":

            self.velocidade = 2

            if agora - self.tempo_modo >= 15000:

                self.modo = "descanso"

                self.tempo_modo = agora

        else:

            self.velocidade = 1

            if agora - self.tempo_modo >= 4000:

                self.modo = "ativo"

                self.tempo_modo = agora

        if self.alinhado_no_tile():

            if self.modo == "descanso":

                alvo_x, alvo_y = self.alvos_descanso[self.tipo]

                if random.randint(0, 10) <= 2:

                    direcoes = [

                        (self.velocidade, 0),
                        (-self.velocidade, 0),

                        (0, self.velocidade),
                        (0, -self.velocidade)
                    ]

                    random.shuffle(direcoes)

                    for dx, dy in direcoes:

                        teste = self.rect.copy()

                        teste.x += dx
                        teste.y += dy

                        if mapa.colide_parede(teste) == False:

                            mover_x = dx
                            mover_y = dy
                            break

                else:

                    mover_x, mover_y = self.escolher_melhor_direcao(
                        alvo_x,
                        alvo_y,
                        mapa
                    )

            else:

                if self.tipo == "blinky":

                    mover_x, mover_y = self.escolher_melhor_direcao(
                        jogador.x,
                        jogador.y,
                        mapa
                    )

                elif self.tipo == "pinky":

                    alvo_x = jogador.x
                    alvo_y = jogador.y

                    frente = 96

                    if jogador.direcao == "direita":
                        alvo_x += frente

                    elif jogador.direcao == "esquerda":
                        alvo_x -= frente

                    elif jogador.direcao == "cima":
                        alvo_y -= frente

                    elif jogador.direcao == "baixo":
                        alvo_y += frente

                    mover_x, mover_y = self.escolher_melhor_direcao(
                        alvo_x,
                        alvo_y,
                        mapa
                    )

                elif self.tipo == "inky":

                    direcoes = [

                        (self.velocidade, 0),
                        (-self.velocidade, 0),

                        (0, self.velocidade),
                        (0, -self.velocidade)
                    ]

                    random.shuffle(direcoes)

                    mover_x = self.mover_x
                    mover_y = self.mover_y

                    for dx, dy in direcoes:

                        teste = self.rect.copy()

                        teste.x += dx
                        teste.y += dy

                        if mapa.colide_parede(teste) == False:

                            mover_x = dx
                            mover_y = dy
                            break

                elif self.tipo == "clyde":

                    distancia = math.sqrt(

                        (jogador.x - self.x) ** 2 +
                        (jogador.y - self.y) ** 2
                    )

                    if distancia < 120:

                        alvo_x, alvo_y = self.alvos_descanso["clyde"]

                    else:

                        alvo_x = jogador.x
                        alvo_y = jogador.y

                    mover_x, mover_y = self.escolher_melhor_direcao(
                        alvo_x,
                        alvo_y,
                        mapa
                    )

            teste = self.rect.copy()

            teste.x += mover_x
            teste.y += mover_y

            if mapa.colide_parede(teste) == False:

                self.mover_x = mover_x
                self.mover_y = mover_y

        teste = self.rect.copy()

        teste.x += self.mover_x
        teste.y += self.mover_y

        if mapa.colide_parede(teste) == False:

            self.x += self.mover_x
            self.y += self.mover_y

        else:

            self.mover_x = 0
            self.mover_y = 0

        if self.x < 0:
            self.x = 0

        elif self.x > largura - self.tamanho:
            self.x = largura - self.tamanho

        if self.y < 0:
            self.y = 0

        elif self.y > altura - self.tamanho:
            self.y = altura - self.tamanho

        self.rect.x = self.x
        self.rect.y = self.y

    def morrer(self):

        self.vivo = False

        self.tempo_morte = pygame.time.get_ticks()

    def desenhar(self, tela):

        if self.vivo == False:
            return

        if self.liberado == False:
            return

        self.contador_animacao += 1

        if self.contador_animacao >= 10:

            self.contador_animacao = 0

            self.frame += 1

            if self.frame >= len(self.sprites[self.tipo]):
                self.frame = 0

        sprite = self.sprites[self.tipo][self.frame]

        tela.blit(sprite, (self.x, self.y))