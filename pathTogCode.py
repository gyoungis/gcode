import numpy as np
import scipy
import pandas


def startUp():
	#3D printer start-up code

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


def boundaryGCode(path, file):
	#gcode for boundaries