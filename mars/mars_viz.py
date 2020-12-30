from matplotlib import pyplot as plt
from shapely.geometry.polygon import LinearRing, Polygon
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

def mars_plot(statistics, solution, steps, name):

    regions = statistics["regions"]
    min_x, max_x = statistics["min_x"], statistics["max_x"]
    min_y, max_y = statistics["min_y"], statistics["max_y"]
    max_E = statistics["max_E"]
    initial_state, goal_states = statistics["initial_state"], statistics["goal_states"]

    ratio = 1
    fig = plt.figure()
    ax = plt.subplot(111)
    axes = fig.gca()
    axes.set_xlim([min_x, max_x])
    axes.set_ylim([min_y, max_y])
    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()
    ax.set_aspect(abs((xright - xleft) / (ybottom - ytop)) * ratio)


    for region in regions:
        type = region["type"]
        if type == "charge":
            location = region["polygon"]
            ax.plot([location[0]], [location[1]], color = "darkorange",
                     marker = ">", markersize = 15)
        else:
            if type == "obstacle":
                color = "dimgray"
                alpha = 0.4
            if type == "ground":
                color = "green" #"#d0f0cc"
                alpha = 0.3
            elif type == "mountain":
                color = "red"#"rosybrown"
                alpha = 0.3
            elif type == "basin":
                color = "blue"# "lightsteelblue"
                alpha = 0.3
            poly = Polygon(region["polygon"])
            x, y = poly.exterior.xy
            ax.fill(x, y, facecolor = color, alpha = alpha)

    # plot solution
    xR_route = [solution["xR_"+str(i)] for i in range(steps+1)]
    yR_route = [solution["yR_"+str(i)] for i in range(steps+1)]
    xA_route = [solution["xA_"+str(i)] for i in range(steps+1)]
    yA_route = [solution["yA_"+str(i)] for i in range(steps+1)]

    # Initial State
    ax.text(xR_route[0]-9, yR_route[0]-4, r'Rover', color='firebrick',fontsize=15)
    ax.text(xA_route[0]-14, yA_route[0]-4, r'Astronaut', color='navy', fontsize=15)
    ax.text(xA_route[steps] - 30, yA_route[steps] - 4, r'Destination', color='navy', fontsize=15)

    for i in range(1,steps):
        if solution["E_"+str(i+1)] - solution["E_"+str(i)]> 0:
            ax.text(xR_route[i]-9, yR_route[i]+4, r'Charge', color='darkorange', fontsize=15)
        if solution["E_"+str(i+1)] - solution["E_"+str(i)] <= 0:
            if solution["FAR_" + str(i-1)] == 0 and solution["FAR_" + str(i)] == 1:
                ax.text(xR_route[i] - 6, yR_route[i] + 4, r'Off', color='darkgreen', fontsize=15)
        if solution["E_" + str(i)] - solution["E_" + str(i-1)] <= 0:
            if solution["FAR_" + str(i-1)] == 1 and solution["FAR_" + str(i)] == 0:
                ax.text(xR_route[i] - 6, yR_route[i] + 4, r'On', color='darkgreen', fontsize=15)

    for i in range(steps):
        if solution["FAR_"+str(i)] == 0:
            ax.plot([xR_route[i],xR_route[i+1]], [yR_route[i],yR_route[i+1]],  label='Merge',
                     color='darkgreen', linewidth=2,
                     marker='x', markersize=7)
        else:
            ax.plot([xR_route[i],xR_route[i+1]], [yR_route[i],yR_route[i+1]], label = 'Rover',
                     color = 'firebrick', linewidth = 2,
                     marker = 'x', markersize = 7)
            ax.plot([xA_route[i],xA_route[i+1]], [yA_route[i],yA_route[i+1]],  label = 'Astro',
                     color = 'navy', linewidth = 2,
                     marker = 'x', markersize = 7)
    plt.axis('off')
    plt.margins(0, 0)

    plt.show()
    fig.savefig(name + ".pdf", bbox_inches='tight',pad_inches = 0)
