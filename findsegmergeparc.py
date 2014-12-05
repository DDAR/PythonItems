#!/usr/bin/python
#title			:findsegmergeparc.py
#description	:Search the Seg table to find missing parcel numbers
#author			:DD Arnett
#date			:20120705
#version		:1.0
#usage			:python findsegmergeparc.py
#notes			:
#python_version	:2.6.6
#==============================================================================
import os
import string
import sys
import arcpy
import time
import csv
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from arcpy import env
from datetime import date

mail_recipient = 'donna.arnett@co.yakima.wa.us'

# Methods ----------------------------------------------------------------------

def message(msg):
	LocalTime = time.asctime(time.localtime(time.time()))
	mmsg = msg + LocalTime; arcpy.AddMessage(mmsg); print mmsg

def WriteReport(txtFile, orgNo, parentList, segNum, segDate):
	int = 0
	listCnt = len(parentList)
	#print int
	#print listCnt
	reportfile = open(txtFile, 'a')
	while listCnt > int:
			if int == 0:
				writeLine =  '\n' + '  ' + orgNo + '         	   ' + segNum + '            ' + segDate + '           ' + parentList[int]
			else:
				writeLine =  '\n                                                                   ' + parentList[int] + '\n'
			reportfile.write(writeLine)
			int = int + 1
	reportfile.close()

def WriteTitle(txtFile, defRange):
    reportFile = open(txtFile, 'a')
    writeLine = '             Parcels not found in 2006 - Range: ' + defRange + '\n'
    reportFile.write(writeLine)
    reportFile.close()


def killObject( object ):
    if arcpy.Exists(object):
        arcpy.Delete_management(object)

def addToTable(table, num, prob, field, oldval, newval):
    rows = arcpy.InsertCursor(table)
    row = rows.newRow()
    row.ASSESSOR_N = num
    row.PROBLEM = prob
    row.FIELD = field
    row.OLD_VALUE = oldval
    row.NEW_VALUE = newval
    rows.insertRow(row)
    del row
    del rows

def sendMail(to, files=[]):
    assert type(to)==list
    assert type(files)==list
    fro = "DD at donna.arnett@co.yakima.wa.us"
    sub = "Change to Parcels"
    t1 = "This is to alert you that there has been a change with the comparing Parcels.\nPlease check attached tables for the changes."
    t2 = "\n\n\nThis email was generated from D:\\Data\\DDA\\python\\assessorcompare.py\nTable can be found at D:\Data\Compare_Results.dbf."
    text = t1 + t2

    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = sub

    msg.attach( MIMEText(text) )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file, "rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(part)

    smtp = smtplib.SMTP('ntx7.co.yakima.wa.us')
    smtp.sendmail(fro, to, msg.as_string() )
    smtp.close()

def checkChildTable(lookup, childTable, parentTable):
	#print lookup
	newParcs = []
	mergenum = ''
	mergDate = ''
	nwhere_clause = '"ASSESSOR_N" = ' + "'" + lookup + "'"
	selparent = arcpy.SearchCursor(childTable, nwhere_clause)
	if selparent == None:
		print "no children"
	else:
		for pSel in selparent:
		  mergenum = pSel.getValue("SEG_MERGE_")
		  twhere_clause = '"SEG_MERGE_" = ' + "'" + mergenum + "'"
		  count = 0
		  newParcs = []
		  cnt, selchild = None, None
		  selchild = arcpy.SearchCursor(parentTable, twhere_clause)
		  if selchild == None:
	   		print "no parents"
	   		newParcs = []
  		  else:
			for cnt in selchild:
				count +=1
				parc = cnt.getValue("ASSESSOR_N")
				mergDate = cnt.getValue("EFF_TO_DAT")
				newParcs.append(parc)
		  del selchild
	return newParcs, mergenum, mergDate

def CreateChildsReport(parcID, textFile):
	lookup = parcID
	listA = []
##	textWrite = open(textFile, 'a')
##	writeLine =  '\n\nParcel : ' + lookup + '\n'
##	textWrite.write(writeLine)
##	writeLine =  '   Problem - Not in 2006 parcel layer \nParcel Genealogy \n'
##	textWrite.write(writeLine)
##	writeLine =  'Seg Children			Seg Merge ID		Date		   Seg Parents'
##	textWrite.write(writeLine)
##	textWrite.close()
	listA, smNum, smDate = checkChildTable(lookup, smChild, smParent)
	if listA == []:
		textWrite = open(textFile, 'a')
		writeLine =  '\n' + lookup + '  No Genealogy found'
		textWrite.write(writeLine)
		textWrite.close()
	elif listA == None:
		textWrite = open(textFile, 'a')
		writeLine =  '\n' + lookup + '  No Genealogy found'
		textWrite.write(writeLine)
		textWrite.close()
	else:
		textWrite = open(textFile, 'a')
		writeLine =  '\n\nParcel : ' + lookup + '\n'
		textWrite.write(writeLine)
		#writeLine =  '   Problem - Not in 2006 parcel layer \nParcel Genealogy \n'
		#textWrite.write(writeLine)
		writeLine =  'Seg Children		Seg Merge ID		Date		   Seg Parents'
		textWrite.write(writeLine)
		textWrite.close()
		octCnt = len(listA)
		listCnt = octCnt
		int = 0
		WriteReport(textFile, lookup, listA, smNum, smDate)
		for parc in listA:
			checkParc.append(parc)
		cntParc = len(checkParc)
		while cntParc > 0:
			print "checkParc ---"
			print checkParc
			bLookup = checkParc[0]
			print "bLookup value"
			print bLookup
		   	listB, smNumB, dateB = checkChildTable(bLookup, smChild, smParent)
			print "B list --------------------------"
			print listB
			if listB == []:
				textWrite = open(textFile, 'a')
				writeLine = '\n' + '  ' + bLookup + "	 No Parent Record Found"
				textWrite.write(writeLine)
				textWrite.close()
			elif listB == None:
				textWrite = open(textFile, 'a')
				writeLine = '\n	' + bLookup + '	   No Parent Record Found'
				textWrite.write(writeLine)
				textWrite.close()
			else:
				WriteReport(textFile, bLookup, listB, smNumB, dateB)
				for asel in listB:
					checkParc.append(asel)
			del checkParc[0]
			cntParc = len(checkParc)
# Variables --------------------------------------------------------------------
pullFolder = r'D:\Data'
pullFileBase = 'Results_'
pullFileEnd = '.dbf'
baseFolder = r'M:\informix'
smChild = os.path.join(baseFolder, 'sm_chld_nfo.dbf')
smParent = os.path.join(baseFolder, 'sm_prnt_nfo.dbf')
township = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
tempBaseFileName = 'tempResults.dbf'
tempBaseFile = r'D:\Data\tempResults.dbf'
testParcNo = '15150341406'
smNum = ''
checkParc = []
listA = []
childReport = r'D:\Data\ParcelCompare_06X12\childResults_23.txt'
baseFile = r'D:\Data\Results_23.dbf'
rng = '23'


try:
	killObject(childReport)
   	killObject(tempBaseFile)
	WriteTitle(childReport, rng)
	nwhere_clause = '"PROBLEM" = ' + "'Parcel not in 06 Parcels'"
	print nwhere_clause
	arcpy.TableToTable_conversion(baseFile, pullFolder, "tempResults.dbf", nwhere_clause)
	probList = []
	baseRecords = arcpy.SearchCursor(tempBaseFile)
	for sel in baseRecords:
		probList.append(sel.getValue("ASSESSOR_N"))
	print probList
	probCnt = len(probList)
	if probCnt > 0:
		for prb in probList:
			testParcNo = prb
			CreateChildsReport(testParcNo, childReport)
	else:
		print 'No list available'


except arcpy.ExecuteError:
    msgs = arcpy.GetMessages(2)
    print arcpy.AddMessage("There was a problem...script bailing")
    arcpy.AddError(msgs)
    print msgs
