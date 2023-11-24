import pygame
import sys
import time

import tictactoe as ttt

# Inicializacao do Pygame
pygame.init()
size = width, height = 900, 600

# Definicao de cores
black = (0, 0, 0)
white = (255, 255, 255)

# Icone transparente
icon_size = (32, 32)  # Tamanho do icone
transparent_icon = pygame.Surface(icon_size, pygame.SRCALPHA)
transparent_icon.fill((0, 0, 0, 0))  # Preenche com cor transparente

# Titulo da janela
screen = pygame.display.set_mode(size)
pygame.display.set_icon(transparent_icon)
pygame.display.set_caption("BLACKBARGS")

# Definicao de fontes
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 30)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 42)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 62)

# Variaveis
user = None
board = ttt.initial_state()
ai_turn = False

# Loop main do joguinho
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Deixa o usuario escolher como deseja iniciar
    if user is None:

        # Tela de escolha
        title = largeFont.render("JOGAR :)", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Desenha os botoes de escolha
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Jogar com: X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Jogar com: O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Da um bizu se alguma coisa foi selecionada
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:

        # Tabuleiro 
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Mostra algumas informacoes
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Fim De Jogo: Empatou"
            else:
                title = f"Fim De Jogo: {winner} Venceu!"
        elif user == player:
            title = f"Sua Vez:  {user}"
        else:
            title = f"AI Pensando..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Verifica se eh a vez da AI
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Verifica se eh a vez do usuario
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("JOGAR DE NOVO", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    pygame.display.flip()
