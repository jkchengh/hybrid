import gurobipy as gp
from gurobipy import GRB
from constraint import *

def solve(problem, steps, time_limit = 600):

    print_problem(problem)

    # get prolem components
    initial_state = problem["initial_state"]
    goal_states = problem["goal_states"]
    dvars = problem["dvars"]
    cvars = problem["cvars"]
    avars = problem["avars"]
    flows = problem["flows"]
    jumps = problem["jumps"]

    # initialize model
    model = gp.Model("Model")
    model.setParam('TimeLimit', time_limit)
    model.setParam('OutputFlag', 0)
    model._1stObj = GRB.INFINITY
    model._1stTime = 0
    model._incObj = GRB.INFINITY
    model._incTime = 0
    gp_vars = {}

    # /* variables */
    # copy state variables for every step
    for i in range(steps+1):
        for variables in [dvars, cvars]:
            for var_name in variables:
                param = variables[var_name]
                gp_vars[var_name + "_" + str(i)] = model.addVar(vtype = param[0], name = var_name + "_" + str(i),
                                                                lb = param[1], ub = param[2])
    # variables for operations
    ovars, jvars, fvars = {}, {}, {}
    ## operation type variables
    ovars["J"] = (GRB.INTEGER, 0, 1)
    ovars["F"] = (GRB.INTEGER, 0, 1)
    ## jump variables
    for jump_name in jumps: jvars[jump_name] = (GRB.INTEGER, 0, 1)
    ## flow variables
    for cluster_name in flows:
        fvars[cluster_name] = {}
        for flow_name in flows[cluster_name]:
            fvars[cluster_name][flow_name] = (GRB.INTEGER, 0, 1)
    # copy operation variables for every step
    for i in range(steps):
        for variables in [ovars, jvars] + list(fvars.values()) + [avars]:
            for var_name in variables:
                param = variables[var_name]
                gp_vars[var_name + "_" + str(i)] = model.addVar(vtype = param[0], name = var_name + "_" + str(i),
                                                                lb = param[1], ub = param[2])
    # /* objective */
    model.setObjective(gp.LinExpr([1] * steps, [gp_vars["dt_" + str(i)] for i in range(steps)]), GRB.MINIMIZE)

    # /* constraints */
    param_M = 1000000 # solution parameters
    # initial state
    for var_name in initial_state:
        model.addConstr(gp_vars[var_name + "_0"] == initial_state[var_name], "init_" + var_name)
    # goal states
    for var_name in goal_states:
        model.addConstr(gp_vars[var_name + "_" + str(steps)] == goal_states[var_name], "goal_" + var_name)

    # Constraints imposed by operatiron
    for i in range(steps):
    # Only one flow for each variable is active
        model.addConstr(gp_vars["J" + "_" + str(i)] + gp_vars["F" + "_" + str(i)] == 1, "JF_" + str(i))
        ## jumps activation
        gp_jvars = [gp_vars[name + "_" + str(i) ] for name in list(jvars.keys())]
        model.addConstr(gp.LinExpr([1] * len(gp_jvars) + [-1], gp_jvars + [gp_vars["J" + "_" + str(i)]])
                        == len(gp_jvars) - 1 )
        ## flow activation
        for cluster_name in fvars:
            gp_fvars = [gp_vars[name + "_" + str(i) ] for name in list(fvars[cluster_name].keys())]
            model.addConstr(gp.LinExpr([1] * len(gp_fvars) + [-1], gp_fvars + [gp_vars["F" + "_" + str(i)]])
                            == len(gp_fvars) - 1)
        ## flows don't change discrete varaibles
        constrlist2gpconstr(identical_effects(list(dvars.keys()), []),
                            "F", param_M, i, gp_vars, model)
        # ## jumps has zero durations
        constrlist2gpconstr([Constr(["over"], [1], ["dt"], "==", 0)],
                             "J", param_M, i, gp_vars, model)
        ## preconditions and effects of jumps
        for jump_name in jumps:
            jump = jumps[jump_name]
            constrlist2gpconstr(jump["pre"] + jump["eff"], jump_name, param_M, i, gp_vars, model)
        ## precondition and effects of flows
        for cluster_name in flows:
            for flow_name in flows[cluster_name]:
                condlist, efflist = flows[cluster_name][flow_name]["cond"], flows[cluster_name][flow_name]["eff"]
                constrlist2gpconstr(condlist + efflist, flow_name, param_M, i, gp_vars, model)


    # redundant constraings
    conflict_flows = conflicting_concurrent_flows(flows, dvars, cvars, avars)
    print("Conflicitng Concurreng Flows", conflict_flows)
    for i in range(steps):
        for flow_nameA, flow_nameB in conflict_flows:
            model.addConstr(gp_vars[flow_nameA + "_" + str(i)] + gp_vars[flow_nameB + "_" + str(i)] <= 1,
                            "conflict_concurrent_flows_(" + flow_nameA + "," + flow_nameB + ")" + "_" + str(i))
    conflict_operators = conflicting_subsequent_operators(flows, jumps, dvars, cvars, avars)
    print("Conflicitng Subsequent Operators", conflict_operators)
    for i in range(steps):
        for op_nameA, op_nameB in conflict_flows:
            model.addConstr(gp_vars[op_nameA + "_" + str(i)] + gp_vars[op_nameB + "_" + str(i+1)] <= 1,
                            "conflict_subsequent_operators_(" + op_nameA + "," + op_nameB + ")" + "_" + str(i))

    # optimization Model
    model.optimize(cbWrite)

    # extract solution
    variable_vars = {}
    for d in [dvars, cvars]: variable_vars.update(d)
    operation_vars = {}
    for d in [jvars] + list(fvars.values()): operation_vars.update(d)
    solution = {}
    for v in model.getVars(): solution[v.varName] = v.x

    stats = extract_solution_stats(model)
    # print_solution(variable_vars, operation_vars, avars, steps, solution)

    return solution, stats

def print_problem(problem):
    flows = problem["flows"]
    jumps = problem["jumps"]
    # print jumps and flows
    for jump_name in jumps:
        jump = jumps[jump_name]
        prelist, efflist = jump["pre"], jump["eff"]
        print(jump_name)
        print("Preconditions")
        for constr in prelist: constr.print()
        print("Effects")
        for constr in efflist: constr.print()
    for cvar_name in flows:
        for flow_name in flows[cvar_name]:
            condlist, efflist = flows[cvar_name][flow_name]["cond"], flows[cvar_name][flow_name]["eff"]
            print(flow_name)
            print("Conditions")
            for constr in condlist: constr.print()
            print("Effects")
            for constr in efflist: constr.print()

def print_solution(variable_vars, operation_vars, avars, steps, solution):
    print("-- State [0]-- ")
    for variable_name in variable_vars:
        print('%s = %g' % (variable_name, solution[variable_name + "_" + str(0)]))
    for i in range(1, steps + 1):
        operation = []
        print("-- operation [%g]-- " % (i - 1))
        for op_name in operation_vars:
            if solution[op_name + "_" + str(i - 1)] <= 0.05: operation.append(op_name)
        print(operation)
        for variable_name in avars:
            print('%s = %g' % (variable_name, solution[variable_name + "_" + str(i - 1)]))
        print("-- State [%g]-- " % i)
        for variable_name in variable_vars:
            print('%s = %g' % (variable_name, solution[variable_name + "_" + str(i)]))

def extract_solution_stats(model):
    runtime = model.Runtime
    numVC = model.NumVars - model.NumIntVars
    numVI = model.NumIntVars
    numC = model.NumConstrs

    presolved = model.presolve()
    numPreVC = presolved.NumVars - presolved.NumIntVars
    numPreVI = presolved.NumIntVars
    numPreC = presolved.NumConstrs

    return {"t": runtime, "g": model.objVal, "t1": model._1stTime, "g1": model._1stObj, "t*": model._incTime,
            "#VC": numVC, "#VC'": numPreVC, '#VI': numVI, "#VI'": numPreVI, "#C": numC, "#C'": numPreC}

    #model.printStats()

def cbWrite(model, where):
    if where == GRB.Callback.MIPSOL:
        model._incTime = model.cbGet(GRB.Callback.RUNTIME)
        model._incObj = model.cbGet(GRB.Callback.MIPSOL_OBJ)
        if model._1stTime == 0:
            model._1stTime = model._incTime
            model._1stObj = model._incObj

def conflicting_concurrent_flows(flows, dvars, cvars, avars):
    conflict_flows = []
    for nameA in flows:
        for flow_nameA in flows[nameA]:
            for nameB in flows:
                for flow_nameB in flows[nameB]:
                    if nameA is not nameB:
                        condA = flows[nameA][flow_nameA]["cond"]
                        condB = flows[nameB][flow_nameB]["cond"]
                        check = gp.Model("check")
                        checked_vars = {}
                        for variables in [dvars, cvars, avars]:
                            for var_name in variables:
                                param = variables[var_name]
                                checked_vars[var_name + "_0"] = check.addVar(vtype=param[0],
                                                                             name=var_name + "_0",
                                                                             lb=param[1], ub=param[2])
                                checked_vars[var_name + "_1"] = check.addVar(vtype=param[0],
                                                                             name=var_name + "_1",
                                                                             lb=param[1], ub=param[2])
                        constrlist2gpconstr(condA + condB, None, None, 0, checked_vars, check)
                        check.setParam('OutputFlag', 0)
                        check.optimize()
                        if check.status == GRB.INFEASIBLE:
                            conflict_flows = conflict_flows + [[flow_nameA, flow_nameB]]
                        check.dispose()
    return conflict_flows

def conflicting_subsequent_operators(flows, jumps, dvars, cvars, avars):
    conflict_operators = []
    all_flows = {}
    for name in flows:
        for flow_name in flows[name]:
            all_flows[flow_name] = flows[name][flow_name]

    # flow -> flow
    for flow_nameA in all_flows:
        for flow_nameB in all_flows:
            condA = all_flows[flow_nameA]["cond"]
            effA = all_flows[flow_nameA]["eff"]
            condB = all_flows[flow_nameB]["cond"]
            effB = all_flows[flow_nameB]["eff"]
            check = gp.Model("check")
            checked_vars = {}
            for variables in [dvars, cvars, avars]:
                for var_name in variables:
                    param = variables[var_name]
                    checked_vars[var_name + "_0"] = check.addVar(vtype=param[0],
                                                                 name=var_name + "_0",
                                                                 lb=param[1], ub=param[2])
                    checked_vars[var_name + "_1"] = check.addVar(vtype=param[0],
                                                                 name=var_name + "_1",
                                                                 lb=param[1], ub=param[2])
                    checked_vars[var_name + "_2"] = check.addVar(vtype=param[0],
                                                                 name=var_name + "_2",
                                                                 lb=param[1], ub=param[2])
            constrlist2gpconstr(condA+effA, None, None, 0, checked_vars, check)
            constrlist2gpconstr(condB+effB, None, None, 1, checked_vars, check)
            constrlist2gpconstr(identical_effects(list(dvars.keys()), []), None, None, 0, checked_vars, check)
            constrlist2gpconstr(identical_effects(list(dvars.keys()), []), None, None, 1, checked_vars, check)
            check.optimize()
            if check.status == GRB.INFEASIBLE:
                conflict_operators = conflict_operators + [[flow_nameA, flow_nameB]]
            check.dispose()

    # jump -> jump
    for jump_nameA in jumps:
        for jump_nameB in jumps:
            condA = jumps[jump_nameA]["pre"]
            effA = jumps[jump_nameA]["eff"]
            condB = jumps[jump_nameB]["pre"]
            effB = jumps[jump_nameB]["eff"]
            check = gp.Model("check")
            checked_vars = {}
            for variables in [dvars, cvars, avars]:
                for var_name in variables:
                    param = variables[var_name]
                    checked_vars[var_name + "_0"] = check.addVar(vtype=param[0],
                                                                 name=var_name + "_0",
                                                                 lb=param[1], ub=param[2])
                    checked_vars[var_name + "_1"] = check.addVar(vtype=param[0],
                                                                 name=var_name + "_1",
                                                                 lb=param[1], ub=param[2])
                    checked_vars[var_name + "_2"] = check.addVar(vtype=param[0],
                                                                 name=var_name + "_2",
                                                                 lb=param[1], ub=param[2])
            constrlist2gpconstr(condA + effA, None, None, 0, checked_vars, check)
            constrlist2gpconstr(condB + effB, None, None, 1, checked_vars, check)
            constrlist2gpconstr([Constr(["over"], [1], ["dt"], "==", 0)], None, None, 0, checked_vars, check)
            constrlist2gpconstr([Constr(["over"], [1], ["dt"], "==", 0)], None, None, 1, checked_vars, check)
            check.optimize()
            if check.status == GRB.INFEASIBLE:
                conflict_operators = conflict_operators + [[jump_nameA, jump_nameB]]
            check.dispose()

    # jump -> flow
    for jump_nameA in jumps:
        for flow_nameB in all_flows:
            condA = jumps[jump_nameA]["pre"]
            effA = jumps[jump_nameA]["eff"]
            condB = all_flows[flow_nameB]["cond"]
            effB = all_flows[flow_nameB]["eff"]
            check = gp.Model("check")
            checked_vars = {}
            for variables in [dvars, cvars, avars]:
                for var_name in variables:
                    param = variables[var_name]
                    checked_vars[var_name + "_0"] = check.addVar(vtype=param[0],
                                                                 name=var_name + "_0",
                                                                 lb=param[1], ub=param[2])
                    checked_vars[var_name + "_1"] = check.addVar(vtype=param[0],
                                                                 name=var_name + "_1",
                                                                 lb=param[1], ub=param[2])
                    checked_vars[var_name + "_2"] = check.addVar(vtype=param[0],
                                                                 name=var_name + "_2",
                                                                 lb=param[1], ub=param[2])
            constrlist2gpconstr(condA + effA, None, None, 0, checked_vars, check)
            constrlist2gpconstr(condB + effB, None, None, 1, checked_vars, check)
            constrlist2gpconstr([Constr(["over"], [1], ["dt"], "==", 0)], None, None, 0, checked_vars, check)
            constrlist2gpconstr(identical_effects(list(dvars.keys()), []), None, None, 1, checked_vars, check)
            check.optimize()
            if check.status == GRB.INFEASIBLE:
                conflict_operators = conflict_operators + [[jump_nameA, flow_nameB]]
            check.dispose()

    # flow -> jump
    for flow_nameA in all_flows:
        for jump_nameB in jumps:
            condA = all_flows[flow_nameA]["cond"]
            effA = all_flows[flow_nameA]["eff"]
            condB = jumps[jump_nameA]["pre"]
            effB = jumps[jump_nameA]["eff"]
            check = gp.Model("check")
            checked_vars = {}
            for variables in [dvars, cvars, avars]:
                for var_name in variables:
                    param = variables[var_name]
                    checked_vars[var_name + "_0"] = check.addVar(vtype=param[0],
                                                                 name=var_name + "_0",
                                                                 lb=param[1], ub=param[2])
                    checked_vars[var_name + "_1"] = check.addVar(vtype=param[0],
                                                                 name=var_name + "_1",
                                                                 lb=param[1], ub=param[2])
                    checked_vars[var_name + "_2"] = check.addVar(vtype=param[0],
                                                                 name=var_name + "_2",
                                                                 lb=param[1], ub=param[2])
            constrlist2gpconstr(condA + effA, None, None, 0, checked_vars, check)
            constrlist2gpconstr(condB + effB, None, None, 1, checked_vars, check)
            constrlist2gpconstr(identical_effects(list(dvars.keys()), []), None, None, 0, checked_vars, check)
            constrlist2gpconstr([Constr(["over"], [1], ["dt"], "==", 0)], None, None, 1, checked_vars, check)
            check.optimize()
            if check.status == GRB.INFEASIBLE:
                conflict_operators = conflict_operators + [[flow_nameA, jump_nameB]]
            check.dispose()

    return conflict_operators