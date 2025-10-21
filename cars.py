import pygame
import random
import sys

# --- 1. Inicialização e Configurações ---
pygame.init()

# Cores
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0) # Cor para os buracos/obstáculos

# Configurações da Tela
LARGURA_TELA = 500
ALTURA_TELA = 700
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Unicode Car Game")

# Fontes (usamos 'monospace' para garantir que os caracteres se alinhem)
# Você pode precisar de um arquivo .ttf que suporte os caracteres Unicode para um melhor visual.
# Se 'freesansbold.ttf' não funcionar para o seu sistema, tente usar 'None' para a fonte padrão
# e confie no sistema para encontrar uma que suporte os caracteres.
try:
    # Tenta carregar uma fonte padrão do Pygame que geralmente suporta Unicode
    fonte = pygame.font.Font('freesansbold.ttf', 40) 
except:
    # Caso não encontre a fonte, usa a fonte padrão do sistema
    fonte = pygame.font.Font(None, 40) 

# Caracteres Unicode para os elementos do jogo
CAR_JOGADOR_CHAR = "▲" # Pode ser "🏎" ou "🚗" se a fonte suportar!
CAR_INIMIGO_CHAR = "▼"
BURACO_CHAR = "●"
MARCA_ESTRADA_CHAR = "|"

# Configurações do Jogo
velocidade_jogo = 5
fps = 60
clock = pygame.time.Clock()

# Posição e Dimensões dos Elementos (baseados no tamanho da fonte)
TAM_CAR = 30 # Largura e altura aproximada do bloco de texto do caractere
CAR_X = LARGURA_TELA // 2
CAR_Y = ALTURA_TELA - 60
CAR_VELOCIDADE = 5

# Posições das Pistas (para simplificar o movimento lateral)
PISTA_LARGURA = 100
PISTA_ESQ = LARGURA_TELA // 2 - PISTA_LARGURA
PISTA_CENTRO = LARGURA_TELA // 2
PISTA_DIR = LARGURA_TELA // 2 + PISTA_LARGURA

posicoes_pista = [PISTA_ESQ, PISTA_CENTRO, PISTA_DIR]
car_pista_idx = 1 # Começa na pista do meio (índice 1)

# Lista de Obstáculos
obstaculos = [] # (x, y, tipo)

# --- 2. Funções de Desenho ---

def desenhar_texto(superficie, texto, cor, x, y):
    """Desenha um caractere/texto na tela."""
    texto_surface = fonte.render(texto, True, cor)
    # Centraliza o caractere no ponto (x, y)
    texto_rect = texto_surface.get_rect(center=(x, y)) 
    superficie.blit(texto_surface, texto_rect)

def desenhar_carro_jogador(x, y):
    """Desenha o carro do jogador (Unicode)"""
    desenhar_texto(tela, CAR_JOGADOR_CHAR, PRETO, x, y)

def desenhar_obstaculos():
    """Desenha todos os obstáculos (carros inimigos e buracos)"""
    for obs in obstaculos:
        x, y, tipo = obs
        if tipo == 'carro':
            desenhar_texto(tela, CAR_INIMIGO_CHAR, VERMELHO, x, y)
        elif tipo == 'buraco':
            desenhar_texto(tela, BURACO_CHAR, PRETO, x, y)

def desenhar_estrada():
    """Desenha o fundo da estrada Amarela e as marcações"""
    # Desenha o fundo Amarelo para simular a estrada (se for para ser a estrada amarela)
    # Se fosse uma estrada cinza, mudaríamos aqui.
    tela.fill(AMARELO) 
    
    # Desenha as marcações da pista (opcional)
    MARCA_TAM = 20
    MARCA_ESPACAMENTO = 40
    for y in range(0, ALTURA_TELA, MARCA_ESPACAMENTO):
        # Linha pontilhada do centro
        if (y // MARCA_ESPACAMENTO) % 2 == 0:
             desenhar_texto(tela, MARCA_ESTRADA_CHAR, PRETO, PISTA_CENTRO, y)

# --- 3. Lógica do Jogo ---

def mover_carro_jogador(direcao):
    global car_pista_idx
    novo_idx = car_pista_idx + direcao
    # Garante que o carro permaneça dentro das 3 pistas
    if 0 <= novo_idx < len(posicoes_pista):
        car_pista_idx = novo_idx
        return posicoes_pista[car_pista_idx]
    return posicoes_pista[car_pista_idx]


def gerar_obstaculo():
    """Gera um novo obstáculo (carro ou buraco) no topo da tela"""
    tipo = random.choice(['carro', 'buraco'])
    # Escolhe uma das 3 pistas aleatoriamente
    x = random.choice(posicoes_pista)
    y = -30 # Começa fora da tela
    obstaculos.append((x, y, tipo))

def mover_obstaculos():
    """Move os obstáculos para baixo e remove os que saem da tela"""
    global obstaculos
    novos_obstaculos = []
    for x, y, tipo in obstaculos:
        novo_y = y + velocidade_jogo
        if novo_y < ALTURA_TELA + TAM_CAR: # Mantém o obstáculo na tela
            novos_obstaculos.append((x, novo_y, tipo))
    obstaculos = novos_obstaculos
    
    # Lógica de spawn: probabilidade de gerar um novo obstáculo a cada frame
    if random.randint(1, 40) == 1: 
        gerar_obstaculo()

def checar_colisao(car_x, car_y):
    """Verifica se o carro colidiu com algum obstáculo"""
    car_rect = pygame.Rect(car_x - TAM_CAR//2, car_y - TAM_CAR//2, TAM_CAR, TAM_CAR)
    
    for x, y, tipo in obstaculos:
        obs_rect = pygame.Rect(x - TAM_CAR//2, y - TAM_CAR//2, TAM_CAR, TAM_CAR)
        
        # Aumentamos um pouco a área de colisão (hitbox) para facilitar a detecção visual
        if car_rect.colliderect(obs_rect):
            return True # Colisão detectada
    return False

# --- 4. Loop Principal do Jogo ---

jogo_ativo = True
fim_jogo = False

while jogo_ativo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo_ativo = False
        
        if not fim_jogo:
            # Controle de movimento
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    CAR_X = mover_carro_jogador(-1)
                if event.key == pygame.K_RIGHT:
                    CAR_X = mover_carro_jogador(1)
        else:
            # Se o jogo acabou, permite reiniciar
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                fim_jogo = False
                CAR_X = posicoes_pista[1]
                obstaculos = []
                velocidade_jogo = 5


    if not fim_jogo:
        # Lógica de Atualização
        mover_obstaculos()
        
        # O carro do jogador é desenhado no X da pista selecionada e Y fixo
        CAR_X = posicoes_pista[car_pista_idx]
        
        if checar_colisao(CAR_X, CAR_Y):
            fim_jogo = True
            
        # Desenho
        desenhar_estrada()
        desenhar_obstaculos()
        desenhar_carro_jogador(CAR_X, CAR_Y)
        
    else:
        # Tela de Fim de Jogo
        tela.fill(PRETO)
        fonte_grande = pygame.font.Font(None, 75)
        texto_fim = fonte_grande.render("FIM DE JOGO!", True, VERMELHO)
        tela.blit(texto_fim, (LARGURA_TELA // 2 - texto_fim.get_width() // 2, ALTURA_TELA // 2 - 50))
        
        fonte_pequena = pygame.font.Font(None, 30)
        texto_reiniciar = fonte_pequena.render("Pressione 'R' para Reiniciar", True, AMARELO)
        tela.blit(texto_reiniciar, (LARGURA_TELA // 2 - texto_reiniciar.get_width() // 2, ALTURA_TELA // 2 + 50))


    # Atualiza a tela
    pygame.display.flip()
    
    # Limita o FPS
    clock.tick(fps)

# Sai do Pygame
pygame.quit()
sys.exit()
