import pygame

LARGURA    = 960
ALTURA_MAPA = 704
ALTURA_UI  = 96

AMARELO  = (255, 220,   0)
BRANCO   = (255, 255, 255)
VERMELHO = (210,  30,  30)
CINZA    = (160, 160, 160)
CINZA_ESC= ( 40,  40,  40)
PRETO    = (  0,   0,   0)
AZUL     = (  0,   0, 180)
AZUL_CL  = ( 30,  30, 220)

CORES_ARMA = {
    "ak":     ( 80, 220,  80),
    "sniper": ( 80, 180, 255),
    "bazuca": (255, 140,  50),
    None:     (100, 100, 100),
}

NOMES_ARMA = {
    "ak":     "AK-47",
    "sniper": "SNIPER",
    "bazuca": "BAZUCA",
    None:     "SEM ARMA",
}


class HUD:
    def __init__(self):
        pygame.font.init()

        self.fonte_titulo  = pygame.font.SysFont("arialblack", 78, bold=True)
        self.fonte_sub     = pygame.font.SysFont("impact",  38)
        self.fonte_ui      = pygame.font.SysFont("consolas", 30, bold=True)
        self.fonte_label   = pygame.font.SysFont("consolas", 18)
        self.fonte_controle= pygame.font.SysFont("consolas", 24, bold=True)
        self.fonte_grande  = pygame.font.SysFont("impact",  80, bold=True)
        self.fonte_media   = pygame.font.SysFont("consolas", 34, bold=True)

    def desenhar_texto_contornado(self, tela, fonte, texto, cor, contorno, centro):
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2)]:
            sombra = fonte.render(texto, True, contorno)
            tela.blit(sombra, sombra.get_rect(center=(centro[0] + dx, centro[1] + dy)))

        texto_render = fonte.render(texto, True, cor)
        tela.blit(texto_render, texto_render.get_rect(center=centro))

    # ------------------------------------------------------------------ tela de início

    def desenhar_inicio(self, tela):
        tela.fill(PRETO)

        # Grade de pontos decorativa
        for x in range(0, LARGURA, 48):
            for y in range(0, ALTURA_MAPA + ALTURA_UI, 48):
                pygame.draw.circle(tela, (18, 18, 50), (x, y), 3)

        # Linhas de borda decorativas
        pygame.draw.rect(tela, AZUL,   (0, 0, LARGURA, ALTURA_MAPA + ALTURA_UI), 8)
        pygame.draw.rect(tela, AZUL_CL,(4, 4, LARGURA - 8, ALTURA_MAPA + ALTURA_UI - 8), 2)

        # Sombra do título
        centro_y = (ALTURA_MAPA + ALTURA_UI) // 2 - 100
        titulo_texto = "PAK 47-MAN"

        # Título
        self.desenhar_texto_contornado(
            tela,
            self.fonte_titulo,
            titulo_texto,
            AMARELO,
            (90, 0, 0),
            (LARGURA // 2, centro_y)
        )

        # Traço vermelho embaixo do título
        larg_titulo = self.fonte_titulo.size(titulo_texto)[0]
        pygame.draw.rect(
            tela, VERMELHO,
            (LARGURA // 2 - larg_titulo // 2, centro_y + 58, larg_titulo, 5)
        )

        # Instrução piscante
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            self.desenhar_texto_contornado(
                tela,
                self.fonte_sub,
                "PRESSIONE ENTER PARA JOGAR",
                BRANCO,
                (0, 0, 0),
                (LARGURA // 2, centro_y + 110)
            )

        # Tabela de controles
        caixa = pygame.Rect(0, 0, 420, 110)
        caixa.center = (LARGURA // 2, centro_y + 205)
        pygame.draw.rect(tela, (5, 5, 18), caixa)
        pygame.draw.rect(tela, AZUL_CL, caixa, 2)

        controles = [
            ("MOVER",    "SETAS DO TECLADO"),
            ("ATIRAR",   "Z"),
        ]
        y_ctrl = caixa.y + 34
        for acao, tecla in controles:
            s_acao  = self.fonte_controle.render(acao,  True, BRANCO)
            s_tecla = self.fonte_controle.render(tecla, True, AMARELO)

            espaco = 24
            largura_linha = s_acao.get_width() + espaco + s_tecla.get_width()
            inicio_x = LARGURA // 2 - largura_linha // 2

            tela.blit(s_acao, s_acao.get_rect(left=inicio_x, centery=y_ctrl))
            tela.blit(
                s_tecla,
                s_tecla.get_rect(left=inicio_x + s_acao.get_width() + espaco, centery=y_ctrl)
            )
            y_ctrl += 42

    # ------------------------------------------------------------------ tela de game over

    def desenhar_game_over(self, tela, pontos):
        # Overlay escuro sobre o jogo congelado
        overlay = pygame.Surface((LARGURA, ALTURA_MAPA + ALTURA_UI), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        tela.blit(overlay, (0, 0))

        centro_y = (ALTURA_MAPA + ALTURA_UI) // 2

        # Título GAME OVER
        go = self.fonte_grande.render("GAME  OVER", True, VERMELHO)
        tela.blit(go, go.get_rect(center=(LARGURA // 2, centro_y - 100)))

        # Linha separadora
        pygame.draw.rect(
            tela, VERMELHO,
            (LARGURA // 2 - 220, centro_y - 48, 440, 4)
        )

        # Pontuação final
        pts = self.fonte_media.render(f"PONTUAÇÃO FINAL:  {pontos}", True, AMARELO)
        tela.blit(pts, pts.get_rect(center=(LARGURA // 2, centro_y + 10)))

        # Instrução piscante
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            reiniciar = self.fonte_label.render(
                "ENTER — jogar novamente          ESC — sair",
                True, BRANCO
            )
            tela.blit(reiniciar, reiniciar.get_rect(center=(LARGURA // 2, centro_y + 80)))

    # ------------------------------------------------------------------ faixa inferior (em jogo)

    def desenhar_ui(self, tela, pontos, arma, vidas):
        """
        Desenha a faixa de UI na parte de baixo da tela (abaixo do mapa).
        Deve ser chamada por último no bloco de desenho, depois de tudo.
        """
        base_y = ALTURA_MAPA

        # Fundo da faixa
        pygame.draw.rect(tela, (20, 20, 20), (0, base_y, LARGURA, ALTURA_UI))

        # Linha de separação entre mapa e UI
        pygame.draw.line(tela, AZUL_CL, (0, base_y), (LARGURA, base_y), 3)

        # --- PONTOS (lado esquerdo) ---
        label_pts = self.fonte_label.render("PONTOS", True, CINZA)
        valor_pts = self.fonte_ui.render(f"{pontos:06d}", True, BRANCO)
        tela.blit(label_pts, (28, base_y + 14))
        tela.blit(valor_pts, (28, base_y + 36))

        # Divisores
        pygame.draw.line(
            tela, CINZA_ESC,
            (LARGURA // 3, base_y + 12),
            (LARGURA // 3, base_y + ALTURA_UI - 12),
            2
        )

        pygame.draw.line(
            tela, CINZA_ESC,
            (2 * LARGURA // 3, base_y + 12),
            (2 * LARGURA // 3, base_y + ALTURA_UI - 12),
            2
        )

        # --- VIDAS (centro) ---
        label_vidas = self.fonte_label.render("VIDAS", True, CINZA)
        tela.blit(label_vidas, (LARGURA // 3 + 28, base_y + 14))

        for i in range(max(0, vidas)):
            centro_x = LARGURA // 3 + 44 + i * 38
            centro_y = base_y + 58

            pygame.draw.circle(tela, AMARELO, (centro_x, centro_y), 13)
            pygame.draw.polygon(
                tela,
                (20, 20, 20),
                [
                    (centro_x, centro_y),
                    (centro_x + 13, centro_y - 7),
                    (centro_x + 13, centro_y + 7),
                ]
            )

        # --- ARMA (lado direito) ---
        cor_arma  = CORES_ARMA.get(arma, CINZA)
        nome_arma = NOMES_ARMA.get(arma, "???")

        label_arma = self.fonte_label.render("ARMA EQUIPADA", True, CINZA)
        valor_arma = self.fonte_ui.render(nome_arma, True, cor_arma)

        tela.blit(label_arma, (2 * LARGURA // 3 + 28, base_y + 14))
        tela.blit(valor_arma, (2 * LARGURA // 3 + 28, base_y + 36))

        # Indicador visual: bolinha da cor da arma
        if arma is not None:
            pygame.draw.circle(
                tela, cor_arma,
                (LARGURA - 48, base_y + ALTURA_UI // 2),
                14
            )
            pygame.draw.circle(
                tela, BRANCO,
                (LARGURA - 48, base_y + ALTURA_UI // 2),
                14, 2
            )
    def desenhar_vitoria(self, tela, pontos):
        # Overlay escuro sobre o jogo congelado
        overlay = pygame.Surface((LARGURA, ALTURA_MAPA + ALTURA_UI), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        tela.blit(overlay, (0, 0))

        centro_y = (ALTURA_MAPA + ALTURA_UI) // 2

        # Título VITÓRIA
        vitoria = self.fonte_grande.render("VITÓRIA!", True, AZUL_CL)
        tela.blit(vitoria, vitoria.get_rect(center=(LARGURA // 2, centro_y - 100)))

        # Linha separadora
        pygame.draw.rect(
            tela, AZUL_CL,
            (LARGURA // 2 - 220, centro_y - 48, 440, 4)
        )

        # Pontuação final
        pts = self.fonte_media.render(f"PONTUAÇÃO FINAL:  {pontos}", True, AMARELO)
        tela.blit(pts, pts.get_rect(center=(LARGURA // 2, centro_y + 10)))

        # Instrução piscante
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            reiniciar = self.fonte_label.render(
                "ENTER — jogar novamente          ESC — sair",
                True, BRANCO
            )
            tela.blit(reiniciar, reiniciar.get_rect(center=(LARGURA // 2, centro_y + 80)))
