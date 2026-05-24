import random
from projetil import Projetil
import pygame

pygame.mixer.init()

TILE = 32

class player:

    def __init__(self, largura, altura):

        self.tamanho = 32

        self.x = 32 * 14
        self.y = 32 * 16

        self.velocidade = 2

        self.direcao = "esquerda"
        self.proxima_direcao = "esquerda"

        self.sprite = 0
        self.contador_animacao = 0

        self.arma = None

        self.armas = ["sniper", "ak", "bazuca"]

        self.sprites_armas = {

            "sniper": pygame.image.load(
                'assets/guns/Sniper-rifle-3-scoped.png'
            ),

            "ak": pygame.image.load(
                'assets/guns/Assaut-rifle-1.png'
            ),

            "bazuca": pygame.image.load(
                'assets/guns/RPG-reisized.png'
            )
        }

        self.sprites_projetil = {

            "sniper": pygame.image.load(
                'assets/guns/p_sniper.png'
            ),

            "ak": pygame.image.load(
                'assets/guns/p_ak.png'
            ),

            "bazuca": pygame.image.load(
                'assets/guns/AmoB1.png'
            )
        }

        self.projeteis = []

        self.rect = pygame.Rect(
            self.x,
            self.y,
            32,
            32
        )
        self.sprites = [

            pygame.image.load(
                'assets/PacManAssets-PacMan_0_0.png'
            ),

            pygame.image.load(
                'assets/PacManAssets-PacMan_0_1.png'
            ),

            pygame.image.load(
                'assets/PacManAssets-PacMan_0_2.png'
            )
        ]

    def alinhado_no_tile(self):

        tolerancia = self.velocidade

        alinhado_x = (
            abs((self.rect.centerx % TILE) - TILE // 2)
            <= tolerancia
        )

        alinhado_y = (
            abs((self.rect.centery % TILE) - TILE // 2)
            <= tolerancia
        )

        return alinhado_x and alinhado_y

    def obter_vetor(self, direcao):

        if direcao == "direita":
            return self.velocidade, 0

        elif direcao == "esquerda":
            return -self.velocidade, 0

        elif direcao == "cima":
            return 0, -self.velocidade

        elif direcao == "baixo":
            return 0, self.velocidade

        return 0, 0

    def mover(self, mapa):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.proxima_direcao = "esquerda"

        elif keys[pygame.K_RIGHT]:
            self.proxima_direcao = "direita"

        elif keys[pygame.K_UP]:
            self.proxima_direcao = "cima"

        elif keys[pygame.K_DOWN]:
            self.proxima_direcao = "baixo"

        if self.alinhado_no_tile():

            dx, dy = self.obter_vetor(
                self.proxima_direcao
            )

            teste = self.rect.copy()

            teste.x += dx
            teste.y += dy

            if mapa.colide_parede(teste) == False:

                self.direcao = self.proxima_direcao

        dx, dy = self.obter_vetor(self.direcao)

        teste = self.rect.copy()

        teste.x += dx
        teste.y += dy

        if mapa.colide_parede(teste) == False:

            self.rect.x += dx
            self.rect.y += dy

        self.x = self.rect.x
        self.y = self.rect.y

        if dx != 0 or dy != 0:

            self.contador_animacao += 1

            if self.contador_animacao >= 8:

                self.contador_animacao = 0

                self.sprite += 1

                if self.sprite >= 3:
                    self.sprite = 0

    def pegar_arma(self):

        self.arma = random.choice(self.armas)

    def atirar(self):

        if self.arma is not None:

            tiro_x = self.rect.centerx
            tiro_y = self.rect.centery

            # AJUSTE LATERAL DA BAZUCA
            if self.arma == "bazuca":

                if self.direcao == "direita":
                    tiro_y -= 8

                elif self.direcao == "esquerda":
                    tiro_y -= 8

                elif self.direcao == "cima":
                    tiro_x += 8

                elif self.direcao == "baixo":
                    tiro_x -= 8

            novo_projetil = Projetil(

                tiro_x,
                tiro_y,

                self.direcao,

                self.arma,

                self.sprites_projetil[self.arma]
            )

            self.projeteis.append(novo_projetil)

            self.arma = None

    def desenhar(self, tela):
        pygame.draw.rect(
            tela,
            (0, 255, 0),
            self.rect,
            2
        )
        sprite = self.sprites[self.sprite]

        if self.direcao == 'esquerda':

            sprite = pygame.transform.rotate(
                sprite,
                180
            )

        elif self.direcao == 'cima':

            sprite = pygame.transform.rotate(
                sprite,
                90
            )

        elif self.direcao == 'baixo':

            sprite = pygame.transform.rotate(
                sprite,
                -90
            )

        for projetil in self.projeteis:
            projetil.desenhar(tela)

        tela.blit(sprite, (self.x, self.y))
        if self.arma is not None:

            arma_sprite = self.sprites_armas[self.arma]

            if self.direcao == "esquerda":

                arma_sprite = pygame.transform.rotate(
                    arma_sprite,
                    180
                )

                tela.blit(
                    arma_sprite,
                    (self.x - 32, self.y - 8)
                )

            elif self.direcao == "direita":

                tela.blit(
                    arma_sprite,
                    (self.x + 16, self.y + 8)
                )

            elif self.direcao == "cima":

                arma_sprite = pygame.transform.rotate(
                    arma_sprite,
                    90
                )

                tela.blit(
                    arma_sprite,
                    (self.x + 8, self.y - 32)
                )

            elif self.direcao == "baixo":

                arma_sprite = pygame.transform.rotate(
                    arma_sprite,
                    -90
                )

                tela.blit(
                    arma_sprite,
                    (self.x - 8, self.y + 16)
                )