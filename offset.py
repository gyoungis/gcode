import pyclipper

points = []
with open('perim.csv', 'r') as f:
		lines = f.readlines()
i = 0
z = -1
for line in lines:
	split = line.split(',')
	if i == 0:
		i += 1
		continue
	elif i == 1:
		z = split[2]
		# print(z)
	if (split[2] == z):
		points.append((float(split[0]), float(split[1])))
	# x.append(float(split[0]))
	# y.append(float(split[1]))
	# z.append(float(split[2]))
tuplePoints = tuple(points)
# print(tuplePoints)

pco = pyclipper.PyclipperOffset()

pco.AddPath(pyclipper.scale_to_clipper(tuplePoints), pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)

solution = pyclipper.scale_from_clipper(pco.Execute(-1.0))

# print('solution: ', pyclipper.scale_from_clipper(solution))
# print(solution[0])
print('x, y')
for pointTuple in solution[0]:
	print('%s, %s' % (pointTuple[0], pointTuple[1]))

