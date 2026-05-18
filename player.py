import pygame
class player:
    def __init__(self, largura, altura):
        self.tamanho = 32

        self.x = largura // 2 - self.tamanho // 2
        self.y = altura // 2 - self.tamanho // 2
        self.velocidade = 4

        self.direcao = 'direita'
        self.sprite = 0
        self.contador_animacao = 0

        #aqui a gente coloca os sprites
        self.sprites = [ 
                pygame.image.load('assets/PacManAssets-PacMan_0_0.png'),
                pygame.image.load('assets/PacManAssets-PacMan_0_1.png'),
                pygame.image.load('assets/PacManAssets-PacMan_0_2.png')
            ]
    def mover(self, largura, altura):
        keys = pygame.key.get_pressed()
        movendo = False
        if keys[pygame.K_LEFT]:
            self.x -= self.velocidade
            self.direcao = 'esquerda'
            movendo = True
        
        elif keys[pygame.K_RIGHT]:
            self.x += self.velocidade
            self.direcao = 'direita'
            movendo = True
        
        elif keys[pygame.K_UP]:
            self.y -= self.velocidade
            self.direcao = 'cima'
            movendo = True
        
        elif keys[pygame.K_DOWN]:
            self.y += self.velocidade
            self.direcao = 'baixo'
            movendo = True
        
        #Aqui a gente faz a animação do personagem
        if movendo == True:
            self.contador_animacao += 1
            if self.contador_animacao >= 10:
                self.contador_animacao = 0
                self.sprite += 1
                if self.sprite >= 3:
                    self.sprite = 0
        else:
            self.sprite = 0
        
        if self.x < 0:
            self.x = 0
        elif self.x > largura - self.tamanho:
            self.x = largura - self.tamanho
        
        if self.y < 0:
            self.y = 0
        elif self.y > altura - self.tamanho:
            self.y = altura - self.tamanho
    
       
    def desenhar(self, tela):
        sprite = self.sprites[self.sprite]
        #Aqui o sprite roda conforme a direção
        if self.direcao == 'esquerda':
            sprite = pygame.transform.rotate(sprite, 180)
        elif self.direcao == 'cima':
            sprite = pygame.transform.rotate(sprite, 90)
        elif self.direcao == 'baixo':
            sprite = pygame.transform.rotate(sprite, -90)
        
        #desenha o sprite na tela
        tela.blit(sprite, (self.x, self.y))
