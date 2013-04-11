#!/usr/bin/python3.3

""" 
This is a very poorly written python code
that makes the job done.
It essentially pings the host and checks the RTT 
and if there is time out error.
All of the data is written later to a .csv file wrt 
to the time when ping test conducted.
The software uses paping.exe to accomplish the task.
Currently, paping can only ping TCP ports.
WireShark reports the typical TCP packet size is 66 bytes or 528 bits.

paping can be downloaded from here:
https://code.google.com/p/paping/
Personally suggesting to get x86 version

Next tasks for far far future
1) give error for large time delays
2) email to the user if any exception is happening during the run-time such as
   long time delays or repeated time outs
"""

"""
Rev hist: 
1.1: Some new and minimal info added to the comments
1.2: It writes the max and min ping values to the file now
     It creates a new output.txt file each time program runs
1.2.1: GitHUb rep on https://github.com/aliirmak/pypaping/
"""

## written by Ali Irmak Ozdagli, 2013
## Version: 1.2.1

import os
import re
import csv
import datetime
import time

# writes the results to a csv file
# each row contains time and min/max/avg ms
def write_to_file(date_file_name, n_t_argument):
    try:
        with open('output_' + date_file_name + '.txt', 'a', newline='') as outputfile:
            wrtr  = csv.writer(outputfile, dialect = 'excel-tab')
            now_wrt = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            text_input = [now_wrt] + n_t_argument
            wrtr.writerow(text_input)
    finally:
        outputfile.close()
        

# check the time
# if current time is larger than the target time program exits
def check_time(until_when):
    if until_when < datetime.datetime.now():
        input('Task has been finished.\nPress any key to quit\n')
        exit()    

# First check if the paping file exist
# if it does not program quits
if not os.path.exists('paping.exe'):
    print('Paping does not exist!')
    input('Task has FAILED.\nPress any key to quit\n')
    exit()
    
# how long do you want to run the test?
# for different setting  change hours to days or minutes or seconds
# days longer than 1 may be inaccurate, 
# but it still works properly for the cause
now = datetime.datetime.now()
how_long = 1    # how long do you want to run paping
def_time = 'hours' # hours, day, minutes?
time_length = {def_time:how_long}
then = now + datetime.timedelta(**time_length)
date_file = datetime.datetime.now().strftime('%Y%m%d%H%M%S') # will be used to open the text file

# how frequently do you want to run the test?
timeout = 60

# default paping interface parameters
my_command = "paping"
myUrl = "128.46.160.229"
myport = "-p 80"
my_count = "-c 4"
my_tout = "-t 1000"
nocolor = "--nocolor"
paping_command = my_command + ' ' + myUrl + ' ' + myport + ' ' + my_count + ' ' + my_tout + ' ' + nocolor


while True:
    # opens the command window and sends the ping command
    stream = os.popen(paping_command).read()
    
    # finds the min/max/average ping result 'as string' and converts it to number  
    min_result = re.search('Minimum = (.*)ms, Maximum', stream)
    min_ping = float(min_result.group(1))
    
    max_result = re.search('Maximum = (.*)ms, Average', stream)
    max_ping = float(max_result.group(1))
    
    avr_result = re.search('Average = (.*)ms', stream)
    avr_ping = float(avr_result.group(1))
    
    # possible errors during pinging
    # searches for a string in the output
    # CASES: time out; large time delay (not implemented yet/maybe will never be unless asked)
    connection_error = 'Connection timed out'
    
    # search for errors
    toe = connection_error in stream
        
    if toe:
        error_to = 'Time out error!'
        print(error_to)
        write_to_file(error_to)
    else:
        print('Average latency is ' + str(avr_ping) +' ms')
        write_to_file(date_file, [min_ping, max_ping, avr_ping] )
    
    # check the time. if current time is larger then the time set, program will stop    
    check_time(then)
    
    # Pause program for the next iteration for timeout value. 
    # When time passes next while loop will start 
    time.sleep(timeout)    
