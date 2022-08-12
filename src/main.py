import sys

from agent import *
from constants import *
from gui import *
from tetris import *

import pygame
from pygame.locals import *


def main():
    if len(sys.argv) > 1:
        try:
            fall_speed = float(sys.argv[1])
        except ValueError:
            print("The fall speed must be a number between 0 and 1", file=sys.stderr)
            exit(-1)
    else:
        fall_speed = FALL_SPEED

    assert 0 < fall_speed < 1, "The fall speed must be a number between 0 and 1"

    game_state = Tetris(fall_speed)
    agent = Agent(game_state)
    gui = GUI(game_state)
    gui.draw()

    human_playing = False
    frame_count = 0
    last_frame_lateral_input = 0
    while True:
        pygame.time.Clock().tick(FPS)
        change_orientation_input = False
        pause_input = False
        lateral_input = None
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    change_orientation_input = True
                if event.key == K_LEFT:
                    lateral_input = 'left'
                    last_frame_lateral_input = frame_count
                if event.key == K_RIGHT:
                    lateral_input = 'right'
                    last_frame_lateral_input = frame_count
                if event.key == K_ESCAPE:
                    pause_input = True
                if event.key == K_SPACE:
                    human_playing = not human_playing
                    print("Human" if human_playing else "Agent", "is playing.")

        if human_playing:
            keys_pressed = pygame.key.get_pressed()
            fall_input = bool(keys_pressed[K_DOWN])
            if keys_pressed[K_LEFT] and frame_count - last_frame_lateral_input > 5:
                lateral_input = 'left'
                last_frame_lateral_input = frame_count
            elif keys_pressed[K_RIGHT] and frame_count - last_frame_lateral_input > 5:
                lateral_input = 'right'
                last_frame_lateral_input = frame_count
        else:
            lateral_input, fall_input, change_orientation_input = agent.get_action()

        is_game_finished = not game_state.next_state(lateral_input, fall_input, change_orientation_input, pause_input)
        gui.draw()

        if is_game_finished:
            print("Game finished")
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

        frame_count += 1


if __name__ == '__main__':
    main()
