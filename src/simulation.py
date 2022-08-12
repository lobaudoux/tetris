import time

from agent import *
from tetris import *


def main():
    n_games = 100
    results = []

    start = time.time()

    for i in range(1, n_games + 1):
        game_state = Tetris()
        agent = Agent(game_state)
        lateral_input, fall_input, change_orientation_input = agent.get_action()
        while game_state.next_state(lateral_input, fall_input, change_orientation_input, False):
            lateral_input, fall_input, change_orientation_input = agent.get_action()

        print(f"Game {i} finished, {game_state.lines_cleared} lines cleared !")
        results.append(game_state.lines_cleared)

    results.sort()
    mean_lines_cleared = round(sum(results) / len(results), 2)
    print(f"Min number of lines cleared is {results[0]} lines")
    print(f"Max number of lines cleared is {results[-1]} lines")
    print(f"Mean number of lines cleared is {mean_lines_cleared} lines")
    print(f"Median number of lines cleared is {results[len(results) // 2]} lines")
    print(f"It took {round(time.time() - start, 2)} seconds to run")


if __name__ == '__main__':
    main()
