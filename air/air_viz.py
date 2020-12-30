from matplotlib import pyplot as plt
from shapely.geometry.polygon import LinearRing, Polygon
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

def air_plot(stats, solution, steps, name):

    regions =  stats["regions"]
    blip_num = stats["blip_num"]
    min_x = stats["min_x"]
    max_x = stats["max_x"]
    min_y = stats["min_y"]
    max_y = stats["max_y"]

    ratio = 1
    fig = plt.figure()
    ax = plt.subplot(111)
    axes = fig.gca()
    axes.set_xlim([min_x-5, max_x+5])
    axes.set_ylim([min_y-5, max_y+5])
    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()
    ax.set_aspect(abs((xright - xleft) / (ybottom - ytop)) * ratio)

    for region in regions:
        facecolor = "purple"
        linecolor = "black"
        alpha = 0.4
        poly = Polygon(region["polygon"])
        x, y = poly.exterior.xy
        ax.fill(x, y, facecolor = facecolor, color = linecolor, alpha = alpha)

    # plot initial states and goals
    ax.text(70, 3, r'Start', color='black', fontsize=15)
    ax.text(30, 87, r'End', color='black', fontsize=15)

    # plot solution
    xB_route = [[solution["xB%s_%s"%(j, i)] for i in range(steps+1)] for j in range(blip_num)]
    yB_route = [[solution["yB%s_%s"%(j, i)] for i in range(steps+1)] for j in range(blip_num)]

    xR_route = [solution["xR_"+str(i)] for i in range(steps+1)]
    yR_route = [solution["yR_"+str(i)] for i in range(steps+1)]

    colors = ['navy', 'darkgreen']
    for i in range(steps):
        for j in range(blip_num):
            ax.plot([xB_route[j][i], xB_route[j][i + 1]], [yB_route[j][i], yB_route[j][i + 1]], label='UAV'+str(j),
                    color = colors[j], linewidth=2,
                    marker='x', markersize=7)

        ax.plot([xR_route[i],xR_route[i+1]], [yR_route[i],yR_route[i+1]],  label='Tank Plane',
                 color= 'firebrick', linewidth=2,
                 marker='x', markersize=7)

        charge = 0
        for j in range(blip_num):
            if solution["FBR%s_%s" % (j, i)] < 0.1:
                charge = 1
        if charge == 1:
            ax.plot([xR_route[i], xR_route[i + 1]], [yR_route[i], yR_route[i + 1]], label='Tank Plane',
                    color='darkorange', linewidth=15, alpha = 0.8,
                    marker='x', markersize=7)

    plt.axis('off')
    plt.margins(0, 0)

    plt.show()
    fig.savefig(name + ".pdf", bbox_inches='tight',pad_inches = 0)
