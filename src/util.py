from constants import *

UNVISITED = 0


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __copy__(self):
        return Position(self.x, self.y)

    def __str__(self):
        return str((self.x, self.y))


class ConnectedComponents:
    def __init__(self, board):
        self.board = board
        self.cc_board = [[UNVISITED for _ in range(SIZE_Y)] for _ in range(SIZE_X)]
        self.cur_connected_component_id = 1

    def get_neighbours(self, pos):
        neighbours = []
        new_pos = Position(pos.x + 1, pos.y)
        if new_pos.x < SIZE_X and self.board[new_pos.x][new_pos.y] is None:
            neighbours.append(new_pos)

        new_pos = Position(pos.x - 1, pos.y)
        if new_pos.x >= 0 and self.board[new_pos.x][new_pos.y] is None:
            neighbours.append(new_pos)

        new_pos = Position(pos.x, pos.y + 1)
        if new_pos.y < SIZE_Y and self.board[new_pos.x][new_pos.y] is None:
            neighbours.append(new_pos)

        new_pos = Position(pos.x, pos.y - 1)
        if new_pos.y >= 0 and self.board[new_pos.x][new_pos.y] is None:
            neighbours.append(new_pos)
        return neighbours

    def visit(self, pos):
        self.cc_board[pos.x][pos.y] = self.cur_connected_component_id
        for neighbour in self.get_neighbours(pos):
            if not self.cc_board[neighbour.x][neighbour.y]:
                self.visit(neighbour)

    def get_connected_components(self):
        for x in range(SIZE_X):
            for y in range(SIZE_Y):
                if self.cc_board[x][y] == UNVISITED and self.board[x][y] is None:
                    self.visit(Position(x, y))
                    self.cur_connected_component_id += 1
        return self.cc_board, self.cur_connected_component_id - 1
