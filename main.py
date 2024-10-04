from algorithms.Wave_algorithm import wavefront
from algorithms.IDDFS import iddfs
from algorithms.Jump_point_search import jps
from algorithms.auxiliary_functions import create_context
from config.settings import window_config
from visuals.visualization import generator
from algorithms.A_star import searching_of_path
from maze.сreating_a_maze import divide_window

import random

class Main:
    def __init__(self, algorithms: list[callable], num_parts: int, seed: int = random.randint(0, 100000)):
        self.algorithms = algorithms
        self.num_parts = num_parts
        self.parts = divide_window(window_config.screenSize[0], window_config.screenSize[0], num_parts)
        self.data = [create_context(part, seed) for part in self.parts]

    def start_process(self):
        generator(self.algorithms, self.data)


if __name__ == '__main__':
    start = Main([searching_of_path, jps, iddfs, wavefront], 4) 
    start.start_process()