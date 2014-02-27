Polygontool
===========

Creates a jml file for OpenJump from excavation measurement data.


Software dependencies:
======================

- python <b>lxml</b> module: http://lxml.de/
- maybe you need also libxml2 and libxslt, install with your linux package-managment system


Config files:
=============

<p><b>linetypes.conf</b></p> - this types will be converted to JML-lines, all others to JML-polygons<br>

<p><b>nameconvention.conf</b></p> - you can set here the delemiter between objectnumber and sequenznumber<br>
 - numberdigits_after_delemiter sets the length of the sequenznumber<br>
 - numberdigits_passmarker sets the length of the sequenznumber to recognise a passmarkerline.<br>
 - passmarkertoken sets which lines will be recognized as passmarkerlines<br>

<p><b>objectdescription.conf</b></p> - you can set here the fullnames in english and german for the objecttypes<br>

<p><b>xmlheader.xml</b></p> - template for a empty jml file, do not change anything


Program args:
=============

<b>-i myinputFile.txt</b> --- convert/extract this file<br>
<b>-o myoutputDir</b> --- write created files to this directory, this arg is optional<br>
<b>-v</b> --- verbose mode, print more output, this arg is optional<br>


Example call:
=============

python main.py -i spw20131031-01.csv

