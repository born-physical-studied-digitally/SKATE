
### Download Data
Once the seismogram is complete, the results can be downloaded to the user’s machine
by clicking on *Download Data*. The data will be saved as a .zip file with the name of the
seismogram record. You must be in Editor mode in order to access the download menu.

All of the data will be saved in a JSON format. Assignments will also be saved as a .csv
file. Refer to www.json.org for details on the JSON format.

There are four JSON data files that are downloadable after analysis: roi.json;
meanlines.json; segments.json; assignment.json. Their descriptions follow.

<a href="#roi">roi.json</a><br>
<a href="#meanlines">meanlines.json</a><br>
<a href="#segments">segments.json</a><br>
<a href="#assignment">assignment.json</a><br>
<a href="#assignment_csv">assignment.csv</a><br>
<a href="#mseed">mseed</a><br>

<p id="roi"></p>

**roi.json**

The .json file looks like the following.

{"type":"FeatureCollection","features":[{"geometry":{"type":"Polygon","coordinates":[[[184,813],[1
4442,938],[14381,5555],[144,5431],[184,813]]]},"type":"Feature","id":null,"properties":{}}]}

The coordinates start in the upper left hand corner and follow a clockwise path around
the image. Note that there are five coordinate pairs; the fifth is identical to the first, closing the
polygon that defines the ROI.

<p id="meanlines"></p>

**meanlines.json**

Meanlines are reported with an ID, and start and finish coordinates in an (x,y) format.
The first few lines of the .json collection is shown below.

{"type":"FeatureCollection","features":[{"geometry":{"type":"LineString","coordinates":[[0,4356],[1
5456,4716]]},"type":"Feature","id":0,"properties":{}},{"geometry":{"type":"LineString","coordinates"
:[[0,4041],[15454,4378]]},"type":"Feature","id":1…}

Note that there may be gaps in the meanline ID numbering, and that they are not
necessarily in a top to bottom order. This is a result of editing. Moving, adding or deleting lines
will affect only the ID of the meanline being operated on, but will not affect other IDs.

The ID is an important identifier, as later it is used as the binding element to which all
segments’ centerline values are tied.

<p id="segments"></p>

**segments.json**

Segments.json presents as:

{"type":"FeatureCollection","features":[{"geometry":{"type":"LineString","coordinates":[[10529,471
3],[10530,4713]]},"type":"Feature","id":6769},{“geometry”…}

The “coordinates” are the (x,y) pairs of the centerlines for each segment. The coordinate
system starts at the upper left of the image, with +y in the downward direction, and +x to the
right. The “id” is the segment ID. This segment ID is used in conjunction with the meanline ID in
the subsequently described assignment.json file.

<p id="assignment"></p>

**assignment.json**

The assignment.json file describes those segments that are associated with each
meanline. The file looks like:

{"0":[segment ID 01,
segment ID 02,…
segment ID 0n],"
1":[segment ID 11,
segment ID
12,…
segment ID 1n],
“N”:[segment ID N1…
segment ID Nn]}

The values in quotes are the meanline IDs. The values in brackets are the IDs of the
segments belonging

<p id="assignment_csv"></p>

**assignment.csv**

To download a .csv file of the assigned (i.e. connected) segments, choose *Open in
Editor* and select *Download CSV*. The data is organized with column headers as: x0, y0;
x1,y1;...;xN,yN. Each (xN,yN) pair corresponds to a single meanline, which in the case of long
period WWSSN seismograms represents a one hour line of data. Note that typical spreadsheet
plots, such as in Microsoft Excel, display positive Y values in Quadrant I of cartesian coordinate
systems. However, the data in SKATE was obtained using Python, which plots positive Y
values in Quadrant IV. Hence, Excel plotted data will be flipped about the horizontal axis with
respect to the original image. Again, note that the meanline IDs will not necessarily be sorted
from top to bottom, as editing and other actions might alter this sequence. Nevertheless, the
data is easily parsed and represents the true output of the program.

<p id="mseed"></p>

**mSEED**

Not currently available, the data will be made available in mSEED format in the future.