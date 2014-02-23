#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import getopt #www.tutorialspoint.com/python/python_command_line_arguments.htm
import sys
import fileinput
import os

import jmlcreate

def writeBlankFile(outputPath, container, filename):
    outputfile = open(outputPath + os.sep + filename, 'w')
    for elem in container:
        outputfile.write(elem)
    outputfile.close()

if __name__ == "__main__":
    debugFlag = False
    inputfile = ""
    outputdir = ""
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"vi:o:",["inputfile=","outputdir="])
    except getopt.GetoptError:
        print 'main.py -v -> optional means MORE OUTPUT'
        print 'main.py -i filewithdata.txt -> obligate input'
        print 'main.py -o outputdir -> optional outputdirectory'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            debugFlag = True
        if opt in ("-i", "--inputfile"):
            inputfile = arg
        if opt in ("-o", "--outputdir"):
            outputdir = arg

    #inputfile = "spw131010-03.csv"
    
    if outputdir == "":
        outputdir = "output" + "_" + inputfile
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

    if inputfile == "":
        print 'No inputfile was given. Exiting...'
        sys.exit(2)
           
    try:
        open(inputfile, 'r')
    except:
        sys.exit("[!] Cannot read file: " + inputfile);
        
    lines=([])
    for line in fileinput.input([inputfile]):
        lines.extend([line])

    config = {}
    execfile("config/nameconvention.conf", config)
    seqdelem = str(config['sequencenumber_delemiter'])
    
    passmarkcontainer = []
    fotomarkcontainer = []
    objemarkcontainer = []
    unknmarkcontainer = []
    
    for line in lines:
        if line.startswith("#"):
            continue
        if len(line.strip()) == 0:
            continue
        
        line = line.replace('\n', '')
        parts = line.split(",")        
        objname = parts[0]
        objNr = objname.split(seqdelem)[0][-3:]
        
        if not len(parts) == 5:
            unknmarkcontainer.append(line)
        elif objNr == "xxx":
            unknmarkcontainer.append(line) 
        elif seqdelem in objname:
            seqnumber = objname.split(seqdelem)[1]
            seqlength = len(seqnumber)
            if seqlength == 2:
                passmarkcontainer.append(line)
            elif seqlength == 3:
                if seqnumber[0:1] == 'f':
                    fotomarkcontainer.append(line)
                elif seqnumber[0:1] == 'n':
                    unknmarkcontainer.append(line)
                else:
                    objemarkcontainer.append(line)
            else:
                unknmarkcontainer.append(line)
        else:
            unknmarkcontainer.append(line)
    
    writeBlankFile(outputdir, fotomarkcontainer, inputfile +"_fotomarker.csv")
    writeBlankFile(outputdir, passmarkcontainer, inputfile +"_passmarker.txt")
    writeBlankFile(outputdir, unknmarkcontainer, inputfile +"_error.txt")
            
    jmlcreate.createJML(outputdir + os.sep + inputfile +"_objects.jml", objemarkcontainer, seqdelem)
