def getYLayers(coords):
	layers = {} #{[{x, y, z}]}
	for coord in coords: #partition by z value

		if (coord['y'] not in layers):
			layers[coord['y']] = []
		# else:
		# 	if (coord['y'] == -0.814937):
		# 		print(coord['y'], ' already in layers')
		layers[coord['y']].append(coord)
	return layers






def findPerimY(layer, voxelSize):
	#print(layer[0]['x'])
	#array of point objects {x, y, z}
	#create 2d array like layers with 1st dimension as y values and 2nd as x values of that y position
	#for each y
		#sort x values
	#for each y
		#state = something
		#add y[0] to perim
		#val = 0
		#for i in len(y) val += voxelSize
			#case nothing:
				#if something
					#add point to perim
					#state = something
			#case something
				#if nothing
					#add prev to perim
					#state = nothing
				#prev = cur
		#add y[lastIndex] to perim
	#return set of points on perim

	yLayers = getYLayers(layer)
	i = 0
	# print(yLayers
	perim = []
	for _, yLayer in yLayers.items():
		state = 'inShape'
		perim.append(yLayer[0])
		expectedX = yLayer[0]['x']
		prev = yLayer[0]
		for coord in yLayer:
			if (state == 'notInShape'):
				if (coord['x'] == expectedX):
					perim.append(coord)
					state = 'inShape'
			elif (state == 'inShape'):
				if coord['x'] != expectedX:
					perim.append(prev)
					state = 'notInShape'
			prev = coord
		perim.append(yLayer[len(yLayer) - 1])
	return perim


	# print('words')

def getLayers():
	layers = {} #{[{x, y, z}]}
	i = 0
	for coord in coords: #partition by z value

		if (coord['z'] not in layers):
			layers[coord['z']] = []
		layers[coord['z']].append(coord)

	diff = 0
	for z, layer in layers.items():
		if (i == 0):
			diff = z
		elif (i == 1):
			diff -= z
			diff = abs(diff)
			break
	return (layers, diff)





def parseFile():

	midPoints = open("hemisphere.txt", "r")


	lines = midPoints.readlines()

	coords = [] #[{x, y, z}]



	#Model from blender has y-coord as 3rd col and z as 2nd col
	del lines[0]
	for x in lines:
		coord = {}
		split = x.split(' ')
		coord['x'] = float(split[0])
		coord['y'] = float(split[2].split('\n')[0])
		coord['z'] = float(split[1])
		coords.append(coord)
	midPoints.close()
	return coords






def findPerim(layers, voxelSize):
	perim = []
	for _, layer in layers.items():
		# print(layer[0]['x'])
		yPerim = findPerimY(layer, voxelSize)
		for coord in yPerim:
			perim.append(coord)
		#append new points to perim array
	return perim


def writeGCode():
	gcode = open("gcode.txt", "w")

	#Start-Up code
	gcode.write("G28 ;\n")  #home all axes
	gcode.write("G92 E0\n")
	gcode.write("G1 X30 Y30 F3000\n")
	gcode.write("G1 Z5 F2000 ;\n")
	gcode.write("G1 F3000 X220\n")
	gcode.write("G1 F2000 Z0\n")
	gcode.write("G1 F200 E10\n")
	gcode.write("G1 F1000 E9\n")
	gcode.write("G1 F3000 X190 Y50\n")
	gcode.write("G92 E-1\n")
	gcode.write("G1 F2000 Z1\n")
	gcode.write("G21\n")
	gcode.write("G90\n")
	gcode.write("M82\n")
	gcode.write("G92 E0\n")


def getBoundaryPath(currentLayer):
	path = {} #{[x, y]} holds path for 3d printing


if __name__ == "__main__":
	coords = parseFile()
	layers, voxelSize = getLayers()
	# print(layers[0.971563])
	perim = findPerim(layers, voxelSize)
	print('%s, %s, %s' % ('x', 'y', 'z'))
	for coord in perim:
		# print(coord)
		print('%s, %s, %s' % (coord['x'], coord['y'], coord['z']))

	layer1 = np.split(layers, np.where(orig[:-1, 2] != orig[1:, 2])[0]+1)
	print(layer1)

	writeGCode()