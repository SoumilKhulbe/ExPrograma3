import pygame
from player import player

pygame.init()

LARGURA = 800
ALTURA = 600

TELA = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption("Pac-Man")

clock = pygame.time.Clock()

spritesheet_items = pygame.image.load('assets/PacManAssets-Items/PacManAssets-Items_0_0.png')
super_ponto_sprite = spritesheet_items.subsurface((16, 16, 16, 16))
player = player(LARGURA, ALTURA)

super_pontos = [
    pygame.Rect(100, 100, 16, 16),
    pygame.Rect(700, 100, 16, 16),
    pygame.Rect(100, 500, 16, 16),
    pygame.Rect(700, 500, 16, 16)
]

rodando = True

while rodando:

    clock.tick(60)

    # Eventos
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                player.atirar()
 
    player.mover(LARGURA, ALTURA)

    for super_ponto in super_pontos:
        if player.rect.colliderect(super_ponto):
            super_pontos.remove(super_ponto)
            player.pegar_arma()

    TELA.fill((0, 0, 0))

    for super_ponto in super_pontos:
        TELA.blit(super_ponto_sprite, (super_ponto.x, super_ponto.y))

    player.desenhar(TELA)

    pygame.display.update()

pygame.quit()