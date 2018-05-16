from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D


def visualize_file():
	x = []
	y = []
	z = []
	with open('perim.csv', 'r') as f:
		lines = f.readlines()
	i = 0
	for line in lines:
		if i == 0:
			i += 1
			continue
			
		split = line.split(',')
		x.append(float(split[0]))
		y.append(float(split[1]))
		z.append(float(split[2]))


	print(x, y, z)
	fig = pyplot.figure()
	ax = Axes3D(fig)


	ax.scatter(x, y, z)
	pyplot.show()

def show_level_path(path):
	x = []
	y = []
	z = []
	for point in path:
		x.append(point['x'])
		y.append(point['y'])
		z.append(point['z'])
	fig = pyplot.figure()
	ax = Axes3D(fig)


	ax.plot(x, y, z, '.r-')
	pyplot.show()
