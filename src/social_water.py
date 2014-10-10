import numpy as np
import email, imaplib
from datetime import datetime, timedelta
import re
import time
import base64
import sys
import os
import string
import xml.etree.ElementTree as ET

# fuzzywuzzy is a fuzzy string matching code from:
# https://github.com/seatgeek/fuzzywuzzy
# note that not really installing it here - just putting the code in locally
import fuzz
import process



class inpardata:
    def __init__(self,parfilename):
        self.parfilename = parfilename
        
    def read_parfile(self):
    # read in the case-specific parameters from the parfile
        try:
            inpardat = ET.parse(self.parfilename)
        except:
            raise(FileOpenFail(self.parfilename))  
        inpars = inpardat.getroot()
        # obtain EMAIL ACCOUNT INFORMATION
        self.usr = inpars.findall('.//main_account/usr')[0].text
        self.pwd_encoded = inpars.findall('.//main_account/pwd_encoded')[0].text
        self.email_scope = inpars.findall('.//main_account/email_scope')[0].text
        
        # obtain TIMEZONE OFFSETS
        self.dst_time_utc_offset = int(inpars.findall('.//tz_offsets/dst_time_utc_offset')[0].text)
        self.std_time_utc_offset = int(inpars.findall('.//tz_offsets/std_time_utc_offset')[0].text)
        # get the stations and bounds
        self.stations = []
        self.statnums = []
        self.stations_and_bounds = dict()
        stats = inpars.findall('.//stations/station')
        for cstat in stats:
            self.stations_and_bounds[cstat.text]=cstat.attrib
            self.stations_and_bounds[cstat.text]['lbound'] = float(self.stations_and_bounds[cstat.text]['lbound'])
            self.stations_and_bounds[cstat.text]['ubound'] = float(self.stations_and_bounds[cstat.text]['ubound'])
            self.statnums.append(int(re.findall("\d+",cstat.text)[0]))
        self.minstatnum = min(self.statnums)    
        self.maxstatnum = max(self.statnums)
        # get the station_ID keywords
        msg_ids = inpars.findall('.//msg_identifiers/id')
        self.msg_ids = []
        for cv in msg_ids:
            self.msg_ids.append(cv.text)
            
        # get the keywords to remove from messages during parsing
        msg_rms = inpars.findall('.//msg_remove_items/remitem')
        self.msg_rms = []
        for cv in msg_rms:
            self.msg_rms.append(cv.text)


class gage_results:
    # initialize the class
    def __init__(self,gage):
        self.gage = gage
        self.date = list()
        self.datenum = list()
        self.height = list()
        
class timezone_conversion_schedule:
    def __init__(self,start_month,start_day,end_month,end_day):
        self.dst_start_month = start_month
        self.dst_start_day = start_day
        self.dst_end_month = end_month
        self.dst_end_day = end_day

class timezone_conversion_data:
    def __init__(self,site_params):
        # set the timezone-specific values -- currently applies to all measurements
        self.std_time_utc_offset = timedelta(hours = site_params.std_time_utc_offset)
        self.dst_time_utc_offset = timedelta(hours = site_params.dst_time_utc_offset)
        # make a table of DST starting and ending times
        self.dst_start_hour = 2
        self.dst_end_hour = 2
        # these data SUBJECT TO CHANGE --> source is http://www.itronmeters.com/dst_dates.htm
        dst_start_month = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        
        dst_start_day=[13, 11,  10,  9,  8,  13,  12,  11,  10,  8,  14,  13,  12,  
             10,  9,  8,  14,  12,  11,  10,  9,  14,  13,  12,  11,  9,  8,  14,  13,  11]
        
        dst_end_month=[11, 11,  11,  11,  11,  11,  11,  11,  11,  11,  11, 11,  11,  11,  11,  
              11,  11,  11,  11,  11, 11,  11,  11,  11,  11,  11,  11,  11,  11,  11]
        
        dst_end_day=[6,4,  3,  2,  1,  6,  5,  4,  3,  1,  7,  6,  5,  3,  2, 
                       1,  7,  5,  4,  3,  2,  7,  6,  5,  4,  2,  1,  7,  6,  4]
        
        year=[2011, 2012,  2013,  2014,  2015,  2016,  2017,  2018,  2019,  2020,  
             2021,  2022,  2023,  2024,  2025,  2026,  2027,  2028,  2029,  
             2030,  2031,  2032,  2033,  2034,  2035,  2036,  2037,  2038,  2039,  2040]      
        
        self.dst_sched = dict()
        for i, cyear in enumerate(year):
            self.dst_sched[cyear] = timezone_conversion_schedule(dst_start_month[i],
                                                                 dst_start_day[i],
                                                                 dst_end_month[i],
                                                                 dst_end_day[i])

class email_reader:
    # initialize the class
    def __init__ (self,site_params):
        self.name = 'crowdhydrology'
        self.user = site_params.usr
        self.pwd = base64.b64decode(site_params.pwd_encoded)
        self.email_scope = site_params.email_scope
        self.data = dict()
        self.dfmt = '%a, %d %b %Y %H:%M:%S '
        self.outfmt = '%m/%d/%Y %H:%M:%S'
        # make a list of valid station IDs
        self.stations = site_params.stations_and_bounds.keys()
        for i in self.stations:
            self.data[i] = gage_results(i)
        self.tzdata = timezone_conversion_data(site_params)
        self.minstatnum = site_params.minstatnum
        self.maxstatnum = site_params.maxstatnum
        

    # read the previous data from the CSV files
    def read_CSV_data(self):
    # loop through the stations
        for cg in self.stations:
            if os.path.exists('../data/' + cg.upper() + '.csv'):
                indat = np.genfromtxt('../data/' + cg.upper() + '.csv',dtype=None,delimiter=',',names=True)
                dates = np.atleast_1d(indat['Date_and_Time'])
                gageheight = np.atleast_1d(indat['Gage_Height_ft']) 
                datenum = np.atleast_1d(indat['POSIX_Stamp'])
                try:
                    len_indat = len(indat)
                    for i in xrange(len_indat):
                        self.data[cg].date.append(dates[i])
                        self.data[cg].height.append(gageheight[i])
                        self.data[cg].datenum.append(datenum[i])
                except:
                        self.data[cg].date.append(dates[0])
                        self.data[cg].height.append(gageheight[0])
                        self.data[cg].datenum.append(datenum[0])            
    # login in to the server
    def login(self):
        try:
            self.m = imaplib.IMAP4_SSL("imap.gmail.com")
            self.m.login(self.user,self.pwd)
            self.m.select("[Gmail]/All Mail")
        except:
            raise(LogonFail(self.user))
        
    # check for new messages
    def checkmail(self):
        # find only new messages
        # other options available 
        # (http://www.example-code.com/csharp/imap-search-critera.asp)
        resp, self.msgids = self.m.search(None, self.email_scope)

    # parse the new messages into new message objects
    def parsemail(self):
        tot_msgs = len(self.msgids[0].split())
        kmess = 0
        self.messages = list()
        for cm in self.msgids[0].split():
            kmess+=1
            kmrat = np.ceil(100*(kmess/float(tot_msgs)))
            if kmess == 0:
                rems = 0
            else:
                rems = np.remainder(100,kmess)
            if rems == 0:
                print '-',
                sys.stdout.flush()
            resp, data = self.m.fetch(cm, "(RFC822)")
            msg = email.message_from_string(data[0][1])  #TODO: check this array for misalignment of text from email vs sms
            if 'sms from' in msg['Subject'].lower(): #same story here
                self.messages.append(email_message(msg['Date'],msg['Subject'],msg.get_payload()))  ##
        print '-'
        
    # now parse the actual messages -- date and body
    def parsemsgs(self,site_params):
        # parse through all the messages
        for currmess in self.messages:
            # first the dates
            tmpdate = currmess.rawdate[:-5]
            currmess.date = datetime.strptime(tmpdate,self.dfmt)
            currmess.date = tz_adjust_STD_DST(currmess.date,self.tzdata)
            currmess.dateout = datetime.strftime(currmess.date,self.outfmt)
            currmess.datestamp = time.mktime(datetime.timetuple(currmess.date)) 
            # now the message bodies
            cm = currmess.body 
            # do a quick check that the message body is only a string - not a list
            # a list happens if there is a forwarded message
            if not isinstance(cm,str):   
                cm = cm[0].get_payload()
            maxratio = 0
            maxrat_count = -99999
           # maxrat_line = -99999
            line = cm.lower()
            line = string.rstrip(line,line[string.rfind(line,'sent using sms-to-email'):])
            line = re.sub('(\r)',' ',line)
            line = re.sub('(\n)',' ',line)
            line = re.sub('(--)',' ',line)
            
            for citem in site_params.msg_ids:
                if citem.lower() in line:
                    currmess.is_gage_msg = True 
                       
            if currmess.is_gage_msg == True:
                matched = False # set a flag to see if a match has been found
                # now check for the obvious - that the exact station number is in the line
                for j,cs in enumerate(self.stations):
                    # see if there's an exact match first
                    if cs.lower() in line.lower():
                        maxratio = 100
                        maxrat_count = j
                        matched = True
                        # also strip out the station ID, including possibly a '.' on the end
                        line = re.sub(cs.lower()+'\.','',line)
                        line = re.sub(cs.lower(),'',line)                  
                        currmess.station_line = line                        
                        break
                # if no exact match found, get fuzzy!
                if matched == False:
                    # we will test the line, but we need to remove some terms using regex substitutions
                    for cremitem in site_params.msg_rms:
                        line = re.sub('('+cremitem.lower()+')','',line)
                    # now get rid of the floating point values that should be the stage
                    # using regex code from: http://stackoverflow.com/questions/385558/
                    # python-and-regex-question-extract-float-double-value
                    currmess.station_line = line
                    line = re.sub("[+-]? *(?:\d+(?:\.\d*)|\.\d+)(?:[eE][+-]?\d+)?",'', line)  ## TODO: fully read this out, maybe rewrite this to be more specific and not use *'s
                    tmp_ints = re.findall("\d+",line)
                    remaining_ints = []
                    for cval in tmp_ints:
                        remaining_ints.append(int(cval))

                    if len(remaining_ints) < 1:
                        maxratio = 0
                        
                    elif ((max(remaining_ints) < self.minstatnum) or 
                        (min(remaining_ints) > self.maxstatnum)):
                        maxratio = 0
                        
                    else:
                        for j,cs in enumerate(self.stations):
                            # get the similarity ratio
                            crat = fuzz.ratio(line,cs)
                            if crat > maxratio:
                                maxratio = crat
                                maxrat_count = j
                currmess.max_prox_ratio = maxratio    
                currmess.closest_station_match = maxrat_count
                
                # rip the float out of the line
                v = re.findall("[+-]? *(?:\d+(?:\.\d*)|\.\d+)(?:[eE][+-]?\d+)?", currmess.station_line) ##TODO: mm- I have a bad feeling about these regex, make a unit test for these. They might be better but I am 90% that they are too broad.
                try:
                    currmess.gageheight = float(v[0])
                except:
                    continue


    # for the moment, just re-populate the entire data fields
    def update_data_fields(self,site_params):
        #mnfdebug ofpdebug = open('debug.dat','w')
        for cm in self.messages:
            if cm.is_gage_msg and cm.closest_station_match != -99999:
                lb = site_params.stations_and_bounds[self.stations[cm.closest_station_match]]['lbound']
                ub = site_params.stations_and_bounds[self.stations[cm.closest_station_match]]['ubound']
                if ((cm.gageheight > lb) and  (cm.gageheight < ub)):
                    self.data[self.stations[cm.closest_station_match]].date.append(cm.date.strftime(self.outfmt))
                    self.data[self.stations[cm.closest_station_match]].datenum.append(cm.datestamp)
                    self.data[self.stations[cm.closest_station_match]].height.append(cm.gageheight)
                   #mnfdebug ofpdebug.write('%25s%20f%12f%12s\n' %(cm.date.strftime(self.outfmt),cm.datestamp,cm.gageheight,self.stations[cm.closest_station_match]))
        #mnfdebug ofpdebug.close()
    # write all data to CSV files                       
    def write_all_data_to_CSV(self):
    # loop through the stations
        for cg in self.stations:
            ofp = open('../data/' + cg.upper() + '.csv','w')
            ofp.write('Date and Time,Gage Height (ft),POSIX Stamp\n')
            datenum = self.data[cg].datenum # POSIX time stamp fmt for sorting
            dateval = self.data[cg].date
            gageheight = self.data[cg].height
            outdata = np.array(zip(datenum,dateval,gageheight))
            if len(outdata) == 0:
                print '%s has no measurements yet' %(cg)
            else:
                unique_dates =np.unique(outdata[:,0])
                indies = np.searchsorted(outdata[:,0],unique_dates)
                final_outdata = outdata[indies,:]
                for i in xrange(len(final_outdata)):
                    ofp.write(final_outdata[i,1] + ',' + str(final_outdata[i,2]) + ',' + str(final_outdata[i,0]) + '\n')
            ofp.close()
                
    # plot the results in a simple time series using Dygraphs javascript (no Flash ) option
    def plot_results_dygraphs(self):
        # loop through the stations
        for cg in self.stations:
            hh = '../charts/' + cg.upper() + '_dygraph.html'
            if os.path.exists('../charts/' + cg.upper() + '_dygraph.html') == 0:
                header = ('<!DOCTYPE html>\n<html>\n' +
                        '  <head>\n' +
                        '    <meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7; IE=EmulateIE9">\n' +
                        '    <!--[if IE]><script src="js/graph/excanvas.js"></script><![endif]-->\n' +
                        '  </head>\n' +
                            '  <body>\n' +
                            "  "*2 + '<script src="js/graph/dygraph-combined.js" type="text/javascript"></script> \n'+
                            "  "*3 +  '<div id="graphdiv"></div>\n<script>\n')
                footer = ("  "*4 + 'g = new Dygraph(\n' +
                        "  "*4 + 'document.getElementById("graphdiv"),\n' +
                        "  "*4 + '"../data/%s.csv",\n' %cg + 
                        "  "*4 + '{   title: "Hydrograph at ' +cg+ '",\n'  + 
                        "  "*4 + "labelsDivStyles: { 'textAlign': 'right' },\n" +
                        "  "*4 + 'showRoller: true,\n' + 
                        "  "*4 + "xValueFormatter: Dygraph.dateString_,\n" + 
                        "  "*4 + "xTicker: Dygraph.dateTicker,\n" +
                        "  "*4 + "labelsSeparateLines: true,\n" +
                        "  "*4 + "labelsKMB: true,\n" +
                        "  "*4 + "visibility: [true,false],\n" +                    
                        "  "*4 + "drawXGrid: false,\n" + 
                        "  "*4 + " width: 640,\n" + 
                        "  "*4 + "height: 300,\n" +
                        "  "*4 + "xlabel: 'Date',\n" + 
                        "  "*4 + "ylabel: 'Gage Height (ft.)',\n" + 
                        "  "*4 + 'colors: ["blue"],\n' + 
                        "  "*4 + "strokeWidth: 2,\n" + 
                        "  "*4 + "showRangeSelector: true\n"  +
                        "  "*4 + "}\n" +
                        "  "*4 + ");\n" +
                        "</script>\n</body>\n</html>\n")

            
                self.data[cg].charttext = header  + footer
                ofp = open('../charts/' + cg.upper() + '_dygraph.html','w')
                ofp.write(self.data[cg].charttext)
                ofp.close()

def tz_adjust_STD_DST(cdateUTC,tzdata):
    # make the adjustment, based on 2012 and onward, STD/DST schedule
    # based on the general schedule and data provided by the user
    cyear= cdateUTC.year
    
    dst_start = datetime(cyear,tzdata.dst_sched[cyear].dst_start_month,
                         tzdata.dst_sched[cyear].dst_start_day,
                         tzdata.dst_start_hour)
    dst_end = datetime(cyear,tzdata.dst_sched[cyear].dst_end_month,
                       tzdata.dst_sched[cyear].dst_end_day,
                       tzdata.dst_end_hour)
    # see if the current time in UTC falls within DST or not and adjust accordingly
    if ((cdateUTC >= dst_start) and (cdateUTC <= dst_end)):
        cdate = cdateUTC - tzdata.dst_time_utc_offset
    else:
        cdate = cdateUTC - tzdata.std_time_utc_offset
    return cdate


    
class email_message:
    # initialize an individual message
    def __init__(self,date,header,txt):

        self.is_gage_msg = False
        self.header=header
        self.body=txt
        self.rawdate = date
        self.date = ''
        self.dateout = ''
        self.max_prox_ratio = 0
        self.closest_station_match = ''
        self.station_line = ''
        self.gageheight = -99999
        self.fromUUID = None
        

        
           
# ####################### #
# Error Exception Classes #        
# ####################### #
# -- cannot log on
class LogonFail(Exception):
    def __init__(self,username):
        self.name=username
    def __str__(self):
        return('\n\nLogin Failed: \n' +
               'Cannot log on ' + self.name)

# -- user did not provide a parameter filename when calling sw_driver.py
class NoParfileFail(Exception):
    def __init__(self):
        self.err = ''
    def __str__(self):
        return('\n\nCould not find parameter filename. \n' +
               'Call should be made as "python sw_driver.py <parfilename>"\n' +
               'where <parfilename> is the name of a parameter file.')
# -- cannot open an input file
class FileOpenFail(Exception):
    def __init__(self,filename):
        self.fn = filename
    def __str__(self):
        return('\n\nCould not open %s.' %(self.fn))    
# -- Invalid station value for bounds
class InvalidBounds(Exception):
    def __init__(self,statID):
        self.station = statID
    def __str__(self):
        return('\n\nStation "%s" not in the list of stations above.\nCheck for consistency.' %(self.station))
