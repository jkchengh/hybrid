
def make_mars_statistics_a():

    regions = [{"type": "charge",
                "constraints": [(1, 0, "==", 100),
                                (0, 1, "==", 45)],
                "polygon": [100, 45],
                "velocity": 0,
                "battery": 10},

               {"type": "ground",
                "constraints": [(1, 0, ">=", 0),
                                (1, 0, "<=", 20),
                                (0, 1, ">=", 0),
                                (0, 1, "<=", 60)],
                "polygon": [(0, 0), (0, 60), (20, 60), (20,0), (0, 0)],
                "velocity": 50,
                "battery": -2},

               {"type": "basin",
                "constraints": [(1, 0, ">=", 20),
                                (1, 0, "<=", 60),
                                (0, 1, ">=", 20),
                                (0, 1, "<=", 40)],
                "polygon": [(20, 20), (20, 40), (60, 40), (60, 20), (20, 20)],
                "velocity": 30,
                "battery": -2},

               {"type": "mountain",
                "constraints": [(1, 0, ">=", 40),
                                (1, 0, "<=", 130),
                                (0, 1, ">=", 0),
                                (0, 1, "<=", 20)],
                "polygon": [(40, 0), (40, 20), (130, 20), (130, 0), (40, 0)],
                "velocity": 10,
                "battery": -3},

               {"type": "ground",
                "constraints": [(1, 0, ">=", 40),
                                (1, 0, "<=", 90),
                                (0, 1, ">=", 40),
                                (0, 1, "<=", 60),
                                (2, -1, "<=", 120)],
                "polygon": [(40, 40), (40, 60), (90, 60), (80, 40), (40, 40)],
                "velocity": 50,
                "battery": -2},

               {"type": "basin",
                "constraints": [(1, 0, ">=", 80),
                                (1, 0, "<=", 110),
                                (0, 1, ">=", 20),
                                (0, 1, "<=", 60),
                                (2, -1, ">=", 120)],
                "polygon": [(80, 40), (90, 60), (110, 60), (110, 20), (80, 20), (80,40)],
                "velocity": 30,
                "battery": -2},

               {"type": "obstacle",
                "constraints": [(1, 0, ">=", 20),
                                (1, 0, "<=", 40),
                                (0, 1, ">=", 0),
                                (0, 1, "<=", 20)],
                "polygon": [(20, 0), (20, 20), (40, 20), (40, 0), (20, 0)],
                "velocity": 0,
                "battery": 0},

               {"type": "obstacle",
                "constraints": [(1, 0, ">=", 20),
                                (1, 0, "<=", 40),
                                (0, 1, ">=", 40),
                                (0, 1, "<=", 60)],
                "polygon": [(20, 40), (20, 60), (40, 60), (40, 40), (20, 40)],
                "velocity": 0,
                "battery": 0},

               {"type": "obstacle",
                "constraints": [(1, 0, ">=", 60),
                                (1, 0, "<=", 80),
                                (0, 1, ">=", 20),
                                (0, 1, "<=", 40)],
                "polygon": [(60, 20), (60, 40), (80, 40), (80, 20), (60, 20)],
                "velocity": 0,
                "battery": 0},

               {"type": "obstacle",
                "constraints": [(1, 0, ">=", 110),
                                (1, 0, "<=", 130),
                                (0, 1, ">=", 20),
                                (0, 1, "<=", 60)],
                "polygon": [(110, 20), (110, 60), (130, 60), (130, 20), (110, 20)],
                "velocity": 0,
                "battery": 0}]

    min_x = 0
    max_x = 130
    min_y = 0
    max_y = 60
    max_E = 300
    max_walk = 2

    initial_state = {"xA": 50, "yA": 25,
                     "xR": 10, "yR": 10,
                     "E": 100}

    goal_states = {"xA": 120, "yA": 10}

    statistics = {"regions": regions,
                  "min_x": min_x, "max_x": max_x,
                  "min_y": min_y, "max_y": max_y,
                  "max_E": max_E, "max_walk": max_walk,
                  "initial_state": initial_state,
                  "goal_states": goal_states}

    return statistics
