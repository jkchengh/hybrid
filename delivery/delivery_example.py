from matplotlib import pyplot as plt
from shapely.geometry.polygon import LinearRing, Polygon
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

name = "truck_drone"
fig = plt.figure()
ax = plt.subplot(111)
axes = fig.gca()
axes.set_xlim([-5, 105])
axes.set_ylim([0, 55])
y1 = 30
y2 = 20
# ratio = 1
# xleft, xright = ax.get_xlim()
# ybottom, ytop = ax.get_ylim()
# ax.set_aspect(abs((xright - xleft) / (ybottom - ytop)) * ratio)


# path
ax.plot([0, 100], [y1] * 2,
        linewidth=50, label="depot", color="dimgray", alpha=0.5)
ax.plot([-5, 20, 45, 71, 97], [y1] * 5, marker = 4, markersize = 40,
        linewidth=0, label="depot", color="dimgray", alpha=0.5)
ax.plot([0, 100], [y2] * 2,
        linewidth=50, label="depot", color="dimgray", alpha=0.5)
ax.plot([3, 29, 55, 80, 105], [y2] * 5, marker = 5, markersize = 40,
        linewidth=0, label="depot", color="dimgray", alpha=0.5)

# all route
T1x_route = [65, 60, 45, 5]
T1y_route = [y1-2] * len(T1x_route)
T2x_route = [35, 40, 55, 95]
T2y_route = [y2+2] * len(T2x_route)

# text
ax.text(T1x_route[0]+2, T1y_route[0]-3, r'Package1', color='darkgreen', fontsize=12)
ax.text(T1x_route[0]+2, T1y_route[0], r'Truck1', color='firebrick', fontsize=12)
ax.text(T1x_route[0]+2, T1y_route[0]+3, r'Drone1', color='navy', fontsize=12)
ax.text(T2x_route[0]-12, T2y_route[0], r'Truck2', color='firebrick', fontsize=12)
ax.text(T2x_route[0]-12, T2y_route[0]-3, r'Drone2', color='navy', fontsize=12)
ax.text(T2x_route[0]-16, T2y_route[0]-6, r'Package2', color='darkgreen', fontsize=12)

ax.text(T1x_route[1]-2, T1y_route[1]+1, r'Off', color='darkgreen', fontsize=12)
ax.text(T1x_route[2]-2, T1y_route[2]+1, r'On', color='darkgreen', fontsize=12)
ax.text(T1x_route[3]+1, T1y_route[3]+1, r'Off', color='darkgreen', fontsize=12)

ax.text(T2x_route[1]-3, T2y_route[0]-3, r'Off', color='darkgreen', fontsize=12)
ax.text(T2x_route[2]-3, T2y_route[0]-3, r'On', color='darkgreen', fontsize=12)
ax.text(T2x_route[3]-8, T2y_route[0]-3, r'Off', color='darkgreen', fontsize=12)

ax.text(62, 12, r'Package1 Destination', color='darkgreen', fontsize=12)
ax.text(3, 36, r'Package2 Destination', color='darkgreen', fontsize=12)

# truck route
ax.plot(T1x_route, T1y_route, label = 'T1',
                     color = 'darkgreen', linewidth = 2,
                     marker = 'x', markersize = 7)
ax.plot(T2x_route, T2y_route, label = 'T1',
                     color = 'darkgreen', linewidth = 2,
                     marker = 'x', markersize = 7)
ax.plot(T1x_route[1:3], T1y_route[1:3], label = 'T1',
                     color = 'firebrick', linewidth = 2,
                     marker = 'x', markersize = 7)
ax.plot(T2x_route[1:3], T2y_route[1:3], label = 'T1',
                     color = 'firebrick', linewidth = 2,
                     marker = 'x', markersize = 7)

# drone router
ax.plot([60,55], [y1-2, y2+2], label = 'D1',
                     color = 'navy', linewidth = 2,
                     marker = 'x', markersize = 7)
ax.plot([40,45], [y2+2, y1-2], label = 'TD1',
                     color = 'navy', linewidth = 2,
                     marker = 'x', markersize = 7)
ax.plot([5,0], [y1-2, 38], label = 'D1',
                     color = 'navy', linewidth = 2,
                     marker = 'x', markersize = 7)
ax.plot([95,100], [y2+2, 12], label = 'TD1',
                     color = 'navy', linewidth = 2,
                     marker = 'x', markersize = 7)


plt.axis('off')
plt.margins(0, 0)

plt.show()
fig.savefig(name + ".pdf", bbox_inches='tight',pad_inches = 0)