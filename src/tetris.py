from copy import deepcopy
import math
import random

from constants import *
from util import *


class Tetris:
    def __init__(self, fall_speed):
        self.fall_speed = fall_speed
        self.is_paused = False
        self.lost = False
        self.frame_count = 0
        self.first_stuck_frame = None
        self.cur_piece = Piece(random.randint(1, 7), Position(SIZE_X // 2 - 1, 1))
        self.next_piece_type = random.randint(1, 7)
        self.board = [[None for _ in range(SIZE_Y)] for _ in range(SIZE_X)]
        self.lines_cleared = 0

    def next_state(self, lateral_input, fall_input, change_orientation_input, pause_input):
        if pause_input:
            self.is_paused = not self.is_paused
        if not self.is_paused:
            self.frame_count += 1

            if change_orientation_input:
                self.change_orientation()

            if lateral_input is not None:
                if lateral_input == 'left':
                    self.shift_piece_x(self.cur_piece, -1)
                elif lateral_input == 'right':
                    self.shift_piece_x(self.cur_piece, 1)

            if fall_input:
                for _ in range(5):
                    self.shift_piece_y(self.cur_piece, self.fall_speed)

            if not self.shift_piece_y(self.cur_piece, self.fall_speed):
                if self.first_stuck_frame is None:
                    self.first_stuck_frame = self.frame_count
                elif self.frame_count - self.first_stuck_frame > STUCK_FRAME_TOLERANCE:
                    for bloc in self.cur_piece.blocs:
                        self.board[bloc.pos.x][int(bloc.pos.y)] = bloc.type
                    self.cur_piece = Piece(self.next_piece_type, Position(SIZE_X // 2 - 1, 1))
                    self.next_piece_type = random.randint(1, 7)
                    self.first_stuck_frame = None
                else:
                    pass
            else:
                self.first_stuck_frame = None

            self.clear_lines()

            # check if the game is finished
            for bloc in self.cur_piece.blocs:
                if self.board[bloc.pos.x][int(bloc.pos.y)] is not None:
                    return False
        return True

    def shift_piece_x(self, piece, distance):
        for bloc in piece.blocs:
            new_x = bloc.pos.x + distance
            if not 0 <= new_x <= SIZE_X - 1:
                return False
            if self.board[new_x][math.floor(bloc.pos.y)] is not None or self.board[new_x][math.ceil(bloc.pos.y)] is not None:
                return False
        for bloc in piece.blocs:
            bloc.pos.x += distance
        return True

    def shift_piece_y(self, piece, distance):
        collision_detected = False
        for bloc in piece.blocs:
            new_y = bloc.pos.y + distance
            if not new_y <= SIZE_Y - 1:
                distance = min(distance, SIZE_Y - 1 - bloc.pos.y)
                collision_detected = True
            elif self.board[bloc.pos.x][math.ceil(new_y)] is not None:
                distance = min(distance, math.floor(new_y) - bloc.pos.y)
                collision_detected = True
        if collision_detected:
            for bloc in piece.blocs:
                bloc.pos.y = round(bloc.pos.y + distance)
            return False
        else:
            for bloc in piece.blocs:
                bloc.pos.y += distance
            return True

    def is_pos_valid(self, piece):
        for bloc in piece.blocs:
            if not 0 <= bloc.pos.x <= SIZE_X - 1 or not 0 <= bloc.pos.y <= SIZE_Y - 1 or \
                    self.board[bloc.pos.x][math.floor(bloc.pos.y)] is not None or self.board[bloc.pos.x][math.ceil(bloc.pos.y)] is not None:
                return False
        return True

    def change_orientation(self):
        piece_copy = deepcopy(self.cur_piece)
        if piece_copy.type == TYPES['I']:
            if piece_copy.orientation == 0:
                piece_copy.blocs[0].pos.x += 1
                piece_copy.blocs[0].pos.y -= 1
                piece_copy.blocs[2].pos.x -= 1
                piece_copy.blocs[2].pos.y += 1
                piece_copy.blocs[3].pos.x -= 2
                piece_copy.blocs[3].pos.y += 2
                piece_copy.orientation = 1
            elif piece_copy.orientation == 1:
                piece_copy.blocs[0].pos.x -= 1
                piece_copy.blocs[0].pos.y += 1
                piece_copy.blocs[2].pos.x += 1
                piece_copy.blocs[2].pos.y -= 1
                piece_copy.blocs[3].pos.x += 2
                piece_copy.blocs[3].pos.y -= 2
                piece_copy.orientation = 0
        elif piece_copy.type == TYPES['O']:
            return
        elif piece_copy.type == TYPES['T']:
            if piece_copy.orientation == 0:
                piece_copy.blocs[0].pos.x += 1
                piece_copy.blocs[0].pos.y += 1
                piece_copy.blocs[1].pos.x += 1
                piece_copy.blocs[1].pos.y -= 1
                piece_copy.blocs[3].pos.x -= 1
                piece_copy.blocs[3].pos.y += 1
                piece_copy.orientation = 1
            elif piece_copy.orientation == 1:
                piece_copy.blocs[0].pos.x -= 1
                piece_copy.blocs[0].pos.y += 1
                piece_copy.blocs[1].pos.x += 1
                piece_copy.blocs[1].pos.y += 1
                piece_copy.blocs[3].pos.x -= 1
                piece_copy.blocs[3].pos.y -= 1
                piece_copy.orientation = 2
            elif piece_copy.orientation == 2:
                piece_copy.blocs[0].pos.x -= 1
                piece_copy.blocs[0].pos.y -= 1
                piece_copy.blocs[1].pos.x -= 1
                piece_copy.blocs[1].pos.y += 1
                piece_copy.blocs[3].pos.x += 1
                piece_copy.blocs[3].pos.y -= 1
                piece_copy.orientation = 3
            elif piece_copy.orientation == 3:
                piece_copy.blocs[0].pos.x += 1
                piece_copy.blocs[0].pos.y -= 1
                piece_copy.blocs[1].pos.x -= 1
                piece_copy.blocs[1].pos.y -= 1
                piece_copy.blocs[3].pos.x += 1
                piece_copy.blocs[3].pos.y += 1
                piece_copy.orientation = 0
        elif piece_copy.type == TYPES['J']:
            if piece_copy.orientation == 0:
                piece_copy.blocs[0].pos.x += 2
                piece_copy.blocs[0].pos.y -= 1
                piece_copy.blocs[1].pos.x += 1
                piece_copy.blocs[1].pos.y -= 2
                piece_copy.blocs[2].pos.y -= 1
                piece_copy.blocs[3].pos.x -= 1
                piece_copy.orientation = 1
            elif piece_copy.orientation == 1:
                piece_copy.blocs[0].pos.y += 2
                piece_copy.blocs[1].pos.x += 1
                piece_copy.blocs[1].pos.y += 1
                piece_copy.blocs[3].pos.x -= 1
                piece_copy.blocs[3].pos.y -= 1
                piece_copy.orientation = 2
            elif piece_copy.orientation == 2:
                piece_copy.blocs[0].pos.x -= 2
                piece_copy.blocs[1].pos.x -= 1
                piece_copy.blocs[1].pos.y += 1
                piece_copy.blocs[3].pos.x += 1
                piece_copy.blocs[3].pos.y -= 1
                piece_copy.orientation = 3
            elif piece_copy.orientation == 3:
                piece_copy.blocs[0].pos.y -= 1
                piece_copy.blocs[1].pos.x -= 1
                piece_copy.blocs[2].pos.y += 1
                piece_copy.blocs[3].pos.x += 1
                piece_copy.blocs[3].pos.y += 2
                piece_copy.orientation = 0
        elif piece_copy.type == TYPES['L']:
            if piece_copy.orientation == 0:
                piece_copy.blocs[0].pos.y += 1
                piece_copy.blocs[1].pos.x += 1
                piece_copy.blocs[1].pos.y -= 2
                piece_copy.blocs[2].pos.y -= 1
                piece_copy.blocs[3].pos.x -= 1
                piece_copy.orientation = 1
            elif piece_copy.orientation == 1:
                piece_copy.blocs[0].pos.x -= 2
                piece_copy.blocs[1].pos.x += 1
                piece_copy.blocs[1].pos.y += 1
                piece_copy.blocs[3].pos.x -= 1
                piece_copy.blocs[3].pos.y -= 1
                piece_copy.orientation = 2
            elif piece_copy.orientation == 2:
                piece_copy.blocs[0].pos.y -= 2
                piece_copy.blocs[1].pos.x -= 1
                piece_copy.blocs[1].pos.y += 1
                piece_copy.blocs[3].pos.x += 1
                piece_copy.blocs[3].pos.y -= 1
                piece_copy.orientation = 3
            elif piece_copy.orientation == 3:
                piece_copy.blocs[0].pos.x += 2
                piece_copy.blocs[0].pos.y += 1
                piece_copy.blocs[1].pos.x -= 1
                piece_copy.blocs[2].pos.y += 1
                piece_copy.blocs[3].pos.x += 1
                piece_copy.blocs[3].pos.y += 2
                piece_copy.orientation = 0
        elif piece_copy.type == TYPES['S']:
            if piece_copy.orientation == 0:
                piece_copy.blocs[1].pos.x -= 1
                piece_copy.blocs[1].pos.y -= 1
                piece_copy.blocs[2].pos.x += 2
                piece_copy.blocs[3].pos.x += 1
                piece_copy.blocs[3].pos.y -= 1
                piece_copy.orientation = 1
            elif piece_copy.orientation == 1:
                piece_copy.blocs[1].pos.x += 1
                piece_copy.blocs[1].pos.y += 1
                piece_copy.blocs[2].pos.x -= 2
                piece_copy.blocs[3].pos.x -= 1
                piece_copy.blocs[3].pos.y += 1
                piece_copy.orientation = 0
        elif piece_copy.type == TYPES['Z']:
            if piece_copy.orientation == 0:
                piece_copy.blocs[0].pos.x += 1
                piece_copy.blocs[0].pos.y -= 1
                piece_copy.blocs[2].pos.x -= 1
                piece_copy.blocs[2].pos.y -= 1
                piece_copy.blocs[3].pos.x -= 2
                piece_copy.orientation = 1
            elif piece_copy.orientation == 1:
                piece_copy.blocs[0].pos.x -= 1
                piece_copy.blocs[0].pos.y += 1
                piece_copy.blocs[2].pos.x += 1
                piece_copy.blocs[2].pos.y += 1
                piece_copy.blocs[3].pos.x += 2
                piece_copy.orientation = 0
        if self.is_pos_valid(piece_copy):
            self.set_piece_as_cur_piece(piece_copy)
        else:
            for bloc in piece_copy.blocs:
                if not 0 <= bloc.pos.y <= SIZE_Y - 1:
                    break  # one of the bloc is outside of the board on the y-axis, it's useless to try to shift it on the x-axis
            else:
                if self.shift_piece_x(piece_copy, 1):
                    self.set_piece_as_cur_piece(piece_copy)
                elif self.shift_piece_x(piece_copy, -1):
                    self.set_piece_as_cur_piece(piece_copy)
                elif piece_copy.type == TYPES['I']:
                    if self.shift_piece_x(piece_copy, 2):
                        self.set_piece_as_cur_piece(piece_copy)
                    elif self.shift_piece_x(piece_copy, -2):
                        self.set_piece_as_cur_piece(piece_copy)

    def set_piece_as_cur_piece(self, piece):
        # not changing the current piece id is useful for the agent to detect when a new piece is generated
        self.cur_piece.type = piece.type
        for i in range(4):
            self.cur_piece.blocs[i] = piece.blocs[i]
        self.cur_piece.orientation = piece.orientation

    def clear_lines(self):
        lines_to_clear = []
        for j in range(SIZE_Y):
            for i in range(SIZE_X):
                if self.board[i][j] is None:
                    break
            else:
                lines_to_clear.append(j)
        for line_index in lines_to_clear:
            for i in range(SIZE_X):
                del self.board[i][line_index]
                self.board[i].insert(0, None)
        self.lines_cleared += len(lines_to_clear)

    def get_preview_piece(self):
        preview_piece = deepcopy(self.cur_piece)
        while self.shift_piece_y(preview_piece, 0.99):
            pass
        return preview_piece


class Piece:
    def __init__(self, piece_type, position=None):
        self.blocs = None
        self.type = piece_type
        if position:
            if piece_type == TYPES['I']:
                self.blocs = [
                    Bloc(piece_type, Position(position.x - 1, position.y)),
                    Bloc(piece_type, Position(position.x, position.y)),
                    Bloc(piece_type, Position(position.x + 1, position.y)),
                    Bloc(piece_type, Position(position.x + 2, position.y)),
                ]
            elif piece_type == TYPES['O']:
                self.blocs = [
                    Bloc(piece_type, Position(position.x, position.y)),
                    Bloc(piece_type, Position(position.x + 1, position.y)),
                    Bloc(piece_type, Position(position.x, position.y + 1)),
                    Bloc(piece_type, Position(position.x + 1, position.y + 1)),
                ]
            elif piece_type == TYPES['T']:
                self.blocs = [
                    Bloc(piece_type, Position(position.x, position.y)),
                    Bloc(piece_type, Position(position.x - 1, position.y + 1)),
                    Bloc(piece_type, Position(position.x, position.y + 1)),
                    Bloc(piece_type, Position(position.x + 1, position.y + 1)),
                ]
            elif piece_type == TYPES['J']:
                self.blocs = [
                    Bloc(piece_type, Position(position.x - 1, position.y)),
                    Bloc(piece_type, Position(position.x - 1, position.y + 1)),
                    Bloc(piece_type, Position(position.x, position.y + 1)),
                    Bloc(piece_type, Position(position.x + 1, position.y + 1)),
                ]
            elif piece_type == TYPES['L']:
                self.blocs = [
                    Bloc(piece_type, Position(position.x + 1, position.y)),
                    Bloc(piece_type, Position(position.x - 1, position.y + 1)),
                    Bloc(piece_type, Position(position.x, position.y + 1)),
                    Bloc(piece_type, Position(position.x + 1, position.y + 1)),
                ]
            elif piece_type == TYPES['S']:
                self.blocs = [
                    Bloc(piece_type, Position(position.x, position.y)),
                    Bloc(piece_type, Position(position.x + 1, position.y)),
                    Bloc(piece_type, Position(position.x - 1, position.y + 1)),
                    Bloc(piece_type, Position(position.x, position.y + 1)),
                ]
            elif piece_type == TYPES['Z']:
                self.blocs = [
                    Bloc(piece_type, Position(position.x - 1, position.y)),
                    Bloc(piece_type, Position(position.x, position.y)),
                    Bloc(piece_type, Position(position.x, position.y + 1)),
                    Bloc(piece_type, Position(position.x + 1, position.y + 1)),
                ]
        self.orientation = 0

    def __copy__(self):
        new_piece = Piece(self.type)
        new_piece.blocs = self.blocs

    def __str__(self):
        return ", ".join(str(bloc) for bloc in self.blocs)


class Bloc:
    def __init__(self, bloc_type, position):
        self.type = bloc_type
        self.pos = position

    def __copy__(self):
        return Bloc(self.type, self.pos)

    def __str__(self):
        return str((self.type, str(self.pos)))
