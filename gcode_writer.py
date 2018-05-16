import numpy as np
import scipy
import pandas
from pprint import pprint

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
	zValues = []
	i = 0
	for coord in coords: #partition by z value

		if (coord['z'] not in layers):
			layers[coord['z']] = []
			zValues.append(coord['z'])
		layers[coord['z']].append(coord)

	diff = 0
	#for z, layer in layers.items():
	counter = 0
	for z, layer in layers.items():
		if (counter == 0):
			diff = z
			#diff = layer
			counter += 1
		elif (counter == 1):
			diff -= z
			#diff -= layer
			diff = abs(diff)
			break




	print(zValues)
	print("voxel Size is ")
	print(diff)
	return (layers, diff, zValues)





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


def getBoundaryPath(curLevel, voxelSize):
	path = {} #{[x, y]} holds path for 3d printing
	currentLayer = curLevel
	radius = np.sqrt(voxelSize**2 + voxelSize**2)
	#print(curLevel)
	minPoint = getMinPoint(currentLayer)
	currentPoint = minPoint
	refPoint = pathSetup(currentLayer, radius, minPoint)
	#print(minPoint)
	path.update(minPoint)
	path.update(refPoint)
	moveTo = findRightMost(curLevel, radius, currentPoint, refPoint)
	#print(moveTo)


	# while moveTo != minPoint:
	# 	moveTo = findRightMost(curLevel, radius, currentPoint, refPoint)
	# 	# if (moveTo != refPoint):
	# 	# 	print('minPoint: ', minPoint, 'moveTo: ', moveTo)
	# 	path.update(moveTo)
	# 	currentPoint = refPoint

	# 	refPoint = moveTo
	# 	print('refPoint: ', refPoint)



def pointEquals(point1, point2):
	ret = point1['x'] == point2['x'] and point1['y'] == point2['y'] and point1['z'] == point2['z']
	#print(ret)
	return ret


def validPoint(point):
	if 'x' in point and 'y' in point and 'z' in point:
		return point['x'] != None and point['y'] != None and point['z'] != None
	return False

def findRightMost(curLevel, radius, currentPoint, refPoint):
	counter = 0
	moveTo = {}

	for coord in curLevel:
		if not validPoint(coord) or not validPoint(refPoint) or not validPoint(currentPoint):
			print('Invalid point one of: ', coord, refPoint, currentPoint)
			pass
		# print(coord)

		distance = np.sqrt((coord['x'] - refPoint['x'])**2 + (coord['y'] - refPoint['y'])**2)
		if not pointEquals(coord, refPoint) and not pointEquals(coord, currentPoint) and distance <= radius:#distance <= radius and coord != refPoint:
			xProd = (refPoint['x'] - currentPoint['x']) * (coord['y'] - currentPoint['y']) - (refPoint['y'] - currentPoint['y']) * (coord['x'] - currentPoint['x'])
			if counter < 1:
				turnIndex = xProd
				moveTo = coord
				counter += 1
			else:
				if xProd < turnIndex:
					turnIndex = xProd
					moveTo = coord
	print("this is move to ")
	print(moveTo)
	return moveTo


	
					

def pathSetup(curLevel, radius, minPoint):
	#Gets first first move for each layer
	state1 = {}
	state2 = {}
	state3 = {}
	state4 = {}
	nextPoint = {}
	for coord in curLevel:
		if coord['x'] > minPoint['x']:
			if coord['y'] == minPoint['y']:
				state1 = coord
			else:
				state2 = coord
		if coord['x'] == minPoint['x']:
			state3 = coord
		if coord['x'] > minPoint['x']:
			state4 = coord

	if state1 is not None:
		nextPoint = state1

	if state1 is None and state2 is not None:
		nextPoint = state2

	if state1 is None and state2 is None and state3 is not None:
		nextPoint = state3

	if state1 is None and state2 is None and state3 is None and state4 is not None:
		nextPoint = state4

	return nextPoint




	
def getMinPoint(curLevel):
	minPoint = curLevel[0]
	for coord in curLevel: #Find minimum y-coordinate
		if coord['y'] <= minPoint['y']:
			minPoint = coord

	for coord in curLevel: #If multiple min-y, pick the min-x
		if coord['y'] == minPoint['y']:
			if coord['x'] < minPoint['x']:
				minPoint = coord

	return minPoint


def nextPoint(currentPoint, radius, curLevel):
	
	for coord in curLevel:
		distance = np.sqrt((coord['x']-currentPoint['x'])**2 + (coord['y']-currentPoint['y'])**2)
		#if distance <= radius:




def seperateLayers(perim, zValues, voxelSize):

	for value in zValues:
		curLevel = []
		for coord in perim:
			if coord['z'] == value:
				curLevel.append(coord)

		getBoundaryPath(curLevel, voxelSize)
		print(value)


#def getPath(value, perim):
	#curLevel = []
	#for coord in perim:
	#	if coord['z'] == value:
	#		curLevel.append(coord)

	#print(curLevel)





if __name__ == "__main__":
	coords = parseFile()
	layers, voxelSize, zValues = getLayers()
	# print(layers[0.971563])
	#print(voxelSize)
	perim = findPerim(layers, voxelSize)
	print('%s, %s, %s' % ('x', 'y', 'z'))
	seperateLayers(perim, zValues, voxelSize)

	
	#for coord in perim:
		# print(coord)
		#print('%s, %s, %s' % (coord['x'], coord['y'], coord['z']))



	writeGCode()