import pygame
import random
import math

class Fantasma:
    def __init__(self, x, y, tipo, spawn_x, spawn_y):

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
            16,
            16
        )

        # sprites
        self.sprites = {
            "blinky": [pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_0_0.png"), pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_0_1.png"), pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_0_2.png"), pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_0_3.png")],
            "pinky": [pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_1_0.png"), pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_1_1.png"), pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_1_2.png"), pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_1_3.png")],
            "inky": [pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_2_0.png"), pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_2_1.png"), pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_2_2.png"), pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_2_3.png")],
            "clyde": [pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_3_0.png"), pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_3_1.png"), pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_3_2.png"), pygame.image.load("assets/PacManAssets-Ghosts/PacManAssets-Ghosts_3_3.png")]
        }
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y

        self.vivo = True

        self.tempo_respawn = 0
        self.direcao_pinky = "horizontal"

        self.tempo_decisao = 0
        
        self.modo = "ativo"

        self.tempo_modo = pygame.time.get_ticks()

        self.alvos_descanso = {

            "blinky": (750, 50),

            "pinky": (50, 50),

            "inky": (50, 550),

            "clyde": (750, 550)
        }
    def mover(self, jogador, largura, altura):
        if self.vivo == False:

            agora = pygame.time.get_ticks()

            if agora - self.tempo_morte >= 3000:

                self.vivo = True

                self.x = self.spawn_x
                self.y = self.spawn_y

            return
        if self.modo == "descanso":

            alvo_x, alvo_y = self.alvos_descanso[self.tipo]

            if alvo_x > self.x:
                self.x += self.velocidade

            elif alvo_x < self.x:
                self.x -= self.velocidade

            if alvo_y > self.y:
                self.y += self.velocidade

            elif alvo_y < self.y:
                self.y -= self.velocidade


        elif self.tipo == "blinky":
            if jogador.x > self.x:
                self.x += self.velocidade

            elif jogador.x < self.x:
                self.x -= self.velocidade

            if jogador.y > self.y:
                self.y += self.velocidade

            elif jogador.y < self.y:
                self.y -= self.velocidade


        elif self.tipo == "pinky":

            alvo_x = jogador.x
            alvo_y = jogador.y

            if jogador.direcao == "direita":
                alvo_x += 80

            elif jogador.direcao == "esquerda":
                alvo_x -= 80

            elif jogador.direcao == "cima":
                alvo_y -= 80

            elif jogador.direcao == "baixo":
                alvo_y += 80

            dx = alvo_x - self.x
            dy = alvo_y - self.y

            agora = pygame.time.get_ticks()

            if agora - self.tempo_decisao > 300:

                self.tempo_decisao = agora

                if abs(dx) > abs(dy):

                    self.direcao_pinky = "horizontal"

                else:

                    self.direcao_pinky = "vertical"

            if self.direcao_pinky == "horizontal":

                if abs(dx) > 10:

                    if dx > 0:
                        self.x += self.velocidade

                    else:
                        self.x -= self.velocidade

            else:

                if abs(dy) > 10:

                    if dy > 0:
                        self.y += self.velocidade

                    else:
                        self.y -= self.velocidade
        elif self.tipo == "inky":

            self.x += random.randint(-2, 2)
            self.y += random.randint(-2, 2)


        elif self.tipo == "clyde":

            distancia = math.sqrt(
                (jogador.x - self.x) ** 2 +
                (jogador.y - self.y) ** 2
            )

            if distancia < 120:
                self.modo = "descanso"
                alvo_x, alvo_y = self.alvos_descanso["clyde"]

                if alvo_x > self.x:
                    self.x += self.velocidade

                elif alvo_x < self.x:
                    self.x -= self.velocidade

                if alvo_y > self.y:
                    self.y += self.velocidade

                elif alvo_y < self.y:
                    self.y -= self.velocidade
            else:

                if jogador.x > self.x:
                    self.x += self.velocidade

                elif jogador.x < self.x:
                    self.x -= self.velocidade

                if jogador.y > self.y:
                    self.y += self.velocidade

                elif jogador.y < self.y:
                    self.y -= self.velocidade

        # LIMITES DA TELA

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

            tempo = pygame.time.get_ticks()

            for i in range(25):

                if (tempo // 100 + i) % 2 == 0:

                    pixel_x = self.spawn_x + random.randint(-24, 24)

                    pixel_y = self.spawn_y + random.randint(-24, 24)

                    tamanho = random.randint(2, 5)

                    superficie = pygame.Surface(

                        (tamanho, tamanho),

                        pygame.SRCALPHA
                    )

                    pygame.draw.rect(

                        superficie,

                        (255, 0, 0, 140),

                        (0, 0, tamanho, tamanho)
                    )

                    tela.blit(
                        superficie,
                        (pixel_x, pixel_y)
                    )

            return
        agora = pygame.time.get_ticks()

        if self.modo == "ativo":

            troca = 20000

        else:

            troca = 4000

        if agora - self.tempo_modo >= troca:

            self.tempo_modo = agora

            if self.modo == "ativo":

                self.modo = "descanso"

            else:

                self.modo = "ativo"
                self.contador_animacao += 1

                if self.contador_animacao >= 10:
                    self.contador_animacao = 0

            self.frame += 1

            if self.frame >= len(self.sprites[self.tipo]):
                self.frame = 0

        sprite = self.sprites[self.tipo][self.frame]

        tela.blit(sprite, (self.x, self.y))