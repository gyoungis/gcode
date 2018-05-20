import numpy as np
import scipy
import pandas
from pprint import pprint
import visualize_perim as vp
import pathTogCode as ptG



def getYLayers(coords):
	#Find Y-dimension of layer

	layers = {} #{[{x, y, z}]}
	for coord in coords: #partition by z value

		if (coord['y'] not in layers):
			layers[coord['y']] = []
		# else:
		# 	if (coord['y'] == -0.814937):
		# 		print(coord['y'], ' already in layers')
		layers[coord['y']].append(coord)
	return layers

def getXLayers(coords):
	#Find X-dimension of layer

	layers = {}
	for coord in coords:

		if (coord['x'] not in layers):
			layers[coord['x']] = []

		layers[coord['x']].append(coord)

	return layers





def findPerimY(layer, voxelSize):
	#Find all perimeter points

	#Get dimensions of layer
	yLayers = getYLayers(layer)
	xLayers = getXLayers(layer)


	i = 0
	#Search for boundary points along each y-coordinate
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

	#Search for boundary points along each x-coordinate
	for _, xLayer in xLayers.items():
		state = 'inShape'
		perim.append(xLayer[0])
		expectedY = xLayer[0]['y']
		prev = xLayer[0]
		for coord in xLayer:
			if (state == 'notInShape'):
				if (coord['y'] == expectedY):
					perim.append(coord)
					state = 'inShape'
			elif (state == 'inShape'):
				if coord['y'] != expectedY:
					perim.append(prev)
					state = 'notInShape'
			prev = coord
		perim.append(xLayer[len(xLayer) - 1])


	return perim




def getLayers():
	#Find Z-values for each of the layers to be printed
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




	# print(zValues)
	# print("voxel Size is ")
	# print(diff)
	return (layers, diff, zValues)





def parseFile():
	#Get point coordinates from the text file
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
	#Get the values of all the boundary points in the model

	perim = []
	for _, layer in layers.items():
		# print(layer[0]['x'])
		yPerim = findPerimY(layer, voxelSize)
		for coord in yPerim:
			perim.append(coord)
		#append new points to perim array
	return perim





def getBoundaryPath(curLevel, voxelSize):
	#Get path for the boundary of the layer

	path = [] #{[x, y]} holds path for 3d printing
	currentLayer = curLevel
	radius = 2 *np.sqrt(voxelSize**2 + voxelSize**2)
	#print("this is radius: ")
	#print(radius)
	#print(curLevel)
	minPoint = getMinPoint(currentLayer)
	currentPoint = minPoint
	#print("This is the MinPoint: ")
	###print(minPoint)
	refPoint = pathSetup(currentLayer, radius, minPoint)
	
	path.append(minPoint)
	path.append(refPoint)
	moveTo = findRightMost(curLevel, radius, currentPoint, refPoint)
	#print(moveTo)


	# minPoint = refPoint
	# refPoint = moveTo
	# moveTo = findRightMost(curLevel, radius, currentPoint)
	


	while moveTo != minPoint:
		#Keep adding points until you reach the starting point again

		moveTo = findRightMost(curLevel, radius, currentPoint, refPoint)
		# if (moveTo != refPoint):
		# 	print('minPoint: ', minPoint, 'moveTo: ', moveTo)
		path.append(moveTo)
		currentPoint = refPoint

		refPoint = moveTo

	print(path)
	#vp.show_level_path(path)



	




def pointEquals(point1, point2):
	#Tests if the 2 points are the same
	ret = point1['x'] == point2['x'] and point1['y'] == point2['y'] and point1['z'] == point2['z']
	#print(ret)
	return ret


def validPoint(point):
	#Tests if the point exists

	if 'x' in point and 'y' in point and 'z' in point:
		return point['x'] != None and point['y'] != None and point['z'] != None
	return False

def findRightMost(curLevel, radius, currentPoint, refPoint):
	#Finds the next point on the path based on making right turns

	counter = 0
	moveTo = {}

	# print("This is the current: ")
	# print(currentPoint)
	# print("This is the ref: ")
	# print(refPoint)

	for coord in curLevel:
		if not validPoint(coord) or not validPoint(refPoint) or not validPoint(currentPoint):
			print('Invalid point one of: ', coord, refPoint, currentPoint)
			pass
		# print(coord)

		distance = np.sqrt((coord['x'] - refPoint['x'])**2 + (coord['y'] - refPoint['y'])**2)
		if not pointEquals(coord, refPoint) and not pointEquals(coord, currentPoint) and distance <= radius:
			xProd = (refPoint['x'] - currentPoint['x']) * (coord['y'] - currentPoint['y']) - (refPoint['y'] - currentPoint['y']) * (coord['x'] - currentPoint['x'])
			if counter < 1:
				turnIndex = xProd
				moveTo = coord
				counter += 1
			else:
				if xProd < turnIndex:
					turnIndex = xProd
					moveTo = coord
	# print("this is move to ")
	# print(moveTo)
	return moveTo


	
					

def pathSetup(curLevel, radius, minPoint):
	#Gets first first move for each layer

	state1 = {}
	state2 = {}
	state3 = {}
	state4 = {}
	nextPoint = {}
	for coord in curLevel:
		#print(coord)
		distance = np.sqrt((coord['x'] - minPoint['x'])**2 + (coord['y'] - minPoint['y'])**2)
		# print("this is distance: ")
		# print(distance)
		if not pointEquals(coord, minPoint) and distance <= radius:

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

	# print("this is next: ")
	# print(nextPoint)
	return nextPoint




	
def getMinPoint(curLevel):
	#Finds the bottom-most and left-most point in the current layer

	minPoint = curLevel[0]
	for coord in curLevel: #Find minimum y-coordinate
		if coord['y'] <= minPoint['y']:
			minPoint = coord

	for coord in curLevel: #If multiple min-y, pick the min-x
		if coord['y'] == minPoint['y']:
			if coord['x'] < minPoint['x']:
				minPoint = coord

	return minPoint





def seperateLayers(perim, zValues, voxelSize):
	#Gets boundary path for each layer separately

	for value in zValues:
		curLevel = []
		for coord in perim:
			if coord['z'] == value:
				curLevel.append(coord)

		print("Current Level: ")
		print(value)

		getBoundaryPath(curLevel, voxelSize)
		






if __name__ == "__main__":
	coords = parseFile()
	layers, voxelSize, zValues = getLayers()
	# print(layers[0.971563])
	#print(voxelSize)
	#print(zValues)
	perim = findPerim(layers, voxelSize)
	print('%s, %s, %s' % ('x', 'y', 'z'))
	seperateLayers(perim, zValues, voxelSize)

	
	#for coord in perim:
		#print(coord)
		#print('%s, %s, %s' % (coord['x'], coord['y'], coord['z']))



	ptG.startUp()
	#3D printer startup code