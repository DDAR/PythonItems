#-------------------------------------------------------------------------------
# Name:        GetLiDARElev.py
# Purpose:      Takes a point file and finds any bare earth point within a
#               5 feet radius and picks the highest value and reports it in
#               a text file in comma deliminated format.
#
#               note the program also requires a DIST field and BANK field in
#               the input point file. This could be edited out if needed to use
#               for another purpose.
#
# Author:      Donna Arnett
#
# Created:     18/11/2014
# Copyright:   (c) donnaa 2014
# Licence:     Hidden
#-------------------------------------------------------------------------------

import arcpy
from arcpy import env
import numpy
import os


# Variables --------------------------------------------------------------------

    # Point file
leveePoints = r'R:\disk_5\projects\county\pw\surface_water\FedLeveeAnalysis\LeveeCredit\LeveeData.gdb\MeasuredBankPoints'
    # LiDAR bare earth point file
lidarPts = r'R:\Geodatabase\LiDAR\2013_NachesYakima\BareEarthPoints.gdb\BE_Points'
    # Text file for reporting the findings
reportFile = r'R:\disk_5\projects\county\pw\surface_water\FedLeveeAnalysis\LeveeCredit\newElev.txt'

    # If text file exist delete
if os.path.exists(reportFile):
        os.remove(reportFile)
    # Start and open the text file
f = open(reportFile, 'w')
    # Create a feature layer for ease and use in arcpy
arcpy.MakeFeatureLayer_management(lidarPts, 'lidar')
    # Cursor to go through each point within the point file
with arcpy.da.SearchCursor(leveePoints, ['OID@', 'DIST', 'SHAPE@X', 'SHAPE@Y', 'BANK']) as cursor:
    for row in cursor:
            # pull out the x and y values to create a point and establish it's geometry
        ptsSamp = arcpy.Point(row[2], row[3])
        ptGeo = arcpy.PointGeometry(ptsSamp)
            # Buffer the point and select LiDAR BE points - can change the buffer distance here
        arcpy.SelectLayerByLocation_management('lidar', 'intersect', ptGeo.buffer(5))
            # Count how many points were selected
        matchCount = int(arcpy.GetCount_management('lidar').getOutput(0))
        if matchCount > 0:
                # begin a list to place the elevation values into
            heightList = []
                # cursor through selected LiDAR points and place in list
            with arcpy.da.SearchCursor('lidar', ['Z']) as rows:
                for row2 in rows:
                    heightList.append(row2[0])
                # Delete variables
            del rows
            del row2
                # sort list so that the highest value is last and can be selected
            heightList.sort()
            max = str(heightList[-1])
                # determine which bank point belongs to (for the Levee exersize)
            if row[4] == 1:
                bank = 'RIGHT BANK'
            else:
                bank = 'LEFT BANK'
                # Build the line that gets written into the text file - print it to screen and then write to text file
            line = str(row[0]) + ", " + bank + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ", " + max
            print line
            f.write(line + '\n')
    # Delete variables after cursor has closed
del row
del cursor
    # Close the text file.
f.close()
