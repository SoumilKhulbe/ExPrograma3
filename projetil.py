import pygame

class Projetil:

    def __init__(self, x, y, direcao, arma, sprite):

        self.x = x
        self.y = y

        self.direcao = direcao

        self.arma = arma

        self.sprite = sprite

        self.ativo = True

        if arma == "ak":

            self.velocidade = 8
            self.tamanho = 16

        elif arma == "bazuca":

            self.velocidade = 5
            self.tamanho = 32

        elif arma == "sniper":

            self.velocidade = 20
            self.tamanho = 16

        self.rect = pygame.Rect(

            self.x,
            self.y,

            self.tamanho,
            self.tamanho
        )

    def mover(self):

        if self.direcao == "direita":
            self.x += self.velocidade

        elif self.direcao == "esquerda":
            self.x -= self.velocidade

        elif self.direcao == "cima":
            self.y -= self.velocidade

        elif self.direcao == "baixo":
            self.y += self.velocidade

        self.rect.x = self.x
        self.rect.y = self.y

    def desenhar(self, tela):

        sprite = pygame.transform.scale(

            self.sprite,

            (
                self.tamanho,
                self.tamanho
            )
        )

        if self.direcao == "esquerda":

            sprite = pygame.transform.rotate(
                sprite,
                180
            )

        elif self.direcao == "cima":

            sprite = pygame.transform.rotate(
                sprite,
                90
            )

        elif self.direcao == "baixo":

            sprite = pygame.transform.rotate(
                sprite,
                -90
            )

        tela.blit(sprite, (self.x, self.y))