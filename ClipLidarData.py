""" #####################################################
    NAME: cliplidardata.py
    Source Name:    
    Version: ArcGIS 10
    Author: DD Arnett
    Usage: manage lidar geodatabases
    Required Arguments:    
    Optional Arguments:
    Description: Takes the Lidar data and clips then exports the data into section files.    
    Date Created: May 24, 2011
    Updated: 
##################################################### """
import os
import sys
import arcpy
import time
import shutil
import smtplib
import base64
from arcpy import env
from datetime import date

def message(msg):
	LocalTime = time.asctime(time.localtime(time.time()))
	mmsg = msg + LocalTime; arcpy.AddMessage(mmsg); print mmsg

# Set Date and other variables
now = date.today()
user = os.environ["USERNAME"]
rt = "Actual Start Time: "; message(rt)
env.overwriteoutput = True
starttime = time.time()
base = "d:\\data\\DDA\\temp\\misclayers.gdb"
logfile = "d:\\data\\temp\\lidar_update.txt"
lidar_file = "N:\\Geodatabase\\LiDAR\\2000_BOR\\BareEarth.gdb\\YFO_Contours_From_Bare_Earth_LiDAR_2000"
pls_file = base + "\\pls_statewide"
pls_layer = "pls_lyr"
plsSelect = base + "\\plsSelected"
keylist = []
field = "RTS"


try:
	#Select from the statewide pls those that intersect with input layer
	if arcpy.Exists(pls_layer):
		arcpy.Delete_management(pls_layer)
	arcpy.MakeFeatureLayer_management(pls_file, pls_layer)
	arcpy.SelectLayerByLocation_management(pls_layer, "INTERSECT", lidar_file,)
	if arcpy.Exists(plsSelect):
		arcpy.Delete_management(plsSelect)
	arcpy.CopyFeatures_management(pls_layer, plsSelect)

	#Start to walk through and create a list of RTS
	frqRows = arcpy.SearchCursor(plsSelect, "", "", field)
	frqRow = frqRows.next()
	while frqRow:
		keyValue = str(frqRow.getValue(field))
		keylist.append(frqRow.getValue(field))
		frqRow = frqRows.next()

	for key in keylist:
		tkey = str(key)
		clue = '"RTS" = ' + tkey
		ofile = "cont_" + tkey + ".shp"
		outfile = "N:\\Geodatabase\\LiDAR\\2000_BOR\\SHAPEFILES\\CONTOURS\\" + ofile
		if arcpy.Exists(pls_layer):
			arcpy.Delete_management(pls_layer)
		arcpy.MakeFeatureLayer_management(plsSelect, pls_layer)
		arcpy.SelectLayerByAttribute_management(pls_layer, "NEW_SELECTION", clue)
		arcpy.Clip_analysis(lidar_file, pls_layer, outfile)
		arcpy.Delete_management(pls_layer)
		

except IOError as e:
    print 'Exception error is: %s' % e
