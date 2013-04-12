#!/usr/bin/python3.3

""" 
This program essentially pings the host and checks the RTT 
and if there is time out error, it warns user via various ways
such as text output, e-mailing, showing on the console.
All of the data can be written during run-time to a .csv file wrt 
to the time when ping test conducted.
If a certain amount of time out errors are achieved then
program emails to the user.
The software uses paping.exe to accomplish the task.
Currently, paping can only ping TCP ports.
WireShark reports the typical TCP packet size is 66 bytes or 528 bits.

paping can be downloaded from here:
https://code.google.com/p/paping/
Personally suggesting to get x86 version
"""

## written by Ali Irmak Ozdagli, 2013
## Version: 1.3.2

import os       # for commands through dos/cmd
import re       # for regex functions to search for specific strings
import csv      # for writing csv file
import datetime # for recording time
import time     # for timer
import smtplib  # for sending email within this application

# writes the results to a csv file
# each row contains time and min/max/avg ms
def write_to_file(date_file_name, n_t_argument):
    try:
        with open('output_' + date_file_name + '.txt', 'a', newline='') as outputfile:
            wrtr  = csv.writer(outputfile, dialect = 'excel-tab')
            now_wrt = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            if len(n_t_argument) != 3:   # checks here if three arguments are passed or not
                text_input = [now_wrt, n_t_argument]
            else:
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

# sends email when a lot of time out errors are created
# This part takes some time to process, so sometimes wait_time may be larger
# than the timer_tick
def send_email_alert(fromaddr, toaddrs, msg, username, password, sptm_server):
    server = smtplib.SMTP(sptm_server)
    server.ehlo()  
    server.starttls()  
    server.ehlo()
    server.login(username,password)  
    server.sendmail(fromaddr, toaddrs, msg)  
    server.quit() 
    

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
timer_tick = 60 # how frequently do you want to run the test?

# default paping interface parameters
my_command = "paping"
myUrl = "xxx.xxx.xxx.xxx"  # this should be an ip address you want to ping
myport = "-p 80"
my_count = "-c 4"
my_tout = "-t 1000"
nocolor = "--nocolor"
paping_command = my_command + ' ' + myUrl + ' ' + myport + ' ' + my_count + ' ' + my_tout + ' ' + nocolor

# User preference if the file is going to be written
write_file_option = "True"  #if you want to write the results to file, make it "True" otherwise "False"

# parameters regarding email service
counter_to = 0 # initialization of variable that counts how many time outs are there
limit_to = 4   # a time out lime; when achieved email will be sent. should be larger than 0
fromaddr = 'username@gmail.com'  
toaddrs  = ['username@gmail.com']  
msg_subject = 'PyPaping Time out Error'
msg_body = 'PyPaping is getting many time outs! Server may be down.' 
msg = 'Subject: %s\n\n%s' % (msg_subject, msg_body)   
username = 'username'  
password = 'password'  
sptm_server = 'smtp.gmail.com:587'
email_option = "True"  #if you want to send the email, make it "True" otherwise "False"
mail_arg = [fromaddr, toaddrs, msg, username, password, sptm_server]

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
        if write_file_option == "True":
            write_to_file(date_file, error_to)
        counter_to += 1
        if email_option == "True":  # check if user want to send email
            if counter_to >= limit_to :  # if the time out counter is larger or equal than time out limit
                send_email_alert(*mail_arg)  # send the alert email
                counter_to = 0
    else:
        print('Average latency is ' + str(avr_ping) +' ms')
        if write_file_option == "True":
            write_to_file(date_file, [min_ping, max_ping, avr_ping] )
        counter_to = 0
        
    
    # check the time. if current time is larger then the time set, program will stop    
    check_time(then)
    
    # Pause program for the next iteration for timer_tick value. 
    # When time passes next while loop will start 
    time.sleep(timer_tick)    
