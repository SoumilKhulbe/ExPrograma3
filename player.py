import random
from projetil import Projetil
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
        
        self.arma = None

        self.armas = ["sniper", "ak", "bazuca"]

        self.sprites_armas = {
            "sniper": pygame.image.load('assets/guns/Sniper-rifle-3-scoped.png'), 
            "ak": pygame.image.load('assets/guns/Assaut-rifle-1.png'),
            "bazuca": pygame.image.load('assets/guns/RPG-reisized.png')
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


        self.rect = pygame.Rect(self.x, self.y, 16, 16)

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

        self.rect.x = self.x
        self.rect.y = self.y   
        
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
    
    def pegar_arma(self):
        self.arma = random.choice(self.armas)

        
    def atirar(self):

        if self.arma is not None:

            novo_projetil = Projetil(

                self.x,
                self.y,

                self.direcao,

                self.arma,

                self.sprites_projetil[self.arma]
            )

            self.projeteis.append(novo_projetil)

            print(f"Acabou a munição da {self.arma}")

            self.arma = None

    def desenhar(self, tela):
        sprite = self.sprites[self.sprite]
        #Aqui o sprite roda conforme a direção
        if self.direcao == 'esquerda':
            sprite = pygame.transform.rotate(sprite, 180)
        elif self.direcao == 'cima':
            sprite = pygame.transform.rotate(sprite, 90)
        elif self.direcao == 'baixo':
            sprite = pygame.transform.rotate(sprite, -90)
        
        for projetil in self.projeteis:
            projetil.desenhar(tela)
        
        #desenha o sprite do jogador na tela
        tela.blit(sprite, (self.x, self.y))

        #aq é da arma (o que esse jogo é sobre man...)
        if self.arma is not None:
            arma_sprite = self.sprites_armas[self.arma]
            #Botar a arma pra girar junto pelo amor de Deus
            if self.direcao == 'esquerda':
                arma_sprite = pygame.transform.rotate(arma_sprite, 180)
                tela.blit(arma_sprite, (self.x - 32, self.y-8))
            elif self.direcao == 'direita':
                tela.blit(arma_sprite, (self.x + 16, self.y+8))
            elif self.direcao == 'cima':
                arma_sprite = pygame.transform.rotate(arma_sprite, 90)
                tela.blit(arma_sprite, (self.x+8, self.y - 32))
            elif self.direcao == 'baixo':
                arma_sprite = pygame.transform.rotate(arma_sprite, -90)
                tela.blit(arma_sprite, (self.x-8, self.y + 16))

