#-------------------------------------------------------------------------------
# Name:        D:\Data\DDA\python\LidARaddXY.py
# Purpose:      Take shapefiles and add xy coordinates if not available
#
# Author:      donnaa
#
# Created:     22/04/2014
# Copyright:   (c) donnaa 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
from arcpy import env
import os

def main():
    try:
        basefile = r'R:\Geodatabase\LiDAR\2005\SHAPEFILES\BE_POINTS'
        env.workspace = basefile
        fcList = arcpy.ListFeatureClasses("*.shp", "ALL")
        for x in fcList:
            print x
            arcpy.AddXY_management(x)


    except arcpy.ExecuteError:
    	print arcpy.GetMessages()

if __name__ == '__main__':
    main()
