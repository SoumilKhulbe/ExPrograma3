import pygame

class Explosao:

    def __init__(self, x, y, sprites):

        self.x = x
        self.y = y

        self.sprites = sprites

        self.frame = 0

        self.contador = 0

        self.finalizada = False

        self.rect = pygame.Rect(

            self.x - 48,
            self.y - 48,

            96,
            96
        )

    def atualizar(self):

        self.contador += 1

        if self.contador >= 3:

            self.contador = 0

            self.frame += 1

            if self.frame >= len(self.sprites):

                self.finalizada = True

    def desenhar(self, tela):

        tela.blit(

            self.sprites[self.frame],

            (
                self.x - 48,
                self.y - 48
            )
        )