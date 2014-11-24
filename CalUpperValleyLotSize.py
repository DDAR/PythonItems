#-------------------------------------------------------------------------------
# Name:        CalcUpperValleyLotSize.py
# Purpose:      Calculate statistics for parcels in the upper valley
#               based on year and reports the values to a text file that
#               is deliminated by commas.
#
# Version:      ArcGIS 10.2 and Python 2.7.5
#
# Author:      Donna Arnett
#
# Created:     06/11/2014
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

def GetAllList(source_fc, value_field):
    use_vals = []
    with arcpy.da.SearchCursor(source_fc, [value_field]) as rows:
        for row in rows:
            if row[0] != None:
                use_vals.append(row[0])
    if len(use_vals) > 0:
        count = len(use_vals)
        median = GetMedian(use_vals)
        avg = GetAverage(use_vals)
        total = sum(use_vals)

    return (str("%.2f" % median), str("%.2f" % avg), str("%.0f" % count), str("%.2f" % total))

def writeToFile(lyrfile, finFile2):
    matchcount = int(arcpy.GetCount_management('parc_lyr').getOutput(0))
    if matchcount == 0:
        print('No feautures matched spatial and attribute criteria')
    else:
        if arcpy.Exists(finFile2):
            arcpy.Delete_management(finFile2)
    arcpy.CopyFeatures_management('parc_lyr', finFile2)

if __name__ == '__main__':


    # Script tool params

    UpperLands = r'\\GIS-Cascade\Data\disk_5\projects\county\planning\ag_analysis\ag_2014\AnalysisLayers.gdb\UpperValley'
    years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]
    baseFileLocation = r'\\GIS-Cascade\Data\disk_5\projects\county\planning\ag_analysis\ag_2014'
    fileGeoLocation = r'\\GIS-Cascade\Data\disk_5\projects\county\planning\ag_analysis\ag_2014\AnalysisLayers.gdb'
    reportFile = os.path.join(baseFileLocation, "ReportUpperValleyAllYears.txt")
    value_field = 'ACRES'

    if os.path.exists(reportFile):
        os.remove(reportFile)
    f = open(reportFile, 'w')
    line = 'Year, UpperValley, NumberLots, TotalAcres, AverageLot, MedianLot'
    f.write(line + '\n')

    for year in years:
        repfile = "UpperValley" + str(year)
        begParcFile = "Parc" + str(year) + "FinDis"
        parcFile = os.path.join(fileGeoLocation, begParcFile)
        begFinFile = "UpperValley" + str(year)
        finFile = os.path.join(fileGeoLocation, begFinFile)

        if arcpy.Exists('parc_lyr'):
            arcpy.Delete_management('parc_lyr')
        arcpy.MakeFeatureLayer_management(parcFile, 'parc_lyr')
        arcpy.SelectLayerByLocation_management('parc_lyr', 'have_their_center_in', UpperLands)
        writeToFile('parc_lyr', finFile)
        median, average, count, total = GetAllList(finFile, value_field)
        line = str(year) + ", " + "yes" + ", " + count + ", " + total + ", " + average + ", " + median
        print line
        f.write(line + '\n')


        arcpy.SelectLayerByLocation_management('parc_lyr', 'have_their_center_in', UpperLands, "", 'switch_selection')
        writeToFile('parc_lyr', finFile)
        median, average, count, total = GetAllList(finFile, value_field)
        line = str(year) + ", no, " + count + ", " + total + ", " + average + ", " + median
        print line
        f.write(line + '\n')


    f.close()
