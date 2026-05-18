import pygame
from player import player

pygame.init()

LARGURA = 800
ALTURA = 600

TELA = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption("Pac-Man")

clock = pygame.time.Clock()


player = player(LARGURA, ALTURA)


rodando = True

while rodando:

    clock.tick(60)

    # Eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

 
    player.mover(LARGURA, ALTURA)


    TELA.fill((0, 0, 0))

    player.desenhar(TELA)

    pygame.display.update()

pygame.quit()