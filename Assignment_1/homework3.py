import numpy as np


class Utils:

    actions_map = {
        1 :  (1,0,0),
        2 :  (-1,0,0),
        3 :  (0,1,0),
        4 :  (0,-1,0),
        5 :  (0,0,1),
        6 :  (0,0,-1),
        7 :  (1,1,0),
        8 :  (1,-1,0),
        9 :  (-1,1,0),
        10 : (-1,-1,0),
        11 : (1,0,1),
        12 : (1,0,-1),
        13 : (-1,0,1),
        14 : (-1,0,-1),
        15 : (0,1,1),
        16 : (0,1,-1),
        17 : (0,-1,1),
        18 : (0,-1,-1),
    }

    @staticmethod
    def read_file(input_path):
        with open(input_path) as input_file:
            data = [x.strip() for x in input_file.readlines()]

        data[1:] = [list(map(int, x.split())) for x in data[1:]]
        return data

    @staticmethod
    def write_file():
        return

    @staticmethod
    def cal_euclidean_distance(point_1, point_2):
        return sum([(x-y)**2 for x,y in zip(point_1, point_2)])**0.5

    @staticmethod
    def add_action_step(current_point, action):
        return tuple(map(lambda i, j: i + j, current_point, Utils.actions_map[action]))


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


class BFSPathFinder(PathFinder):
    def __init__(self, data):
        super(BFSPathFinder, self).__init__(data)

    def find_reachable_points(self, current_point, allowed_actions):
        reachable_points_from_action = {}
        for action in allowed_actions:
            next_state = Utils.add_action_step(current_point, action)
            if next_state in self.action_points:
                reachable_points_from_action[next_state] = action

        return reachable_points_from_action


if __name__ == '__main__':
    input_case = 'asnlib/public/sample/input1.txt'
    path_finder = PathFinder(Utils.read_file(input_case))
    print('Done')
