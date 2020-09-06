import numpy as np


class Utils:
    @staticmethod
    def read_file(input_path):
        with open(input_path) as input_file:
            data = [x.strip() for x in input_file.readlines()]

        data[1:] = [list(map(int, x.split())) for x in data[1:]]
        return data

    @staticmethod
    def write_file():
        return


class PathFinder:
    def __init__(self, data):
        self.algo = data[0]
        self.grid_dimensions = data[1]
        self.entrance_location = data[2]
        self.goal_location = data[3]
        self.num_action_points = data[4]
        self.action_points = self.get_action_point_action_map(data[5:])

    def get_action_point_action_map(self, action_point_action_list):
        return {tuple(x[:3]): x[3:] for x in action_point_action_list}


if __name__ == '__main__':
    input_case = 'asnlib/public/sample/input1.txt'
    path_finder = PathFinder(Utils.read_file(input_case))
    print('Done')
