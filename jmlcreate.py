#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from lxml import etree

# def printDict(myDdict):
#     print "Länge dict:%s" % len(myDdict.keys())
#     for objKey in myDdict.keys():
#         print "Länge seq:%s" % len(myDdict[objKey].keys())
#         for seqKey in myDdict[objKey].keys():
#             print "beginn new seq"
#             for line in dict[objKey][seqKey]:
#                 print line

# def printDictObj(dict):
#     print "Länge seq:%s" % len(dict.keys())
#     for seqKey in dict.keys():
#         print "beginn new seq"
#         for line in dict[seqKey]:
#             print line

# def createDictFromLines(lines, seqdelem):
#     dictOfObjnr = {}
#     lines.sort()
#     seqIncrementor = 0
#     oldSeqNr = -2
#     
#     for line in lines:
#         lineparts = line.split(",")
#         objname = lineparts[0]
#         seqsplits = objname.split(seqdelem)
#         nameObjNr = seqsplits[0]
#         objNr = int(nameObjNr[-3:])
#         seqNr = int(seqsplits[1])
#         
#         if not objNr in dictOfObjnr.keys():
#             dictOfObjnr[objNr] = {}
#         
#         if int(seqNr) >= (oldSeqNr + 2):
#             seqIncrementor += 1
#             
#         if not seqIncrementor in dictOfObjnr[objNr].keys():
#             dictOfObjnr[objNr][seqIncrementor] = []
#         
#         dictOfObjnr[objNr][seqIncrementor].append(line)
#         oldSeqNr = seqNr
#         
#     return dictOfObjnr

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



# def createContainerFromLines(lines, seqdelem):
#     lines.sort()
#     containerOfObjectsOfObjects = []
#     oldSeqNr = -2
#     oldObjNr = -1
#     subContainer = []
#     subSubContainer = []
#     
#     for line in lines:
#         lineparts = line.split(",")
#         objname = lineparts[0]
#         seqsplits = objname.split(seqdelem)
#         nameObjNr = seqsplits[0]
#         objNr = nameObjNr[-3:]
#         seqNr = seqsplits[1]
#         #print "line zu subSubContainer" + line
#         
# #         if nameObjNr == "spw130730012":
# #             print line
#         
#         if int(seqNr) >= (oldSeqNr + 2) and oldSeqNr > -2: #newitem of object is coming
#             #print "subSubContainer zu subContainer"
#             subContainer.append(subSubContainer)
#             if nameObjNr == "spw130730012":
#                 print "subContainer.append(subSubContainer)"
#             subSubContainer = None
#             subSubContainer = []
#             
#         
#         #print line
#         if int(objNr) > oldObjNr and oldObjNr > -1:
#             #print "subSubContainer zu subContainer"
#             subContainer.append(subSubContainer)
#             if nameObjNr == "spw130730012":
#                 print "subContainer.append(subSubContainer)"
#             subSubContainer = None
#             subSubContainer = []
#             #print "subContainer zu containerOfObjectsOfObjects"
#             containerOfObjectsOfObjects.append(subContainer)
#             if nameObjNr == "spw130730012":
#                 print "containerOfObjectsOfObjects.append(subContainer)"
#             subContainer = None
#             subContainer = []
#         
#         subSubContainer.append(line)
#         if nameObjNr == "spw130730012":
#                 print "subSubContainer.append(line)"
#             
#         oldSeqNr = int(seqNr)
#         oldObjNr = int(objNr)
#     
#     #print "subSubContainer zu subContainer"
#     subContainer.append(subSubContainer)
#     subSubContainer = None
#     subSubContainer = []
#     #print "subContainer zu containerOfObjectsOfObjects"    
#     containerOfObjectsOfObjects.append(subContainer)
#     subContainer = None
#     subContainer = []
#     return containerOfObjectsOfObjects

# def printContainer(containerOfObjects):
#     for obj in containerOfObjects:
#         print "beginn new Object"
#         for seq in obj:
#             print "beginn new seq"
#             for line in seq:
#                 print line

def checkType(seqtype):
    types = ["esc", "ew-lin", "sts-lin", "pit-lin", "ew", "we", "pit", "tr"]
    for t in types:
        if seqtype == t:
            return True
    return False

def createJML(filename, container, seqdelem):
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
            featureNode = etree.SubElement(featureCollectionNode, 'feature')
            geometryNode = etree.SubElement(featureNode, 'geometry')    
            propIdNode = etree.SubElement(featureNode, 'property', name='project_ID')
            
            obj = containerOfObjects[objDate][objKey]
            objName = ""
            
            for seqKey in obj:
                objName = obj[seqKey][0].split(",")[0].split("-")[0]
                isThisaLine = False
                
                seq = obj[seqKey]
                
                if checkType(str(seq[0].split(",")[4]).strip()):
                    isThisaLine = True
                
                if not isThisaLine:    
                    multiPolygonNode = etree.SubElement(geometryNode, '{http://www.opengis.net/gml}MultiPolygon')
                else:
                    lineStringNode = etree.SubElement(geometryNode, '{http://www.opengis.net/gml}LineString')
                
                coordinatesList = []
                if not isThisaLine:
                    if len(seq) >= 4:
                        polygonMemberNode = etree.SubElement(multiPolygonNode, '{http://www.opengis.net/gml}polygonMember')
                        polygonNode = etree.SubElement(polygonMemberNode, '{http://www.opengis.net/gml}Polygon')
                        outerBoundaryIsNode = etree.SubElement(polygonNode, '{http://www.opengis.net/gml}outerBoundaryIs')
                        linearRingNode = etree.SubElement(outerBoundaryIsNode, '{http://www.opengis.net/gml}LinearRing')
                        coordinatesNode = etree.SubElement(linearRingNode, '{http://www.opengis.net/gml}coordinates')
                    else:
                        print "Für Polygon sind mindestens 4 koordinaten notwendig. Vorhanden=%s ObjektName=%s erste Sequenznummer=%s Endung=%s" % (len(seq), objName, seq[0].split(",")[0].split("-")[1], seq[0].split(",")[4])
                        continue
                else:
                    if len(seq) >= 2:
                        coordinatesNode = etree.SubElement(lineStringNode, '{http://www.opengis.net/gml}coordinates')
                    else:
                        print "Für Linien sind mindestens 2 koordinaten notwendig. Vorhanden=%s ObjektName=%s erste Sequenznummer=%s Endung=%s" % (len(seq), objName, seq[0].split(",")[0].split("-")[1], seq[0].split(",")[4])
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
   
    outFile = open(filename, 'w')
    tree.write(outFile, pretty_print=True)    
    
#if __name__ == "__main__":
    