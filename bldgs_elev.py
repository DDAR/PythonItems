#description	:Finding Lowest Elevation around buildings
#author			:DD Arnett
#date			:20120830
#version		:1.0
#usage			:python hazus_bldingpts.py
#notes			:
#python_version	:2.6.6
#==============================================================================


import arcpy
import os
import string
import time
from arcpy import env

# removes existing database
def killObject( object ):
    if arcpy.Exists(object):
        arcpy.Delete_management(object)

def selectPoints(layerFile, fieldsList, obid):
	try:
		obid = int(obid)
		elevComp = 50000.0
		coordX = ""
		coordY = ""
		selClause1 = '"FID_MissingBld" = %i' % obid
		print selClause1
##		fieldsList = arcpy.ListFields(layerFile, "", "String")
##		for field in fieldsList:
##			print field
		cur = arcpy.da.SearchCursor(layerFile, fieldsList, selClause1)
		for c in cur:
			#print c[1]
			if elevComp > float(c[1]):
				elevComp = float(c[1])
				coordX = str(c[2])
				coordY = str(c[3])
				#print elevComp
		if elevComp != 50000.0:
			elev = str(elevComp)
			#print " %s, %s, %s " % (coordX, coordY, elev)
			printOut(coordX, coordY, elev)
		else:
			print elevComp
			pass
	except:
		print arcpy.GetMessages()

def createPrintOut():
    try:
        txtFile = r'R:\disk_5\projects\HAZUS\EmmaLane\bldingpts.txt'
        killObject(txtFile)
        reportFile = open(txtFile, 'a')
        reportText = "X, Y, ELEV\n"
        reportFile.write(reportText)
        reportFile.close()
    except:
        print arcpy.GetMessages()

def printOut(x, y, Elev):
    try:
        txtFile = r'R:\disk_5\projects\HAZUS\EmmaLane\MissingBldPts.txt'
        reportFile = open(txtFile, 'a')
        reportText = "%s, %s, %s \n" %(x, y, Elev)
        reportFile.write(reportText)
        reportFile.close()
    except:
        print arcpy.GetMessages()

#Variables
buildingLines = r'R:\disk_5\projects\HAZUS\EmmaLane\HAZUS_Project.gdb\MissingBld'
lidarPointsBuilding = r'R:\disk_5\projects\HAZUS\EmmaLane\HAZUS_Project.gdb\mb_pts_id_Project'
geoDataBase = r'R:\disk_5\projects\HAZUS\EmmaLane\HAZUS_Project.gdb'
lineFields = ["FID_MissingBld", "ELEVATION", "POINT_X", "POINT_Y"]
newbuild = r'R:\disk_5\projects\HAZUS\EmmaLane\HAZUS_Project.gdb\missingbuildingpoints'

try:
    #arcpy.SelectLayerByAttribute_management(buildingLines, "NEW_SELECTION", """ "FID_buldings_200ft" = '1' """)
    killObject(newbuild)
    arcpy.MakeFeatureLayer_management(lidarPointsBuilding, newbuild)
    createPrintOut()
    for i in range(1, 415):
        print "%i" % i
        selectPoints(newbuild, lineFields, i)


except:
    print arcpy.GetMessages()
