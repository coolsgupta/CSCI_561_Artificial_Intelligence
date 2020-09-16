from collections import deque
from queue import PriorityQueue
import traceback
import time


class Constants:
    LAST_STATE = 'last_state'
    ACTION_TAKEN_TO_REACH = 'action_taken_to_reach'
    COST_OF_LAST_STEP = 'cost_of_last_step'
    COST_TILL_CURRENT_STEP = 'cost_till_current_path'
    D1_dist = 10
    D2_dist = 14


class Utils:
    @staticmethod
    def read_file(input_path):
        with open(input_path) as input_file:
            data = [x.strip() for x in input_file.readlines()]

        data[1:] = [tuple(map(int, x.split())) for x in data[1:]]
        return data

    @staticmethod
    def write_file(path, cost, results_file_name):
        results = [str(cost)]
        if path:
            results.append(str(len(path)))
            for i in range(len(path) - 1, -1, -1):
                results.append('{} {}'.format(' '.join(map(str, path[i][0])), str(path[i][1])))

        with open(results_file_name, 'w') as result_file:
            result_file.write('\n'.join(results))

    @staticmethod
    def get_path_finder(data):
        if data[0] == 'BFS':
            return BFSPathFinder(data)

        if data[0] == 'UCS':
            return UCSPathFinder(data)

        if data[0] == 'A*':
            return AStarPathFinder(data)


class PathFinder:
    def __init__(self, data):
        self.ACTIONS_MAP = {
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
        self.algo = data[0]
        self.grid_dimensions = data[1]
        self.entrance_location = data[2]
        self.goal_location = data[3]
        self.num_action_points = data[4]
        self.action_points_actions_map = {tuple(x[:3]): list(x[3:]) for x in data[5:]}
        self.adjacency_map = {
            self.entrance_location: {
                Constants.LAST_STATE: (-1, -1, -1),
                Constants.ACTION_TAKEN_TO_REACH: -1,
                Constants.COST_OF_LAST_STEP: 0,
                Constants.COST_TILL_CURRENT_STEP: 0
            }
        }
        self.reached_goal = False

    def get_algo(self):
        return self.algo

    def cal_euclidean_distance(self, point_1, point_2):
        # return sum([(x-y)**2 for x, y in zip(list(point_1), list(point_2))])**0.5
        return Constants.D1_dist if abs(sum(map(lambda i, j: i - j, point_1, point_2))) == 1 else Constants.D2_dist

    def add_action_step(self, current_point, action):
        return tuple(map(lambda i, j: i + j, current_point, self.ACTIONS_MAP[action]))

    def find_reachable_points(self, current_point, allowed_actions):
        reachable_points_from_action = {}
        for action in allowed_actions:
            next_state = self.add_action_step(current_point, action)

            if next_state in self.action_points_actions_map:
                cost_to_reach_from_last_state = self.cal_euclidean_distance(current_point, next_state)
                reachable_points_from_action[next_state] = {
                    Constants.LAST_STATE: current_point,
                    Constants.ACTION_TAKEN_TO_REACH: action,
                    Constants.COST_OF_LAST_STEP: cost_to_reach_from_last_state,
                    Constants.COST_TILL_CURRENT_STEP: self.adjacency_map
                        .get(current_point, {}).get(Constants.COST_TILL_CURRENT_STEP, 0) + cost_to_reach_from_last_state
                }

        return reachable_points_from_action

    def backtrack_path(self):
        current_state = self.goal_location
        traced_path = deque()
        traced_path.append(
            (self.goal_location, self.adjacency_map.get(self.goal_location, {}).get(Constants.COST_OF_LAST_STEP, 0))
        )

        while current_state != self.entrance_location:
            current_state = self.adjacency_map.get(current_state, {}).get(Constants.LAST_STATE, 0)
            cost_to_reach = self.adjacency_map.get(current_state, {}).get(Constants.COST_OF_LAST_STEP, 0)
            traced_path.append((current_state, cost_to_reach))

        return traced_path, self.adjacency_map.get(self.goal_location, {}).get(Constants.COST_TILL_CURRENT_STEP, 0)


class BFSPathFinder(PathFinder):
    def __init__(self, data):
        super(BFSPathFinder, self).__init__(data)

    def find_reachable_points(self, current_point, allowed_actions):
        reachable_points_from_action = {}
        for action in allowed_actions:
            next_state = self.add_action_step(current_point, action)

            if next_state in self.action_points_actions_map:
                cost_to_reach_from_last_state = 1
                reachable_points_from_action[next_state] = {
                    Constants.LAST_STATE: current_point,
                    Constants.ACTION_TAKEN_TO_REACH: action,
                    Constants.COST_OF_LAST_STEP: cost_to_reach_from_last_state,
                    Constants.COST_TILL_CURRENT_STEP: self.adjacency_map
                        .get(current_point, {}).get(Constants.COST_TILL_CURRENT_STEP, 0) + cost_to_reach_from_last_state
                }

        return reachable_points_from_action


    def find_path(self):
        visited, bfs_queue = {self.entrance_location}, deque([self.entrance_location])
        while bfs_queue:
            current_state = bfs_queue.popleft()
            reachable_states = self.find_reachable_points(
                current_state,
                self.action_points_actions_map.get(current_state, [])
            )

            if current_state == self.goal_location:
                self.reached_goal = True
                break

            for state in reachable_states:
                if state not in visited:
                    visited.add(state)
                    bfs_queue.append(state)
                    self.adjacency_map[state] = reachable_states[state]

        if self.reached_goal:
            traced_path, traced_path_cost = self.backtrack_path()
            return traced_path, traced_path_cost

        else:
            raise Exception('Path not found')


class UCSPathFinder(PathFinder):
    def __init__(self, data):
        super(UCSPathFinder, self).__init__(data)

    def find_path(self):
        visited, ucs_queue = {self.entrance_location}, PriorityQueue()
        ucs_queue.put((0, self.entrance_location))

        while ucs_queue:
            current_state = ucs_queue.get()[1]
            reachable_states = self.find_reachable_points(
                current_state,
                self.action_points_actions_map.get(current_state, [])
            )

            if current_state == self.goal_location:
                self.reached_goal = True
                break

            for state in reachable_states:
                if state not in visited:
                    visited.add(state)
                    ucs_queue.put((reachable_states[state][Constants.COST_TILL_CURRENT_STEP], state))
                    self.adjacency_map[state] = reachable_states[state]

        if self.reached_goal:
            traced_path, traced_path_cost = self.backtrack_path()
            return traced_path, traced_path_cost

        else:
            raise Exception('Path not found')


class AStarPathFinder(PathFinder):
    def __init__(self, data):
        super(AStarPathFinder, self).__init__(data)

    def heuristic_function(self, state):
        del_dist = sorted(list(map(lambda i, j: abs(i - j), state, self.goal_location)))
        return 10*(del_dist[0] + del_dist[2]) + 4*del_dist[1]

    def find_path(self):
        visited, a_star_queue = {self.entrance_location}, PriorityQueue()
        a_star_queue.put((0, self.entrance_location))

        while a_star_queue:
            current_state = a_star_queue.get()[1]
            reachable_states = self.find_reachable_points(
                current_state,
                self.action_points_actions_map.get(current_state, [])
            )

            if current_state == self.goal_location:
                self.reached_goal = True
                break

            for state in reachable_states:
                if state not in visited:
                    visited.add(state)
                    a_star_queue.put(
                        (
                            reachable_states[state][Constants.COST_TILL_CURRENT_STEP] + self.heuristic_function(state),
                            state
                        )
                    )
                    self.adjacency_map[state] = reachable_states[state]

        if self.reached_goal:
            traced_path, traced_path_cost = self.backtrack_path()
            return traced_path, traced_path_cost

        else:
            raise Exception('Path not found')


if __name__ == '__main__':
    input_case = 'asnlib/public/sample/input13.txt'
    output_file = input_case.split('/')[-1].replace('input', 'output')
    start = time.time()
    try:
        path_finder = Utils.get_path_finder(Utils.read_file(input_case))
        path, cost = path_finder.find_path()
        Utils.write_file(path, cost, output_file)

    except Exception as e:
        print(traceback.format_exc())
        result = 'Fail'
        Utils.write_file([], 'FAIL', output_file)

    print(time.time() - start)
    print('Done')
