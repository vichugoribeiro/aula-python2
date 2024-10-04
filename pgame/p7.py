import pygame, random

# Carregando as imagens.
imagemNave = pygame.image.load("img/tubarao.png")
imagemAsteroide = pygame.image.load("img/asteroide.png")
imagemRaio = pygame.image.load("img/peixe.png")
imagemFundo = pygame.image.load("img/espaco.png")

# Carregando constantes
LARGURAJANELA = 1920
ALTURAJANELA = 1080
CORTEXTO = (255, 255, 255) # Branco
QPS = 40 # quadros por segundo
TAMMINIMO = 90 # tamanho mínimo do asteroide
TAMMAXIMO = 99 # tamanho máximo do asteroide
VELMINIMA = 1 # velocidade mínima do asteroide
VELMAXIMA = 8 # velocidade máxima do asteroide
ITERACOES = 6 # número de iterações antes de criar um novo asteroide
VELJOGADOR = 5 # velocidade da nave
VELRAIO = (0,-20) # velocidade do raio

LARGURANAVE = 50
ALTURANAVE = 50
LARGURARAIO = 25
ALTURARAIO = 30

# Redimensionando as imagens
imagemFundo = pygame.transform.scale(imagemFundo, (LARGURAJANELA, ALTURAJANELA))
imagemNave = pygame.transform.scale(imagemNave, (LARGURANAVE, ALTURANAVE))
imagemRaio = pygame.transform.scale(imagemRaio, (LARGURARAIO, ALTURARAIO))

# Definindo a função moverJogador
def moverJogador(jogador, teclas, dimensaoJanela):
    bordaEsquerda = 0
    bordaSuperior = 0
    bordeDireita = dimensaoJanela[0]
    bordaInferior = dimensaoJanela[1]
    if teclas["esquerda"] and jogador["objRect"].left > bordaEsquerda:
        jogador["objRect"].x -= jogador["vel"]
    if teclas["direita"] and jogador["objRect"].right < bordeDireita:
        jogador["objRect"].x += jogador["vel"]
    if teclas["cima"] and jogador["objRect"].top > bordaSuperior:
        jogador["objRect"].y -= jogador["vel"]
    if teclas["baixo"] and jogador["objRect"].bottom < bordaInferior:
        jogador["objRect"].y += jogador["vel"]

def moverElemento(elemento):
    elemento["objRect"].x += elemento["vel"][0]
    elemento["objRect"].y += elemento["vel"][1]

def terminar():
    pygame.quit()
    exit()

def aguardarEntrada():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    terminar()
                return

def colocarTexto(texto, fonte, janela, x, y):
    objTexto = fonte.render(texto, True, CORTEXTO)
    rectTexto = objTexto.get_rect()
    rectTexto.topleft = (x, y)
    janela.blit(objTexto, rectTexto)

# Configurando pygame, relogio, janela.
pygame.init()
relogio = pygame.time.Clock()

# Criando janela
janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
pygame.display.set_caption("Asteroides Troianos")

pygame.mouse.set_visible(False)
imagemFundoRedim = pygame.transform.scale(imagemFundo,(LARGURAJANELA, ALTURAJANELA))

# Configurando a fonte.
fonte = pygame.font.Font(None, 48)

# Configurando o som.
somFinal = pygame.mixer.Sound("mp3/som-final.mp3")
somRecorde = pygame.mixer.Sound("mp3/recorde.mp3")
somTiro = pygame.mixer.Sound("mp3/laser.mp3")
pygame.mixer.music.load("mp3/musica-fundo.mp3")

# Tela de inicio.
colocarTexto("Asteroides Troianos", fonte, janela, LARGURAJANELA / 5, ALTURAJANELA / 3)
colocarTexto("Pressione uma tecla para começar.", fonte, janela, LARGURAJANELA / 20, ALTURAJANELA / 2)
pygame.display.update()

aguardarEntrada()

recorde = 0
while True:
    asteroides = []
    raios = []
    pontuacao = 0
    deve_continuar = True

    teclas = {"esquerda": False, "direita": False, "cima": False, "baixo": False}
    contador = 0
    pygame.mixer.music.play(-1, 0.0)

    posX = LARGURAJANELA / 2 - LARGURANAVE / 2 
    posY = ALTURAJANELA - ALTURANAVE - 50
    jogador = {"objRect": pygame.Rect(posX, posY, LARGURANAVE, ALTURANAVE), "imagem": imagemNave, "vel": VELJOGADOR}

    while deve_continuar:
        pontuacao += 1
        if pontuacao == recorde:
            somRecorde.play()

        # Checando os eventos ocorridos.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    terminar()
                if evento.key == pygame.K_SPACE:
                    raio = {"objRect": pygame.Rect(jogador["objRect"].centerx, jogador["objRect"].top, LARGURARAIO, ALTURARAIO), "imagem": imagemRaio, "vel": VELRAIO}
                    raios.append(raio)
                    somTiro.play()
            if evento.type == pygame.MOUSEMOTION:
                centroX_jogador = jogador["objRect"].centerx
                centroY_jogador = jogador["objRect"].centery
                jogador["objRect"].move_ip(evento.pos[0] - centroX_jogador, evento.pos[1] - centroY_jogador)
            if evento.type == pygame.MOUSEBUTTONDOWN:
                raio = {"objRect": pygame.Rect(jogador["objRect"].centerx, jogador["objRect"].top, LARGURARAIO, ALTURARAIO), "imagem": imagemRaio, "vel": VELRAIO}
                raios.append(raio)
                somTiro.play()

        teclas = pygame.key.get_pressed()
        teclas = {
            "esquerda": teclas[pygame.K_LEFT] or teclas[pygame.K_a], "direita": teclas[pygame.K_RIGHT] or teclas[pygame.K_d],
            "cima": teclas[pygame.K_UP] or teclas[pygame.K_w], "baixo": teclas[pygame.K_DOWN] or teclas[pygame.K_s],
        }

        # Preenchendo o fundo da janela com a imagem correspondente.
        janela.blit(imagemFundoRedim, (0, 0))
        colocarTexto("Pontuação: " + str(pontuacao), fonte, janela, 10, 0)
        colocarTexto("Recorde: " + str(recorde), fonte, janela, 10, 40)

        # Adicionando asteroides quando indicado.
        contador += 1
        if contador >= ITERACOES:
            contador = 0
            tamAsteroide = random.randint(TAMMINIMO, TAMMAXIMO)
            posX = random.randint(0, LARGURAJANELA - tamAsteroide)
            posY = - tamAsteroide
            vel_x = random.randint(-1, 1)
            vel_y = random.randint(VELMINIMA, VELMAXIMA)
            asteroide = {"objRect": pygame.Rect(posX, posY, tamAsteroide, tamAsteroide), "imagem": pygame.transform.scale(imagemAsteroide, (tamAsteroide, tamAsteroide)), "vel": (vel_x, vel_y)}
            asteroides.append(asteroide)

        # Movimentando e desenhando os asteroides.
        for asteroide in asteroides:
            moverElemento(asteroide)
            janela.blit(asteroide["imagem"], asteroide["objRect"])

        # Eliminando os asteroides que passam pela base da janela.
        for asteroide in asteroides:
            if asteroide["objRect"].top > ALTURAJANELA:
                asteroides.remove(asteroide)

        # Movimentando e desenhando os raios.
        for raio in raios:
          moverElemento(raio)
          janela.blit(raio["imagem"], raio["objRect"])
        
        # Eliminando os raios que passam pelo topo da janela.
        for raio in raios[:]:  # Use uma cópia da lista para evitar problemas ao remover
            if raio["objRect"].bottom < 0:
                raios.remove(raio)

        # Movimentando e desenhando jogador(nave).
        moverJogador(jogador, teclas, (LARGURAJANELA, ALTURAJANELA))
        janela.blit(jogador["imagem"], jogador["objRect"])

        # Checando se jogador ou algum raio colidiu com algum asteroide.
        for asteroide in asteroides:  # Use uma cópia da lista para evitar problemas ao remover
            jogadorColidiu = jogador["objRect"].colliderect(asteroide["objRect"])
            if jogadorColidiu:
                if pontuacao > recorde:
                    recorde = pontuacao
                deve_continuar = False  # O jogo termina se a nave colidir com um asteroide
                break  # Não precisamos verificar mais, pois o jogo já acabou

            for raio in raios:  # Use uma cópia da lista para evitar problemas ao remover
                raioColidiu = raio["objRect"].colliderect(asteroide["objRect"])
                if raioColidiu:
                    raios.remove(raio)
                    asteroides.remove(asteroide)
                    break  # Saia do loop assim que encontrar uma colisão

        pygame.display.update()
        relogio.tick(QPS)

    # Parando o jogo e mostrando a tela final.
    pygame.mixer.music.stop()
    somFinal.play()
    colocarTexto("GAME OVER", fonte, janela, (LARGURAJANELA / 3), (ALTURAJANELA / 3))
    colocarTexto("Pressione uma tecla para jogar.", fonte, janela, (LARGURAJANELA / 10), (ALTURAJANELA / 2))
    pygame.display.update()

    # Aguardando entrada por teclado para reiniciar o jogo ou sair.
    aguardarEntrada()
    somFinal.stop()
