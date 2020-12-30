from numpy import array
from pypoman import compute_polytope_halfspaces

def make_air_statistics_d():
    min_x = 0
    max_x = 100
    min_y = 0
    max_y = 100
    max_blip_b = 1000
    blip_num = 2
    max_blip_velocity = 3
    max_ref_velocity = 0.5
    max_tank_velocity = 2
    refuel_rate = 10
    refuel_range = 2

    polygons = [[(69.28348, 48.10923),
                 (68.00933, 45.38239),
                 (73.61835, 42.22267),
                 (74.51618, 48.55133),
                 (69.28348, 48.10923)],
                [(8.00984, 57.59487),
                 (7.01760, 51.92697),
                 (9.45458, 50.25484),
                 (14.20403, 53.92992),
                 (8.00984, 57.59487)],
                [(23.52966, 20.52394),
                 (28.28920, 22.87291),
                 (25.77673, 27.59659),
                 (22.34778, 24.69332),
                 (23.52966, 20.52394)],
                [(49.99606, 18.74888),
                 (54.37759, 24.80803),
                 (52.85137, 25.66706),
                 (49.60897, 24.57518),
                 (49.99606, 18.74888)],
                [(59.35168, 78.26495),
                 (57.61885, 83.77747),
                 (52.45846, 80.30299),
                 (56.94561, 76.10759),
                 (59.35168, 78.26495)],
                [(69.44408, 81.01133),
                 (76.84911, 80.79492),
                 (72.46184, 85.59022),
                 (69.59860, 82.25114),
                 (69.44408, 81.01133)],
                [(86.01190, 76.47692),
                 (86.77536, 71.26417),
                 (92.74643, 74.07788),
                 (92.06696, 77.54789),
                 (86.01190, 76.47692)],
                [(6.06741, 72.34679),
                 (10.60437, 70.60312),
                 (12.49697, 72.05647),
                 (7.90962, 77.97412),
                 (6.06741, 72.34679)]]

    regions = []
    for polygon in polygons:
        A, b = compute_polytope_halfspaces(map(array, polygon))
        constraints = [(A[idx][0], A[idx][1], "<=", b[idx]) for idx in range(len(b))]
        regions.append({"constraints": constraints,
                        "polygon": polygon})

    # initial location
    initial_state = {"xB0": 70, "yB0": 10, "bB0": 10,
                     "xB1": 70, "yB1": 10, "bB1": 100,
                     "xR": 70, "yR": 10}

    # goals
    goal_states = {"xB0": 31, "yB0": 81, "xB1": 31, "yB1": 81,
                   "xR": 31, "yR": 81}

    for idx in range(len(regions)):
        name = "photo%s" % (idx)
        initial_state[name] = 0
        goal_states[name] = 1

    # # solve
    stats = {"blip_num": blip_num,
             "regions": regions,
             "min_x": min_x, "max_x": max_x,
             "min_y": min_y, "max_y": max_y,
             "max_blip_b": max_blip_b,
             "max_blip_velocity": max_blip_velocity,
             "max_ref_velocity": max_ref_velocity,
             "max_tank_velocity": max_tank_velocity,
             "refuel_rate": refuel_rate,
             "refuel_range": refuel_range,
             "initial_state": initial_state,
             "goal_states": goal_states}

    return stats