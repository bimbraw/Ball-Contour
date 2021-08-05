import csv

#import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt

fig = plt.figure()
ax = p3.Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)

fileName = 'FistRelax-200205-01-Mocap'
with open('C:/Users/Jacka/Desktop/Research/3D Model/Data/CSVs/Formatted/' + fileName + '.csv') as csv_file:
    coords = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    x_coords = []
    y_coords = []
    z_coords = []
    rowNum = 0
    for row in coords:
        coordCount = 1
        x_row = []
        y_row = []
        z_row = []
        for num in row:
            if coordCount % 3 == 1:
                x_row.append(num)
            elif coordCount % 3 == 2:
                y_row.append(num)
            else:
                z_row.append(num)
            coordCount += 1
        x_coords.append(x_row)
        y_coords.append(y_row)
        z_coords.append(z_row)
        rowNum += 1

global frameNum

frameNum = 1
x = np.array(x_coords[frameNum - 1])
y = np.array(y_coords[frameNum - 1])
z = np.array(z_coords[frameNum - 1])

points, = ax.plot(x, y, z, '*')
lines, = ax.plot(x, y, z, 'none')

fingersColor = 'r-'
thumb, = ax.plot(x[0:4], y[0:4], z[0:4], fingersColor)
pointer, = ax.plot(x[4:8], y[4:8], z[4:8], fingersColor)
middle, = ax.plot(x[8:12], y[8:12], z[8:12], fingersColor)
ring, = ax.plot(x[12:16], y[12:16], z[12:16], fingersColor)
pinky, = ax.plot(x[16:20], y[16:20], z[16:20], fingersColor)
fingers = [thumb, pointer, middle, ring, pinky]


def update_plot(num, x, y, z, points, lines, fingers):
    global frameNum
    skipNum = 1

    frameNum += skipNum
    new_x = np.array(x_coords[frameNum - 1])
    new_y = np.array(y_coords[frameNum - 1])
    new_z = np.array(z_coords[frameNum - 1])

    if frameNum + skipNum >= rowNum:
        frameNum = 1

    points.set_data(new_x, new_y)
    points.set_3d_properties(new_z, 'z')
    lines.set_data(new_x, new_y)
    lines.set_3d_properties(new_z, 'z')

    pointCount = 0
    for finger in fingers:
        finger.set_data(new_x[pointCount:pointCount + 4], new_y[pointCount:pointCount + 4])
        finger.set_3d_properties(new_z[pointCount:pointCount + 4], 'z')
        pointCount += 4


ani = animation.FuncAnimation(fig, update_plot, interval=1, fargs=(x, y, z, points, lines, fingers))
#ani.save(fileName + '.mp4', fps=1000)
plt.show()
