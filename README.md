pypaping
========

paping railing on python
-------------------------

This is a very poorly written python code that makes the job done. <br/>
It essentially pings the host and checks the RTT and if there is time out error. <br/>
All of the data is written later to a .csv file wrt to the time when ping test conducted. <br/>
The software uses paping.exe to accomplish the task. Currently, paping can only ping TCP ports. <br/>
WireShark reports the typical TCP packet size is 66 bytes or 528 bits. <br/>

paping can be downloaded from here:<br/>
https://code.google.com/p/paping/<br/>
Personally suggesting to get x86 version.<br/>

Next tasks for far far future<br/>
1) give error for large time delays<br/>
2) email to the user if any exception is happening during the run-time such as long time delays or repeated time outs.<br/>


***
Rev hist: 
1.1: Some new and minimal info added to the comments
1.2: It writes the max and min ping values to the file now
     It creates a new output.txt file each time program runs
***
