import pygame, random

# Carregando imagens
imagemTubarao = pygame.image.load("img/cenario.png")
imagemPeixe = pygame.image.load("img/tubarao.png")
imagemFundo = pygame.image.load("img/peixe.png")

# Definindo algumas constantes
LARGURAJANELA = 800
ALTURAJANELA = 700
LARGURAPEIXE = 80
ALTURAPEIXE = 30
LARGURATUBARAO = 290
ALTURATUBARAO = 190
VEL = 6
ITERACOES = 30

# Redimensionando as imagens
imagemFundo = pygame.transform.scale(imagemFundo, (LARGURAJANELA, ALTURAJANELA))
imagemPeixe = pygame.transform.scale(imagemPeixe, (LARGURAPEIXE, ALTURAPEIXE))
imagemTubarao = pygame.transform.scale(imagemTubarao, (LARGURATUBARAO, ALTURATUBARAO))

# Definindo a função moverJogador
def moverJogador(jogador, teclas, dimensaoJanela):
    bordaEsquerda = 0
    bordaSuperior = 0
    bordeDireita = dimensaoJanela[0]
    bordaInferior = dimensaoJanela[1]
    if teclas["esquerda"] and jogador["objRect"].right < bordaEsquerda:
        jogador["objRect"].x -= jogador["vel"]
    if teclas["direita"] and jogador["objRect"].left > bordeDireita:
        jogador["objRect"].x += jogador["vel"]
    if teclas["cima"] and jogador["objRect"].top > bordaSuperior:
        jogador["objRect"].y -= jogador["vel"]
    if teclas["baixo"] and jogador["objRect"].bottom < bordaInferior:
        jogador["objRect"].y += jogador["vel"]

# Definindo a função moverPeixe
def moverPeixe(peixe):
    peixe["objRect"].x += peixe["vel"]

# Inicializando pygame
pygame.init()

relogio = pygame.time.Clock()

# Criando janela
janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
pygame.display.set_caption("Imagem e Som")

# Ao criar o jogador, defina a área de colisão
jogador = {
    "objRect": pygame.Rect(300, 100, LARGURATUBARAO, ALTURATUBARAO),
    "imagem": imagemTubarao,
    "vel": VEL,
    "colisaoRect": pygame.Rect(300 + 50, 100 + 50, LARGURATUBARAO - 100, ALTURATUBARAO - 100)  # Ajuste conforme necessário
}

# Configurando o som
somComer = pygame.mixer.Sound("mp3/comer.mp3")  
# # Carregar a música de fundo
# pygame.mixer.music.load('mp3/musicaFundo.mp3')
# # Definir o volume (por exemplo, 0.1 para 10% do volume máximo)
# pygame.mixer.music.set_volume(0.1)
# # Reproduzir a música em loop
# pygame.mixer.music.play(-1, 0.0)
somAtivado = True

# Definindo o dicionário que guardará as direções pressionadas
teclas = {"esquerda": False, "direita": False, "cima": False, "baixo": False}

# Inicializando outras variáveis
contador = 0
peixes = []
deve_continuar = True

# Loop do jogo
while deve_continuar:
    # Checando os eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            deve_continuar = False

        # Quando uma tecla é pressionada
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                deve_continuar = False
            if evento.key == pygame.K_m:
                if somAtivado:
                    pygame.mixer.music.stop()
                    somAtivado = False
                else:
                    pygame.mixer.music.play(-1, 0.0)
                    somAtivado = True

        # Quando um botão do mouse é pressionado
        if evento.type == pygame.MOUSEBUTTONDOWN:
            peixes.append({"objRect": pygame.Rect(evento.pos[0], evento.pos[1], LARGURAPEIXE, ALTURAPEIXE), "imagem": imagemPeixe, "vel": VEL - 3})

    # Verificando o estado atual das teclas
    teclas = pygame.key.get_pressed()
    teclas = {
        "esquerda": teclas[pygame.K_LEFT] or teclas[pygame.K_a],
        "direita": teclas[pygame.K_RIGHT] or teclas[pygame.K_d],
        "cima": teclas[pygame.K_UP] or teclas[pygame.K_w],
        "baixo": teclas[pygame.K_DOWN] or teclas[pygame.K_s],
    }

    contador += 1
    if contador >= ITERACOES:
        # Adicionando um novo peixe
        contador = 0
        posY = random.randint(0, ALTURAJANELA - ALTURAPEIXE)
        posX = -LARGURAPEIXE
        velRandom = random.randint(VEL - 3, VEL + 3)
        peixes.append({"objRect": pygame.Rect(posX, posY, LARGURAPEIXE, ALTURAPEIXE), "imagem": imagemPeixe, "vel": velRandom})

    # Preenchendo a janela com a imagem de fundo
    janela.blit(imagemFundo, (0, 0))

    # Movendo jogador
    moverJogador(jogador, teclas, (LARGURAJANELA, ALTURAJANELA))

    # Desenhando jogador
    janela.blit(jogador["imagem"], jogador["objRect"])

    # Na parte do loop onde verifica colisões, utilize o novo rect
    for peixe in peixes:
        comeu = jogador["colisaoRect"].colliderect(peixe["objRect"])
        if comeu and somAtivado:
            somComer.play()
        if comeu or peixe["objRect"].x > LARGURAJANELA:
            peixes.remove(peixe)
    
    # Não esqueça de atualizar a posição do rect de colisão a cada movimento do jogador
    jogador["colisaoRect"].topleft = (jogador["objRect"].x + 50, jogador["objRect"].y + 50)

    # Movendo e desenhando os peixes
    for peixe in peixes:
        moverPeixe(peixe)
        janela.blit(peixe["imagem"], peixe["objRect"])

    # Atualizando a janela
    pygame.display.update()

    relogio.tick(40)

# Encerrando módulos de Pygame
pygame.quit()
