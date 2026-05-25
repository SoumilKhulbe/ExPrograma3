import pygame

TILE = 32

# Mapa 30 colunas x 22 linhas = 960x704 pixels (tamanho exato da tela)
#
# Valores de cada célula:
#   0 = caminho livre (sem item)
#   1 = parede
#   2 = item normal  (bolinha — coletável, sem efeito especial)
#   3 = power-up     (super ponto — dá arma ao player)

LAYOUT = [

    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

    [1,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,1],

    [1,2,1,1,2,1,1,2,1,1,2,1,1,2,2,1,1,2,1,1,2,1,1,2,1,1,2,1,2,1],

    [1,2,1,1,2,1,1,2,1,1,2,1,1,2,2,1,1,2,1,1,2,1,1,2,1,1,2,1,2,1],

    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],

    [1,2,1,1,2,1,2,1,1,2,1,1,2,1,1,2,1,1,2,1,1,2,1,1,2,1,2,1,2,1],

    [1,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,1],

    [1,1,1,1,2,1,1,1,2,1,2,1,1,0,0,0,1,1,2,1,2,1,1,1,2,1,1,1,1,1],

    [1,2,2,2,2,2,2,1,2,1,2,2,2,0,0,0,2,2,2,1,2,1,2,2,2,2,2,2,2,1],

    [1,2,1,1,2,1,2,1,2,1,1,1,2,0,0,0,2,1,1,1,2,1,2,1,2,1,1,2,2,1],

    [0,0,0,0,2,1,2,2,2,2,2,2,2,0,0,0,2,2,2,2,2,2,2,1,2,0,0,0,0,0],

    [1,1,1,1,2,1,1,1,2,1,1,1,2,2,2,2,2,1,1,1,2,1,1,1,2,1,1,1,1,1],

    [1,2,2,2,2,2,2,1,2,2,2,2,2,1,1,1,2,2,2,2,2,1,2,2,2,2,2,2,2,1],

    [1,2,1,1,2,1,2,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,2,1,2,1,1,2,2,1],

    [1,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,1],

    [1,2,1,1,2,1,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,1,1,2,1,1,1,2,1],

    [1,3,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,3,1],

    [1,1,1,1,2,1,1,1,2,1,2,1,1,1,1,1,1,1,2,1,2,1,1,1,2,1,1,1,1,1],

    [1,2,2,2,2,2,2,1,2,1,2,2,2,2,2,2,2,2,2,1,2,1,2,2,2,2,2,2,2,1],

    [1,2,1,1,2,1,2,1,2,1,1,1,2,1,1,2,1,1,1,1,2,1,2,1,2,1,1,1,2,1],

    [1,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,1],

    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

COR_PAREDE = (0, 0, 180)
COR_BORDA  = (30, 30, 220)
COR_ITEM   = (255, 230, 150)
COR_POWER  = (255, 80,  200)


class Mapa:
    def __init__(self):
        
        self.grade = [linha[:] for linha in LAYOUT]

        self.linhas  = len(self.grade)
        self.colunas = len(self.grade[0])

        
        self.paredes = []
        for li in range(self.linhas):
            for co in range(self.colunas):
                if self.grade[li][co] == 1:
                    self.paredes.append(
                        pygame.Rect(co * TILE, li * TILE, TILE, TILE)
                    )

    # ------------------------------------------------------------------ colisão
    def destruir_parede(self, x, y):

        col = x // TILE
        lin = y // TILE

        if 0 <= lin < self.linhas and 0 <= col < self.colunas:

            if self.grade[lin][col] == 1:

                self.grade[lin][col] = 0

                self.paredes = []

                for li in range(self.linhas):

                    for co in range(self.colunas):

                        if self.grade[li][co] == 1:

                            self.paredes.append(

                                pygame.Rect(
                                    co * TILE,
                                    li * TILE,
                                    TILE,
                                    TILE
                                )
                            )
    def resolver_colisao_x(self, entidade_rect, dx):
        entidade_rect.x += dx
        for parede in self.paredes:
            if entidade_rect.colliderect(parede):
                if dx > 0:
                    entidade_rect.right = parede.left
                elif dx < 0:
                    entidade_rect.left  = parede.right
        return entidade_rect.x

    def resolver_colisao_y(self, entidade_rect, dy):
        entidade_rect.y += dy
        for parede in self.paredes:
            if entidade_rect.colliderect(parede):
                if dy > 0:
                    entidade_rect.bottom = parede.top
                elif dy < 0:
                    entidade_rect.top    = parede.bottom
        return entidade_rect.y

    def colide_parede(self, rect):

        hitbox = rect.inflate(-4, -4)

        for parede in self.paredes:

            if hitbox.colliderect(parede):
                return True

        return False

    # ------------------------------------------------------------------ coleta

    def coletar(self, px, py):
        """
        Recebe a posição em pixels do player, converte para tile e
        verifica se há item (2) ou power-up (3) nessa célula.

        Retorna:
          2  →  item normal coletado
          3  →  power-up coletado (deve dar arma ao player)
          0  →  nada para coletar
        """
        col = px // TILE
        lin = py // TILE

        if 0 <= lin < self.linhas and 0 <= col < self.colunas:
            valor = self.grade[lin][col]
            if valor in (2, 3):
                self.grade[lin][col] = 0   # remove o item do mapa
                return valor

        return 0

    # ------------------------------------------------------------------ desenho

    def desenhar(self, tela):
        for li in range(self.linhas):
            for co in range(self.colunas):
                valor = self.grade[li][co]
                x = co * TILE
                y = li * TILE

                if valor == 1:
                    pygame.draw.rect(tela, COR_PAREDE, (x, y, TILE, TILE))
                    pygame.draw.rect(tela, COR_BORDA,  (x, y, TILE, TILE), 2)

                elif valor == 2:
                    cx = x + TILE // 2
                    cy = y + TILE // 2
                    pygame.draw.circle(tela, COR_ITEM, (cx, cy), 4)

                elif valor == 3:
                    cx = x + TILE // 2
                    cy = y + TILE // 2
                    pygame.draw.circle(tela, COR_POWER, (cx, cy), 9)
                    pygame.draw.circle(tela, (255,255,255), (cx, cy), 9, 2)