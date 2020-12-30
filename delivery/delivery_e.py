
def make_delivery_statistics_e():

    # parameters
    min_x, max_x = 0, 10
    min_y, max_y = 0, 10

    # numbers
    M = 1  # number of homogeneous trucks in the fleet
    N = 1  # number of drones on each truck
    P = 1  # number of packages
    D = 2  # number of depots

    # initial location
    initial_state = {
        "LT0": 0, "xT0": 0, "yT0": 0,
        "xD0-0": 0, "yD0-0": 0,
        "xP0": 5, "yP0": 1}

    # goals
    goal_states = { "xT0": 10, "yT0": 0,
                    "xP0": 10, "yP0": 0,
                   "xD0-0": 10, "yD0-0": 0}

    # model specifications
    depots = [(0, 0), (10, 0)] # depots
    paths = [(0, 0), (1, 1),
             (0, 1), (1, 0)]
    path_shapes = {
        "0-0": ([0, 0], [0, 0], {}),
        "1-1": ([10, 10], [0, 0], {}),
        "0-1": ([0, 10], [0, 0], [0, 1, 0]),
        "1-0": ([0, 10], [0, 0], [0, 1, 0])}
    truck_speed_bounds = {
        "0-0": ([0, 0], [0, 0], []),
        "1-1": ([0, 0], [0, 0], []),
        "0-1": ([5/60, 50/60], [0, 0], [0, 1, 0]),
        "1-0": ([-50/60, 0], [0, 0], [0, 1, 0])}

    drone_speed_bound = [-5/60, 5/60]

    stats = {"M": M, "N": N, "P": P, "D": D,
             "depots": depots, "paths": paths, "path_shapes": path_shapes,
             "truck_speed_bounds": truck_speed_bounds, "drone_speed_bound": drone_speed_bound,
             "min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y,
             "initial_state": initial_state, "goal_states": goal_states, "package_tasks": {}}

    return stats

