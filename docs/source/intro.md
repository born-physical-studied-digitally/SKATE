# Introduction 

## User Note
<p style="color:red">
SKATE is a work in progress, and the current version reflects research and development
that was done up to the completion of current DOE SBIR Phase II funding. It is currently not
complete, and users should understand that the purpose of making this software publicly
available is to allow qualified researchers to evaluate the work to date, and to make detailed
comments and suggestions as to how it can be improved. Known issues include improved
meanline detection, significant reduction in spurious features, and most importantly
incorporating advanced connection algorithms that we are developing.
</p>
<p style="color:red">
We anticipate future funding that will allow us to complete this software, and encourage
users to contact Retriever Technology with any and all comments.
</p>

## Important Note on Updates
<p style="color:red">
Because SKATE is continually being updated, users need to ensure that their browser
has the latest software. SKATE downloads and runs an app in the user’s browser; in order to
update this software, the browser’s cache needs to be cleared. In Chrome, go to History >
Clear Browsing Data, and select Cached Images and Files. A restart of the browser might be
required to run the latest version of the app.  
</p>

SKATE (Seismogram Kit for Automatic Trace Extraction) is a webbased
software tool
for the digitization of seismic traces in historic analog seismograms. This work was performed
under DOE contract DESC0008219.
SKATE is designed to address the need to digitize [^1] the millions of historic seismograms
that are currently unavailable for analysis. While there exist other digitizing programs, they are
typically limited by the need for significant user interaction, slow speed, and/or proprietary
software requirements. The design of SKATE specifically addresses these limitations by:
* Webbased
architecture. To operate SKATE, the user simply needs to direct a browser
to the software’s web location at seismo.redfish.com. No software needs to be installed
on the user’s machine; modern browser capabilities allow the entire process to be run on
a remote server.
* Fast and parallelized processing. Tens of thousands of seismograms have already
been processed using Amazon EC2 virtual computers, running in parallel. Processing time per seismogram is currently 15 minutes. We anticipate that this will be speeded
significantly in future versions.
* Reduced user interaction. We have designed robust and detailed algorithms to extract
and separate real trace information from background noise and other spurious features.
Segment connection algorithms automatically track traces across crossings when there
is significant seismic activity. User interaction is still recommended and required in
order to eliminate spurious features, but easy to use tools and intelligent algorithm
design reduces this effort significantly.

This is the alpha version of SKATE, and users should recognize that testing of the
product is ongoing. Hence, this manual will contain phrases like ‘should’ and ‘likely,’ which
indicate that while we believe most features will behave as described, uncertainties such as
variabilities in browsers and versions and end user machines can affect the behavior. The user
should understand that SKATE is constantly being upgraded, and as such features will be
added and subtracted without warning. Please contact andy@retrievertech.com with
questions and comments about operation, updates and suggestions.

[^1]: ‘Digitize’ refers to the creation of (x,y) timeseries data for seismic traces. ‘Scanning’ refers to the
creation of a digital image from an original paper or film record. A scanned image has not yet been
digitized.