import pygame
import random
import time  # Biblioteca para medir tempo


# Perguntamos no terminal antes de iniciar a tela do Pygame
while True:
    try:
        NUM_JOGADORES = int(input("Digite a quantidade de jogadores que deseja simular (ex: 5, 10, 50): "))
        if NUM_JOGADORES > 0:
            break
        print("Por favor, digite um número maior que 0.")
    except ValueError:
        print("Entrada inválida. Digite um número inteiro.")
# ______________________________________________________________________

# Inicializacao basica
pygame.init()

# Obtem a resolucao maxima do monitor atual
info_tela = pygame.display.Info()
LARGURA = info_tela.current_w
ALTURA = info_tela.current_h

# tela Fullscreen 
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)

pygame.display.set_caption("Game com Multiplos Jogadores")

relogio = pygame.time.Clock()

VERMELHO = (255, 50, 50)
PRETO = (30, 30, 30)
VERDE = (50, 255, 150)
AZUL = (50, 150, 255)
BRANCO = (255, 255, 255)

fonte = pygame.font.SysFont("Arial", 40)
fonte_pequena = pygame.font.SysFont("Arial", 30)

class Jogador:
    def __init__(self, x, y, velocidade=7, alcance=200, cor=AZUL): 
        self.largura = 30
        self.altura = 80
        self.x = x
        self.y = y
        self.vel = velocidade 
        self.distancia_deteccao = alcance 
        self.cor = cor
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        self.vivo = True 

    def desenhar(self, superficie):
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        pygame.draw.rect(superficie, self.cor, self.rect)

    def decidir_movimento(self, obstaculos):
        ameaca_proxima = None
        for obs in obstaculos:
            if self.y > obs.y and (self.y - obs.y) < self.distancia_deteccao:
                area_projecao = pygame.Rect(self.x - 40, 0, self.largura + 80, ALTURA)
                if obs.colliderect(area_projecao):
                    ameaca_proxima = obs
                    break

        if ameaca_proxima:
            centro_player = self.x + self.largura / 2
            centro_obs = ameaca_proxima.x + (ameaca_proxima.width / 2)
            if centro_player < centro_obs:
                self.x -= self.vel 
            else:
                self.x += self.vel 
        self.x = max(0, min(self.x, LARGURA - self.largura))

# Configuracoes dos Obstaculos
obs_largura = 30
obs_altura = 50
obs_vel = 10

obstaculos = []
densidade_chuva = 2

def criar_obstaculo():
    x = random.randint(0, LARGURA - obs_largura)
    y = -obs_altura
    return pygame.Rect(x, y, obs_largura, obs_altura)

# LISTA DE OBJETOS DO TIPO JOGADOR 
jogadores = []

def inicializar_jogadores():
    global jogadores
    jogadores = []
    
    # Divide a largura da tela igualmente baseada na quantidade de jogadores inserida
    espacamento = LARGURA / (NUM_JOGADORES + 1)
    
    # Criamos os jogadores dinamicamente usando um laço de repetição
    for i in range(1, NUM_JOGADORES + 1):
        # Gera atributos levemente aleatórios para cada um ter uma "personalidade" diferente
        vel_aleatoria = round(random.uniform(6.0, 9.5), 1)
        alcance_aleatorio = random.randint(150, 260)
        cor_aleatoria = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        
        # Instancia e adiciona o jogador posicionado corretamente na tela
        pos_x = int(espacamento * i)
        jogadores.append(Jogador(pos_x, ALTURA - 100, velocidade=vel_aleatoria, alcance=alcance_aleatorio, cor=cor_aleatoria))

def salvar_resultado_no_arquivo(segundos_sobrevividos):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{timestamp}] Rodada Encerrada. Sobrevivencia: {segundos_sobrevividos:.2f} segundos | Frequencia de Chuva Final: {densidade_chuva} | Jogadores: {NUM_JOGADORES}\n"
    with open("resultados.txt", "a") as arquivo:
        arquivo.write(linha)

def resetar_jogo():
    global obstaculos, morto, tempo_inicio, tempo_salvo
    obstaculos = []
    inicializar_jogadores() 
    morto = False
    tempo_inicio = time.time()  
    tempo_salvo = False

# Inicializa os objetos jogadores pela primeira vez
inicializar_jogadores()

# Estados do Jogo (Booleans)
rodando = True
morto = False

tempo_inicio = time.time()  
tempo_salvo = False         
duracao_final = 0.0         

# Loop principal
while rodando:
    tela.fill(PRETO)
    
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False 
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False
            
            if not morto:
                if evento.key == pygame.K_UP:
                    densidade_chuva = max(1, densidade_chuva - 1)
                elif evento.key == pygame.K_DOWN:
                    densidade_chuva = min(30, densidade_chuva + 1)
        
        if morto and evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            botao_rect = pygame.Rect(LARGURA//2 - 100, ALTURA//2 + 50, 200, 50)
            if botao_rect.collidepoint(mouse_pos):
                resetar_jogo()

    if not morto:
        if random.randint(1, densidade_chuva) == 1:
            obstaculos.append(criar_obstaculo())

        for obs in obstaculos[:]:
            obs.y += obs_vel
            if obs.y > ALTURA:
                obstaculos.remove(obs)
                
        todos_morreram = True
        for jor in jogadores:
            if jor.vivo:
                todos_morreram = False 
                jor.decidir_movimento(obstaculos)
                jor.desenhar(tela)
        
                for obs in obstaculos:
                    if jor.rect.colliderect(obs):
                        jor.vivo = False

        for obs in obstaculos:
            pygame.draw.rect(tela, VERMELHO, obs)

        tempo_atual = time.time() - tempo_inicio 
        
        texto_cronometro = fonte_pequena.render(f"Tempo: {tempo_atual:.2f}s | Qtd: {NUM_JOGADORES}", True, BRANCO)
        tela.blit(texto_cronometro, (20, 20))
        
        escala_intensidade = 31 - densidade_chuva
        texto_densidade = fonte_pequena.render(f"Intensidade da Chuva: {escala_intensidade} (Setas UP / DOWN)", True, VERDE)
        tela.blit(texto_densidade, (20, 60))

        if todos_morreram:
            duracao_final = tempo_atual  
            morto = True

    else:
        if not tempo_salvo:
            salvar_resultado_no_arquivo(duracao_final)
            tempo_salvo = True

        texto_morte = fonte.render("TODOS OS JOGADORES MORRERAM", True, VERMELHO)
        tela.blit(texto_morte, (LARGURA//2 - 250, ALTURA//2 - 50))
        
        texto_tempo_final = fonte_pequena.render(f"Tempo de Sobrevivencia: {duracao_final:.2f} segundos", True, BRANCO)
        tela.blit(texto_tempo_final, (LARGURA//2 - 230, ALTURA//2 + 5))
        
        botao_rect = pygame.Rect(LARGURA//2 - 100, ALTURA//2 + 50, 200, 50)
        pygame.draw.rect(tela, VERDE, botao_rect)
        
        texto_reset = fonte_pequena.render("REINICIAR", True, PRETO)
        tela.blit(texto_reset, (LARGURA//2 - 65, ALTURA//2 + 60))

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()