import gurobipy as gp
from gurobipy import GRB
from constraint import *


def make_air_problem(stats):

    blip_num = stats["blip_num"]
    regions = stats["regions"]
    min_x = stats["min_x"]
    max_x = stats["max_x"]
    min_y = stats["min_y"]
    max_y = stats["max_y"]
    max_blip_b = stats["max_blip_b"]
    max_blip_velocity = stats["max_blip_velocity"]
    max_ref_velocity = stats["max_ref_velocity"]
    max_tank_velocity = stats["max_tank_velocity"]
    refuel_rate = stats["refuel_rate"]
    refuel_range = stats["refuel_range"]
    initial_state = stats["initial_state"]
    goal_states = stats["goal_states"]

    region_number = len(regions)
    max_dt = 10000

    # Model
    dvars, cvars, avars = {}, {}, {}
    jumps = {}
    flows = {"R": {}}
    for idx in range(blip_num):
        flows["pB%s"%(idx)] = {}

    # /* Variables */
    ## State variables
    for idx in range(region_number):
        dvars["photo%s"%(idx)] = (GRB.INTEGER, 0, 1)
    for idx in range(blip_num):
        cvars["xB%s"%(idx)] = (GRB.CONTINUOUS, min_x, max_x)
        cvars["yB%s"%(idx)] = (GRB.CONTINUOUS, min_y, max_y)
        cvars["bB%s"%(idx)] = (GRB.CONTINUOUS, 0, max_blip_b)

    cvars["xR"] = (GRB.CONTINUOUS, min_x, max_x)
    cvars["yR"] = (GRB.CONTINUOUS, min_y, max_y)

   # Input variables accumulative effects
    max_dvxB = max_x - min_x
    max_dvyB = max_y - min_y
    max_dvxR = max_x - min_x
    max_dvyR = max_y - min_y
    avars["dt"] = (GRB.CONTINUOUS, 0, max_dt)
    for idx in range(blip_num):
        avars["dvxB%s"%(idx)] = (GRB.CONTINUOUS, -max_dvxB, max_dvxB)
        avars["dvyB%s"%(idx)] = (GRB.CONTINUOUS, -max_dvyB, max_dvyB)
    avars["dvxR"] = (GRB.CONTINUOUS, -max_dvxR, max_dvxR)
    avars["dvyR"] = (GRB.CONTINUOUS, -max_dvyR, max_dvyR)

    for blip_idx in range(blip_num):
        xB, yB, pB, bB = "xB%s"%(blip_idx), "yB%s"%(blip_idx), "pB%s"%(blip_idx), "bB%s"%(blip_idx)
        dvxB, dvyB = "dvxB%s"%(blip_idx), "dvyB%s"%(blip_idx)
        FBF, FBR = "FBF%s"%(blip_idx), "FBR%s"%(blip_idx)

        ## [FBF]
        velocity_cond = [Constr(["over", "over"], [1, max_blip_velocity], [dvxB, "dt"], ">=", 0),
                         Constr(["over", "over"], [1, -max_blip_velocity], [dvxB, "dt"], "<=", 0),
                         Constr(["over", "over"], [1, max_blip_velocity], [dvyB, "dt"], ">=", 0),
                         Constr(["over", "over"], [1, -max_blip_velocity], [dvyB, "dt"], "<=", 0)]


        flows[pB][FBF] \
            = {"cond": velocity_cond,
               "eff": [Constr(["post", "pre", "over"], [1, -1, -1], [xB, xB, dvxB], "==", 0),
                       Constr(["post", "pre", "over"], [1, -1, -1], [yB, yB, dvyB], "==", 0),
                       Constr(["post", "pre", "over"], [1, -1, 2], [bB, bB, "dt"], "==", 0)]}
        ## [FBR]
        velocity_cond = [Constr(["over", "over"], [1, max_ref_velocity], [dvxB, "dt"], ">=", 0),
                         Constr(["over", "over"], [1, -max_ref_velocity], [dvxB, "dt"], "<=", 0),
                         Constr(["over", "over"], [1, max_ref_velocity], [dvyB, "dt"], ">=", 0),
                         Constr(["over", "over"], [1, -max_ref_velocity], [dvyB, "dt"], "<=", 0)]

        flows[pB][FBR] \
        = {"cond": velocity_cond +
                   [Constr(["pre", "pre"], [1, -1], ["xR", xB], ">=", -refuel_range),
                    Constr(["pre", "pre"], [1, -1], ["xR", xB], "<=", refuel_range),
                    Constr(["pre", "pre"], [1, -1], ["yR", yB], ">=", -refuel_range),
                    Constr(["pre", "pre"], [1, -1], ["yR", yB], "<=", refuel_range),
                    Constr(["post", "post"], [1, -1], ["xR", xB], ">=", -refuel_range),
                    Constr(["post", "post"], [1, -1], ["xR", xB], "<=", refuel_range),
                    Constr(["post", "post"], [1, -1], ["yR", yB], ">=", -refuel_range),
                    Constr(["post", "post"], [1, -1], ["yR", yB], "<=", refuel_range),],
           "eff": [Constr(["post", "pre", "over"], [1, -1, -1], [xB, xB, dvxB], "==", 0),
                   Constr(["post", "pre", "over"], [1, -1, -1], [yB, yB, dvyB], "==", 0),
                   Constr(["post", "pre", "over"], [1, -1, -refuel_rate], [bB, bB, "dt"], "==", 0)]}


    ## [FRF]
    velocity_cond = [Constr(["over", "over"], [1, max_tank_velocity], ["dvxR", "dt"], ">=", 0),
                     Constr(["over", "over"], [1, -max_tank_velocity], ["dvxR", "dt"], "<=", 0),
                     Constr(["over", "over"], [1, max_tank_velocity], ["dvyR", "dt"], ">=", 0),
                     Constr(["over", "over"], [1, -max_tank_velocity], ["dvyR", "dt"], "<=", 0)]

    flows["R"]["FRF"] \
        = {"cond": velocity_cond,
           "eff": [Constr(["post", "pre", "over"], [1, -1, -1], ["xR", "xR", "dvxR"], "==", 0),
                   Constr(["post", "pre", "over"], [1, -1, -1], ["yR", "yR", "dvyR"], "==", 0)]}

    # Jumps
    dvar_names = list(dvars.keys())
    cvar_names = list(cvars.keys())
    for idx in range(region_number):
        region = regions[idx]
        constraints = region["constraints"]
        for blip_idx in range(blip_num):
            xB, yB = "xB%s" % (blip_idx), "yB%s" % (blip_idx)
            condlist = []
            for k in range(len(constraints)):
                # boundary constraints
                constraint = constraints[k]
                x_weight, y_weight = constraint[0], constraint[1]
                operator = constraint[2]
                offset = constraint[3]
                condlist.append(Constr(["pre", "pre"], [x_weight, y_weight], [xB, yB], operator, offset))
                condlist.append(Constr(["post", "post"], [x_weight, y_weight], [xB, yB], operator, offset))
            jumps["TakePhoto%sbyB%s"%(idx, blip_idx)] \
            = {"pre": condlist + [Constr(["pre"], [1], ["photo%s"%(idx)], "==", 0)],
               "eff": [Constr(["post"], [1], ["photo%s"%(idx)], "==", 1)]
                      + identical_effects(cvar_names + dvar_names, ["photo%s"%(idx)])}

    return {"initial_state": initial_state, "goal_states": goal_states,
            "dvars": dvars, "cvars": cvars, "avars": avars,
            "flows": flows, "jumps": jumps}