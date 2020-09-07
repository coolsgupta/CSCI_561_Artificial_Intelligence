from collections import deque
import heapq
import traceback


class DictKeys:
    LAST_STATE = 'last_state'
    ACTION_TAKEN_TO_REACH = 'action_taken_to_reach'
    COST_OF_LAST_STEP = 'cost_of_last_step'


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

        data[1:] = [tuple(map(int, x.split())) for x in data[1:]]
        return data

    @staticmethod
    def write_file():
        return

    @staticmethod
    def cal_euclidean_distance(point_1, point_2):
        return sum([(x-y)**2 for x, y in zip(list(point_1), list(point_2))])**0.5

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
        self.adjacency_map = {}
        self.reached_goal = False

    def get_action_point_action_map(self, action_point_action_list):
        return {tuple(x[:3]): list(x[3:]) for x in action_point_action_list}

    def find_reachable_points(self, current_point, allowed_actions):
        reachable_points_from_action = {}
        for action in allowed_actions:
            next_state = Utils.add_action_step(current_point, action)
            if next_state in self.action_points:
                reachable_points_from_action[next_state] = {
                    DictKeys.LAST_STATE: current_point,
                    DictKeys.ACTION_TAKEN_TO_REACH: action,
                    DictKeys.COST_OF_LAST_STEP: Utils.cal_euclidean_distance(current_point, next_state)
                }

        return reachable_points_from_action


class BFSPathFinder(PathFinder):
    def __init__(self, data):
        super(BFSPathFinder, self).__init__(data)

    def backtrack_path(self):
        current_state = self.goal_location
        path = deque()
        path.append(self.goal_location)
        cost = 0
        while current_state != self.entrance_location:
            current_state = self.adjacency_map.get(current_state, {}).get(DictKeys.LAST_STATE)
            cost += Utils.cal_euclidean_distance(current_state, path[-1])
            path.append(current_state)
        return path, cost

    def bfs(self):
        visited, bfs_queue = set([self.entrance_location]), deque([self.entrance_location])
        while bfs_queue:
            current_state = bfs_queue.popleft()
            reachable_states = self.find_reachable_points(current_state, self.action_points.get(current_state, []))
            if current_state == self.goal_location:
                self.reached_goal = True
                break

            for state in reachable_states:
                if state not in visited:
                    visited.add(state)
                    bfs_queue.append(state)
                    self.adjacency_map[state] = reachable_states[state]

        if self.reached_goal:
            path, cost = self.backtrack_path()
            return path, cost

        else:
            raise Exception('Path not found')


if __name__ == '__main__':
    input_case = 'asnlib/public/sample/input1.txt'
    try:
        path_finder = BFSPathFinder(Utils.read_file(input_case))
        path, cost = path_finder.bfs()

    except Exception as e:
        print(traceback.format_exc())
        result = 'Fail'

    print('Done')


