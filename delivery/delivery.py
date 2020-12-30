import gurobipy as gp
from gurobipy import GRB
from constraint import *


def make_delivery_problem(stats):

    M = stats["M"]
    N = stats["N"]
    P = stats["P"]
    D = stats["D"]
    depots = stats["depots"]
    paths = stats["paths"]
    path_shapes = stats["path_shapes"]
    truck_speed_bounds = stats["truck_speed_bounds"]
    drone_speed_bound = stats["drone_speed_bound"]
    min_x = stats["min_x"]
    max_x = stats["max_x"]
    min_y = stats["min_y"]
    max_y = stats["max_y"]
    initial_state = stats["initial_state"]
    goal_states  = stats["goal_states"]
    package_tasks = stats["package_tasks"]

    max_dt = 100000

    # Model
    dvars, cvars, avars = {}, {}, {}
    jumps = {}
    flows = {}

    # [Model] state variables
    ## trucks
    for m in range(M):
        LT, xT, yT = "LT" + str(m), "xT" + str(m), "yT" + str(m)
        dvars[LT] = (GRB.INTEGER, 0, len(paths)-1)
        cvars[xT] = (GRB.CONTINUOUS, min_x, max_x)
        cvars[yT] = (GRB.CONTINUOUS, min_y, max_y)
    ## drones
    for m in range(M):
        for n in range(N):
            xD, yD =  "xD" + str(m) + "-" + str(n), "yD" + str(m) + "-" + str(n)
            cvars[xD] = (GRB.CONTINUOUS, min_x, max_x)
            cvars[yD] = (GRB.CONTINUOUS, min_y, max_y)
    ## packages
    for p in range(P):
        strP, LP, cP, xP, yP = "P"+str(p), "LP" + str(p), "cP" + str(p), "xP" + str(p), "yP" + str(p)
        dvars[LP] = (GRB.INTEGER, 0, 1)
        cvars[xP] = (GRB.CONTINUOUS, min_x, max_x)
        cvars[yP] = (GRB.CONTINUOUS, min_y, max_y)
        if strP in package_tasks.keys():
            cvars[cP] = (GRB.CONTINUOUS, 0, max_dt)

    # [Model] control variables
    ## elapsed time
    avars["dt"] = (GRB.CONTINUOUS, 0, max_dt)
    ## trucks
    for m in range(M):
        dvxT, dvyT = "dvxT" + str(m), "dvyT" + str(m)
        avars[dvxT] = (GRB.CONTINUOUS, min_x - max_x, max_x - min_x)
        avars[dvyT] = (GRB.CONTINUOUS, min_y - max_y, max_y - min_y)
    ## drones
    for m in range(M):
        for n in range(N):
            dvxD, dvyD = "dvxD" + str(m) + "-" + str(n), "dvyD" + str(m) + "-" + str(n)
            avars[dvxD] = (GRB.CONTINUOUS, min_x - max_x, max_x - min_x)
            avars[dvyD] = (GRB.CONTINUOUS, min_y - max_y, max_y - min_y)
            # avars[dvxD] = (GRB.CONTINUOUS, min_x - max_x, max_x - min_x)
            # avars[dvyD] = (GRB.CONTINUOUS, min_y - max_y, max_y - min_y)

    # extract names
    dvar_names = list(dvars.keys())
    cvar_names = list(cvars.keys())
    avar_names = list(avars.keys())

    # [Model] jumps
    ## truck jump
    for m in range(M):
        truck_name = "T"+str(m)
        LT, xT, yT = "LT"+str(m), "xT"+str(m), "yT"+str(m)
        for path in paths:
            path_name = str(path[0]) + "-" + str(path[1])
            start_depot = depots[path[0]]
            jumps["[J]_StartPath_" + truck_name + "_" + path_name] \
            = {"pre": [Constr(["pre"], [1], [xT], "==", start_depot[0]),
                       Constr(["pre"], [1], [yT], "==", start_depot[1])],
               "eff": [Constr(["post"], [1], [LT], "==", paths.index(path))] \
                      + identical_effects(cvar_names + dvar_names, [LT])}

    # package jumps
    for strp in package_tasks.keys():
        gxP, gyP, ub = package_tasks[strp]
        LP, xP, yP, cP = "L"+strp, "x"+strp, "y"+strp, "c"+strp
        jumps[LP + "_Signed"] \
            = {"pre": [Constr(["pre"], [1], [xP], "==", gxP),
                       Constr(["pre"], [1], [yP], "==", gyP),
                       Constr(["pre"], [1], [cP], ">=", ub)],
               "eff": [Constr(["post"], [1], [LP], "==", 1)] \
                      + identical_effects(cvar_names + dvar_names, [LP])}

    # [Model] flows
    for m in range(M): flows["pT" + str(m)] = {}
    for m in range(M):
        for n in range(N): flows["pD" + str(m) + "-" + str(n)] = {}
    for p in range(P): flows["pP" + str(p)] = {}

    ## truck flows
    for m in range(M):
        for path in paths:
            path_shape = path_shapes[str(path[0]) + "-" + str(path[1])]
            speed_limit = truck_speed_bounds[str(path[0]) + "-" + str(path[1])]
            LT, pT, xT, yT, dvxT, dvyT = "LT"+str(m), "pT"+str(m), "xT"+str(m), "yT"+str(m), "dvxT"+str(m), "dvyT"+str(m)
            x_bound, y_bound = path_shape[0], path_shape[1]
            vx_bound, vy_bound = speed_limit[0], speed_limit[1]
            condlist = []
            # conditions
            condlist.append(Constr(["pre"], [1], [LT], "==", paths.index(path)))
            condlist.append(Constr(["post"], [1], [LT], "==", paths.index(path)))
            condlist.append(Constr(["pre"], [1], [xT], ">=", x_bound[0]))
            condlist.append(Constr(["post"], [1], [xT], ">=", x_bound[0]))
            condlist.append(Constr(["pre"], [1], [xT], "<=", x_bound[1]))
            condlist.append(Constr(["post"], [1], [xT], "<=", x_bound[1]))
            condlist.append(Constr(["pre"], [1], [yT], ">=", y_bound[0]))
            condlist.append(Constr(["post"], [1], [yT], ">=", y_bound[0]))
            condlist.append(Constr(["pre"], [1], [yT], "<=", y_bound[1]))
            condlist.append(Constr(["post"], [1], [yT], "<=", y_bound[1]))
            if len(path_shape[2]) == 3:
                x_weight, y_weight, offset = path_shape[2]
                condlist.append(Constr(["pre", "pre"], [x_weight, y_weight], [xT, yT], "==", -offset))
                condlist.append(Constr(["post", "post"], [x_weight, y_weight], [xT, yT], "==", -offset))
            condlist.append(Constr(["over", "over"], [1, -vx_bound[0]], [dvxT, "dt"], ">=", 0))
            condlist.append(Constr(["over", "over"], [1, -vx_bound[1]], [dvxT, "dt"], "<=", 0))
            condlist.append(Constr(["over", "over"], [1, -vy_bound[0]], [dvyT, "dt"], ">=", 0))
            condlist.append(Constr(["over", "over"], [1, -vy_bound[1]], [dvyT, "dt"], "<=", 0))
            if len(speed_limit[2]) == 3:
                vx_weight, vy_weight, offset = speed_limit[2]
                condlist.append(Constr(["over", "over", "over"], [vx_weight, vy_weight, offset], [dvxT, dvyT, "dt"], "==", 0))
                condlist.append(Constr(["over", "over", "over"], [vx_weight, vy_weight, offset], [dvxT, dvyT, "dt"], "==", 0))
            # make flows
            flows[pT]["[F]_OnPath_" + pT + "_" + str(path[0]) + "-" + str(path[1])] \
            = {"cond": condlist,
               "eff": [Constr(["post", "pre", "over"], [1, -1, -1], [xT, xT, dvxT], "==", 0),
                       Constr(["post", "pre", "over"], [1, -1, -1], [yT, yT, dvyT], "==", 0)]}
    ## drone flows
    for m in range(M):
        xT, yT, dvxT, dvyT = "xT" + str(m), "yT" + str(m), "dvxT" + str(m), "dvyT" + str(m)
        for n in range(N):
            pD, xD, yD = "pD" + str(m) + "-" + str(n), "xD" + str(m) + "-" + str(n), "yD" + str(m) + "-" + str(n)
            dvxD, dvyD = "dvxD" + str(m) + "-" + str(n), "dvyD" + str(m) + "-" + str(n)
            ## Flow_[Fly]
            vx_bound = drone_speed_bound
            vy_bound = drone_speed_bound
            flows[pD]["[F]_Fly_" + pD] \
                = {"cond": [Constr(["over", "over"], [1, -vx_bound[0]], [dvxD, "dt"], ">=", 0),
                           Constr(["over", "over"], [1, -vx_bound[1]], [dvxD, "dt"], "<=", 0),
                            Constr(["over", "over"], [1, -vy_bound[0]], [dvyD, "dt"], ">=", 0),
                            Constr(["over", "over"], [1, -vy_bound[1]], [dvyD, "dt"], "<=", 0)],
                   "eff": [Constr(["post", "pre", "over"], [1, -1, -1], [xD, xD, dvxD], "==", 0),
                           Constr(["post", "pre", "over"], [1, -1, -1], [yD, yD, dvyD], "==", 0)]}
            ## Flow_[LandTruck]
            flows[pD]["[F]_MoveTruck_" + pD] \
                = {"cond": [Constr(["pre", "pre"], [1, - 1], [xT, xD], "==", 0),
                            Constr(["post", "post"], [1, - 1], [xT, xD], "==", 0),
                            Constr(["pre", "pre"], [1, - 1], [yT, yD], "==", 0),
                            Constr(["post", "post"], [1, - 1], [yT, yD], "==", 0)],
                   "eff": [Constr(["post", "pre", "over"], [1, -1, -1], [xD, xD, dvxT], "==", 0),
                           Constr(["post", "pre", "over"], [1, -1, -1], [yD, yD, dvyT], "==", 0)]}

            ## Flow_[LandDepot]
            for d in range(D):
                flows[pD]["[F]_OnDepot" + str(d) + "_" + pD] \
                    = {"cond": [Constr(["pre"], [1], [xD], "==", depots[d][0]),
                                Constr(["post"], [1], [xD], "==", depots[d][0]),
                                Constr(["pre"], [1], [yD], "==", depots[d][1]),
                                Constr(["post"], [1], [yD], "==", depots[d][1])],
                       "eff": [Constr(["post", "pre"], [1, -1], [xD, xD], "==", 0),
                               Constr(["post", "pre"], [1, -1], [yD, yD], "==", 0)]}
    ## package flows
    for p in range(P):
        strP, cP, pP, xP, yP = "P"+str(p), "cP" + str(p), "pP" + str(p), "xP" + str(p), "yP" + str(p)
        ## Flow [Ground]
        eff = [Constr(["post", "pre"], [1, -1], [xP, xP], "==", 0),
               Constr(["post", "pre"], [1, -1], [yP, yP], "==", 0),]
        if strP in package_tasks.keys():
            eff = eff + [Constr(["post", "pre", "over"], [1, -1, -1], [cP, cP, "dt"], "==", 0)]
        flows[pP]["[F]_Ground_" + xP] \
            = {"cond": [],
               "eff": eff}
        ## Flow [MoveTruck]
        for m in range(M):
            truck_name = "T" + str(m)
            xT, yT = "xT" + str(m), "yT" + str(m)
            dvxT, dvyT = "dvxT" + str(m), "dvyT" + str(m)
            eff = [Constr(["post", "pre", "over"], [1, -1, -1], [xP, xP, dvxT], "==", 0),
                   Constr(["post", "pre", "over"], [1, -1, -1], [yP, yP, dvyT], "==", 0)]
            if strP in package_tasks.keys():
                eff = eff + [Constr(["post", "pre", "over"], [1, -1, -1], [cP, cP, "dt"], "==", 0)]
            flows[pP]["[F]_MoveTruck_" + pP + "_" + truck_name] \
                = {"cond": [Constr(["pre", "pre"], [1, -1], [xP, xT], "==", 0),
                           Constr(["post", "post"], [1, -1], [xP, xT], "==", 0),
                           Constr(["pre", "pre"], [1, -1], [yP, yT], "==", 0),
                           Constr(["post", "post"], [1, -1], [yP, yT], "==", 0)],
                   "eff": eff}

        ## Flow [MoveDrone]
        for m in range(M):
            for n in range(N):
                drone_name = "D" + str(m) + "-" + str(n)
                xD, yD = "xD" + str(m) + "-" + str(n), "yD" + str(m) + "-" + str(n)
                dvxD, dvyD = "dvxD" + str(m) + "-" + str(n), "dvyD" + str(m) + "-" + str(n)
                eff = [Constr(["post", "pre", "over"], [1, -1, -1], [xP, xP, dvxD], "==", 0),
                       Constr(["post", "pre", "over"], [1, -1, -1], [yP, yP, dvyD], "==", 0)]
                if strP in package_tasks.keys():
                    eff = eff + [Constr(["post", "pre", "over"], [1, -1, -1], [cP, cP, "dt"], "==", 0)]
                flows[pP]["[F]_MoveDrone_" + pP + "_" + drone_name] \
                    = {"cond": [Constr(["pre", "pre"], [1, -1], [xP, xD], "==", 0),
                               Constr(["post", "post"], [1, -1], [xP, xD], "==", 0),
                               Constr(["pre", "pre"], [1, -1], [yP, yD], "==", 0),
                               Constr(["post", "post"], [1, -1], [yP, yD], "==", 0)],
                       "eff": eff}

    return {"initial_state": initial_state, "goal_states": goal_states,
            "dvars": dvars, "cvars": cvars, "avars": avars,
            "flows": flows, "jumps": jumps}
