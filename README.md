Polygontool
===========

Creates a jml file for OpenJump from excavation measurement data.


Software dependencies:
======================

- python lxml module: http://lxml.de/
- maybe you need also libxml2 and libxslt, install with your linux package-managment system


Config files:
=============

linetypes.conf - this types will be converted to JML-lines, all others to JML-polygons
nameconvention.conf - you can set here the delemiter between objectnumber and sequenznumber
objectdescription.conf - you can set here the fullnames in english and german for the objecttypes
xmlheader.xml - template for a empty jml file


Program args:
=============

-i myinputFile.txt --- convert/extract this file 
-o myoutputDir --- write created files to this directory, this arg is optional
-v --- verbose mode, print more output, this arg is optional


Example call:
=============

python main.py -i spw20131031-01.csv
