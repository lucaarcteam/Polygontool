#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from lxml import etree
import os

def createDictFromLines2(lines, seqdelem):
    dictOfObjnr = {}
    lines.sort()
    seqIncrementor = 0
    oldSeqNr = -2
    
    for line in lines:
        lineparts = line.split(",")
        objname = lineparts[0]
        seqsplits = objname.split(seqdelem)
        nameObjNr = seqsplits[0]
        objName = nameObjNr[:-3]
        objNr = int(nameObjNr[-3:])
        seqNr = int(seqsplits[1])
        
        if not objName in dictOfObjnr.keys():
            dictOfObjnr[objName] = {}
            
        if not objNr in dictOfObjnr[objName].keys():
            dictOfObjnr[objName][objNr] = {}
        
        if int(seqNr) >= (oldSeqNr + 2):
            seqIncrementor += 1
            
        if not seqIncrementor in dictOfObjnr[objName][objNr].keys():
            dictOfObjnr[objName][objNr][seqIncrementor] = []
        
        dictOfObjnr[objName][objNr][seqIncrementor].append(line)
        oldSeqNr = seqNr
        
    return dictOfObjnr

def checkType(seqtype, lineTypes):
    #types = ["ew-lin", "sts-lin", "pit-lin"]
    if seqtype in lineTypes:
        return True
    return False

def createLinTypes():
    f = open("config/linetypes.conf", 'r')
    lintypes = []
    
    for line in f:
        if line.startswith("#"):
            continue
        if len(line.strip()) == 0:
            continue            
        lintypes.append(line.strip())
    
    return lintypes

def createObjDescriptionDict(lang):
    f = open("config/objectdescription.conf", 'r')
    descObjDesc = {}
    for line in f:
        if line.startswith("#"):
            continue
        if len(line.strip()) == 0:
            continue
            
        parts = line.split(";")
        
        if lang == "de":
            descObjDesc[parts[0].strip()] = parts[2].strip()
        elif lang == "it":
            descObjDesc[parts[0].strip()] = parts[3].strip()
        elif lang == "en":
            descObjDesc[parts[0].strip()] = parts[1].strip()
        
    f.close()
    return descObjDesc

def createJML(outputDir, fileName, container, seqdelem, fileNameError):
    dictObjDesc_en = createObjDescriptionDict("en")
    dictObjDesc_de = createObjDescriptionDict("de")
    dictObjDesc_it = createObjDescriptionDict("it")
    linTypes = createLinTypes()
    
    outputfileError = open(outputDir + os.sep + fileNameError, 'a+')
    
    containerOfObjects = createDictFromLines2(container, seqdelem)
    #printDictObj(containerOfObjects[1])
    #printContainer(containerOfObjects)
    NSMAP = {"gml" : 'http://www.opengis.net/gml'}
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse("config/xmlheader.xml", parser) #basic jml file
    
    rootNode = tree.getroot()
    featureCollectionNode = etree.SubElement(rootNode, 'featureCollection')
    
    for objDate in containerOfObjects:
        # -- LOOP each object
        for objKey in containerOfObjects[objDate]:
            #featureNode = etree.SubElement(featureCollectionNode, 'feature')
            #geometryNode = etree.SubElement(featureNode, 'geometry')    
            #propIdNode = etree.SubElement(featureNode, 'property', name='project_ID')
            #propDescNode = etree.SubElement(featureNode, 'property', name='description')
            #propBeschNode = etree.SubElement(featureNode, 'property', name='beschreibung')
            
            obj = containerOfObjects[objDate][objKey]
            objName = ""
            
            for seqKey in obj:
                featureNode = etree.SubElement(featureCollectionNode, 'feature')
                geometryNode = etree.SubElement(featureNode, 'geometry')    
                propIdNode = etree.SubElement(featureNode, 'property', name='project_ID')
                propDescNode = etree.SubElement(featureNode, 'property', name='description')
                propBeschNode = etree.SubElement(featureNode, 'property', name='beschreibung')
                propDescITNode = etree.SubElement(featureNode, 'property', name='descrizione')
                
                objName = obj[seqKey][0].split(",")[0].split("-")[0]
                
                objDesc = obj[seqKey][0].split(",")[4].strip()
                if objDesc in dictObjDesc_en.keys():
                    objDesc = dictObjDesc_en[objDesc]
                
                objBesch = obj[seqKey][0].split(",")[4].strip()
                if objBesch in dictObjDesc_de.keys():
                    objBesch = dictObjDesc_de[objBesch]
                    
                objDescIT = obj[seqKey][0].split(",")[4].strip()
                if objDescIT in dictObjDesc_it.keys():
                    objDescIT = dictObjDesc_it[objDescIT]
                
                isThisaLine = False
                
                seq = obj[seqKey]
                
                if checkType(str(seq[0].split(",")[4]).strip(), linTypes):
                    isThisaLine = True
                
                if not isThisaLine:    
                    multiPolygonNode = etree.SubElement(geometryNode, '{http://www.opengis.net/gml}MultiPolygon')
                else:
                    lineStringNode = etree.SubElement(geometryNode, '{http://www.opengis.net/gml}LineString')
                
                coordinatesList = []
                if not isThisaLine:
                    if len(seq) >= 3:
                        polygonMemberNode = etree.SubElement(multiPolygonNode, '{http://www.opengis.net/gml}polygonMember')
                        polygonNode = etree.SubElement(polygonMemberNode, '{http://www.opengis.net/gml}Polygon')
                        outerBoundaryIsNode = etree.SubElement(polygonNode, '{http://www.opengis.net/gml}outerBoundaryIs')
                        linearRingNode = etree.SubElement(outerBoundaryIsNode, '{http://www.opengis.net/gml}LinearRing')
                        coordinatesNode = etree.SubElement(linearRingNode, '{http://www.opengis.net/gml}coordinates')
                    else:
                        errorMess = "Für Polygon sind mindestens 4 Koordinaten notwendig. Vorhanden=%s ObjektName=%s erste Sequenznummer=%s Endung=%s" % (len(seq), objName, seq[0].split(",")[0].split("-")[1], seq[0].split(",")[4])
                        outputfileError.write(errorMess + "\n")
                        continue
                else:
                    if len(seq) >= 2:
                        coordinatesNode = etree.SubElement(lineStringNode, '{http://www.opengis.net/gml}coordinates')
                    else:
                        errorMess =  "Für Linien sind mindestens 2 Koordinaten notwendig. Vorhanden=%s ObjektName=%s erste Sequenznummer=%s Endung=%s" % (len(seq), objName, seq[0].split(",")[0].split("-")[1], seq[0].split(",")[4])
                        outputfileError.write(errorMess + "\n")
                        continue
                i = 0
                for line in seq:
                    parts = line.split(",")
                    coord = parts[1] + "," + parts[2] + "," + parts[3]
                    if i == 0:
                        firstline = coord
                    coordinatesList.append(coord + "\n")
                    i += 1
                if not isThisaLine:
                    coordinatesList.append(firstline)
                coordinatesNode.text = "".join(coordinatesList)
                    
                propIdNode.text = str(objName)
                propDescNode.text = str(objDesc)
                propBeschNode.text = str(objBesch)
                propDescITNode.text = str(objDescIT)
   
    outputfileError.close()
    outFile = open(outputDir + os.sep + fileName, 'w')
    tree.write(outFile, pretty_print=True)    
    
if __name__ == "__main__":
    createObjDescriptionDict()
    
