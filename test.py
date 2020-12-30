from solve import *

from mars.mars import make_mars_problem
from mars.mars_viz import mars_plot
from mars.mars_a import make_mars_statistics_a
from mars.mars_b import make_mars_statistics_b
from mars.mars_c import make_mars_statistics_c
from mars.mars_d import make_mars_statistics_d

from air.air import make_air_problem
from air.air_viz import air_plot
from air.air_a import make_air_statistics_a
from air.air_b import make_air_statistics_b
from air.air_c import make_air_statistics_c
from air.air_d import make_air_statistics_d

from delivery.delivery import make_delivery_problem
from delivery.delivery_viz import delivery_plot
from delivery.delivery_a import make_delivery_statistics_a
from delivery.delivery_b import make_delivery_statistics_b
from delivery.delivery_c import make_delivery_statistics_c
from delivery.delivery_d import make_delivery_statistics_d
from delivery.delivery_e import make_delivery_statistics_e

f = open("results.txt", "w")
f.write("||            ||    t|    g|   t1|   g1|   t*||    n|  #VC| #VC'|  #VI| #VI'|   #C|  #C'||\n")
runtime_limit = 600

# mars_a
problem_stats, steps = make_mars_statistics_a(), 6
problem = make_mars_problem(problem_stats)
solution, stats = solve(problem, steps, runtime_limit)
mars_plot(problem_stats, solution, steps, "images/mars_a")
f.write("||    mars (a)||%5.1f|%5.1f|%5.1f|%5.1f|%5.1f||%5d|%5d|%5d|%5d|%5d|%5d|%5d||\n"
      %(stats["t"], stats["g"], stats["t1"], stats["g1"], stats["t*"],steps,
        stats["#VC"], stats["#VC'"], stats["#VI"], stats["#VI'"], stats["#C"], stats["#C'"]))

# mars_b
problem_stats, steps = make_mars_statistics_b(), 5
problem = make_mars_problem(problem_stats)
solution, stats = solve(problem, steps, runtime_limit)
mars_plot(problem_stats, solution, steps, "images/mars_b")
f.write("||    mars (b)||%5.1f|%5.1f|%5.1f|%5.1f|%5.1f||%5d|%5d|%5d|%5d|%5d|%5d|%5d||\n"
      %(stats["t"], stats["g"], stats["t1"], stats["g1"], stats["t*"],steps,
        stats["#VC"], stats["#VC'"], stats["#VI"], stats["#VI'"], stats["#C"], stats["#C'"]))

# mars_c
problem_stats, steps = make_mars_statistics_c(), 9
problem = make_mars_problem(problem_stats)
solution, stats = solve(problem, steps, runtime_limit)
mars_plot(problem_stats, solution, steps, "images/mars_c")
f.write("||    mars (c)||%5.1f|%5.1f|%5.1f|%5.1f|%5.1f||%5d|%5d|%5d|%5d|%5d|%5d|%5d||\n"
      %(stats["t"], stats["g"], stats["t1"], stats["g1"], stats["t*"],steps,
        stats["#VC"], stats["#VC'"], stats["#VI"], stats["#VI'"], stats["#C"], stats["#C'"]))

# mars_d
problem_stats, steps = make_mars_statistics_d(), 9
problem = make_mars_problem(problem_stats)
solution, stats = solve(problem, steps, runtime_limit)
mars_plot(problem_stats, solution, steps, "images/mars_d")
f.write("||    mars (d)||%5.1f|%5.1f|%5.1f|%5.1f|%5.1f||%5d|%5d|%5d|%5d|%5d|%5d|%5d||\n"
      %(stats["t"], stats["g"], stats["t1"], stats["g1"], stats["t*"],steps,
        stats["#VC"], stats["#VC'"], stats["#VI"], stats["#VI'"], stats["#C"], stats["#C'"]))

# air_a
problem_stats, steps = make_air_statistics_a(), 7
problem = make_air_problem(problem_stats)
solution, stats = solve(problem, steps, runtime_limit)
air_plot(problem_stats, solution, steps, "images/air_a")
f.write("||     air (a)||%5.1f|%5.1f|%5.1f|%5.1f|%5.1f||%5d|%5d|%5d|%5d|%5d|%5d|%5d||\n"
      %(stats["t"], stats["g"], stats["t1"], stats["g1"], stats["t*"],steps,
        stats["#VC"], stats["#VC'"], stats["#VI"], stats["#VI'"], stats["#C"], stats["#C'"]))

# air_b
problem_stats, steps = make_air_statistics_b(), 12
problem = make_air_problem(problem_stats)
solution, stats = solve(problem, steps, runtime_limit)
air_plot(problem_stats, solution, steps, "images/air_b")
f.write("||     air (b)||%5.1f|%5.1f|%5.1f|%5.1f|%5.1f||%5d|%5d|%5d|%5d|%5d|%5d|%5d||\n"
      %(stats["t"], stats["g"], stats["t1"], stats["g1"], stats["t*"], steps,
        stats["#VC"], stats["#VC'"], stats["#VI"], stats["#VI'"], stats["#C"], stats["#C'"]))

# air_c
problem_stats, steps = make_air_statistics_c(), 24
problem = make_air_problem(problem_stats)
solution, stats = solve(problem, steps, runtime_limit)
air_plot(problem_stats, solution, steps, "images/air_c")
f.write("||     air (c)||%5.1f|%5.1f|%5.1f|%5.1f|%5.1f||%5d|%5d|%5d|%5d|%5d|%5d|%5d||\n"
      %(stats["t"], stats["g"], stats["t1"], stats["g1"], stats["t*"], steps,
        stats["#VC"], stats["#VC'"], stats["#VI"], stats["#VI'"], stats["#C"], stats["#C'"]))

# air_d
problem_stats, steps = make_air_statistics_d(), 18
problem = make_air_problem(problem_stats)
solution, stats = solve(problem, steps, runtime_limit)
air_plot(problem_stats, solution, steps, "images/air_d")
f.write("||     air (d)||%5.1f|%5.1f|%5.1f|%5.1f|%5.1f||%5d|%5d|%5d|%5d|%5d|%5d|%5d||\n"
      %(stats["t"], stats["g"], stats["t1"], stats["g1"], stats["t*"], steps,
        stats["#VC"], stats["#VC'"], stats["#VI"], stats["#VI'"], stats["#C"], stats["#C'"]))

# delivery_a
problem_stats, steps = make_delivery_statistics_a(), 7
problem = make_delivery_problem(problem_stats)
solution, stats = solve(problem, steps, runtime_limit)
f.write("||delivery (a)||%5.1f|%5.1f|%5.1f|%5.1f|%5.1f||%5d|%5d|%5d|%5d|%5d|%5d|%5d||\n"
      %(stats["t"], stats["g"], stats["t1"], stats["g1"], stats["t*"], steps,
        stats["#VC"], stats["#VC'"], stats["#VI"], stats["#VI'"], stats["#C"], stats["#C'"]))

# delivery_b
problem_stats, steps = make_delivery_statistics_b(), 7
problem = make_delivery_problem(problem_stats)
solution, stats = solve(problem, steps, runtime_limit)
f.write("||delivery (b)||%5.1f|%5.1f|%5.1f|%5.1f|%5.1f||%5d|%5d|%5d|%5d|%5d|%5d|%5d||\n"
      %(stats["t"], stats["g"], stats["t1"], stats["g1"], stats["t*"], steps,
        stats["#VC"], stats["#VC'"], stats["#VI"], stats["#VI'"], stats["#C"], stats["#C'"]))

# delivery_c
problem_stats, steps = make_delivery_statistics_c(), 11
problem = make_delivery_problem(problem_stats)
solution, stats = solve(problem, steps, runtime_limit)
f.write("||delivery (c)||%5.1f|%5.1f|%5.1f|%5.1f|%5.1f||%5d|%5d|%5d|%5d|%5d|%5d|%5d||\n"
      %(stats["t"], stats["g"], stats["t1"], stats["g1"], stats["t*"],steps,
        stats["#VC"], stats["#VC'"], stats["#VI"], stats["#VI'"], stats["#C"], stats["#C'"]))

# delivery_d
problem_stats, steps = make_delivery_statistics_d(), 11
problem = make_delivery_problem(problem_stats)
solution, stats = solve(problem, steps, runtime_limit)
f.write("||delivery (d)||%5.1f|%5.1f|%5.1f|%5.1f|%5.1f||%5d|%5d|%5d|%5d|%5d|%5d|%5d||\n"
      %(stats["t"], stats["g"], stats["t1"], stats["g1"], stats["t*"], steps,
        stats["#VC"], stats["#VC'"], stats["#VI"], stats["#VI'"], stats["#C"], stats["#C'"]))

# delivery_e
problem_stats, steps = make_delivery_statistics_e(), 5
problem = make_delivery_problem(problem_stats)
solution, stats = solve(problem, steps, runtime_limit)
delivery_plot(problem_stats, solution, steps, "images/delivery_e")
f.write("||delivery (d)||%5.1f|%5.1f|%5.1f|%5.1f|%5.1f||%5d|%5d|%5d|%5d|%5d|%5d|%5d||\n"
      %(stats["t"], stats["g"], stats["t1"], stats["g1"], stats["t*"], steps,
        stats["#VC"], stats["#VC'"], stats["#VI"], stats["#VI'"], stats["#C"], stats["#C'"]))

f.close()