from matplotlib import pyplot as plt
from shapely.geometry.polygon import LinearRing, Polygon

def delivery_plot(stats, solution, steps, name):

    depots = stats["depots"]
    paths = stats["paths"]
    M = stats["M"]
    N = stats["N"]
    P = stats["P"]
    min_x = stats["min_x"]
    max_x = stats["max_x"]
    min_y = stats["min_y"]
    max_y = stats["max_y"]

    fig = plt.figure()
    ax = plt.subplot(111)
    axes = fig.gca()
    axes.set_xlim([min_x-1, max_x+1])
    axes.set_ylim([min_y-1, max_y+1])

    for path in paths:
        src, dst = path
        src_depot, dst_depot = depots[src], depots[dst]
        ax.plot([src_depot[0], dst_depot[0]], [src_depot[1], dst_depot[1]],
                linewidth=20, label="depot", color="dimgray", alpha=0.3)
        for depot in depots:
            ax.plot([depot[0]], [depot[1]], label="depot", color="black",
                    marker='s', markersize=5)

    for m in range(M):
        xT_route = [solution["xT" + str(m) + "_" + str(i)] for i in range(steps + 1)]
        yT_route = [solution["yT" + str(m) + "_" + str(i)]-1/20 for i in range(steps + 1)]
        ax.plot(xT_route, yT_route, label='Truck', color='firebrick', linewidth=2, marker='x', markersize=7)
        ax.text(xT_route[0] , yT_route[0]-0.5, r'Truck_'+str(m), color='firebrick', fontsize=20)
        for n in range(N):
            xD_route = [solution["xD" + str(m) + "-" + str(n) + "_" + str(i)] for i in range(steps + 1)]
            yD_route = [solution["yD" + str(m) + "-" + str(n) + "_" + str(i)] + 1/20 for i in range(steps + 1)]
            ax.plot(xD_route, yD_route, label='Drone', color='navy', linewidth=2, marker='x', markersize=7)

    plt.axis('off')
    plt.margins(0, 0)

    plt.show()
    fig.savefig(name + ".pdf", bbox_inches='tight',pad_inches = 0)