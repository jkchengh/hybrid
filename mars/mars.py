from gurobipy import GRB
from constraint import *
from math import *


def make_mars_problem(statistics):

    regions = statistics["regions"]
    min_x, max_x = statistics["min_x"], statistics["max_x"]
    min_y, max_y = statistics["min_y"], statistics["max_y"]
    max_E = statistics["max_E"]
    max_walk = statistics["max_walk"]
    initial_state, goal_states = statistics["initial_state"], statistics["goal_states"]
    region_number = len(regions)
    bases = [[cos(n * pi / 3), sin(n * pi / 3)] for n in range(3)]

    # Model
    dvars, cvars, avars = {}, {}, {}
    jumps = {}
    flows = {"A": {}, "R": {}}

    # /* Variables */
    ## State variables
    cvars["xA"] = (GRB.CONTINUOUS, min_x, max_x)
    cvars["yA"] = (GRB.CONTINUOUS, min_y, max_y)
    cvars["xR"] = (GRB.CONTINUOUS, min_x, max_x)
    cvars["yR"] = (GRB.CONTINUOUS, min_y, max_y)
    cvars["E"] = (GRB.CONTINUOUS, 0, max_E)

    # Input variables accumulative effects
    max_dvxA = max_x - min_x
    max_dvyA = max_y - min_y
    max_dvxR = max_x - min_x
    max_dvyR = max_y - min_y
    avars["dt"] = (GRB.CONTINUOUS, 0, 10000)
    avars["dvxA"] = (GRB.CONTINUOUS, -max_dvxA, max_dvxA)
    avars["dvyA"] = (GRB.CONTINUOUS, -max_dvyA, max_dvyA)
    avars["dvxR"] = (GRB.CONTINUOUS, -max_dvxR, max_dvxR)
    avars["dvyR"] = (GRB.CONTINUOUS, -max_dvyR, max_dvyR)

    ## [FAR]
    flows["A"]["FAR"] \
    = {"cond": [Constr(["pre", "pre"], [1, -1], ["xR", "xA"], "==", 0),
                Constr(["post", "post"], [1, -1], ["xR", "xA"], "==", 0),
                Constr(["pre", "pre"], [1, -1], ["yR", "yA"], "==", 0),
                Constr(["post", "post"], [1, -1], ["yR", "yA"], "==", 0),
                Constr(["over"], [1], ["dvxA"], "==", 0),
                Constr(["over"], [1], ["dvyA"], "==", 0)],
       "eff": [Constr(["post", "pre", "over"], [1, -1, -1], ["xA", "xA", "dvxR"], "==", 0),
               Constr(["post", "pre", "over"], [1, -1, -1], ["yA", "yA", "dvyR"], "==", 0)]}

    ## [FAW]
    velocity_cond = []
    for base in bases:
        velocity_cond = velocity_cond + [Constr(["over", "over", "over"], base + [max_walk], ["dvxA", "dvyA","dt"], ">=", 0),
                                         Constr(["over", "over", "over"], base + [-max_walk], ["dvxA", "dvyA", "dt"], "<=", 0)];

    flows["A"]["FAW"] \
        = {"cond": velocity_cond,
       "eff": [Constr(["post", "pre", "over"], [1, -1, -1], ["xA", "xA", "dvxA"], "==", 0),
               Constr(["post", "pre", "over"], [1, -1, -1], ["yA", "yA", "dvyA"], "==", 0)]}

    ## [FRS]
    flows["R"]["FRS"] \
    = {"cond": [Constr(["over"], [1], ["dvxR"], "==", 0),
                Constr(["over"], [1], ["dvyR"], "==", 0),],
       "eff": [Constr(["post", "pre"], [1, -1], ["xR", "xR"], "==", 0),
               Constr(["post", "pre"], [1, -1], ["yR", "yR"], "==", 0),
               Constr(["post", "pre"], [1, -1], ["E", "E"], "==", 0)]}

    ## [FR*]
    for j in range(region_number):
        region = regions[j]
        if not region["type"] == "obstacle":
            constraints = region["constraints"]
            velocity = region["velocity"]
            battery = region["battery"]
            condlist = []
            for k in range(len(constraints)):
                # boundary constraints
                constraint = constraints[k]
                x_weight, y_weight = constraint[0], constraint[1]
                operator = constraint[2]
                offset = constraint[3]
                condlist.append(Constr(["pre", "pre"], [x_weight, y_weight], ["xR", "yR"], operator, offset))
                condlist.append(Constr(["post", "post"], [x_weight, y_weight], ["xR", "yR"], operator, offset))
            # velocity
            velocity_cond = []
            for base in bases:
                velocity_cond = velocity_cond + [
                    Constr(["over", "over", "over"], base + [velocity], ["dvxR", "dvyR", "dt"], ">=", 0),
                    Constr(["over", "over", "over"], base + [-velocity], ["dvxR", "dvyR", "dt"], "<=", 0)];

            flows["R"]["FR-"+str(j)] \
            = {"cond": condlist + velocity_cond,
               "eff": [Constr(["post", "pre", "over"], [1, -1, -1], ["xR", "xR", "dvxR"], "==", 0),
                       Constr(["post", "pre", "over"], [1, -1, -1], ["yR", "yR", "dvyR"], "==", 0),
                       Constr(["post", "pre", "over"], [1, -1, -battery], ["E", "E", "dt"], "==", 0)]}

    return {"initial_state": initial_state, "goal_states": goal_states,
            "dvars": dvars, "cvars": cvars, "avars": avars,
            "flows": flows, "jumps": jumps}