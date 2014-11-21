#-------------------------------------------------------------------------------
# Name:        getMedian.py
# Purpose:     Calculates median statistics on a list of values.
# Version:     ArcGIS 10.2 and Python 2.7.5
#
# For:         Planning - Agriculture Zoning Evaluation
#
# Author:      DD Arnett
#
# Created:     23/10/2014
# Copyright:   (c) donnaa 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
import sys
import traceback
import numpy

#Calculates Median Statistics
# env settings

arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False

def GetMedian(in_list):
    medianValue = numpy.median(in_list)
    return medianValue

def GetAverage(in_list):
    avgValue = numpy.average(in_list)
    return avgValue


def GetMedianValues(source_fc, value_field):
    use_vals = []
    with arcpy.da.SearchCursor(source_fc, [value_field]) as rows:
        for row in rows:
            if row[0] != None:
                use_vals.append(row[0])
    if len(use_vals) > 0:
        median = GetMedian(use_vals)
        avg = GetAverage(use_vals)


    return (str("%.2f" % median), str("%.2f" % avg))

def GetAgList(sValue, source_fc, value_field):
    where_Clause = whereClause = '"PARC"' + " = " + str(sValue)
    print where_Clause
    use_vals = []
    with arcpy.da.SearchCursor(source_fc, [value_field], where_Clause) as rows:
        for row in rows:
            if row[0] != None:
                use_vals.append(row[0])
    if len(use_vals) > 0:
        count = len(use_vals)
        median = GetMedian(use_vals)
        avg = GetAverage(use_vals)
        total = sum(use_vals)

    return (str("%.2f" % median), str("%.2f" % avg), str("%.0f" % count), str("%.2f" % total))

if __name__ == '__main__':


    # Script tool params
    reportFile = r'\\GIS-Cascade\Data\disk_5\projects\county\planning\ag_analysis\ag_2014\reportfile_2014Gov.txt'
    fileLocation = r'\\GIS-Cascade\Data\disk_5\projects\county\planning\ag_analysis\ag_2014\AnalysisLayers.gdb'
    fileFeature = os.path.join(fileLocation, 'GovAgLands2014')
    year = '2014'
    value_field = 'ACRES'
    if os.path.exists(reportFile):
        os.remove(reportFile)

    vList = [99993, 99990, 99992, 99988]
    f = open(reportFile, 'w')
    line = 'Year, Government, NumLots, TotAcres, AvgLot, MedLot'
    f.write(line + '\n')
    for x in vList:
        median, average, count, total = GetAgList(x, fileFeature, value_field)
        line = year + ", " + str(x) + ", " + count + ", " + total + ", " + average + ", " + median
        print line
        f.write(line + '\n')
    f.close()



##    fileAgUse = 'City2000AgUse'
##    f = open(reportFile, 'w')
##    yearFile = os.path.join(fileLocation, fileAgUse)
##    median, average = GetMedianValues(yearFile, value_field)
##    line = "2000 - Median: " + median + " Average: "+ average
##    print line
##    f.write(line + '\n')
##    f.close()

##    f = open(reportFile, 'w')
##    for x in year:
##        year_file = 'Parc' + str(x) + 'FinDis'
##        yearFile = os.path.join(fileLocation, year_file)
##        #print yearFile
##        median, average = GetMedianValues(yearFile, value_field)
##        #print retVals
##        line = str(x) + " - Median: " + median + " Average: "+ average
##        print line
##        f.write(line + '\n')
##    f.close()
