import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice

pygame.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')

LARGURA = 640
ALTURA = 480

BRANCO = (173,216,230)

tela = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption('Cat Game')

sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'spritecat.png')).convert_alpha()

colidiu = False

escolha_obstaculo = choice([0, 1])

pontos = 0

velocidade_jogo = 10

def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('Arial', tamanho, True, False)
    mensagem = f'{msg}' 
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

def reiniciar_jogo():
    global pontos, velocidade_jogo, colidiu, escolha_obstaculo
    pontos = 0
    velocidade_jogo = 10
    colidiu = False
    cat.rect.y = ALTURA - 64 - 96//2
    cat.pulo = False
    rato.rect.x = LARGURA
    cogumelo.rect.x = LARGURA
    escolha_obstaculo = choice([0, 1])

class Cat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_gato = []
        for i in range(4):
            img = sprite_sheet.subsurface((i*32,0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagens_gato.append(img)
        
        self.index_lista = 0
        self.image = self.imagens_gato[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = ALTURA - 64 - 96//2
        self.rect.center = [100, ALTURA - 64]
        self.pulo = False

    def pular(self):
        self.pulo = True

    def update(self):
        if self.pulo == True:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 20
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 20
            else:
                self.rect.y = self.pos_y_inicial

        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_gato[int(self.index_lista)]

class Estrela(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((9*32, 0), (32,32))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = LARGURA - randrange(30, 300, 90)

    def altura_estrela(self):
        self.rect.y = randrange(50, 200, 50)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA 
            self.altura_estrela()
        self.rect.x -= velocidade_jogo

class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((8*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y = ALTURA - 70
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x -= 10

class Cogumelo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.center = (LARGURA,  ALTURA - 64)
        self.rect.x = LARGURA

    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo

class Rato(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_rato = []
        for i in range(4, 7):
            img = sprite_sheet.subsurface((i*32, 0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagens_rato.append(img)

        self.index_lista = 0
        self.image = self.imagens_rato[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, 300)
        self.rect.x = LARGURA
    
    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo

            if self.index_lista > 2:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_rato[int(self.index_lista)]

todas_as_sprites = pygame.sprite.Group()
cat = Cat()
todas_as_sprites.add(cat)

for i in range(3):
    estrela = Estrela()
    todas_as_sprites.add(estrela)

for i in range(LARGURA*2//64):
    chao = Chao(i)
    todas_as_sprites.add(chao) 

cogumelo = Cogumelo()
todas_as_sprites.add(cogumelo)

rato = Rato()
todas_as_sprites.add(rato)

grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(cogumelo)
grupo_obstaculos.add(rato)

relogio = pygame.time.Clock()
while True:
    relogio.tick(30)
    tela.fill(BRANCO)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if cat.rect.y != cat.pos_y_inicial:
                    pass
                else:
                    cat.pular()

            if event.key == K_r and colidiu == True:
                reiniciar_jogo()

    colisoes = pygame.sprite.spritecollide(cat, grupo_obstaculos, False, pygame.sprite.collide_mask)

    todas_as_sprites.draw(tela)

    if cogumelo.rect.topright[0] <= 0 or rato.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0, 1])
        cogumelo.rect.x = LARGURA
        rato.rect.x = LARGURA
        cogumelo.escolha = escolha_obstaculo
        rato.escolha = escolha_obstaculo


    if colisoes and colidiu == False:
        colidiu = True

    if colidiu == True:
        if pontos % 100 == 0:
            pontos += 1

        game_over = exibe_mensagem('GAME OVER', 40, (0,0,0))
        tela.blit(game_over, (LARGURA//2, ALTURA//2))
        restart = exibe_mensagem('Pressione r para reiniciar', 20, (0,0,0))
        tela.blit(restart, (LARGURA//2, (ALTURA//2) + 60))

        pass
    else:
        pontos += 1
        todas_as_sprites.update()
        texto_pontos = exibe_mensagem(pontos, 40, (0,0,0))

    if pontos % 100 == 0:
        if velocidade_jogo >= 20:
            velocidade_jogo += 0
        else:
            velocidade_jogo += 1
        
    tela.blit(texto_pontos, (520, 30))


    pygame.display.flip()