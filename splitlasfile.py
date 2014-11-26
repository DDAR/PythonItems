#!/usr/bin/python
#title			:splitlasfile.py
#description	:splits a LiDAR file into four files
#author			:DDA
#date			:20130417
#version		:1.0
#usage			:python splitlasfile.py
#notes			:
#python_version	:2.6.6
#==============================================================================

import os
import itertools
import sys
import arcpy
import string
from arcpy import env

def killObject( object ):
    if arcpy.Exists(object):
        arcpy.Delete_management(object)

def slicefile(filename, start, end):
    lines = open(filename)
    return itertools.islice(lines, start, end)

putDir = "R:\\Geodatabase\\LiDAR\\2005\\LAS"
dirt = r'D:\temp\LiDAR\q46120e31'
frontfile = 'q46120e3105A.txt'
endfile =  os.path.join(dirt, 'q46120e3105A1.txt')
endfile2 =  os.path.join(dirt, 'q46120e3105A2.txt')
endfile3 =  os.path.join(dirt, 'q46120e3105A3.txt')
endfile4 =  os.path.join(dirt, 'q46120e3105A4.txt')
origTxt = os.path.join(dirt, frontfile)


out = open(endfile4, "w")
for line in slicefile(origTxt, 1425278, 1900367):
    out.write(line)
out.close()
