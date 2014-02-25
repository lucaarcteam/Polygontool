#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os

def createPM(outputDir, fileName, container, seqdelem, projectname):
    oldObjNr = ""
    f = None
    
    for line in container:
        parts = line.split(",")        
        objname = parts[0]
        objNr = objname.split(seqdelem)[0][-3:]
        print objNr
        
        if not oldObjNr == objNr:
            if not oldObjNr == "":
                f.close()
            print "openfile"
            f = open(outputDir + os.sep + projectname + fileName + "_" + objNr + ".txt", 'w')
        
        f.write(line)
        oldObjNr = objNr
        
    f.close()
        
        