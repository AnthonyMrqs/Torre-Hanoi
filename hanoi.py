# importacoes necessarias
import pygame as pg
import copy
from time import sleep


# Iniciando projeto Pygame
pg.init()

# Constantes
COLORS: dict = {
    "RED":   (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE":  (0, 0, 255),
    "ORANGE": (255, 165, 0),
    "Yellow": (255, 255, 0),
    "Violet": (238, 130, 238),
    "Indigo": (75, 0, 130)
    
} # Cores de cada disco

BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
BROWN: tuple[int, int, int] = (165, 42, 42)


SIZE: tuple[int, int] = (720, 540) # Tamanho da tela


def main() -> None:
    global movimentos, discos, pos_atual, count, mensagem
    
    movimentos = []
    discos = {} # Informacao de posicao e cor dos discos
    pos = [50, 430, 180, 20] 
    
    # Desenhado a tela
    tela: pg.Surface = pg.display.set_mode(SIZE)
    pg.display.set_caption("Torre de Hanoi")
    tela.fill(WHITE) 

    num = caixa_de_texto(tela)

    torre: list = [[], [], []]
    iterador = iter(COLORS)

    # Inicializar a primeira torre com os discos
    for i in range(num): 
        torre[0].append(str(i + 1))
        discos[str(num - i)] = [next(iterador), pos.copy(), 1] # Definindo as cores, posicoes dos discos e o destino do disco
        pos[0], pos[1], pos[2] = pos[0] + 10, pos[1] - 20, pos[2] - 20 # Calculando a posicao do disco
    
    clock: pg.Clock = pg.time.Clock()
    
    pos_atual = [copy.deepcopy(torre)] # Define a posicao atual dos discos
    desenharTorreDeHanoi(tela=tela, mov=pos_atual)
    
    # Resolver o problema 
    hanoi(num, 1, 2, 3, torre)
    
    count = 0 # Contador de movimentos realizados
    total_mov: int = len(movimentos) # Total de movimentos
    
    mensagem = "" # Mensagem que e exibida na tela

    executando: bool = True
    index: int = 0

    # Rodando loop do jogo
    while executando:
        for event in pg.event.get(): # Verificao dos eventos
            if event.type == pg.QUIT: # Evento para fechar a tela
                executando = False
                break

        if index < total_mov:
            desenharTorreDeHanoi(tela=tela, mov=movimentos[index]) # Desenhando torre de hanoi
            index += 1
        
        sleep(1)
        clock.tick(120)  # Limitando FPS para 120
        
        pg.display.update() # Atualiza a tela

    pg.quit() # Fechando o jogo
    

# Desenha a torre de hanoi
def desenharTorreDeHanoi(*, tela: pg.Surface, mov: list) -> None:
    desenharBasesEHastes(tela) # Desenha as bases e hastes
    
    # Verifica se o array de movimentos e diferente do array da posicao atual dos discos
    if mov != pos_atual:
        atualizarPosicaoDosDiscos(tela, mov) # Atualiza a posicao dos discos
    
    desenharDiscos(tela, mov)


def desenharBasesEHastes(tela: pg.Surface) -> None:
    tela.fill(WHITE) # Limpa a tela
    
    # Posicoes das bases e hastes das torres
    base:  list[int, int, int, int] = [40, 450, 200, 20]
    haste: list[int, int, int, int] = [130, 150, 20, 300]
    
    # Desenhando as hastes e bases
    for _ in range(3):
        pg.draw.rect(tela, BROWN, base)
        pg.draw.rect(tela, BROWN, haste)
        base[0] += 220
        haste[0] += 220


def desenharDiscos(tela: pg.Surface, mov: list) -> None:
    size: int = len(mov)
    
    for i in range(size):
        for j in range(len(mov[i])):
            for k in range(len(mov[i][j])):
                pg.draw.rect(tela, discos[mov[i][j][k]][0], discos[mov[i][j][k]][1]) # Desenha os discos em suas determinadas posicoes


# Atualiza as posicoes dos discos
def atualizarPosicaoDosDiscos(tela: pg.Surface, mov: list) -> None:
    global pos_atual
    
    size: int = len(pos_atual[0])

    for j in range(size):
        for k in range(len(pos_atual[0][j])):
            if pos_atual[0][j][k] not in mov[j]:
                saida = (0, j, k)
                destino = buscarDestinoDoDisco(pos_atual[0][j][k], mov)     
                moverDisco(tela, mov, saida, destino)
                atualizarTextoNaTela(tela)
                pos_atual = [mov]
                return


# Busca posicao do elemento para mover ele
def buscarDestinoDoDisco(value: int, mov: list) -> tuple:
    size: int = len(mov)
    return [(i, j) for i in range(size) for j in range(len(mov[i])) if value == mov[i][j]][0]


# Move os discos para suas determinadas posicoes
def moverDisco(tela: pg.Surface, mov: list, saida: tuple, destino: tuple) -> None:
    global discos, count, mensagem
    
    key: str = pos_atual[saida[0]][saida[1]][saida[2]] # Pega a chave para acessar o disco

    eixo_x: int = abs((discos[key][1][0] - 220 * (destino[0] - saida[1])) - discos[key][1][0])
    passo_x: int = -2 if destino[0] < saida[1] else 2
    
    eixo_y: int = discos[key][1][1] - 110
    
    count += 1
        
    discos[key][2] = destino[0] + 1
    mensagem = f"Movimentos: {count} | Disco {key} moveu para a haste {discos[key][2]}" # Atualizando a mensagem da tela

    # Movimentando os discos
    for _ in range(0, eixo_y, 2): # Movimento o disco para cima (eixo y)
        discos[key][1][1] -= 2

        desenharBasesEHastes(tela)

        desenharDiscos(tela, mov)

        atualizarTextoNaTela(tela)

        pg.display.update()
    
    for _ in range(0, eixo_x, 2): # Movimenta o disco no eixo x
        discos[key][1][0] += passo_x
        
        desenharBasesEHastes(tela)
        
        desenharDiscos(tela, mov)
        
        atualizarTextoNaTela(tela)
        
        pg.display.update()

    eixo_y = abs((discos[key][1][1] - 20 * len(pos_atual[saida[0]][destino[0]])) + 210)
    
    for _ in range(0, eixo_y, 2): # Movimento o disco para baixo (eixo y)
        discos[key][1][1] += 2

        desenharBasesEHastes(tela)
        
        desenharDiscos(tela, mov)

        atualizarTextoNaTela(tela)
        
        pg.display.update()
        

# Atualiza o contador de movimentos
def atualizarTextoNaTela(tela: pg.Surface) -> None:
    global mensagem

    # Configurando a fonte
    font: str = pg.font.match_font("arialblack")
    fontsys: pg.Font = pg.font.Font(font, 25)
    
    # Criando a area onde o texto sera desenhado
    txt_rect: pg.Rect = pg.Rect(30, 30, 500, 50)
    
    # Apaga a area anterior para evitar sobreposicao
    tela.fill(WHITE, txt_rect)

    # Renderiza o texto
    txt: pg.Surface = fontsys.render(mensagem, True, BLACK)

    # Desenha o texto
    tela.blit(txt, txt_rect)


# Busca o menor caminho para a torre de hanoi
def hanoi(n: int, origem: int, aux: int, destino: int, t: list) -> None:
    if n > 0:
        hanoi(n - 1, origem, destino, aux, t)
       
        # Mover disco da origem para o destino
        t[destino - 1].insert(0, t[origem - 1][0])
        t[origem - 1].pop(0)

        # Armazenar uma cópia do estado atual das torres
        movimentos.append(copy.deepcopy(t))

        hanoi(n - 1, aux, origem, destino, t)

# Monta a caixa de texto para inserir o número de discos
def caixa_de_texto(tela):

    # Parâmetros da caixa de texto
    caixa = pg.Rect(200, 200, 140, 32)
    cor_0 = pg.Color('lightskyblue3')
    cor_1 = pg.Color('dodgerblue2')
    cor_principal = cor_0
    cond = False
    text = ''
    num = None

    font = pg.font.Font(None, 32)
    clock: pg.Clock = pg.time.Clock()

    while num is None or not (1 <= num <= 7):  # Continua solicitando a entrada enquanto num não estiver entre 1 e 7
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            
            # Ativar ou desativar a caixa de texto ao clicar (muda a cor da borda)
            if event.type == pg.MOUSEBUTTONDOWN: 
                if caixa.collidepoint(event.pos):
                    cond = not cond
                else:
                    cond = False
                cor_principal = cor_1 if cond else cor_0
                
            if event.type == pg.KEYDOWN:
                if cond:
                    if event.key == pg.K_RETURN:
                        try:
                            num = int(text)
                        except:
                            num = None  # Redefine num se a entrada não for uma string

                        if not (1 <= num <= 7):
                            text = ''  # Limpa o texto se o número for inválido
                            num = None

                    elif event.key == pg.K_BACKSPACE: # Apaga o ultimo caractere digitado
                        text = text[:-1]
                    else:
                        text += event.unicode

        tela.fill(WHITE)

        # Renderiza o texto
        msg = font.render("Digite o número de discos (1-7):", True, BLACK)
        tela.blit(msg, (50, 150))

        # Renderiza o texto dentro da caixa de entrada
        txt_caixa = font.render(text, True, BLACK)

        # Aumenta a caixa de acordo com o texto
        width = max(200, txt_caixa.get_width() + 10)
        caixa.w = width
        tela.blit(txt_caixa, (caixa.x + 5, caixa.y + 5))
        pg.draw.rect(tela, cor_principal, caixa, 2)

        # Atualiza a tela
        pg.display.flip()
        clock.tick(120)

    return num

main()