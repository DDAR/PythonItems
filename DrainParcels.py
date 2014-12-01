""" #####################################################
	NAME: DrainParcels.py
	Source Name:
	Version: ArcGIS 10.2 - python 2.7
	Author: DD Arnett
	Usage: Check an excel spreadsheet and find the previous parcel numbers
	Required Arguments: none
	Optional Arguments: none
	Description: Used to check the drain parcels not found to find current parcels
	Date Created: Dec 10, 2013
##################################################### """
import os
import string
import sys
import arcpy
from arcpy import env

# Methods ----------------------------------------------------------------------

def message(msg):
	LocalTime = time.asctime(time.localtime(time.time()))
	mmsg = msg + LocalTime; arcpy.AddMessage(mmsg); print mmsg

def killObject( object ):
	if arcpy.Exists(object):
		arcpy.Delete_management(object)

def getAcres(sqft):
    ac = sqft/43560
    return(ac)

def findMerge(assnum):
    trline = "'" + assnum.strip() + "'"
    query = '"ASSESSOR_N" = ' + trline
    selobj = arcpy.SearchCursor(parentInfo, query)
    count = 0
    results = [assnum.strip()]
    for sel in selobj:
        count += 1
    if count == 0:
        results.append('Not Available')
    else:
        selparent = arcpy.SearchCursor(parentInfo, query)
        for e in selparent:
            merge = e.getValue("SEG_MERGE_")
            results.append(merge.strip())

    return(results)

def returnParcfromTables(mergeNumber):
    finSet = set()
    st = "'" + mergeNumber + "'"
    query = '"SEG_MERGE_" = ' + st
    selChild = arcpy.SearchCursor(childInfo, query)
    for sel in selChild:
        mergeSS = sel.getValue("ASSESSOR_N")
        finSet.add(mergeSS)
    return(finSet)

def createSetParc(txtfile):
    parc = set([])
    txtR = open(txtfile)
    while 1:
        line = txtR.readline()
        if not line: break
        s = line.strip()
        parc.add(s)
    txtR.close()
    return(parc)

def writeToFile(writeString):
    csvW = open(outDrainExcel, 'a')
    csvW.write(writeString)
    csvW.close()

def getParcAcres(assnum):
    trline = "'" + str(assnum) + "'"
    query = '"ASSESSOR_N" = ' + trline
    selobj = arcpy.SearchCursor(parcelLayer, query)
    count = 0
    for e in selobj:
        count += 1
    if count == 0:
        poppy = '0'
    elif count == 1:
        selparc = arcpy.SearchCursor(parcelLayer, query)
        for e in selparc:
            area = e.getValue("AREA")
            acres = getAcres(area)
            poppy = (str(acres))
    else:
        acres = 0.00
        selparc = arcpy.SearchCursor(parcelLayer, query)
        for e in selparc:
            area = e.getValue("AREA")
            a = getAcres(area)
            acres += a
        poppy = (str(acres))
    return (poppy)

def testParcExists(assnum):
    # Returns True if assessor number found in the parcel layer
    trline = "'" + str(assnum) + "'"
    query = '"ASSESSOR_N" = ' + trline
    selobj = arcpy.SearchCursor(parcelLayer, query)
    poppy = False
    count = 0
    for e in selobj:
        count += 1
    if count > 0:
        poppy = True
    return (poppy)

# Variables --------------------------------------------------------------------
env.overwriteoutput = True
startDrainList = r"R:\disk_5\projects\county\pw\DrainParcels\drainparcels.txt"
outDrainExcel = r"R:\disk_5\projects\county\pw\DrainParcels\fixDrain_Parcels4_test.txt"
parentInfo = r"M:\Geodatabase\Taxlots\Tables.gdb\sm_prnt_nfo"
childInfo = r"M:\Geodatabase\Taxlots\Tables.gdb\sm_chld_nfo"
env.workspace = r"R:\disk_5\projects\county\pw\DrainParcels\tempfiles.gdb"
baseDrainExcel = r"R:\disk_5\projects\county\pw\DrainParcels\fixDrain_Parcels2_test.txt"
outDrainAcres = r"R:\disk_5\projects\county\pw\DrainParcels\fix_ParcelsAcres4.txt"
parcelLayer = r"M:\Geodatabase\Taxlots\Taxlots.gdb\parcels"

# Program ----------------------------------------------------------------------
try:
    killObject(outDrainExcel)

    # Creates a set with all Parcel numbers with no duplicates
    testingParcs = createSetParc(startDrainList)
    runList = []
    for line in testingParcs:
        finList = ['assnum', 'newnum', 'acres', 'merge']
        finList[0] = line.strip()
        runList.append(line)
        print line
        while len(runList) > 0:
            cLine = runList[0]
            if testParcExists(cLine):
                pparcAcres = getParcAcres(cLine)
                nString = finList[0] + ', ' + cLine + ', ' + pparcAcres + '\n'
                #print nString
                writeToFile(nString)
                trout = runList.pop(0)
            else:
                # Checking parent table
                newMerge = findMerge(cLine)
                mergeList = newMerge[1:]
                if len(mergeList) > 0:
                    for tl in mergeList:
                        # Checking child table
                        rett2 = returnParcfromTables(tl)
                        if len(rett2) > 0:
                            for tm in rett2:
                                #print tm
                                runList.append(tm)
                        else:
                            nString = finList[0] + ',  merge id '+ tl + ' not found in child table.\n'
                            #print nString
                            writeToFile(nString)
                else:
                    nString = finList[0] + ', parcel number not found in parent table.\n'
                    #print nString
                    writeToFile(nString)
                trout = runList.pop(0)
##                if newMerge[1] == 'Not Available':
##                    print cLine + " Was not found in the Parent Table"
##                    trout = runList.pop(0)
##                else:



##
##
##        newMerge = findMerge(line)
##        if newMerge[1] == 'Not Available':
##            nstring = finList[0] + ', ' + newMerge[1] + '\n'
##            writeToFile(nstring)
##        elif len(newMerge) == 2:
##            rett2 = returnParcfromTables(newMerge[1])
##            if len(rett2) == 0:
##                nstring = finList[0] + ', ' + newMerge[1] + ', Merge number not found in Child Table\n'
##                writeToFile(nstring)
##
##            else:
##                for r in rett2:
##                    parcAcres = getParcAcres(str(r))
##                    if parcAcres == "Not Found":
##                        seek1 = findMerge(r)
##                        print finList[0] + ', ' + newMerge[1] + ', ' + str(r) + ', New parcel number not found in current parcel table'
##                    else:
##                        finList[1] = str(r)
##                        finList[2] = parcAcres
##                        finList[3] = newMerge[1]
##                        mystring =  finList[0] + ', ' + finList[1] + ', ' + finList[2] + ', ' + finList[3] + '\n'
##                        writeToFile(mystring)
##        else:
##            idNum = newMerge.pop(0)
##            for merge in newMerge:
##                parnum = returnParcfromTables(merge)
##                if len(parnum) == 0:
##                    nstring = finList[0] + ', ' + idNum + ', ' + merge + ', Merge number not found in Child Table\n'
##                    writeToFile(nstring)
##
##                else:
##                    for parcnum in parnum:
##                        parAcre = getParcAcres(str(idNum))
##                        if parAcre == "Not Found":
##                            seek2 = findMerge(parcnum)
##                            print str(idNum) + ', ' + merge + ', New parcel number not found in current parcel table #2'
##                        else:
##                            finList[1] = str(parcnum)
##                            finList[2] = parAcre
##                            finList[3] = merge
##                            mystring =  finList[0] + ', ' + finList[1] + ', ' + finList[2] + ', ' + finList[3] + '\n'
##                            writeTofile(mystring)



except arcpy.ExecuteError:
	print arcpy.GetMessages()
