from constants import *
from tetris import *
from util import *

import pygame


class GUI:
    def __init__(self, game_state):
        pygame.init()
        self.game_state = game_state
        self.display = pygame.display.set_mode((DISPLAY_SIZE_X, DISPLAY_SIZE_Y))
        pygame.display.set_caption("Tetris")
        self.scores_font = pygame.font.Font('freesansbold.ttf', int(0.8 * BLOC_SIZE))
        self.pause_font = pygame.font.Font('freesansbold.ttf', 64)

    def draw_bloc(self, bloc_type, pos, alpha=255):
        bloc_surface = pygame.Surface((BLOC_SIZE, BLOC_SIZE))
        bloc_surface.set_alpha(alpha)

        # draw bloc itself
        bloc_surface.fill(BLOC_COLORS[bloc_type])

        # draw lighter top left corner
        lighter_color = tuple(val * 1.2 for val in BLOC_COLORS[bloc_type])
        pygame.draw.rect(bloc_surface, lighter_color, (0, 0, BLOC_SIZE, BLOC_LIGHT_EFFECT_SIZE))
        pygame.draw.rect(bloc_surface, lighter_color, (0, 0, BLOC_LIGHT_EFFECT_SIZE, BLOC_SIZE))

        # draw darker bottom right corner
        darker_color = tuple(val * 0.8 for val in BLOC_COLORS[bloc_type])
        pygame.draw.rect(bloc_surface, darker_color, (0, BLOC_SIZE - BLOC_LIGHT_EFFECT_SIZE, BLOC_SIZE, BLOC_LIGHT_EFFECT_SIZE))
        pygame.draw.rect(bloc_surface, darker_color, (BLOC_SIZE - BLOC_LIGHT_EFFECT_SIZE, 0, BLOC_LIGHT_EFFECT_SIZE, BLOC_SIZE))

        # restore lighter bottom left triangle
        pygame.draw.polygon(bloc_surface, lighter_color, ((0, BLOC_SIZE - BLOC_LIGHT_EFFECT_SIZE - 1),
                                                          (BLOC_LIGHT_EFFECT_SIZE - 1, BLOC_SIZE - BLOC_LIGHT_EFFECT_SIZE - 1),
                                                          (0, BLOC_SIZE - 1)))

        # restore lighter top right triangle
        pygame.draw.polygon(bloc_surface, lighter_color, ((BLOC_SIZE - 1, 0),
                                                          (BLOC_SIZE - BLOC_LIGHT_EFFECT_SIZE, BLOC_LIGHT_EFFECT_SIZE - 1),
                                                          (BLOC_SIZE - BLOC_LIGHT_EFFECT_SIZE, 0)))

        self.display.blit(bloc_surface, (int((pos.x + 1) * BLOC_SIZE), int((pos.y + 1) * BLOC_SIZE)))

    def draw_board_contour(self):
        # draw board background
        pygame.draw.rect(self.display, (0, 0, 0), (0, 0, BOARD_SIZE_X * BLOC_SIZE, BOARD_SIZE_Y * BLOC_SIZE))

        # draw top blocs
        for i in range(-1, BOARD_SIZE_X - 1):
            self.draw_bloc(0, Position(i, -1))

        # draw bottom blocs
        for i in range(-1, BOARD_SIZE_X - 1):
            self.draw_bloc(0, Position(i, SIZE_Y))

        # draw left blocs
        for i in range(-1, BOARD_SIZE_Y - 1):
            self.draw_bloc(0, Position(-1, i))

        # draw right blocs
        for i in range(-1, BOARD_SIZE_Y - 1):
            self.draw_bloc(0, Position(SIZE_X, i))

    def draw_right_panel(self):
        # draw panel background
        pygame.draw.rect(self.display, (220, 220, 220), (int(BOARD_SIZE_X * BLOC_SIZE), 0, RIGHT_PANEL_SIZE_X * BLOC_SIZE, BOARD_SIZE_Y * BLOC_SIZE))
        
        # draw next bloc contour
        # draw top blocs
        for i in range(BOARD_SIZE_X, BOARD_SIZE_X + RIGHT_PANEL_SIZE_X):
            self.draw_bloc(0, Position(i - 1, -1))

        # draw bottom blocs
        for i in range(BOARD_SIZE_X, BOARD_SIZE_X + RIGHT_PANEL_SIZE_X):
            self.draw_bloc(0, Position(i - 1, NEXT_BLOC_FRAME_HEIGHT))

        # draw right blocs
        for i in range(NEXT_BLOC_FRAME_HEIGHT):
            self.draw_bloc(0, Position(SIZE_X + RIGHT_PANEL_SIZE_X, i))

        # draw next piece
        x_correction = - 2 if self.game_state.next_piece_type not in {TYPES['I'], TYPES['O']} else - 2.5
        y_correction = - 1 if self.game_state.next_piece_type != TYPES['I'] else - 0.5
        next_piece = Piece(self.game_state.next_piece_type, Position(BOARD_SIZE_X + RIGHT_PANEL_SIZE_X // 2 + x_correction, NEXT_BLOC_FRAME_HEIGHT // 2 + y_correction))
        for bloc in next_piece.blocs:
            self.draw_bloc(bloc.type, bloc.pos)

        # draw lines cleared
        text_surface = self.scores_font.render("LINES: {}".format(self.game_state.lines_cleared), True, BLACK)
        self.display.blit(text_surface, ((BOARD_SIZE_X + 0.05 * RIGHT_PANEL_SIZE_X) * BLOC_SIZE, int(0.3 * DISPLAY_SIZE_Y)))

    def draw_board(self):
        for i in range(SIZE_X):
            for j in range(SIZE_Y):
                if self.game_state.board[i][j] is not None:
                    self.draw_bloc(self.game_state.board[i][j], Position(i, j))

        for bloc in self.game_state.get_preview_piece().blocs:
            self.draw_bloc(bloc.type, bloc.pos, alpha=64)

        for bloc in self.game_state.cur_piece.blocs:
            self.draw_bloc(bloc.type, bloc.pos)

    def draw_pause_screen(self):
        pause_surface = pygame.Surface((DISPLAY_SIZE_X, DISPLAY_SIZE_Y))
        pause_surface.set_alpha(200)
        pause_surface.fill((100, 100, 100))
        self.display.blit(pause_surface, (0, 0))

        text = self.pause_font.render('Pause', True, (180, 180, 180))
        text_rect = text.get_rect()
        text_rect.center = (DISPLAY_SIZE_X // 2, DISPLAY_SIZE_Y // 2)
        self.display.blit(text, text_rect)

    def draw(self):
        self.display.fill((0, 0, 0))
        self.draw_board_contour()
        self.draw_right_panel()
        self.draw_board()
        if self.game_state.is_paused:
            self.draw_pause_screen()
        pygame.display.update()
