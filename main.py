#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import getopt #www.tutorialspoint.com/python/python_command_line_arguments.htm
import sys
import fileinput
import os

import jmlcreate
import passmarkercreate

def writeFotoMarker(outputPath, container, filename, fileNameError):
    outputfile = open(outputPath + os.sep + filename, 'w')
    for elem in container:
        elem = elem.strip()
        elems = elem.split(",")
        if len(elems) == 5:
            himmelUndGrad = elems[4].split(" ")
            if len(himmelUndGrad) == 2:
                line = elems[0] + "," + elems[1] + "," + elems[2] + "," + \
                        elems[3] + "," + himmelUndGrad[0] + "," + himmelUndGrad[1]
                outputfile.write(line + "\n")
            else:
                outputfileError = open(outputPath + os.sep + fileNameError, 'a+')
                outputfileError.write(elem + "\n")
                outputfileError.close()
        else:
            outputfile.write(elem + "\n")
    outputfile.close()
    
def writeBlankFile(outputPath, container, filename):
    outputfile = open(outputPath + os.sep + filename, 'w')
    for elem in container:
        outputfile.write(elem)
    outputfile.close()    
    
def countLinesInFile(path, filename):
    count = 0
    f = open(path + os.sep + filename, 'r')
    for elem in f:
        print elem
        count += 1
    f.close()
    return count

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
    seqlength_default = int(str(config['numberdigits_after_delemiter']))
    seqlength_passmarker = int(str(config['numberdigits_passmarker']))
    
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
        
        objparts = objname.split(seqdelem)
        
        if len(objparts) > 2:
            unknmarkcontainer.append(line)
            continue
        
        temp = seqlength_default * -1
        objNr = objparts[0][temp:]
        
        if not len(parts) == 5:
            unknmarkcontainer.append(line)
        elif objNr == "xxx":
            unknmarkcontainer.append(line) 
        elif seqdelem in objname:
            seqnumber = objname.split(seqdelem)[1]
            seqlength = len(seqnumber)
            if seqlength == seqlength_passmarker:
                passmarkcontainer.append(line)
            elif seqlength == seqlength_default:
                if seqnumber[0:1] == 'f':
                    fotomarkcontainer.append(line)
                elif parts[4].strip() == "gcp":
                    passmarkcontainer.append(line)
                elif seqnumber[0:1] == 'n':
                    unknmarkcontainer.append(line)
                else:
                    objemarkcontainer.append(line)
            else:
                unknmarkcontainer.append(line)
        else:
            unknmarkcontainer.append(line)
    
    errorFileName = "_error.txt"
    writeBlankFile(outputdir, unknmarkcontainer, inputfile + errorFileName)
    writeFotoMarker(outputdir, fotomarkcontainer, inputfile + "_fotomarker.csv", inputfile + errorFileName)
    writeBlankFile(outputdir, passmarkcontainer, inputfile + "_passmarker.txt")
    passmarkercreate.createPM(outputdir, "_passmarker", passmarkcontainer, seqdelem, inputfile)
                
    jmlcreate.createJML(outputdir, inputfile +"_objects.jml", objemarkcontainer, seqdelem, inputfile + errorFileName)
    
    print "\nEine Fehlerdatei: %s wurde geschrieben!\n" % \
        (outputdir + os.sep + inputfile + errorFileName)
