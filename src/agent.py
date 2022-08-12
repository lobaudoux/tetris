from copy import deepcopy

from constants import *
from tetris import *
from util import *


class Agent:
    def __init__(self, game_state):
        self.game_state = game_state
        self.next_actions = []
        self.cur_piece = None

    def get_action(self):
        if self.game_state.cur_piece != self.cur_piece:
            self.cur_piece = self.game_state.cur_piece
            n_orientations = 1 if self.game_state.cur_piece.type == TYPES['O'] else 2 if self.game_state.cur_piece.type in [TYPES['I'], TYPES['S'], TYPES['Z']] else 4
            next_states = []
            for i in range(n_orientations):
                self.game_state.cur_piece = deepcopy(self.cur_piece)
                for _ in range(i):
                    self.game_state.change_orientation()

                # let the bloc fall straight down
                actions = ['change_orientation' for _ in range(i)]
                score = self.get_score_if_bloc_fall()
                next_states.append({
                    'score': score,
                    'actions': actions,
                })

                # try to move it on the left
                n_left_moves = 0
                while self.game_state.shift_piece_x(self.game_state.cur_piece, -1):
                    n_left_moves += 1
                    actions = ['left' for _ in range(n_left_moves)]
                    actions.extend(['change_orientation' for _ in range(i)])

                    score = self.get_score_if_bloc_fall()
                    next_states.append({
                        'score': score,
                        'actions': actions,
                    })

                self.game_state.shift_piece_x(self.game_state.cur_piece, n_left_moves)

                # try to move it on the right
                n_right_moves = 0
                while self.game_state.shift_piece_x(self.game_state.cur_piece, 1):
                    n_right_moves += 1
                    actions = ['right' for _ in range(n_right_moves)]
                    actions.extend(['change_orientation' for _ in range(i)])

                    score = self.get_score_if_bloc_fall()
                    next_states.append({
                        'score': score,
                        'actions': actions,
                    })

            self.game_state.cur_piece = self.cur_piece

            self.next_actions = max(next_states, key=lambda state: state['score'])['actions']

        if self.next_actions:
            action = self.next_actions.pop()
            if action == 'change_orientation':
                return None, False, True
            elif action == 'left':
                return 'left', False, False
            elif action == 'right':
                return 'right', False, False
        else:
            return None, True, False

    def evaluate_state(self, piece):
        board = self.game_state.board

        # find the number of empty cells columns which have a bloc above them
        empty_pos_with_bloc_on_top = 0
        for x in range(SIZE_X):
            y = SIZE_Y - 1
            while y >= 0:
                empty_cells = 0
                while y >= 0 and board[x][y] is not None:
                    y -= 1
                while y >= 0 and board[x][y] is None:
                    empty_cells += 1
                    y -= 1
                if y >= 0:
                    empty_pos_with_bloc_on_top += empty_cells

        # find the maximum depth of the board
        max_depth = 0
        for x in range(SIZE_X):
            depth = 0
            y = 0
            # find the first bloc in that column
            while y < SIZE_Y and board[x][y] is None:
                y += 1
            y -= 1  # we need to go up one cell as we want to be on the first cell above the bloc (or the base of the board)

            while y >= 0 and (x - 1 < 0 or board[x - 1][y] is not None) and (x + 1 >= SIZE_X or board[x + 1][y] is not None):
                y -= 1
                depth += 1
            if depth > max_depth:
                max_depth = depth

        # mean height of the newly placed bloc
        mean_bloc_height = sum(SIZE_Y - bloc.pos.y for bloc in piece.blocs) / 4

        return -30 * empty_pos_with_bloc_on_top - 10 * mean_bloc_height - 10 * max_depth

    def get_score_if_bloc_fall(self):
        piece_copied = deepcopy(self.game_state.cur_piece)
        while self.game_state.shift_piece_y(piece_copied, 0.99):
            pass
        for bloc in piece_copied.blocs:
            self.game_state.board[bloc.pos.x][int(bloc.pos.y)] = bloc.type
        score = self.evaluate_state(piece_copied)
        for bloc in piece_copied.blocs:
            self.game_state.board[bloc.pos.x][int(bloc.pos.y)] = None

        return score
