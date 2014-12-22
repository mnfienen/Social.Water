from social_water import *
import os
import base64
import sys
print '############################'
print '#       Social.Water       #'
print '#       Version 1.1        #'
print '#    a m!ke@usgs joint     #'
print '############################'
print 'Making some initializations'


try:
    parfilename = sys.argv[1]
except:
    raise(NoParfileFail())

# create a class to store data read in from the parameter file
site_params = inpardata(parfilename)

# read in the site-specific parameters
print 'Reading in the site-specific parameter file:\n\t %s' %(sys.argv[1])
site_params.read_parfile()


# get things rolling
# email_scope dictates whether read all or just update using the following options:
#'ALL' means every message, 
#'UNSEEN' means just new unread ones
allmsg = email_reader(site_params)

print 'Reading previous data from CSV files'
allmsg.read_CSV_data()

allmsg.count_contributions()

print 'Attempting to log on to gmail account:\n\t%s' %(site_params.usr)
# login to the account
allmsg.login()
print 'Succesfully logged on to gmail account'
# check the mail -- allmsg.checking_all_unseen 
# dictates whether read all or just update using the following options:
#'ALL' means every message, 
#'UNSEEN' means just new unread ones
print 'checking for messages'
allmsg.checkmail()

# make a quick check to see if any new messages. If there are not, quit without
# rewriting the charts and CSV files
if len(allmsg.msgids[0].split()) == 0:
    print 'No new messages: quitting now'
else:
    
    ##load up our old contributor data
    
    print 'parsing messages'
    # parse the messages
    allmsg.parsemail()
    print 'reading messages'
    # parse the individual messages
    allmsg.parsemsgs(site_params)
    
    # drop the data into a data fields
    print 'pushing data into fields'
    allmsg.update_data_fields(site_params)
    
    # write all data to CSV files
    print 'Writing data to CSV files'
    allmsg.write_all_data_to_CSV()
    
    # plot the results usung dygraphs
    print 'plot the results using dygraphs'
    allmsg.plot_results_dygraphs()
    
   
    print 'write out new contributor data'
    allmsg.write_contributions()
    
    
print '\nAll done for now!'
