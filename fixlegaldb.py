#!/usr/bin/python
#title			:fixlegaldb.py
#description	: fixes legal descriptions
#author			:DD Arnett
#date			:20130514
#version		:1.0
#usage			:python fixlegaldb.py
#notes			:
#python_version	:2.6.6
#==============================================================================


import arcpy
import os
from textwrap import wrap
import time

# *********************** PARMETERS ***********************************
outFreqDB = r'D:\temp\DDAplications\legalFreq.dbf'
legalDB_in = r'M:\Geodatabase\Taxlots\Tables.gdb\Legal'
outLegalDB = r'D:\temp\DDAplications\outLegal.txt'
#                ************************


#  ************* Defining Functions *******************
# Standard GIS Kill Object Function
def killObject( object ):
    if arcpy.Exists(object):
        arcpy.Delete_management(object)

def defineFreq(inputFile, outFreqFile):
    try:
        frequencyField = ['ASSESSOR_N']
        killObject(outFreqFile)
        arcpy.Frequency_analysis(inputFile, outFreqFile, frequencyField)
        arcpy.AddIndex_management(outFreqFile, "ASSESSOR_N", "AssFreq", "UNIQUE", "ASCENDING")
    except:
        print "There was a problem in executing the defineFreq function."
    finally:
        pass

def checkOne(assNumber, legalDB, outText):
    try:
        myFields = ["ASSESSOR_N", "LINE_NR", "SEG_CHILD_", "LEGAL_LINE"]
        where_Clause = whereClause = '"ASSESSOR_N"' + " = '" + str(assNumber) + "'"
        rotton = arcpy.da.SearchCursor(legalDB, myFields, whereClause)
        for rot in rotton:
            legalDesc = rot[3]
            chld = rot[2]
            if chld == None:
                chld = ''
            lineNO = rot[1]
            lenLegal = len(legalDesc)
            brokenlegal = ""
            width = 162
            if int(lenLegal) > 162:
                with open(outText, 'a') as myfile:
                    lpCounter = 0
                    sliced = wrap(legalDesc, width)
                    for line in sliced:
                        lpCounter += 1
                        brokenlegal = "%s|%s|%s|%s|\n" % (assNumber, str(lpCounter), chld, line)
                        #print brokenlegal
                        myfile.write(brokenlegal)
            else:
                with open(outText, 'a') as myfile:
                    brokenlegal = "%s|%s|%s|%s|\n" % (assNumber, "1", chld, legalDesc)
                    #print brokenlegal
                    myfile.write(brokenlegal)
    except:
        print "There was a problem in excuting checkOne function. ", assNumber
    finally:
        pass

def checkMore(freqency, assNumber, legalDB, outText):
    try:
        longLine = ''
        chld = ''

        for i in range(freqency):
            tt = i + 1
            myFields = ["ASSESSOR_N", "LINE_NR", "SEG_CHILD_", "LEGAL_LINE"]
            where_Clause = '"ASSESSOR_N"' + " = '%s' and " % (str(assNumber)) + '"LINE_NR"' + ' = %i' % (tt)
            rotton = arcpy.da.SearchCursor(legalDB, myFields, where_Clause)
            for rot in rotton:
                legalDesc = rot[3]
                chld = rot[2]
                if chld == None:
                    chld = ''
                longLine = longLine + legalDesc

        width = 162
        lenLegal = len(longLine)
        if int(lenLegal) > 162:
            with open(outText, 'a') as myfile:
                lpCounter = 0
                sliced = wrap(longLine, width)
                for line in sliced:
                    lpCounter += 1
                    brokenlegal = "%s|%s|%s|%s|\n" % (assNumber, str(lpCounter), chld, line)
                    #print brokenlegal
                    myfile.write(brokenlegal)
        else:
            with open(outText, 'a') as myfile:
                brokenlegal = "%s|%s|%s|%s|\n" % (assNumber, "1", chld, longLine)
                #print brokenlegal
                myfile.write(brokenlegal)


    except:
        print "There was a problem in the checkMore function. ", assNumber
    finally:
        pass
#             *****************************


# **************Main Program****************************************
def main():
    pass

if __name__ == '__main__':
    main()
    start = time.time()
    print 'Program started at ', start, '.'
    killObject(outLegalDB)
    defineFreq(legalDB_in, outFreqDB)
    freq_view = arcpy.management.MakeTableView(outFreqDB, 'freqview')
    legal_view = arcpy.management.MakeTableView(legalDB_in, 'legalview')
    try:
        cursor = arcpy.da.SearchCursor(freq_view, ['ASSESSOR_N', 'FREQUENCY'])
        for row in cursor:
            assNum = row[0]
            freq = row[1]
            if freq == 1:
                checkOne(assNum, legal_view, outLegalDB)
            else:
                checkMore(freq, assNum, legal_view, outLegalDB)
            cursor.next()
    except:
        print "there is a problem with the main program"
    finally:
        print 'It took ', (time.time()-start)/60, 'minutes.'
        pass
