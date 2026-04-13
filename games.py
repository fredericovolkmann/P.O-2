import pygame
import random

# Inicialização básica
pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("game")
relogio = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 50, 50)
AZUL = (50, 150, 255)

# Configurações do Jogador
player_largura = 50
player_altura = 80
player_x = LARGURA // 2
player_y = ALTURA - 100
player_vel = 7

# Configurações dos Obstáculos
obs_largura = 30
obs_altura = 50
obs_vel = 5
obstaculos = []

def criar_obstaculo():
    x = random.randint(0, LARGURA - obs_largura)
    y = -obs_altura
    return pygame.Rect(x, y, obs_largura, obs_altura)

# Loop principal
rodando = True
while rodando:
    tela.fill((30, 30, 30)) # Fundo escuro
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    #  Criar novos obstáculos
    if random.randint(1, 30) == 1:
        obstaculos.append(criar_obstaculo())

    # 2. Mover obstáculos 
    for obs in obstaculos[:]:
        obs.y += obs_vel
        if obs.y > ALTURA:
            obstaculos.remove(obs)

    # LÓGICA DE ESQUIVA
    ameaca_proxima = None
    distancia_minima = 200 # Raio de detecção

    
    for obs in obstaculos:
        
        if player_y > obs.y and (player_y - obs.y) < distancia_minima:
            
            if obs.colliderect(pygame.Rect(player_x - 40, 0, player_largura + 80, ALTURA)):
                ameaca_proxima = obs
                break

    
    if ameaca_proxima:
        centro_player = player_x + player_largura / 2
        centro_obs = ameaca_proxima.x + obs_largura / 2
        
        if centro_player < centro_obs:
            player_x -= player_vel 
        else:
            player_x += player_vel 

    # Manter o jogador dentro da tela
    player_x = max(0, min(player_x, LARGURA - player_largura))

    
    # Jogador
    player_rect = pygame.Rect(player_x, player_y, player_largura, player_altura)
    pygame.draw.rect(tela, AZUL, player_rect)

    # Obstáculos
    for obs in obstaculos:
        pygame.draw.rect(tela, VERMELHO, obs)
        # Se houver colisão real, poderíamos resetar o jogo aqui
        if player_rect.colliderect(obs):
            # Opcional: print("Bateu!")
            pass

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()