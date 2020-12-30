import gurobipy as gp
from gurobipy import GRB

class Constr:
    def __init__(self, times, coeffs, vars, op, value, orders = []):
        self.times = times
        self.coeffs = coeffs
        self.vars = vars
        self.op = op
        self.value = value
        if orders == []:
            orders = [1] * len(vars)
        self.orders = orders
    def print(self):
        print(self.times, "o", self.orders, "^",
              self.coeffs, "x", self.vars, self.op, self.value)

def identical_effects(var_names, exc_names):
    eff_list = []
    for var_name in var_names:
        if var_name not in exc_names:
            eff_list.append(Constr(["pre", "post"], [1, -1], [var_name, var_name], "==", 0))
    return eff_list

def constrlist2gpconstr(constrlist, guard_name, M, step, gp_vars, model):
    for constr in constrlist:
        expr = 0
        for i in range(len(constr.vars)):
            if (constr.times[i] == "pre") or (constr.times[i] == "over"):
                var = gp_vars[constr.vars[i] + "_" + str(step)]
            elif constr.times[i] == "post":
                var = gp_vars[constr.vars[i] + "_" + str(step + 1)]
            if constr.orders[i] == 1:
                expr = expr + constr.coeffs[i] * var
            elif constr.orders[i] == 2:
                expr = expr + constr.coeffs[i] * var * var
        if guard_name is None:
            if constr.op == "==":
                model.addConstr(expr >= constr.value)
                model.addConstr(expr <= constr.value)
            elif constr.op == ">=":
                model.addConstr(expr >= constr.value)
            elif constr.op == "<=":
                model.addConstr(expr <= constr.value)
        else:
            flag = gp_vars[guard_name + "_" + str(step)]
            if constr.op == "==":
                model.addConstr(expr + M * flag >= constr.value)
                model.addConstr(expr - M * flag <= constr.value)
            elif constr.op == ">=":
                model.addConstr(expr + M * flag >= constr.value)
            elif constr.op == "<=":
                model.addConstr(expr - M * flag <= constr.value)
    return []

