# Current Status and Available Images

Retriever Technology has scanned approximately 150,000 WWSSN images under
several contracts, including but not limited to USGS Awards G09PC00116, G09PD02064, and
G10PD02236. These images were saved as high resolution, uncompressed .tif files, and were
delivered to the USGS. Retriever Technology has used these images to develop SKATE, and
has stored them for this project as lossless .png files on an Amazon S3 server. As of now, we
have completed two types of digitizing of WWSSN images:
* What we call ‘raw data,’ meaning that we have processed approximately 17,000
randomly selected images up to the point of automatic meanline assignment, and
segment and centerline identification. These data have not been run through the final
segment assignment algorithm. This assignment algorithm can be run at any time, but
we feel that absent some user interaction and editing, the final result will have less than
ideal results. These images were limited to WWSSN long period seismograms from
1970 and on.
* The second type of processed images are listed as ‘has edited data.’ This is a small
subset of approximately 20 images that we have hand edited to remove spurious
features and to ensure that the meanlines are properly placed. They were then run
through the segment assignment algorithm and have data that is ready to be
downloaded. Please refer to later sections in this manual that discuss editing and
downloading of data.
* There is a third category available through the UI called ‘no data.’ There are over
150,000 of these high resolution scans available for viewing only. Budget limitations
due to Amazon’s EC2 operational costs prevent these from being processed or
downloaded at this time.

Currently, users cannot upload and process their own images, nor create ‘raw data’ on
any of the ‘no data’ seismograms. This feature will be added shortly, please refer to the website
for updates and information on upgrades. What users can do is edit any of the ‘raw data’
seismograms, and run the assignment editor on them. Please note that there are severely
limited funds to maintain and operate the web server. As such, we ask that users design their
experiments to maximize results while minimizing computational time. Downloading data incurs
costs as well, so only download data when editing and all processing is complete.

While SKATE has been optimized for project development purposes for long period
WWSSN images, it can readily be configured to digitize short period images, of which there is
an example in the ‘edited data.’ In addition, we have successfully digitized data from the
Caltech archives, see the following reference for information on this archive:
<a href="http://ds.iris.edu/seismoarchives/projects/caltech_archive/Caltech_Seismograms_v2.pdf">http://ds.iris.edu/seismoarchives/projects/caltech_archive/Caltech_Seismograms_v2.pdf</a>.
We
are working to expand the types of seismograms that can be digitized. This includes partial
images that contain only an event of interest. This effort is limited only by the need to
understand and address particulars of resolution, size and other general features found in these
images. SKATE’s algorithms are very general for finding seismic features as lines traces. We
have even digitized historic mareograms (tide gauge charts).

## Requirements
The SKATE seismogram processing package is hosted on a remote web server. There is no
need to install any software. Computer and browser requirements are:
* <u>Browser</u>. SKATE has been tested in Chrome only. The most current version tested is
45.0.2454.101 m. It is recommended that the user update Chrome to the latest version.
There are no known settings or permissions required. Internet Explorer 11 has not been
tested but should work. Mozilla Firefox version 45.0.2454.101 m has not been tested
extensively, but should work as well. It is highly recommended that Chrome is used. If
other browsers are used, it is highly recommended that the user update to the latest
version.
* <u>System requirements</u>. Because SKATE runs in the browser, client system requirements
are light. Reasonable and standard RAM and CPU performance should suffice. Users
might want to consider an upgraded graphics card if the display does not respond
quickly to commands. A desktop or laptop computer is recommended. Though we
have tested SKATE on Android tablets and phones, these devices have not yet been
fully optimized.