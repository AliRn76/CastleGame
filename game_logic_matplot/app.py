import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Initialize
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1, .3, .3, 1]))
ax.set_axis_off()
X_MIN, X_MAX = 1, 11
Y_MIN, Y_MAX = 0, 3
Z_MIN, Z_MAX = 0, 3

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # Add Borders
border_color = 'black'
line_x_min = np.linspace(X_MIN, X_MIN, 100)
line_y_min = np.linspace(Y_MIN, Y_MIN, 100)
line_z_min = np.linspace(Z_MIN, Z_MIN, 100)

line_x_max = np.linspace(X_MAX, X_MAX, 100)
line_y_max = np.linspace(Y_MAX, Y_MAX, 100)
line_z_max = np.linspace(Z_MAX, Z_MAX, 100)

line_x = np.linspace(X_MIN, X_MAX    , 100)
line_y = np.linspace(Y_MIN, Y_MAX, 100)
line_z = np.linspace(Z_MIN, Z_MAX, 100)

# Bottom
ax.plot(line_x, line_y_min, line_z_min, color=border_color)
ax.plot(line_x, line_y_max, line_z_min, color=border_color)
ax.plot(line_x_min, line_y, line_z_min, color=border_color)
ax.plot(line_x_max, line_y, line_z_min, color=border_color)

# Top
# ax.plot(line_x, line_y_min, line_z_max, color=border_color)
# ax.plot(line_x, line_y_max, line_z_max, color=border_color)
ax.plot(line_x_min, line_y, line_z_max, color=border_color)
ax.plot(line_x_max, line_y, line_z_max, color=border_color)

# Side
ax.plot(line_x_min, line_y_min, line_z, color=border_color)
ax.plot(line_x_min, line_y_max, line_z, color=border_color)
ax.plot(line_x_max, line_y_min, line_z, color=border_color)
ax.plot(line_x_max, line_y_max, line_z, color=border_color)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # Set Towers
alpha = .9
axes = [12, 3, 3]
data = np.ones(axes, dtype=np.bool)
colors = np.empty(axes + [4], dtype=np.float32)

for i in range(12):
    colors[i] = [1, 0, 1, alpha]

data[-1] = True
data[-12] = True
for i in range(2, 12):
    data[-i] = False

ax.voxels(data, facecolors=colors)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # Set Archers
archer1_x = [X_MIN - 0.5]
archer2_x = [X_MAX + 0.5]
archer_y = [(Y_MAX + Y_MIN) / 2]
archer_z = [Z_MAX + 0.5]

ax.scatter3D(archer1_x, archer_y, archer_z, s=70, color='green')
ax.scatter3D(archer2_x, archer_y, archer_z, s=70, color='green')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
plt.show()

# TODO:
#   1. Create Unit
#   2. Move Unit in straight line
#   3. Search for enemy in range
#   4. Attack Enemy (Print Something till one of them die)


